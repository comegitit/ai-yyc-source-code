# Search Console: the checks due 2026-09-30

Working document for Claude Code and for future me. Written 2026-09-13.
This is step 7, the last open item of the SEO plan agreed 2026-09-08.
Steps 1 to 6 are done. Step 7 is a wait, and this file is what to do when
the wait is over.

**Read this before touching anything in Search Console on the 30th.**

---

## What is actually being waited on

Google indexes `https://www.ai-yyc.com/` while every canonical tag on the
site declares `https://ai-yyc.com/`. Google is disagreeing with the site
about which host is canonical.

The fix shipped on 2026-09-08 and is live:

- `.htaccess` lines 7 to 8 301 `www.ai-yyc.com` to `ai-yyc.com`, path preserved
- every page carries `<link rel="canonical">` on the bare domain
- `sitemap.xml` lists only bare-domain URLs and is registered in Search Console
- `BlogPosting` and `BreadcrumbList` JSON-LD ship on every post

Nothing on the site side is outstanding. **The only thing being waited on is
Google recrawling `www` and seeing the 301.** That is not something a button
makes happen faster.

Confirmed in Search Console on 2026-09-09: `https://www.ai-yyc.com/` reported
"URL is on Google", `https://ai-yyc.com/` reported "URL is not on Google".
Every stale thing found during this work was Google's cache, never the content.

---

## Reading an inspection result correctly

Two panels use confusingly similar wording. Only one of them means anything here.

| Panel | Wording | What it reads |
| --- | --- | --- |
| Main inspection result | "URL is **on** Google" | The index. **This is the signal.** |
| Test Live URL | "URL is **available to** Google" | A fresh fetch from the server, right now |

The live test returns "available to Google" every single time, as long as the
page serves 200 and is not noindexed. It cannot fail, so it measures nothing
about indexing. It is a useful check that Cloudflare and the origin are serving
correctly. It is not a propagation check.

The precise instrument is one level down. On an inspection result, expand
**Page indexing** and compare two fields:

- **User-declared canonical**, what the page's own tag says
- **Google-selected canonical**, what Google decided

Their disagreement is the defect itself, and it moves before the top-line
banner does.

---

## The decision tree for the 30th

Inspect **both** hosts, then act on the table. Do not request a reindex on
sight of "not on Google".

1. Inspect `https://ai-yyc.com/` and read the banner.
2. Inspect `https://www.ai-yyc.com/`, expand Page indexing, read Google-selected canonical.

| What you see | Meaning | Action |
| --- | --- | --- |
| `ai-yyc.com` reports "URL is on Google" | The flip landed | **Nothing.** Close step 7. |
| `ai-yyc.com` still "not on Google", but www now selects `ai-yyc.com` as canonical | Mid-flip, working | **Nothing.** Re-check in two weeks. |
| `ai-yyc.com` still "not on Google" **and** www still selects itself | Stuck after three weeks | Request indexing on `https://ai-yyc.com/`, then work the list below. |

Only the third row justifies the request. It will have been three weeks since
the last one, so it is a reasonable second ask rather than quota churn.

### If it is stuck

Request Indexing does not force canonical selection. Google weighs the 301,
the `rel=canonical` tags, the sitemap, and inbound links. The first three have
been correct since 2026-09-09, which leaves one input never audited:

**What still points at `www`?** Start with the website field on the LinkedIn
profile, then anywhere else the link has been posted or shared. Live backlinks
to `www.ai-yyc.com` keep re-asserting www as canonical no matter how many
reindex requests are made. This is the lever that has not been pulled.

Also still available but deliberately deferred: Search Console's **Change of
Address** tool for `ai-yyc.net` to `ai-yyc.com`. Both properties are verified
and the 301 is live, so it can be used. Judged low value while `.com` already
outranks and `.net` is being kept indefinitely as brand defence.

---

## What success looks like

The two hosts swap. `www.ai-yyc.com` starts reporting as a redirect or
"Page with redirect", `ai-yyc.com` becomes the indexed URL, and the
"Roy Aggarwal" snippet picks up the current applied-AI positioning instead of
the retired "AI Governance & Ethics" one.

Google's AI Overview for "ai-yyc.com" already describes the current positioning
correctly, ahead of the classic blue-link snippet, so the snippet is the lagging
surface, not the content.

---

## Do not

- **Do not request indexing on `https://ai-yyc.com/` before the 30th.** Repeat
  requests do not accelerate anything, they spend the daily quota (roughly ten
  URLs per day per property), and they muddy the clean before-and-after read
  this check depends on.
- **Do not resubmit `sitemap.xml`.** See the standing routine below.
- **Do not read "URL is not on Google" on the bare domain as a new problem.**
  It has been the expected state since 2026-09-09.
- **Do not treat a new post being indexed under `www` first as a failure.** The
  canonical points at the bare domain and the 301 is live. It resolves on the
  same recrawl.

---

## Standing routine when publishing a post

Unrelated to step 7, and true after it closes too.

1. **Upload the regenerated `sitemap.xml` to `public_html`. Always.** Post links
   are injected client-side from `BLOG_POSTS`, so they never appear in the served
   HTML of `blog.html` or the category pages. The sitemap is the only dependable
   discovery path.
2. **Never resubmit the sitemap in the GSC Sitemaps panel.** That panel stores a
   *URL*, not a file. `https://ai-yyc.com/sitemap.xml` has been registered since
   2026-09-09 and Google re-fetches it on its own schedule. Resubmitting rewrites
   the same row with the same value.
3. **Request Indexing on the new post URL.** The only action that adds anything.
   Paste the full URL into the "Inspect any URL in ai-yyc.com" bar with the
   `ai-yyc.com` domain property selected, wait for the result, click Request
   Indexing. Once, never twice.

A new post is never a new property, and individual URLs are never "added" to
Search Console. A property is a site. The `ai-yyc.com` domain property already
covers every URL on the host, including pages that do not exist yet.
