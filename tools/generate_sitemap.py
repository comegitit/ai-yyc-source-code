#!/usr/bin/env python3
"""Regenerate sitemap.xml from the HTML pages in this repo.

Run from anywhere:

    python tools/generate_sitemap.py

Each <loc> is read from that page's own <link rel="canonical"> rather than
built from its filename, so the sitemap can never disagree with the canonical
tags. A page whose canonical does not match its path is reported as a warning,
since that almost always means a copy-paste typo in the canonical.

<lastmod> comes from the file's last git commit date, falling back to the
file's modification time for a page that has not been committed yet.

changefreq and priority are deliberately omitted; Google ignores both.
"""

import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://ai-yyc.com/"

# Pages that exist in the repo but are NOT served from public_html.
# Listing a page here that returns 404 would report an error in Search Console.
#   404.html        the error page itself, never belongs in a sitemap
#   statistics.html archived, deliberately not deployed
#   webdev.html     archived, deliberately not deployed
#   privacy.html    parked until the Microsoft Clarity tag ships. REMOVE THIS
#                   LINE when privacy.html goes live.
EXCLUDE = {
    "404.html",
    "statistics.html",
    "webdev.html",
    "privacy.html",
}

# Landing pages first, in a deliberate order. Anything not named here is
# appended automatically, so a new page is never silently dropped.
ORDER = [
    "index.html",
    "capstone.html",
    "education.html",
    "hcai.html",
    "ethics.html",
    "management.html",
    "predictive.html",
    "ai-grading-system_v3.html",
    "blog.html",
]

MARKER = 'rel="canonical" href="'


def canonical_of(path):
    text = path.read_text(encoding="utf-8")
    start = text.find(MARKER)
    if start == -1:
        return None
    start += len(MARKER)
    return text[start:text.index('"', start)]


def last_modified(rel):
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", rel],
        cwd=ROOT, capture_output=True, text=True,
    )
    committed = result.stdout.strip()
    if committed:
        return committed
    mtime = (ROOT / rel).stat().st_mtime
    return date.fromtimestamp(mtime).isoformat()


def collect():
    pages = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(".git/") or rel in EXCLUDE:
            continue
        pages.append(rel)

    categories = sorted(
        p for p in pages if p.startswith("blog/") and not p.startswith("blog/posts/")
    )
    posts = sorted(p for p in pages if p.startswith("blog/posts/"))
    landing = [p for p in ORDER if p in pages]
    remaining = sorted(set(pages) - set(landing) - set(categories) - set(posts))
    return landing + categories + posts + remaining, remaining


def main():
    pages, unlisted = collect()
    if not pages:
        sys.exit("No pages found. Is the repo layout what this script expects?")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    warnings = []

    for rel in pages:
        canonical = canonical_of(ROOT / rel)
        if not canonical:
            sys.exit("%s has no canonical tag. Add one, then re-run." % rel)

        expected = BASE if rel == "index.html" else BASE + rel
        if canonical != expected:
            warnings.append("  %s -> %s (expected %s)" % (rel, canonical, expected))

        lines += [
            "  <url>",
            "    <loc>%s</loc>" % canonical,
            "    <lastmod>%s</lastmod>" % last_modified(rel),
            "  </url>",
        ]

    lines += ["</urlset>", ""]
    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8", newline="\n")

    print("Wrote sitemap.xml with %d pages." % len(pages))
    if unlisted:
        print("Appended at the end (not named in ORDER): %s" % ", ".join(unlisted))
    if warnings:
        print("\nCanonical tags that do not match their path:")
        print("\n".join(warnings))
        print("Check these for typos. The canonical was used as-is.")


if __name__ == "__main__":
    main()
