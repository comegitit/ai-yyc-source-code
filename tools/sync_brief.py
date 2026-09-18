#!/usr/bin/env python3
"""Regenerate a brief's .md from the .docx you edited in Word.

    python tools/sync_brief.py            # sync every root brief that needs it
    python tools/sync_brief.py --check    # report only, write nothing
    python tools/sync_brief.py Publishing-New-Content-Checklist.docx

One direction only: .docx is the source you edit, .md is the generated copy
that git tracks. Two-way sync is not offered on purpose. Round-tripping
through Word is lossy both ways, so it would churn the markdown on every
save, and when both files change there is no honest way to pick a winner.

Word is also an unreliable narrator about time: it rewrites a file's
timestamp when you merely open and close it. The staleness check below is
therefore a hint, not proof. It errs toward telling you to sync.

What it understands, which is what tools/build_*.py produce:

    Heading 1/2/3            #, ##, ###
    a large bold first line  # (the title block)
    List Bullet              -
    List Number              1.  (restarts per list, tracked by numId)
    a one-column table of    a fenced code block
      Consolas text
    a one-column table       > **Label** blockquote
      opening with bold
    any other table          a markdown table, first row as header
    bold / italic / Consolas **, *, `code`
    an empty bordered para   ---

Anything else becomes a plain paragraph, which is the safe failure.
"""

import re
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    from docx.oxml.ns import qn
except ImportError:
    sys.exit("python-docx is not installed. Run: pip install python-docx")

ROOT = Path(__file__).resolve().parent.parent

# Briefs only. Never touch the resumes, which are hand-maintained Word files
# with no markdown counterpart and are tracked in git as-is.
EXCLUDE_DIRS = {"documents", "tools", ".git"}

EM_DASH = "—"


# --------------------------------------------------------------- docx reading
def iter_blocks(doc):
    """Yield Paragraph and Table objects in the order they appear."""
    body = doc.element.body
    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, doc)
        elif child.tag == qn("w:tbl"):
            yield Table(child, doc)


def run_style(run):
    """(bold, italic, is_code) for a run, normalising None to False."""
    name = (run.font.name or "").lower()
    return bool(run.bold), bool(run.italic), name.startswith("consolas")


TAGLIKE = re.compile(r"</?[A-Za-z][A-Za-z0-9]*\s*/?>")


def escape_md(text):
    # Only what would actually change meaning. Underscores are left alone:
    # GFM has no intraword _ emphasis, and escaping them would turn
    # blog_posts.js into blog\_posts.js for no benefit.
    text = re.sub(r"(?<!\\)([*`])", r"\\\1", text)
    # A bare <head> or <h1> in prose would be swallowed as HTML. Word gives
    # no way to mark it as code, so infer it.
    return TAGLIKE.sub(lambda m: "`%s`" % m.group(0), text)


def inline(paragraph):
    """Runs to markdown, merging neighbours that share formatting."""
    merged = []
    for run in paragraph.runs:
        if not run.text:
            continue
        style = run_style(run)
        if merged and merged[-1][0] == style:
            merged[-1][1] += run.text
        else:
            merged.append([style, run.text])

    out = []
    for (bold, italic, code), text in merged:
        if code:
            # Inline code takes precedence; bold/italic inside it is noise.
            out.append("`%s`" % text.strip("`"))
            continue
        lead = len(text) - len(text.lstrip())
        trail = len(text) - len(text.rstrip())
        core = text.strip()
        if not core:
            out.append(text)
            continue
        core = escape_md(core)
        if bold and italic:
            core = "***%s***" % core
        elif bold:
            core = "**%s**" % core
        elif italic:
            core = "*%s*" % core
        out.append(text[:lead] + core + text[len(text) - trail:] if trail
                   else text[:lead] + core)
    return "".join(out).strip()


def first_run_size(paragraph):
    for run in paragraph.runs:
        if run.text.strip() and run.font.size is not None:
            return run.font.size.pt
    return None


def has_bottom_border(paragraph):
    pPr = paragraph._p.find(qn("w:pPr"))
    if pPr is None:
        return False
    bdr = pPr.find(qn("w:pBdr"))
    return bdr is not None and bdr.find(qn("w:bottom")) is not None


def list_id(paragraph):
    """The numId of a numbered paragraph, or None."""
    pPr = paragraph._p.find(qn("w:pPr"))
    if pPr is None:
        return None
    numPr = pPr.find(qn("w:numPr"))
    if numPr is None:
        return None
    numId = numPr.find(qn("w:numId"))
    return numId.get(qn("w:val")) if numId is not None else None


# --------------------------------------------------------------- table shapes
def squeeze(text):
    return re.sub(r"[ \t]{2,}", " ", text)


def cell_text(cell):
    parts = [inline(p) for p in cell.paragraphs]
    return squeeze(" ".join(p for p in parts if p).strip())


def cell_is_code(cell):
    runs = [r for p in cell.paragraphs for r in p.runs if r.text.strip()]
    return bool(runs) and all(run_style(r)[2] for r in runs)


def table_to_md(table):
    cols = len(table.columns)

    if cols == 1:
        cell = table.cell(0, 0)
        if cell_is_code(cell):
            lines = [p.text.rstrip() for p in cell.paragraphs]
            while lines and not lines[0].strip():
                lines.pop(0)
            while lines and not lines[-1].strip():
                lines.pop()
            return ["```"] + lines + ["```"]

        # A callout: one shaded cell that opens with a bold label.
        body = cell_text(cell)
        if body:
            return ["> " + line for line in wrap_none(body)]
        return []

    rows = []
    for row in table.rows:
        rows.append([cell_text(c) or " " for c in row.cells])
    if not rows:
        return []

    header, *rest = rows
    header = [strip_emphasis(c) for c in header]
    out = ["| " + " | ".join(header) + " |",
           "| " + " | ".join("---" for _ in header) + " |"]
    for row in rest:
        out.append("| " + " | ".join(c.replace("\n", " ") for c in row) + " |")
    return out


def wrap_none(text):
    """Markdown reflows anyway, so keep a blockquote on one line."""
    return [text]


# --------------------------------------------------------------- the converter
def docx_to_md(path):
    doc = Document(str(path))
    out = []
    counters = {}
    seen_title = False
    last_was_table = False

    for block in iter_blocks(doc):
        if isinstance(block, Table):
            md = table_to_md(block)
            if md:
                if out and out[-1] != "":
                    out.append("")
                out += md
                out.append("")
            last_was_table = True
            continue

        text = squeeze(inline(block))
        style = block.style.name or "Normal"

        if not text:
            # The builder puts an empty bordered paragraph where a rule goes,
            # and an empty spacer after every table. Keep the first, drop the
            # second.
            if has_bottom_border(block) and not last_was_table:
                if out and out[-1] != "":
                    out.append("")
                out += ["---", ""]
            last_was_table = False
            continue

        last_was_table = False

        if style.startswith("Heading"):
            level = int(style.split()[-1]) if style.split()[-1].isdigit() else 2
            # The title block already claimed #, so everything shifts down one
            # and the document keeps a single top-level heading.
            if seen_title:
                level += 1
            if out and out[-1] != "":
                out.append("")
            out += ["#" * min(level, 6) + " " + text, ""]
            continue

        if style == "List Bullet":
            out.append("- " + text)
            continue

        if style == "List Number":
            key = list_id(block) or "default"
            counters[key] = counters.get(key, 0) + 1
            out.append("%d. %s" % (counters[key], text))
            continue

        # Title block: the first oversized line becomes the document heading.
        size = first_run_size(block)
        if size is not None and not seen_title and size >= 18:
            out += ["# " + strip_emphasis(text), ""]
            seen_title = True
            continue
        if size is not None and not seen_title and size >= 14:
            out += ["## " + strip_emphasis(text), ""]
            continue

        if out and out[-1].startswith(("- ", "1.")) or (
                out and re.match(r"^\d+\. ", out[-1])):
            out.append("")
        out += [text, ""]

    return tidy(out)


def strip_emphasis(text):
    """Header cells are already bold in Word; markdown bolds them again."""
    return re.sub(r"\*+", "", text).strip()


def tidy(lines):
    out = []
    for line in lines:
        if line == "" and (not out or out[-1] == ""):
            continue
        out.append(line)
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) + "\n"


# --------------------------------------------------------------- driver
def briefs():
    """Root-level .docx files that are briefs, not resumes."""
    found = []
    for path in sorted(ROOT.glob("*.docx")):
        if path.name.startswith("~$"):
            continue
        if path.parent.name in EXCLUDE_DIRS:
            continue
        found.append(path)
    return found


def report(path, md_path, wrote, body):
    rel = path.name
    if wrote:
        print("  synced   %s -> %s" % (rel, md_path.name))
    else:
        print("  current  %s" % rel)
    dashes = body.count(EM_DASH)
    if dashes:
        print("           %d em-dash(es) in the text. Word's autocorrect adds "
              "these; replace them before committing." % dashes)


def main():
    args = [a for a in sys.argv[1:]]
    check = "--check" in args
    named = [a for a in args if not a.startswith("--")]

    targets = [ROOT / n for n in named] if named else briefs()
    missing = [t for t in targets if not t.exists()]
    if missing:
        sys.exit("Not found: " + ", ".join(m.name for m in missing))
    if not targets:
        print("No briefs found at the repo root.")
        return

    print("check only, nothing written\n" if check else "")
    changed = 0
    for path in targets:
        md_path = path.with_suffix(".md")
        body = docx_to_md(path)
        current = md_path.read_text(encoding="utf-8") if md_path.exists() else None

        if current == body:
            report(path, md_path, False, body)
            continue

        changed += 1
        if check:
            state = "would be created" if current is None else "is out of date"
            print("  STALE    %s %s" % (md_path.name, state))
            dashes = body.count(EM_DASH)
            if dashes:
                print("           %d em-dash(es) in the .docx text." % dashes)
        else:
            md_path.write_text(body, encoding="utf-8", newline="\n")
            report(path, md_path, True, body)

    if check and changed:
        print("\n%d file(s) out of date. Run without --check to sync." % changed)
        sys.exit(1)
    if not check and changed:
        print("\nReview the markdown diff before committing: git diff")


if __name__ == "__main__":
    main()
