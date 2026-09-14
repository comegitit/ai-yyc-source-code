# Search Console: the checks due 2026-09-30

Working document for Claude Code and for future me. Written 2026-09-13,
updated 2026-09-14 with a live verification pass and a dated reading of the
search result. This is step 7, the last open item of the SEO plan agreed
2026-09-08. Steps 1 to 6 are done. Step 7 is a wait, and this file is what to
do when the wait is over.

**Read this before touching anything in Search Console on the 30th.**

---

## What is actually being waited on

Google indexes `https://www.ai-yyc.com/` while every canonical tag on the
site declares `https://ai-yyc.com/`. Google is disagreeing with the site
about which host is canonical.

The fix shipped on 2026-09-09 (commit `466caf2`) and is live:

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

## How stale the indexed copy actually is

Established 2026-09-14, and sharper than the earlier "retired positioning"
framing. The live "Roy Aggarwal" result reads:

```
Roy Aggarwal - AI Governance & Ethics, Digital ...
ai-yyc.com
https://www.ai-yyc.com
Digital transformation professional with deep enterprise IT experience.
Specializing in AI governance and ethics, focused on bridging business and
technical ..
```

Both strings match commit `6caedfd` (2026-06-15, the initial commit) **exactly**,
down to the lowercase "focused":

| Field | Stored by Google | Source |
| --- | --- | --- |
| Title | `Roy Aggarwal - AI Governance & Ethics, Digital ...` | `6caedfd` title tag |
| Description | `Digital transformation professional with deep enterprise IT experience...` | `6caedfd` meta description |

So Google's stored copy of `www` is roughly **three months old**, not a few
weeks. Google effectively stopped visiting that URL after June.

This explains why the 301 has taken longer than the 24-hour crawl seen after
the sitemap submission. That speed came from sitemap-driven crawls of the
**bare** domain. `www` is not in the sitemap, never will be, and inherits none
of that priority. Its recrawl depends on Request Indexing plus Google's own
schedule for a URL it currently treats as canonical.

---

## Reading a search result correctly

A trap that caused a false positive on 2026-09-14. A modern Google result shows
the **site name** in bold on its own line, then the **URL** beneath it:

```
ai-yyc.com                <- site name display, means nothing here
https://www.ai-yyc.com    <- the actual URL, this is the signal
```

Seeing `ai-yyc.com` on the first line is not evidence the flip landed. Read the
line underneath.

**The URL, title and description all come from one index entry and change
together.** They will not update separately. So there is a single tell: while
the URL line reads `https://www.ai-yyc.com`, nothing has moved, whatever the
title and description say. When it flips, all three change in the same moment.

Incognito is not a sharper test than a normal window. It only strips local
personalisation; it does not reach a fresher index.

Note also that Google rewrites meta descriptions more often than it uses them,
and name queries are a common case. A snippet that never matches the tag word
for word is not a defect.

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

This caught us out on 2026-09-14: "URL is available to Google" on the bare
domain was read as the flip having landed. It was a live fetch of a URL that is
not the one ranking.

The precise instrument is one level down. On an inspection result, expand
**Page indexing** and compare two fields:

- **User-declared canonical**, what the page's own tag says
- **Google-selected canonical**, what Google decided

Their disagreement is the defect itself, and it moves before the top-line
banner does.

**View Crawled Page** (on the indexed result, not the live test) shows Google's
stored HTML verbatim. Searching it for `name="description"` dates the stored
copy definitively.

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

**One request already in flight.** On or just after 2026-09-10, before this
decision tree was written, Roy inspected `https://www.ai-yyc.com/`, ran Test
Live URL, and clicked Request Indexing **on the www URL**. That is a different
URL from the one in the third row above, and it is the request that should
produce the flip. Factor it in on the 30th: if nothing has moved by then, a
three-week-old request on www has failed to land, which strengthens the case
for the inbound-link audit rather than for another request.

### If it is stuck

Request Indexing does not force canonical selection. Google weighs the 301,
the `rel=canonical` tags, the sitemap, and inbound links. The first three have
been correct since 2026-09-09, which leaves one input never fully audited:

**What still points at `www`?**

- ~~The website field on the LinkedIn profile~~ **Checked 2026-09-14, clean.**
  It reads `ai-yyc.com (Portfolio)`, no www. LinkedIn contact links are
  `nofollow` in any case, so this was never going to be the strong signal.
- Anywhere else the link has been posted or shared, including third-party
  backlinks nobody controls. The 301 handles those, but they keep voting for
  www until Google recrawls them too.

Every signal Roy does control now points at the bare domain (see the
verification log below), so a genuinely stuck state points at external
backlinks, not at anything fixable in this repo.

Also still available but deliberately deferred: Search Console's **Change of
Address** tool for `ai-yyc.net` to `ai-yyc.com`. Both properties are verified
and the 301 is live, so it can be used. Judged low value while `.com` already
outranks and `.net` is being kept indefinitely as brand defence.

---

## What success looks like

The two hosts swap. `www.ai-yyc.com` starts reporting as a redirect or
"Page with redirect", `ai-yyc.com` becomes the indexed URL, and the
"Roy Aggarwal" snippet picks up the current applied-AI positioning instead of
the June "AI Governance & Ethics" one.

Google's AI Overview for "ai-yyc.com" already describes the current positioning
correctly, ahead of the classic blue-link snippet, so the snippet is the lagging
surface, not the content.

---

## Verification log, 2026-09-14

Everything below was confirmed live, not read from the repo.

| Signal | Points to | How verified |
| --- | --- | --- |
| `www.ai-yyc.com` | 301 to `https://ai-yyc.com/` | `curl -I`, origin header `x-turbo-charged-by: LiteSpeed` confirms it reached the server, not a Cloudflare-only rule |
| `ai-yyc.net` | 301 to `https://ai-yyc.com/` | `curl -I` |
| `ai-yyc.com` | 200 | `curl -I` |
| Canonical tag | `https://ai-yyc.com/` | `index.html:16` |
| Live `<title>` | current applied-AI wording | `curl` of the live homepage |
| Live meta description | current applied-AI wording | `curl` of the live homepage |
| `sitemap.xml` | 32 bare-domain URLs, no www | repo and live |
| `robots.txt` sitemap line | bare domain | live |
| Internal links | relative | `grep` for www finds only `README.md` |
| LinkedIn website field | `ai-yyc.com (Portfolio)` | profile contact info |

The site side is complete and verified. Nothing in this repo is outstanding.

Useful one-liners:

```bash
curl -I https://www.ai-yyc.com/
curl -s https://ai-yyc.com/ | grep -o "<title>[^<]*</title>"
grep -rn "www.ai-yyc" --exclude-dir=.git .
```

---

## Do not

- **Do not request indexing on `https://ai-yyc.com/` before the 30th.** Repeat
  requests do not accelerate anything, they spend the daily quota (roughly ten
  URLs per day per property), and they muddy the clean before-and-after read
  this check depends on.
- **Do not re-submit Request Indexing on `www` daily either.** Same quota, and
  resubmitting does not advance a URL in the queue. The request from around
  2026-09-10 is live. Let it sit.
- **Do not use the Removals tool on `www`.** It is the obvious-looking button
  and it is a trap. It suppresses results rather than consolidating them, and
  with the 301 in place it can take the real listing down with it for months.
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
