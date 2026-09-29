# Creating New Posts and Pages

*What to do every time a page or post is added to ai-yyc.com, start to finish.*

This is the single guide for publishing. It replaces `Publishing-New-Content-Checklist` (the Word
file and its markdown copy) and `gsc-step-7-checklist.md`, both retired on 29 September 2026. Edit
this file directly. If the scripts change, check this against README.md.

## Before you start

1. **Work in the project folder**, `C:\Projects\ai-yyc-source-code`. Open a terminal there (in VS
   Code: Terminal, New Terminal). Every command below is run from that folder.
2. **Nothing you do in this folder shows up on the live site.** The site is deployed by uploading
   files by hand to `public_html`. Saving a file, running the scripts and pushing to GitHub all
   leave ai-yyc.com exactly as it was. Everything before the upload step can be redone as often as
   you like.
3. **Always start by copying an existing page.** Never build one from scratch. A copy already has
   the canonical tag, the description, the analytics line, the nav hooks and the styling in the
   right places, and you only have to change the words.
4. **Every page needs a canonical link, a meta description and one `<h1>`**, or the scripts stop
   with an error. That is a feature: the script is refusing to publish something half-finished.

> **Filenames:** lowercase, hyphens instead of spaces, ending in `.html`. For example
> `my-new-post.html`. A space or a capital letter will work locally and break on the live server.

## The two scripts

Both are safe to run as often as you like. Running them when nothing has changed changes nothing.

```
python tools/generate_sitemap.py
python tools/generate_structured_data.py
```

**When:** after the page is written and its entry is in `blog_posts.js`, and before you upload
anything. They read those files. `sitemap.xml` is their output, never something you edit.

**Order:** sitemap first, then structured data.

| Script | What it does | Leaves alone |
| --- | --- | --- |
| `generate_sitemap.py` | Rewrites `sitemap.xml` by walking every .html page in the folder. It reads each page's own canonical tag for the address, and warns if a canonical does not match where the file sits, which is almost always a copy-and-paste typo. | 404.html, statistics.html and webdev.html, excluded on purpose. |
| `generate_structured_data.py` | Rewrites the hidden block of search-engine data in the `<head>` of the home page, the blog index, the six category pages and every blog post. It reads the heading, description, address and preview image from the page, and the date and category from `blog_posts.js`. | The root topic and education pages (hcai, ethics, management, predictive, education, capstone). Seeing them missing from the output is correct. |

> **Never hand-edit** `sitemap.xml`, or anything between the two structured data comment markers in
> a page. Both are regenerated from scratch, so hand edits are wiped on the next run. If one is
> wrong, fix the page it was read from, or the script.

## Adding a blog post

The common case.

1. **Copy a recent post** in `blog/posts/` and rename it.
2. **Fix the head.** Change the title, meta description, canonical link, and the og and twitter
   preview text. The canonical must match the real address exactly, for example
   `https://ai-yyc.com/blog/posts/my-new-post.html`. Getting this wrong is the most common mistake.
3. **Write the post.** One `<h1>` only. It becomes the headline search engines see. Keep it short:
   the richer title goes in `<title>`, og/twitter and `blog_posts.js`.
4. **Add the entry to `blog_posts.js`.** Copy the commented template at the bottom. `category` must
   match an existing category exactly (see the warning below). `date` is the day it goes live.
5. **Run both scripts** (see above).
6. **Run `git status`.** For a new post it should list exactly three files: the new post,
   `blog_posts.js` and `sitemap.xml`. That is your upload list. If it lists pages you did not touch,
   stop and look before uploading.
7. **Changed anything after step 5?** If you edited the heading, description, date or category, run
   both scripts again. Body text edits do not need a rerun.
8. **Upload** in cPanel File Manager: the post to `public_html/blog/posts/`, and `blog_posts.js` and
   `sitemap.xml` to `public_html/`. Missing `blog_posts.js` is what makes a post load at its own
   address but never appear in any listing.
9. **Purge the Cloudflare cache** (Caching, Configuration, Purge Everything). Only `blog_posts.js`
   really needs it. Skipping it leaves the blog index up to an hour stale.
10. **Check the live page:** it loads, and it appears on `/blog.html` and its category page.
11. **Request Indexing in Search Console** on the new post's URL. See the Search Console section.
12. **Commit and push.** Your own history only. It does not affect the live site.

> **Category names are keys, not labels.** A category is matched by an exact string in four places:
> the `category` value in `blog_posts.js`, the filter line in the category page, the sidebar label in
> `blog_categories.js`, and the category card on `blog.html`. A typo throws no error; the post just
> never appears on its category page. The site uses `Human-Centred`, hyphenated, British spelling.

## Editing a page that is already live

1. Edit the page, then **commit the edit before running the scripts.** The sitemap dates each page
   from its last commit, so running the scripts first records the old date. (For a brand new page
   the order makes no difference.)
2. Run both scripts only if you changed the heading, meta description, canonical link or preview
   image. Body text alone needs no rerun.
3. Upload the page, plus `sitemap.xml` if `git status` shows it changed.
4. Request Indexing only if the change matters in search results: a new heading, title or
   description, or a substantial rewrite. Typo fixes and small wording changes do not need it.

## Adding a new page at the site root

A services page, a case study, a new topic page. Same rules, plus:

1. **Copy an existing root page** such as `ethics.html`, rename it, and fix the head as in step 2
   above.
2. **Check the analytics line is there.** Every live page carries
   `<script src="/js/analytics.js"></script>` in the `<head>`. A copied page already has it. A page
   built from scratch will not, and will silently collect no visitor data.
3. **Add it to the navigation** in `master_nav.js` if you want it linked. A page with no nav link is
   reachable only by typing the address.
4. **Add the filename to the `ORDER` list** near the top of `tools/generate_sitemap.py` for a
   sensible sitemap position. If you skip this the page is still included, just at the end, and the
   script tells you so.
5. **Run both scripts.** The structured data script deliberately writes nothing into a root topic
   page.
6. **Upload** the page and `sitemap.xml`, plus `master_nav.js` if you edited it. A nav change
   affects every page and is cached for four hours, so purge Cloudflare after one.
7. **Request Indexing** on the new page's URL.

## Adding a new blog category

Rare, and fiddly, because the name has to land in four places at once. Do all four in one sitting.

1. Copy an existing category page in `blog/`, rename it, and change the heading, description,
   canonical and the filter line that reads `post.category === "..."`.
2. Add a sidebar link in `blog_categories.js`, including an icon from `images/`.
3. Add a category card on `blog.html`.
4. Use the new name in the `category` field of at least one post in `blog_posts.js`, or the page
   renders empty.
5. Run both scripts, then upload the new category page, `blog.html`, `blog_categories.js`,
   `blog_posts.js` and `sitemap.xml`.

## Where files go when you upload

Upload per folder with cPanel's multi-file upload. Uploading never deletes, so a retired file has to
be removed by hand.

| This file | Goes to |
| --- | --- |
| A blog post | `public_html/blog/posts/` |
| A category page | `public_html/blog/` |
| A root page, `blog_posts.js`, `blog_categories.js`, `master_nav.js`, `sitemap.xml`, `style.css` | `public_html/` |
| A PDF or other download | `public_html/documents/` |
| An image or icon | `public_html/images/` |

> **Never upload** statistics.html and webdev.html (kept as a record, deliberately 404 on the live
> site), the `documentation/` folder (this guide lives there; not to be confused with `documents/`,
> which is uploaded), `tools/`, or any `.docx` or `.md` file at the project root. The project folder and
> the web root are the same shape, so a stray file uploaded from here becomes publicly readable.

## Search Console

1. **Request Indexing once for every new page**, blog post or any other page. Paste the full URL
   into the "Inspect any URL in ai-yyc.com" bar with the `ai-yyc.com` property selected, wait for the
   result, click Request Indexing. Once, never twice. The quota is roughly ten URLs a day.
2. **Never request indexing for `blog_posts.js` or `sitemap.xml`.** They are not pages.
3. **Upload the regenerated `sitemap.xml` every time.** Post links are built by JavaScript after the
   page loads, so they are not in the HTML a search engine is served. The sitemap is the only
   dependable way a new post gets found.
4. **Never resubmit the sitemap in the Sitemaps panel.** That panel stores an address, not a file,
   and the address has not changed since 2026-09-09. Resubmitting writes the same value into the
   same row.

A new page is never a new property, and URLs are never "added" to Search Console. The `ai-yyc.com`
domain property already covers every URL on the site, including pages that do not exist yet.

### Reading the result

Two panels use confusingly similar wording. Only one of them tells you anything.

| Panel | Wording | What it means |
| --- | --- | --- |
| Main inspection result | "URL is **on** Google" | The page is in Google's index. **This is the signal.** |
| Test Live URL | "URL is **available to** Google" | Google fetched the page just now. It says this every time the page loads at all, so it proves nothing about indexing. |

A new post usually takes a few days to show "URL is on Google". Check back then; do not request
again in the meantime.

## When something looks wrong

| What you see | What it almost always is |
| --- | --- |
| The post opens at its own address but is missing from the blog index and its category page. | `blog_posts.js` was not uploaded, or Cloudflare is still serving the old copy. The most frequent failure by a wide margin. |
| The category page loads but shows no posts. | The category string does not match. Compare the `category` value in `blog_posts.js` against the filter line in the category page, character for character. |
| A script stops and says a page has no canonical tag, no h1, or no meta description. | Exactly what it says. The page is unfinished. Nothing was written, so fix the page and run it again. |
| The sitemap script warns that a canonical does not match its path. | A copy-and-paste leftover from the page you duplicated. Fix it and re-run. |
| `git status` lists pages you did not touch after running the scripts. | Should not happen. Do not upload them; look at `git diff` on one of them first. |
| You uploaded but the live page still looks old. | Your browser, more often than the server. Try a hard reload (Ctrl+F5), then purge Cloudflare. |

## Quick reference: a new blog post

```
1.  copy a recent post in blog/posts/  ->  rename it
2.  fix title, description, canonical, og/twitter
3.  write it, one <h1> only
4.  add the entry to blog_posts.js  (category must match exactly)

5.  python tools/generate_sitemap.py
6.  python tools/generate_structured_data.py
7.  git status        ->  expect: the post, blog_posts.js, sitemap.xml

8.  upload  blog/posts/<new-post>.html   ->  public_html/blog/posts/
9.  upload  blog_posts.js  sitemap.xml   ->  public_html/
10. purge the Cloudflare cache
11. check the live page and /blog.html
12. Search Console: Request Indexing on the new URL, once
13. git commit and push
```

*Steps 1 to 7 are reversible. Step 8 is the one that changes the live site.*
