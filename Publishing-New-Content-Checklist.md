# Publishing New Content

**What to do every time a page or post is added to ai-yyc.com**

Written 17 September 2026 against the scripts and pages as they exist today.
`README.md` and the scripts themselves stay canonical. If this document and
the repo disagree, the repo wins and this gets corrected.

---

## Read this first

Four things to know before you touch anything. They explain most of the
mistakes that are easy to make here.

1. **There are two scripts, not one**, and the file is `sitemap.xml` rather
   than sitemap.html. One script rebuilds the sitemap, the other rebuilds the
   hidden search-engine data block inside each page. You normally run both,
   one after the other.
2. **Nothing you do in this folder shows up on the live site.** The site is
   deployed by uploading files by hand to `public_html`. Saving a file,
   running the scripts, and pushing to GitHub all leave ai-yyc.com exactly as
   it was.
3. **Every new page needs three things in its `<head>`** or the scripts stop
   with an error: a canonical link, a meta description, and an `<h1>` heading
   in the body. This is a feature. The error is the script refusing to publish
   something half-finished.
4. **Always start by copying an existing page.** Never build one from scratch.
   A copy already has the canonical tag, the description, the analytics line,
   the nav hooks and the styling in the right places, and you only have to
   change the words.

> **Filenames:** lowercase, hyphens instead of spaces, ending in `.html`. For
> example `my-new-post.html`. A space or a capital letter in a filename will
> work locally and break on the live server.

---

## The two scripts

Both are run from the project folder, and both are safe to run as often as you
like. Running them when nothing has changed simply changes nothing.

```sh
python tools/generate_sitemap.py
python tools/generate_structured_data.py
```

### `generate_sitemap.py`

Rewrites `sitemap.xml` by walking every `.html` page in the folder. It reads
each page's own canonical tag for the address, so the sitemap can never
disagree with the pages. It tells you if a canonical does not match where the
file actually sits, which is almost always a copy-and-paste typo.

Leaves alone: `404.html`, `statistics.html` and `webdev.html`, which are
excluded on purpose.

### `generate_structured_data.py`

Rewrites the hidden block of search-engine data in the `<head>` of the home
page, the blog index, the six category pages and every blog post. It reads the
heading, description, address and preview image from the page itself, and the
date and category from `blog_posts.js`.

Leaves alone: the topic and education pages at the root (`hcai`, `ethics`,
`management`, `predictive`, `education`, `capstone`). It skips them on
purpose, so seeing them missing from the output is correct.

> **Never hand-edit** `sitemap.xml`, or the block of code between the two
> structured data comment markers in any page. Both are regenerated from
> scratch, so any edit you make there is wiped out the next time a script
> runs. If one of them is wrong, the fix goes in the page it was read from, or
> in the script.

---

## Adding a blog post

This is the common case. Steps 1 to 4 happen on your computer, steps 5 to 8
make it real.

1. **Copy an existing post** inside `blog/posts/` and rename it. Pick a recent
   one, since it will have the newest structure.
2. **Fix the head of the new file.** Change the title, the meta description,
   the canonical link, and the og and twitter preview text. The canonical has
   to match the real address exactly, for example
   `https://ai-yyc.com/blog/posts/my-new-post.html`. Getting this wrong is the
   single most common mistake, and the sitemap script will warn you about it.
3. **Write the post.** One `<h1>` only. That heading becomes the headline
   search engines see, so it has to be the real title of the piece.
4. **Add the entry to `blog_posts.js`.** Copy the commented template at the
   bottom of that file. The `category` value has to match one of the six
   existing categories exactly, character for character. See the warning
   below.
5. **Run both scripts**, then run `git status` to see exactly which files they
   touched. That list is your upload list, and it is more reliable than
   guessing.
6. **Upload to `public_html`:** the new post into `blog/posts/`, plus
   `blog_posts.js` and `sitemap.xml` into the root. Three files, two folders.
   Missing `blog_posts.js` is what makes a post load fine at its own address
   but never appear in any listing.
7. **Purge the Cloudflare cache.** Only `blog_posts.js` genuinely needs it.
   Skipping the purge is not fatal, it just leaves the blog index up to an
   hour stale before it corrects itself.
8. **Request indexing in Search Console.** See the Search Console section
   below. This is the only step there that does anything.
9. **Commit and push.** This is for your own history. It does not affect the
   live site.

> **Category names are keys, not labels.** A category is matched by an exact
> string in four places: the `category:` value in `blog_posts.js`, the filter
> line in the category page itself, the sidebar label in
> `blog_categories.js`, and the category card on `blog.html`. A typo or a
> different spelling does not throw an error. The post just silently never
> appears on its category page. The site uses **Human-Centred**, hyphenated
> and British spelling.

---

## Adding a new page at the site root

A services page, a case study, a new topic page. Same rules, with three extra
things to remember.

1. **Copy an existing root page** such as `ethics.html`, rename it, and fix
   the head exactly as in step 2 above.
2. **Check the analytics line is there.** Every live page carries
   `<script src="/js/analytics.js"></script>` just before `</head>`. A copied
   page already has it. A page built from scratch will not, and it will
   silently collect no visitor data.
3. **Add it to the navigation** in `master_nav.js` if you want it linked. A
   page with no nav link is reachable only by typing the address, which is
   fine for some pages and a mistake for most.
4. **Add the filename to the `ORDER` list** near the top of
   `tools/generate_sitemap.py` if you want it to appear in a sensible
   position. If you skip this the page is still included, just tacked on at
   the end. The script prints which pages it appended, so you will see it.
5. **Run both scripts.** The structured data script will not write anything
   into a root topic page, and that is deliberate rather than a failure.
6. **Upload** the new page and `sitemap.xml`, plus `master_nav.js` if you
   edited it. Changing the nav changes every page on the site, and it is
   cached for four hours, so purge Cloudflare after a nav change.

---

## Adding a new blog category

Rare, and the fiddliest of the three, because the category name has to land in
four places at once. Do all four in one sitting.

1. Copy an existing category page in `blog/`, rename it, and change the
   heading, description, canonical and the filter line that reads
   `post.category === "..."`.
2. Add a sidebar link in `blog_categories.js`, including an icon from
   `images/`.
3. Add a category card on `blog.html`.
4. Use the new name in the `category` field of at least one post in
   `blog_posts.js`, or the page will render empty.
5. Run both scripts, then upload the new category page, `blog.html`,
   `blog_categories.js`, `blog_posts.js` and `sitemap.xml`.

Note the sidebar label is allowed to differ from the key. "Applied AI" is
labelled "Applied AI & Case Studies" in the sidebar while the key everywhere
else is `Applied AI`.

---

## Editing a page that is already live

If you only changed body text, upload the page and you are done. Re-run both
scripts if you changed the heading, the meta description, the canonical link
or the preview image, because those are the values the structured data is
built from.

> **Ordering quirk worth knowing:** the date the sitemap records for a page
> comes from that page's last git commit, and falls back to the file's save
> date only for a file that has never been committed. So for an edit to an
> existing page, commit the edit first and then run the sitemap script. Do it
> the other way round and the sitemap records the old date. For a brand new
> page it makes no difference.

---

## Where files go when you upload

Uploads go per folder using cPanel's multi-file upload. Uploading never
deletes, so a retired file has to be removed by hand.

| This file | Goes to |
| --- | --- |
| A blog post | `public_html/blog/posts/` |
| A category page | `public_html/blog/` |
| A root page, `blog_posts.js`, `blog_categories.js`, `master_nav.js`, `sitemap.xml`, `style.css` | `public_html/` |
| A PDF or other download | `public_html/documents/` |
| An image or icon | `public_html/images/` |

> **Never upload** `statistics.html` and `webdev.html`, which are kept in the
> repo as a record but deliberately return 404 on the live site, and any
> `.docx` or `.md` brief sitting in the project root, including this one. The
> project folder and the web root are the same shape, so a stray file
> uploaded from here becomes publicly readable.

---

## Search Console, after a post goes live

Three rules, and only the last one does anything.

- **Upload the regenerated `sitemap.xml` every time.** Post links are built by
  JavaScript after the page loads, so they do not exist in the HTML a search
  engine is served. The sitemap is the only dependable way a new post gets
  found.
- **Never resubmit the sitemap in the Sitemaps panel.** That panel stores an
  address, not a file, and the address has not changed since 2026-09-09.
  Resubmitting writes the same value into the same row and achieves nothing.
- **Request indexing on the new post's address.** Paste the full URL into the
  Inspect any URL bar with the `ai-yyc.com` property selected, then click
  Request Indexing. Once, not twice. The daily quota is around ten URLs.

Reading the result: the banner saying "URL is on Google" is the real signal.
"Test Live URL" only checks that the page loads right now and will say
"available to Google" every time, so it tells you nothing about whether the
post is indexed.

---

## When something looks wrong

| What you see | What it almost always is |
| --- | --- |
| The post opens at its own address but is missing from the blog index and its category page. | `blog_posts.js` was not uploaded, or Cloudflare is still serving the old copy. This is the most frequent failure by a wide margin. |
| The category page loads but shows no posts at all. | The category string does not match. Compare the `category:` value in `blog_posts.js` against the filter line in the category page, character for character. |
| A script stops and says a page has no canonical tag, no h1, or no meta description. | Exactly what it says. The page is unfinished. Nothing was written, so fix the page and run it again. |
| The sitemap script warns that a canonical does not match its path. | A copy-and-paste leftover from the page you duplicated. The address was used as written, so fix it and re-run. |
| You uploaded but the live page still looks old. | Your browser, more often than the server. Confirm with a cache-busting reload before believing it, then purge Cloudflare. |
| Word will not let a script overwrite a `.docx`. | The file is open in Word. Close it and run again. |

---

## Quick reference: a new blog post, start to finish

```
1.  copy a recent post in blog/posts/  ->  rename it
2.  fix title, description, canonical, og/twitter
3.  write it, one <h1> only
4.  add the entry to blog_posts.js  (category must match exactly)

5.  python tools/generate_sitemap.py
6.  python tools/generate_structured_data.py
7.  git status            <- this is your upload list

8.  upload  blog/posts/<new-post>.html   ->  public_html/blog/posts/
9.  upload  blog_posts.js  sitemap.xml   ->  public_html/
10. purge the Cloudflare cache
11. Search Console: Request Indexing on the new URL
12. git commit and push
```

Steps 1 to 7 are reversible. Step 8 is the one that changes the live site.
