# Analytics — Microsoft Clarity

**Status: installed, deployed and verified 2026-09-15.** This document was the
build spec; it is now the operating record. The install is finished, so read this
for how the thing works and what was decided, not as a task list. The only work
still outstanding is dashboard customization, at the bottom.

Site: hand-written HTML/CSS/JS portfolio at ai-yyc.com, DNS proxied through
Cloudflare on the free plan. Deploy is a **manual upload to `public_html`**, not
git-deployed.

**Project ID: `yiw91bgryt`.**

---

## What is installed

`js/analytics.js` holds Clarity's vendor snippet wrapped in a `localStorage`
self-exclusion gate. Every live page loads it with a single line before `</head>`:

```html
<script src="/js/analytics.js"></script>
```

**35 live pages carry it**: 11 at the root, 6 in `blog/`, 18 in `blog/posts/`.
Verified live after deploy, 35 of 35, none missing and none double-tagged.

Three details in that structure were deliberate and should not be undone:

**Root-absolute path.** `404.html` is served at whatever depth was requested, so a
relative path breaks there. `master_nav.js` is referenced the same way for the same
reason, and `getBasePath()` carries the explanatory comment. The tradeoff is that
`file://` preview does not load the tag. Use `python -m http.server` instead.

**A separate file, not folded into `master_nav.js`.** Tempting, since that file is
already on 34 of the 35 pages and would have been a zero-edit install. Rejected
because it couples tracking to navigation, so a future nav refactor could silently
kill analytics, and because it would miss `ai-grading-system_v3.html`, which does
not include `master_nav.js` at all.

**`ai-grading-system_v3.html` got the line directly.** It has no `master_nav.js`,
no `#site-header` and no `#site-footer`, but it is a real destination linked from
`hcai.html`. It is the page most likely to be missed in any future sweep.

`statistics.html` and `webdev.html` are **not** tagged and must not be. They exist
in the repo and as server-side archives but are not in `public_html`, and are
commented out of the nav deliberately. Their absence from a coverage audit is
correct, not a finding.

### Masking

**Strict**, set before the first session was ever recorded. This is not a
preference. `privacy.html` publicly states the site runs Clarity's strictest
masking, so Strict must stay on for as long as that page is live. The site has no
contact form, only a `mailto:` link, so Strict costs nothing.

### Self-exclusion

Handled client-side, not by IP. Visiting `?notrack=1` sets a `noTrack` flag in
`localStorage` and the tag never loads; `?notrack=0` clears it. Either one shows a
three-second confirmation banner, because the whole point is that this has to be
doable on a phone where there is no dev console. Not an `alert()`, which would
block the page.

Set on all of the owner's browsers and devices on 2026-09-15. Two properties worth
remembering:

- **It is per browser profile, not per machine.** Chrome and Edge on one laptop are
  two separate settings. Two Chrome profiles are two.
- **It must be set in a normal window.** Incognito discards `localStorage` on close,
  so setting it there accomplishes nothing.

A new browser, profile or device will be tracked until `?notrack=1` is visited on
it.

**No IP blocking, and do not add any.** The owner's connection is dual-stack and
dynamically assigned. Clarity matches IPv4 only and cannot reliably block a visitor
who has both stacks. The block would work intermittently and fail silently, which
is worse than no filter at all.

---

## Decisions already made — do not relitigate

**Tool: Microsoft Clarity, free tier.** Re-examined against the actual goal metrics
and confirmed. Alternatives were considered and rejected: Plausible and Fathom fit
the literal metric list slightly better but cost around $9/month; GoatCounter is
free but has no session duration at all; Cloudflare Web Analytics is free and
cookieless but was rejected as overwhelming and cannot do session recordings.

**No cookie consent banner.** Personal portfolio, Canadian, no commercial
transactions, no accounts, no sensitive data. A banner only means something if it
actually gates the tag; one that appears while tracking regardless is a false claim
and worse than none. Meaningful consent must be opt-in, which would thin and skew
the data at this volume. `privacy.html` states this position openly, which is the
substitute for a banner. **Do not add a banner, and do not add a partial or
decorative one.**

**No UTM parameters on outreach links.** Proposed and rejected by the owner,
correctly. A DM link displaying `?utm_source=linkedin&utm_medium=dm` reads as funnel
processing to a contact being asked for help, and it risks the OG preview card,
which is doing real work in the message. At this traffic volume the timestamp is
the attribution.

**Facts baked into `privacy.html` are verified — do not "correct" them.** The
opt-out is the Digital Advertising Alliance tool at `https://optout.aboutads.info/`,
not a Microsoft-hosted page, with `https://youradchoices.com/pmc` to keep the
preference from being cleared with cookies. Clarity does **not** respond to Do Not
Track but **does** support Global Privacy Control. The page deliberately avoids a
blanket "no personal information is collected", because session replay plus
city-level location does not support that claim; it names what specifically is not
collected instead.

---

## Reading the data

**Clarity lags 30 minutes to 2 hours.** It is not real-time. A blank dashboard
fifteen minutes after anything is not evidence of breakage.

**The recordings list is the instrument, not the charts.** Baseline traffic is
roughly five visitors a week, and single-digit session counts make every trend line
useless. Each row of the recordings list is one session with its timestamp,
location, device and duration, which is the entire metric list, per visitor, in
list form. Expect that to stay more useful than the charts until volume grows.

How Clarity covers the goal metrics:

| Wanted | Clarity |
|---|---|
| Unique visitors over time | Standard dashboard card |
| City | Country/State/City tabs, trend line for up to 5 cities |
| Session duration / time on site | Yes |
| Pages visited | Yes |
| Device type | Yes |
| Time of visit | **Weak.** Per-session timestamps, but no time-of-day distribution chart |
| Time spent per page | **Uncertain.** Verify live rather than assume |

**Attribution is weak and that is now permanent.** The install was pulled forward to
measure a LinkedIn DM blitz, but LinkedIn rate-limited the sends as suspected spam,
so they went out slowly over several days rather than in one burst, and **no tag was
live for any of it.** Those clicks are unrecoverable and there is no single spike to
read. Residual value is real though: DM links have a long tail, so the tag catches
stragglers from that round and covers any follow-up messages, which is the more
likely place the intel gets used.

Separately: LinkedIn's suppression of DM link cards at outreach volume is a known,
settled issue. **Do not re-investigate the site as a cause.**

---

## Maintenance

**Every new page needs the line added by hand.** Insert immediately before
`</head>`, never at the top of the file or above `<!DOCTYPE html>`. A page without
it is invisible to Clarity, which shows up as "only the homepage gets traffic".

To audit coverage:

```sh
find . -name "*.html" -not -path "./.git/*" ! -name statistics.html ! -name webdev.html \
  -exec grep -L "js/analytics.js" {} +
```

Anything it prints is missing the tag.

### Caching, and the false alarms it causes

Browser TTL is set by `mod_expires` in `.htaccess`, not by Cloudflare. Cloudflare's
Browser Cache TTL is on "Respect Existing Headers", replacing a flat 4-hour override
that had shadowed the origin. Current values: HTML 5 minutes, CSS and JS 1 hour,
images 7 days, fonts 1 year. Before this change the JS files carried no cache header
at all, which left them on browser heuristic caching and could hold `blog_posts.js`
stale for days after a post was published.

**Purge the Cloudflare cache after uploading any `.js` or `.css`.** HTML is served
`cf-cache-status: DYNAMIC` and goes live immediately; JS and CSS are edge-cached.

**Expect a stale-cache false alarm anyway.** A browser that visited recently keeps
serving its own copy of `master_nav.js` and `style.css` for up to an hour and shows
the pre-deploy site. Verified twice, on 2026-09-08 and again on 2026-09-15: a page
appeared to still have the old nav long after the edge was serving the correct file.
Hard-reload or use incognito before concluding anything is broken.

### Cloudflare rewrites the email address on `privacy.html`

Scrape Shield rewrites the `mailto:roy@ai-yyc.com` link into a
`/cdn-cgi/l/email-protection` link and injects a decoder script, inflating the
served file by roughly 230 bytes against the local copy. This is normal, it is an
anti-scraping feature working as intended, and it is not corruption.

### Sitemap `lastmod`

`generate_sitemap.py` takes `lastmod` from each file's last git commit date. Because
the analytics tag touched all 35 pages in one commit, the next regen will stamp them
all `2026-09-15`, which overstates what changed: a script tag is not a content
change. Not worth fixing, and it self-corrects as pages are edited normally, but do
not be surprised by it. After uploading a regenerated sitemap, **do not resubmit it
in Search Console**; request indexing on specific new URLs instead.

---

## If data ever stops appearing

Check in this order.

**Cloudflare Rocket Loader.** Free plan, under Speed > Optimization. It rewrites and
defers scripts and has a long history of breaking analytics tags. It would also
likely break `master_nav.js`, which listens for `DOMContentLoaded`, so if the nav
works it is probably still off. Confirm rather than assume.

**Missing tags.** Run the audit command above. A page without the tag is invisible.

**Cache.** Purge Cloudflare again, then hard-reload before drawing conclusions.

**Content-Security-Policy.** Verified 2026-09-08 and unchanged since: there is no
CSP anywhere. Every HTML file and `.htaccess` was checked, and no `<meta
http-equiv>` or CSP header is set. The one thing invisible from the repo is a
Cloudflare Transform Rule adding a CSP header server-side, so check the Rules tab.
If one is ever added, Clarity needs `https://www.clarity.ms`, `https://c.bing.com`,
and the lettered subdomains `https://[a-z].clarity.ms`, since Clarity spreads across
lettered subdomains and allowing a single host will not cover it.

**What a healthy load looks like**, from the verification on 2026-09-15. In DevTools
Network, filtered to `clarity`, in an incognito window:

- `yiw91bgryt` · 200 · script · initiator `analytics.js`, which is the wrapper
  injecting the tag
- `clarity.js` · 200 · the tracker proper
- several `collect` · 204 · the session beacons. 204 is success, and this is the row
  that proves data is actually being sent, not merely that the script loaded

---

## Still outstanding: dashboard customization

The only remaining work. Clarity's default dashboard is busy with rage clicks, dead
clicks and scroll depth, which is noise for this use case. The fix is removing and
rearranging cards.

**Deliberately deferred until a week of real data exists**, so 2026-09-22 onward,
once it is clear what actually gets looked at. Budget 45 to 90 minutes,
collaborative. Add 1 to 2 hours if the time-of-day and per-page gaps in the table
above need a charting workaround built from a CSV export.

Own-IP filtering is not a dashboard task. It is the `localStorage` gate, already
done and described above. No IP blocking.
