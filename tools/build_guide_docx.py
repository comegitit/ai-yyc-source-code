#!/usr/bin/env python3
"""Build a Word reference copy of the publishing guide, with screenshots.

    python tools/build_guide_docx.py

Reads   documentation/creating_new_posts.md          (hand-edited, the source)
        documentation/creating_new_posts_images/*.png (local screenshots)
Writes  documentation/creating_new_posts.docx         (the copy, and nothing else)

One direction only, the reverse of sync_brief.py: the .md is what you edit,
the .docx is rebuilt from it. sync_brief.py lists the .docx in
REFERENCE_COPIES so it can never write the .md back from it.

The .docx and the screenshots are both gitignored. The screenshots show
account emails and dashboard details, and this repo is public.

Screenshots and examples are attached to numbered steps by section heading
and step number (EXTRAS below). If the guide is renumbered, the script
reports any attachment that no longer finds its step, and any missing image
is skipped with a warning rather than stopping the build.
"""
import re
import sys
from datetime import date
from pathlib import Path

try:
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt, RGBColor
except ImportError:
    sys.exit("python-docx is not installed. Run: pip install python-docx")

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "documentation"
MD = DOCS / "creating_new_posts.md"
OUT = DOCS / "creating_new_posts.docx"
IMG = DOCS / "creating_new_posts_images"

NAVY = RGBColor(0x2C, 0x3E, 0x6B)
GREY = RGBColor(0x55, 0x55, 0x55)
GOLD = "C9A227"
TEXT_W = 8.5 - 1.8  # page width minus margins, inches

warnings = []


# --------------------------------------------------------------- document
def new_document():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(0.9)
    sec.top_margin = sec.bottom_margin = Inches(0.8)

    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(5)
    st.paragraph_format.line_spacing = 1.1
    for name, size in (("Title", 24), ("Heading 1", 16), ("Heading 2", 13)):
        s = doc.styles[name]
        s.font.name = "Calibri"
        s.font.size = Pt(size)
        s.font.color.rgb = NAVY
        s.font.bold = True
        s.paragraph_format.space_before = Pt(0 if name == "Title" else 16)
        s.paragraph_format.space_after = Pt(6)
        s.paragraph_format.keep_with_next = True
    return doc


doc = new_document()


def shade(el, fill):
    pr = el.get_or_add_pPr() if hasattr(el, "get_or_add_pPr") else el.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    pr.append(shd)


def left_border(p, color, sz=18):
    bdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    for k, v in (("val", "single"), ("sz", str(sz)), ("space", "8"), ("color", color)):
        left.set(qn("w:" + k), v)
    bdr.append(left)
    p._p.get_or_add_pPr().append(bdr)


def small_note(p, text):
    r = p.add_run(text)
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = GREY


INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)")


def add_inline(p, text, size=None, bold=False):
    """**bold**, `code` and *italic*, with code allowed inside bold."""
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**"):
            add_inline(p, part[2:-2], size, bold=True)
            continue
        if part.startswith("`"):
            r = p.add_run(part[1:-1])
            r.bold = bold
            r.font.name = "Consolas"
            r.font.size = Pt((size or 10.5) - 1)
            r.font.color.rgb = RGBColor(0x8B, 0x1E, 0x3F)
            continue
        if part.startswith("*"):
            r = p.add_run(part[1:-1])
            r.italic = True
        else:
            r = p.add_run(part)
        r.bold = r.bold or bold
        if size:
            r.font.size = Pt(size)


def code_block(lines, label=None):
    if label:
        p = doc.add_paragraph()
        small_note(p, label)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
    for i, line in enumerate(lines):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_after = pf.space_before = Pt(0)
        pf.line_spacing = 1.0
        pf.left_indent = Inches(0.1)
        pf.keep_with_next = i < len(lines) - 1
        r = p.add_run(line or " ")
        r.font.name = "Consolas"
        r.font.size = Pt(8.5)
        shade(p._p, "F1F3F7")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def image(name, caption, width=TEXT_W):
    path = IMG / (name + ".png")
    if not path.exists():
        warnings.append(f"missing screenshot, skipped: {path.relative_to(ROOT)}")
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(6)
    p.add_run().add_picture(str(path), width=Inches(width))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_after = Pt(10)
    small_note(c, caption)


def callout(text):
    p = doc.add_paragraph()
    left_border(p, GOLD)
    shade(p._p, "FBF7EA")
    p.paragraph_format.left_indent = Inches(0.15)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(8)
    add_inline(p, text)


def table(rows):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(rows):
        for j, text in enumerate(row):
            cell = t.cell(i, j)
            para = cell.paragraphs[0]
            para.paragraph_format.space_after = Pt(2)
            add_inline(para, text, size=9.5)
            if i == 0:
                for r in para.runs:
                    r.bold = True
                    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                shade(cell._tc, "2C3E6B")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def numbered(n, text):
    # Typed numbers, not Word numbering, so each list starts where the .md says.
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Inches(0.35)
    pf.first_line_indent = Inches(-0.3)
    pf.space_after = Pt(4)
    pf.tab_stops.add_tab_stop(Inches(0.35))
    r = p.add_run(f"{n}.\t")
    r.bold = True
    r.font.color.rgb = NAVY
    add_inline(p, text)


def footer_page_numbers():
    fp = doc.sections[0].footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = fp.add_run("Creating New Posts and Pages  |  page ")
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
    run = fp.add_run()
    run.font.size = Pt(8)
    for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            e = OxmlElement("w:fldChar")
            e.set(qn("w:fldCharType"), tag)
        else:
            e = OxmlElement("w:instrText")
            e.set(qn("xml:space"), "preserve")
            e.text = txt
        run._r.append(e)


# --------------------------------------------------------------- examples
# Read live from the repo, so these stay current on every rebuild.
EXAMPLE_POST = "pacing-the-frontier"


def blog_posts_entry(post_id):
    lines = (ROOT / "blog_posts.js").read_text(encoding="utf-8").splitlines()
    i = next(k for k, l in enumerate(lines) if f'id: "{post_id}"' in l)
    j = next(k for k in range(i, len(lines)) if lines[k].strip() == "},")
    return [l[2:] for l in lines[i - 1 : j + 1]]


def head_lines(post_id):
    page = ROOT / "blog" / "posts" / f"{post_id}.html"
    keys = ("<title>", 'rel="canonical"', 'property="og:url"')
    return [l.strip() for l in page.read_text(encoding="utf-8").splitlines() if any(k in l for k in keys)]


# Captured by hand on 2026-09-29; the label says so.
SCRIPT_RUN = [
    "> python tools/generate_sitemap.py",
    "Wrote sitemap.xml with 35 pages.",
    "Appended at the end (not named in ORDER): privacy.html",
    "",
    "> python tools/generate_structured_data.py",
    "Structured data written to 27 pages:",
    "  blog/agentic_blog.html",
    "  blog/ai-strategy.html",
    "  ...",
    "  blog.html",
    "  index.html",
]

GIT_STATUS = [
    "> git status",
    "On branch main",
    "Changes not staged for commit:",
    "        modified:   blog_posts.js",
    "        modified:   sitemap.xml",
    "",
    "Untracked files:",
    "        blog/posts/my-new-post.html",
]

# (section heading, step number) -> what to add after that step
EXTRAS = {
    ("Adding a blog post", 2): lambda: code_block(
        head_lines(EXAMPLE_POST),
        f"The three lines that must carry the new address (from {EXAMPLE_POST}.html):"),
    ("Adding a blog post", 3): lambda: image(
        "post_h1",
        'The live h1 is just "Pacing the Frontier". The fuller title lives in <title>, '
        "og/twitter and blog_posts.js.", 4.6),
    ("Adding a blog post", 4): lambda: code_block(
        blog_posts_entry(EXAMPLE_POST),
        "A real entry in blog_posts.js. Copy the commented template at the bottom of the file, not this one:"),
    ("Adding a blog post", 5): lambda: code_block(
        SCRIPT_RUN, "What a clean run looks like (captured 29 September 2026). The privacy.html line is normal:"),
    ("Adding a blog post", 6): lambda: code_block(
        GIT_STATUS, "Illustration of the expected result for a new post (three files, nothing else):"),
    ("Adding a blog post", 8): lambda: image(
        "cpanel_upload",
        "cPanel File Manager: type the target folder in the path box and press Go (public_html here; "
        "public_html/blog/posts for a post), then click Upload."),
    ("Adding a blog post", 9): lambda: image(
        "cloudflare_purge",
        "Cloudflare, ai-yyc.com: Caching, Configuration in the left menu, then Purge Everything. "
        "Not Invalidate Everything, just below it."),
    ("Adding a blog post", 10): lambda: (
        image("blog_latest", "The new post should appear at the top of Latest Posts on /blog.html.", 5.2),
        image("category_page",
              "...and on its category page. Missing here but present on /blog.html means the "
              "category string does not match.", 5.6)),
    ("Adding a blog post", 11): lambda: image(
        "gsc_request",
        "Paste the URL into the top bar, wait for the result, then click REQUEST INDEXING once. "
        'A brand new URL shows "URL is not on Google" at first; that is expected.'),
}

# section heading -> what to add after the first table in it
AFTER_TABLE = {
    "Reading the result": lambda: (
        image("gsc_on_google", 'The signal: "URL is on Google" on the main inspection result.'),
        image("gsc_live_test",
              'Not the signal: the LIVE TEST tab says "URL is available to Google" for any page that loads.')),
}


# --------------------------------------------------------------- driver
def build():
    lines = MD.read_text(encoding="utf-8").splitlines()
    used = set()
    section = None
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue

        if s.startswith("# "):
            doc.add_paragraph(s[2:], style="Title")
            small_note(doc.add_paragraph(),
                       "Local reference copy of documentation/creating_new_posts.md, built "
                       f"{date.today():%d %B %Y}, with screenshots. The .md file is the source; "
                       "if the two ever disagree, trust the .md.")
            i += 1
            continue

        if s.startswith("#"):
            section = s.lstrip("#").strip()
            doc.add_heading(section, level=1 if s.startswith("## ") else 2)
            i += 1
            continue

        if s.startswith("```"):
            j = i + 1
            while not lines[j].strip().startswith("```"):
                j += 1
            code_block(lines[i + 1 : j])
            i = j + 1
            continue

        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"-+", c) for c in cells):
                    rows.append(cells)
                i += 1
            table(rows)
            if section in AFTER_TABLE and section not in used:
                AFTER_TABLE[section]()
                used.add(section)
            continue

        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            callout(" ".join(buf))
            continue

        m = re.match(r"(\d+)\.\s+(.*)", s)
        if m:
            n, buf = int(m.group(1)), [m.group(2)]
            i += 1
            while i < len(lines) and lines[i].startswith("   ") and lines[i].strip():
                buf.append(lines[i].strip())
                i += 1
            numbered(n, " ".join(buf))
            if (section, n) in EXTRAS:
                EXTRAS[(section, n)]()
                used.add((section, n))
            continue

        buf = [s]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"(#|```|\||>|\d+\.\s)", lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        text = " ".join(buf)
        p = doc.add_paragraph()
        if text.startswith("*") and text.endswith("*") and not text.startswith("**"):
            r = p.add_run(text[1:-1])
            r.italic = True
            r.font.color.rgb = GREY
        else:
            add_inline(p, text)

    for key in list(EXTRAS) + list(AFTER_TABLE):
        if key not in used:
            warnings.append(f"no longer matches the guide, skipped: {key}")

    footer_page_numbers()


def main():
    if not MD.exists():
        sys.exit(f"Not found: {MD.relative_to(ROOT)}")
    build()
    try:
        doc.save(OUT)
    except PermissionError:
        sys.exit(f"{OUT.name} is open in Word. Close it and run again.")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    for w in warnings:
        print("  warning: " + w)


if __name__ == "__main__":
    main()
