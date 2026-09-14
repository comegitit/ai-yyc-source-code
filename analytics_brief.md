# Analytics Brief — Microsoft Clarity Install

Working document for Claude Code. Rewritten 2026-09-08 to fold in what was
settled and verified in the preceding session. Supersedes the original brief.

Site: hand-written HTML/CSS/JS portfolio at ai-yyc.com, 34 live pages, DNS
proxied through Cloudflare on the free plan. Deploy is a **manual upload to
`public_html`**, not git-deployed.

---

## Status

**Done and live.** The supporting work is finished, deployed and verified on
desktop and mobile:

- The shared footer (`siteFooter` in `master_nav.js`) carries the four top-level
  nav links.
- `education.html` built; the old Education submenu was replaced by a plain nav
  link, so all four nav items are ordinary links.

**Written but deliberately parked.** `privacy.html` exists in the repo and is
finished, but it describes a Clarity install that has not shipped yet, so on
2026-09-08 it was pulled back:

- The file was **removed from `public_html`** by hand. It is still in git.
- The footer privacy link is **commented out** in `siteFooter` in
  `master_nav.js`.

**Not done.** The Clarity tag itself. That is the whole of what remains.

**Blocked on:** signing up at clarity.microsoft.com and copying the project ID.
Nothing else is blocked.

### Restoring the privacy page — required, and easy to forget

This is the last step of the install, not an optional extra. Once the tag is live:

1. Uncomment the privacy link in `siteFooter` in `master_nav.js`. The bottom row
   re-splits on its own; the CSS rule that centres the lone copyright
   (`.footer-bottom p:only-child`) stops matching by itself, so **nothing in
   `style.css` needs undoing.**
2. **Put `privacy.html` back in the sitemap.** Delete the `"privacy.html"` line
   from the `EXCLUDE` set in `tools/generate_sitemap.py`, then regenerate:

   ```sh
   python tools/generate_sitemap.py
   ```

   It was excluded on purpose while the page returned 404, because a sitemap
   listing a 404 reports an error in Search Console. Miss this step and the page
   goes live but stays out of the sitemap, and search engines are far less likely
   to find it. The count should go from 32 URLs to 33.
3. Upload `privacy.html` back into `public_html`, and re-upload `master_nav.js`
   and `sitemap.xml`.
4. Purge the Cloudflare cache. Needed for `master_nav.js`; `privacy.html` and
   `sitemap.xml` are never edge-cached.

**The page also makes a commitment that constrains setup.** It states the site
"runs Clarity's strictest masking setting", so **setting masking to Strict is not
optional** once the page is public again. Do not put the page back without it.

---

## Decisions already made — do not relitigate

**Tool: Microsoft Clarity, free tier.** Re-examined in the last session against
the actual goal metrics and confirmed as the right choice. Do not substitute a
different analytics tool.

**Goal metrics:** unique visitors, city, time of visit, total time on site, all
charted over time. Device type is nice-to-have. Everything else in the dashboard
is noise for this use case.

How Clarity actually covers that list, verified 2026-09-08:

| Metric | Clarity |
|---|---|
| Unique visitors over time | Standard dashboard card |
| City | Yes. Country/State/City tabs with a trend line for up to 5 cities. City and state were added to dashboard cards in October 2025; before that they were filter-only |
| Time of visit | Weak. Per-session timestamps, but no time-of-day distribution chart |
| Total time on site | Yes, session duration / active time spent |
| Device type | Yes |

**The recordings list is the real answer at this traffic level.** Five visitors a
week does not make a meaningful trend line. Each row of Clarity's recordings list
is one session with its timestamp, location, device and duration, which is the
entire metric list, per visitor, in list form. Expect that to be more useful than
the charts until volume grows.

**Alternatives were considered and rejected.** Plausible and Fathom fit the
literal metric list slightly better but cost around $9/month. GoatCounter is free
but has no session duration at all. Cloudflare Web Analytics is free and
cookieless but was rejected as overwhelming, and cannot do session recordings.

**No IP blocking.** The owner's connection is dual-stack and dynamically
assigned. Clarity supports IPv4 only, and cannot reliably block when a visitor
has both stacks. An IP block would work intermittently and fail silently, which
is worse than no filter. **Do not configure IP blocking.**

**Self-exclusion is handled client-side**, by gating the tag behind a
`localStorage` flag with a query-parameter toggle so it can be set on mobile
where there is no dev console. IP-agnostic, survives ISP reassignment.

**No cookie consent banner.** Personal portfolio, Canadian, no commercial
transactions, no accounts, no sensitive data. A banner only means something if it
actually gates the tag; one that appears while tracking regardless is a false
claim and worse than none. Meaningful consent must be opt-in, which would thin
and skew the data. `privacy.html` states this position openly, which is the
substitute for a banner. **Do not add a banner, and do not add a partial or
decorative one.**

---

## Implementation

### Structure

Do not paste the script into 34 files. Create one shared file containing the code
below (no `<script>` wrapper inside the file itself), and add a single line to
each page.

**Path note.** There is currently no `/js/` directory; `master_nav.js` lives at
the repo root. Either create `/js/` or put the file at the root beside
`master_nav.js`. Pick one and be consistent.

**Reference it root-absolutely**, e.g. `/js/analytics.js`. `404.html` already
does this for `master_nav.js`, and the comment in `getBasePath()` explains why:
the error page is served at whatever depth was requested, so relative paths break
there. The tradeoff is that root-absolute paths break `file://` preview; use a
local HTTP server (`python -m http.server`) rather than opening files directly.

**Do not fold this into `master_nav.js`.** Tempting, since that file is already
on 33 of the 34 pages and it would be a zero-file-edit install. Rejected for two
reasons: it couples tracking to navigation, so a future nav refactor could
silently kill analytics; and it would miss `ai-grading-system_v3.html`, which
does not include `master_nav.js` at all.

### The file

```js
(function () {
  var p = new URLSearchParams(location.search);
  if (p.get('notrack') === '1') localStorage.setItem('noTrack', '1');
  if (p.get('notrack') === '0') localStorage.removeItem('noTrack');
  if (localStorage.getItem('noTrack')) return;

  (function(c,l,a,r,i,t,y){
      c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
      t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
  })(window, document, "clarity", "script", "YOUR_PROJECT_ID");
})();
```

**Two provisos:**

1. `YOUR_PROJECT_ID` must be replaced with the real ID. The file does nothing
   until it is.
2. The **inner** block is Clarity's vendor snippet and may have been revised. Use
   whatever Clarity provides at signup for that part, dropped inside the outer
   wrapper. The outer wrapper is the custom piece and should be kept as-is.

### Suggested improvement to the toggle

The `?notrack=1` step gives no feedback, which is exactly why it gets skipped.
Add a brief visible confirmation when the flag is set or cleared: a small
fixed-position element that appears for a couple of seconds. A console log is not
enough, because the whole point is that this has to be done on mobile. **Do not
use `alert()`.**

### Per-page insertion

Add immediately before the closing `</head>` tag:

```html
<script src="/js/analytics.js"></script>
```

Rules for the bulk edit:

- Insert before `</head>`, never at the top of the file or above `<!DOCTYPE html>`.
- **Skip any file that already contains the line.** A re-run must not double-tag.
- If a file has no `<head>`, report it rather than guessing.
- **Output a list of every file changed** when done, for spot-checking.

### Which files, exactly

**34 live pages**: 11 at the root, 6 in `blog/`, 17 in `blog/posts/`. Verify with
`find . -name "*.html" -not -path "./.git/*" ! -name statistics.html ! -name webdev.html | wc -l`
rather than trusting this number. Scope confirmed by survey, not assumption:

- **`ai-grading-system_v3.html` needs the tag added directly.** It has no
  `master_nav.js`, no `#site-header` and no `#site-footer`. It is a real
  destination, linked from `hcai.html`. **This is the single page most likely to
  be missed.**
- **Exclude `statistics.html` and `webdev.html`.** They exist in the repo and as
  server-side archives but are **not in `public_html`**. They are commented out
  of the nav deliberately. Do not tag them, do not link them, do not ask about
  them. Their absence from a coverage audit is correct, not a finding.
- `index_old.html` no longer exists; it was deleted in the last session.
- `education.html` is live and needs the tag. `privacy.html` needs the tag too:
  it is out of `public_html` right now but goes back as the final step, so tag it
  in the same sweep rather than leaving it as a straggler.
- `404.html` needs it too. Tagging the error page is useful, since it surfaces
  broken inbound links.

---

## Setup order

1. Sign up at clarity.microsoft.com and create a project for the domain. Free,
   no card required.
2. Copy the project ID.
3. Create the analytics file with the real project ID substituted in.
4. Add the one-line script tag to all 34 pages before `</head>`.
5. Deploy by manual upload, then **purge the Cloudflare cache.** Skipping this is
   the usual reason data doesn't appear.
6. Set masking to **Strict** in Clarity Settings. See the live-promise note at
   the top: this is now a published commitment, not a nice-to-have. The site has
   no contact form, only a `mailto:` link, so Strict costs nothing.
7. Load a page in an incognito window and confirm requests to `clarity.ms` in the
   Network tab.
8. Visit `ai-yyc.com/?notrack=1` once on **each** browser and device the owner
   uses.

Data takes a couple of hours to appear. Test in incognito, since the normal
browser will have `noTrack` set after step 8.

**Expect a stale-cache false alarm.** A browser that visited recently keeps
serving its own copy of `master_nav.js` and `style.css` and shows the pre-deploy
site. Verified 2026-09-08: a page appeared to still have the old nav until a hard
reload, while the edge was serving the correct file all along. HTML is not
edge-cached (`cf-cache-status: DYNAMIC`), so page edits do go live immediately.
When verifying the tag, hard-reload or use incognito before concluding anything
is broken.

Updated 2026-09-09: the browser TTL is now set by `mod_expires` in `.htaccess`,
not by Cloudflare. Cloudflare's Browser Cache TTL was moved to "Respect Existing
Headers", replacing a flat 4-hour override that had shadowed the origin. Current
values: HTML 5 minutes, CSS and JS 1 hour, images 7 days, fonts 1 year. Before
this change the JS files carried no cache header at all, which left them on
browser heuristic caching and could hold `blog_posts.js` stale for days after a
post was published.

---

## If data never appears, check these in order

**Cloudflare Rocket Loader.** Free plan, under Speed > Optimization. It rewrites
and defers scripts and has a long history of breaking analytics tags. It would
also likely break `master_nav.js`, which listens for `DOMContentLoaded` — since
the nav currently works, Rocket Loader is probably already off, but confirm it
rather than assume.

**Content-Security-Policy.** **Verified 2026-09-08: there is no CSP anywhere.**
Every HTML file and `.htaccess` was checked, and no `<meta http-equiv>` or CSP
header is set. The one thing not visible from the repo is a Cloudflare Transform
Rule adding a CSP header server-side, so check the Rules tab. If one is ever
added, Clarity needs `https://www.clarity.ms`, `https://c.bing.com`, and the
lettered subdomains `https://[a-z].clarity.ms` — Clarity spreads across lettered
subdomains, so allowing a single host will not cover it.

**Cache.** Purge Cloudflare again. HTML is not cached by default on the free
plan, but `master_nav.js` and `style.css` are.

**Missing tags.** A page without the tag is invisible. This shows up as "only the
homepage gets traffic."

---

## Domain verification

Clarity will ask for confirmation of site ownership. It usually detects the tag
automatically once data starts flowing, so installing first and letting it
self-verify is the path of least resistance.

---

## Facts already baked into `privacy.html` — do not "correct" them

(The page is parked out of `public_html` for now; see Status. The copy itself is
signed off and should not be reopened.)

These were verified against Microsoft's own documentation and are deliberate:

- The opt-out is **not** a Microsoft-hosted page. It is the Digital Advertising
  Alliance tool at `https://optout.aboutads.info/`, where you select Microsoft
  from a list. `https://youradchoices.com/pmc` (Protect My Choices) keeps the
  preference from being cleared with cookies.
- Clarity **does not** respond to Do Not Track, but **does** support Global
  Privacy Control (`https://globalprivacycontrol.org/`). Both facts are stated,
  because GPC is a control a visitor can actually use.
- Microsoft Privacy Statement: `https://www.microsoft.com/privacy/privacystatement`
- The page deliberately avoids a blanket "no personal information is collected."
  Session replay plus city-level location does not support that claim. It names
  what specifically is not collected instead.

---

## Out of scope for now

**Dashboard customization.** Stripping the dashboard down to the goal metrics is
a separate, later task. Clarity's default dashboard is busy (rage clicks, dead
clicks, scroll depth) and will provoke the same reaction Cloudflare's did. The
fix is removing and rearranging cards, but do it *after* a week of real data,
once it's clear what actually gets looked at. Get the tag installed and confirmed
working first.

---

## Session notes, 2026-09-09 evening

Decisions made in conversation that are not reflected in the body above. Fold
them in properly when convenient; until then, read this section as authoritative
where it conflicts.

**State verified 2026-09-14: nothing in the install has been done.** No `js/`
directory, no `analytics.js`, no `clarity.ms` reference in any page, privacy link
still commented out in `master_nav.js`, `privacy.html` still in `EXCLUDE`.
**Step 1 of Setup order is the next action.**

### Change to the setup order

**Set masking to Strict before deploying, not after.** The body has it as step 6,
after the tag is live. Move it to immediately after creating the project. Otherwise
the first sessions are captured unmasked, and `privacy.html` promises strictest
masking from the moment it is public. Costs nothing to do early.

### No UTM parameters on outreach links. Decided, do not re-propose.

The install was pulled forward to measure LinkedIn DM outreach conversion. UTM
tagging was proposed and **rejected by the owner**, correctly:

- A DM link displaying `?utm_source=linkedin&utm_medium=dm&utm_content=07` reads
  as funnel processing to a contact being asked for help.
- It risks the OG preview card, which is doing real work in the message.
- **At this traffic volume the timestamp is the attribution.** Baseline is roughly
  five visitors a week. A cluster of sessions in the hours after a blitz is
  unambiguous without any query parameter.

What is lost is per-contact identification. Two free partial recoveries: keep a
send-order log with rough times and cross-reference against session timestamps;
and city is a weak identifier where only one contact lives there.

### Expectations set

- **Clarity lags 30 minutes to 2 hours.** Not real-time. Do not conclude the tag
  is broken from a blank dashboard 15 minutes after install.
- **Single-digit session counts make every chart useless.** The recordings list is
  the instrument, as the body already says.

### Dashboard metrics the owner actually wants

For the later customization task. Verified against Clarity's capabilities:

| Wanted | Clarity |
|---|---|
| Unique visitors over time | Standard card |
| Geographic location | Country/State/City cards |
| Session duration | Yes |
| Pages visited | Yes |
| Device type | Yes |
| Time of day | **Weak.** Per-session timestamps only, no distribution chart |
| Time spent per page | **Uncertain.** Verify live rather than assume |

Own-IP filtering is not a dashboard task. It is the `localStorage` gate, already
decided. No IP blocking.

### Time estimates

Active work is about 2h20m: Phase 1 signup and masking 15 min, Phase 2 code
(analytics file, 34-page insert, privacy restoration, local verify, commit) about
65 min, Phase 3 upload, cache purge and verification about 55 min. Phases 1 and 3
cost no Claude quota. Owner budgets 6 hours elapsed.

Dashboard customization is a separate 45 to 90 minute collaborative session, to be
done after a week of real data. Add 1 to 2 hours if the time-of-day and per-page
gaps need a charting workaround built from a CSV export.

### Update 2026-09-14: the outreach went out untracked

The LinkedIn blitz that pulled this install forward has already happened. LinkedIn
rate-limited the rapid sends as suspected spam, so the messages went out slowly
over several days rather than in one 9:30 AM burst. **No Clarity tag was live for
any of it.** Those clicks are unrecoverable.

Consequences for how this work is framed from here:

- **The install is no longer deadline-driven.** Do it properly rather than fast.
- **Residual value is still real.** DM links have a long tail; people open messages
  days late. Installing now catches stragglers from this round, and covers any
  follow-up messages, which is the more likely place the intel gets used.
- **Timestamp-as-attribution is weaker than planned.** Sends were spread across
  days, so there is no single spike to read. The baseline of roughly five visitors
  a week is still low enough that any elevated traffic is probably outreach, but
  it can no longer be tied to a specific send.
- The send-order log idea in the previous section is now retrospective at best.

Separately: the LinkedIn card-suppression behaviour is a known, settled issue. Do
not re-investigate the site as a cause.
