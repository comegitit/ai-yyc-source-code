# Analytics — Microsoft Clarity

**Status: installed, deployed and verified 2026-09-15.** This document was the
build spec; it is now the operating record. The install is finished and **nothing
is outstanding**, so read this for how the thing works and what was decided, not as
a task list.

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

**Relaxed**, changed 2026-09-15 from Strict. Clarity offers three modes: Strict
masks all content, Balanced (the default) masks numbers and email addresses, and
Relaxed masks nothing except input boxes and dropdowns.

Strict was set at install because `privacy.html` promised "Clarity's strictest
masking setting". It was then changed because that promise was doing no real work:
**this site has no forms, no search box and no input fields at all**, so there is
no visitor-entered data for any mode to protect. The only thing Strict masked was
the site's own published text, which anyone can read by visiting. What it cost was
legibility, since replays and heatmaps are hard to interpret with everything
blocked out.

**The page was edited first, then the toggle.** That order is the rule, not a
detail. The wording now explains rather than asserts: it states that the playbacks
show the same pages a reader is already looking at, and that the site has no input
fields, which a visitor can verify for themselves. The old claim could not be
verified by anyone, and would have become a false statement on a live page the
moment the toggle moved.

**If masking ever changes again, edit `privacy.html` first and upload it before
touching Clarity.** Two notes from Microsoft's docs: changes take up to an hour to
affect new recordings, and **they are never retroactive**, so existing recordings
keep whatever masking was live when they were captured.

Per-element overrides also exist if a specific thing ever needs hiding: CSS
selectors under Settings > Masking, or a `data-clarity-mask="True"` attribute in
the HTML, either of which overrides the global mode.

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

**Where the per-visitor detail actually lives.** A recording card in the Recordings
list shows entry page, exit page, duration, click and page counts, browser, device
and country. **Click "More details" for the two things the card omits: the full page
sequence, and the city.** Verified 2026-09-15: city resolves correctly to Calgary,
and all pages in the session are listed in order. The camera icons on the dashboard
cards are shortcuts into this list, pre-filtered to that group of visitors.

How Clarity covers the goal metrics:

| Wanted | Clarity |
|---|---|
| Unique visitors over time | Standard dashboard card |
| City | Country/State/City tabs, trend line for up to 5 cities |
| Session duration / time on site | Yes |
| Pages visited | Yes |
| Device type | Yes |
| Time of visit | **Weak, accepted.** Per-session timestamps, no distribution chart |
| Time spent per page | **Not available, accepted.** Not pursued at this volume |

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

## Dashboard: no customization needed

**Reviewed live on 2026-09-15 and closed.** The brief previously budgeted 45 to 90
minutes to strip Clarity's default dashboard down to the goal metrics, on the
assumption it would be as noisy as Google Analytics and Cloudflare Web Analytics,
both of which the owner rejected for exactly that reason. It is not. The default
above-the-fold view carries the whole list and little else:

| Wanted | Where it is |
|---|---|
| Unique visitors over time | Users overview card, with a new vs returning split |
| City | Region tab, Countries / States / Cities |
| Session duration | Active time spent tile |
| Pages per session | Pages per session tile |
| Device type | Devices tab |
| Referrer | Referrer card |

Owner's verdict: *"The above-the-fold viewport gives me exactly what I needed, no
more, no less."* **Do not propose a dashboard cleanup session.** If cards populate
below the fold they are simply ignored, which costs nothing.

The one piece of noise in the default view is the **Scroll depth** tile. It was left
alone deliberately; it is not worth a click to remove.

Two gaps remain and are accepted, not open work:

- **Time of day.** Per-session timestamps only, no distribution chart. At roughly
  five visitors a week the Recordings list shows this per session anyway.
- **Time spent per page.** Never verified as available. Not pursued, since the
  per-session figure is sufficient at this volume.

If either ever becomes worth having, the route is a CSV export and a chart built
from it, roughly 1 to 2 hours. Nobody needs to do that now.

Own-IP filtering is not a dashboard task. It is the `localStorage` gate, described
above. No IP blocking.
