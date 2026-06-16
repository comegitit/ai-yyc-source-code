import os
from datetime import date

# ============================================================
# CONFIGURATION — edit these before running
# ============================================================
LOCAL_FOLDER = "."                    # "." = run from your project root
BASE_URL     = "https://ai-yyc.com"  # no trailing slash

# HTML files to exclude (internal/dev pages not meant for public)
EXCLUDE_HTML = {
    "lending_form_V2.html",
    "sitemap_old.xml",
}

# PDFs to explicitly INCLUDE (only public-facing, indexable PDFs)
INCLUDE_PDFS = {
    "documents/Resume_Roy_Aggarwal_Full_April_2026.pdf",
}

# ============================================================
# SCRIPT — no need to edit below this line
# ============================================================
today = date.today().isoformat()
urls  = []

for root, dirs, files in os.walk(LOCAL_FOLDER):
    # Skip hidden folders (e.g. .git)
    dirs[:] = [d for d in dirs if not d.startswith(".")]

    for filename in files:
        full_path = os.path.join(root, filename)
        relative  = os.path.relpath(full_path, LOCAL_FOLDER).replace(os.sep, "/")

        # --- HTML files ---
        if filename.endswith(".html"):
            if filename in EXCLUDE_HTML:
                continue
            if relative == "index.html":
                loc      = BASE_URL + "/"
                priority = "1.00"
            else:
                loc      = BASE_URL + "/" + relative
                priority = "0.80"
            urls.append((loc, priority))

        # --- Explicitly included PDFs only ---
        elif filename.endswith(".pdf"):
            if relative in INCLUDE_PDFS:
                loc = BASE_URL + "/" + relative
                urls.append((loc, "0.60"))

# Sort for tidiness
urls.sort()

# Build the XML
lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]

for loc, priority in urls:
    lines.append("  <url>")
    lines.append(f"    <loc>{loc}</loc>")
    lines.append(f"    <lastmod>{today}</lastmod>")
    lines.append(f"    <priority>{priority}</priority>")
    lines.append("  </url>")

lines.append("</urlset>")

# Write sitemap.xml to project root
output_path = os.path.join(LOCAL_FOLDER, "sitemap.xml")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nDone! {len(urls)} URLs written to {output_path}\n")
for loc, _ in urls:
    print(" ", loc)
