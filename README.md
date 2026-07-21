# Personal site template

A minimal, text-forward personal site (bio + essays + posts + research +
op-eds + interviews), built with plain HTML/CSS/JS — no build step, no
framework. Matches the visual identity of darioamodei.com: a single serif
typeface for everything, warm cream paper in light mode / near-black in
dark mode, underlined text links, bulleted section lists, and a light/dark
toggle switch in the header.

- **Font: ET Book**, the typeface Edward Tufte commissioned for his own
  books (a Bembo-like serif). It's self-hosted — the `.woff`/`.ttf` files
  live in `fonts/et-book/` in this repo, so there's no external request to
  Google Fonts or any CDN. The page renders with the correct typeface on
  first paint with no network round-trip beyond your own domain, and it
  keeps working even if a third-party font CDN goes down.
  License: MIT (Dave Liepmann / Edward Tufte, from the `et-book` and
  `tufte-css` projects — see `fonts/et-book/LICENSE`).
- **Color:** cream `#f0ebdd` / ink `#17140f` in light mode, flipped to
  `#1a1712` / `#f0ebdd` in dark mode, toggled via the switch in the header
  (persists across visits using `localStorage`).

## Files

```
index.html                 → homepage (name, bio, bulleted section lists)
archive.html                → full list of essays/posts
style.css                   → all styling incl. @font-face + theme tokens
theme.js                     → dark-mode toggle + persistence
fonts/et-book/               → self-hosted ET Book font files (woff + ttf)
essay/example-essay.html    → template for a long-form essay (with dek + contents list)
post/example-post.html      → template for a short post
```

## Font performance notes

- Only three weights/styles are included (regular, italic, bold) — the
  ones this template actually uses — to keep the repo small (~370 KB
  total instead of shipping every ET Book variant).
- `index.html` includes a `<link rel="preload">` for the regular weight
  so the browser fetches it immediately instead of discovering it only
  after parsing `style.css`. Add the same preload tag to other pages if
  you want the same effect there.
- `font-display: swap` is set on all three `@font-face` rules, so text
  renders immediately in a fallback serif and swaps to ET Book the
  instant it loads — no invisible-text flash.

## 1. Customize the content

- Edit `index.html`: replace "Your Name", the bio paragraphs, and the
  links in each `<section class="list">` block.
- Duplicate `essay/example-essay.html` or `post/example-post.html` for
  each new piece of writing, rename the file, and link to it from
  `index.html` and `archive.html`.
- Update the `<title>` and `<meta name="description">` tags in each file.

## 2. Host it on GitHub Pages

1. Create a new repository on GitHub (e.g. `yourusername.github.io` for a
   root domain, or any name for a project page).
2. Push these files to the repo:
   ```bash
   git init
   git add .
   git commit -m "Initial site"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```
3. On GitHub: go to **Settings → Pages**.
4. Under **Build and deployment**, set **Source** to "Deploy from a branch",
   branch `main`, folder `/ (root)`. Save.
5. Wait a minute, then your site is live at:
   - `https://YOUR_USERNAME.github.io/` if the repo is named
     `YOUR_USERNAME.github.io`, or
   - `https://YOUR_USERNAME.github.io/YOUR_REPO/` otherwise.

## 3. Custom domain — decentreliability.com

A `CNAME` file with `decentreliability.com` is already included in this
repo (required by GitHub Pages — don't delete it).

**A) DNS records** — at your domain registrar (wherever you bought
`decentreliability.com`), add these records. Exact steps vary by
registrar, but you're looking for a "DNS" or "DNS management" section.

For the root domain (`decentreliability.com`) — add four **A** records,
all pointing to GitHub Pages' IPs:

| Type | Host / Name | Value |
|------|-------------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

For the `www` subdomain — add one **CNAME** record:

| Type | Host / Name | Value |
|------|-------------|-------|
| CNAME | www | YOUR_GITHUB_USERNAME.github.io |

(You can set up either the root domain, `www`, or both — GitHub will
redirect one to the other once configured in the next step.)

**B) GitHub Pages settings** — in your repo, go to **Settings → Pages**:
1. Under **Custom domain**, enter `decentreliability.com` and save.
   (This writes the same value into the `CNAME` file automatically —
   fine if it looks like it's overwriting what's already there.)
2. Wait for the DNS check to go green (can take a few minutes up to
   ~24 hours depending on your registrar's propagation time).
3. Once it's verified, tick **Enforce HTTPS** — GitHub issues a free TLS
   certificate for the domain automatically.

**C) Verify** — DNS propagation can take anywhere from a few minutes to
48 hours. You can check progress with:
```bash
dig decentreliability.com +noall +answer
```
Once it resolves to the four `185.199.10x.153` addresses above, the
site is live at `https://decentreliability.com`.

## Notes

- No JavaScript framework or build tool is required — just static files.
- Fonts load from Google Fonts via CDN; remove the `<link>` tags and
  self-host if you'd rather not depend on it.
- The layout is responsive and respects `prefers-reduced-motion`.
