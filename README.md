# ai-yyc-source-code

**🔗 Live site: [ai-yyc.com](https://ai-yyc.com)**

Source code for [ai-yyc.com](https://ai-yyc.com) — the personal portfolio and
blog of **Roy Aggarwal**, focused on AI governance & ethics, responsible AI, and
digital transformation.

Built solo, one page at a time, vibe-coding with AI. Not a developer by trade,
but an AI professional who ships.

## Overview

A static, multi-page site (HTML/CSS/vanilla JavaScript). There is no build
step and no backend — files are served as-is.

## Stack

- **HTML5 / CSS3** — hand-authored, with a CSS custom-property design system in
  `style.css` (single source of truth for colour, type, and spacing tokens).
- **Vanilla JavaScript** — no framework. Shared header/footer and the blog
  listing are injected client-side.

## Project structure

| Path | Purpose |
| --- | --- |
| `index.html` | Home / career landing page |
| `blog.html` | Blog index (categories + latest posts) |
| `blog/` | Blog category pages |
| `blog/posts/` | Individual blog post pages |
| `*.html` (root) | Coursework and topic pages (ethics, hcai, predictive, etc.) |
| `master_nav.js` | Injects the shared header/footer on every page; resolves paths from any folder depth |
| `blog_posts.js` | Blog post metadata (the data that drives all listings) |
| `blog_categories.js` | Blog sidebar + shared post-card rendering helpers |
| `style.css` | Global styles and design tokens |
| `images/` | Logos, icons (SVG), and social link-preview images |
| `fonts/` | Self-hosted Source Serif 4 (woff2) and its OFL licence |
| `documents/` | Downloadable resumes and coursework artifacts (PDF, etc.) |

## Adding a blog post

1. Create the post HTML in `blog/posts/`.
2. Add a metadata entry to the `BLOG_POSTS` array in `blog_posts.js`
   (see the commented template at the bottom of that file).

Use lowercase, hyphenated filenames (e.g. `my-new-post.html`) — no spaces.

## Local preview

Serve the folder with any static server, for example:

```sh
python -m http.server 8000
```

Then open <http://localhost:8000/index.html>.

## License

© Roy Aggarwal. All rights reserved.
