# Decent Reliability

A minimal, text-forward personal site built with Jekyll. Write content in markdown, commit, and GitHub Pages automatically builds and deploys.

Features the visual identity of darioamodei.com: ET Book serif typeface, warm cream paper in light mode / near-black in dark mode, underlined text links, and a smooth light/dark toggle.

## Quick Start

**To create a new essay:**

1. Create a new file in `_essays/` named `your-title.md`
2. Add frontmatter:
   ```yaml
   ---
   title: "Your Essay Title"
   dek: "Optional subtitle"
   date: 2026-01-15
   ---
   ```
3. Write your content in markdown below the frontmatter
4. Commit and push - GitHub builds automatically

**To create a new post:**

1. Create a new file in `_posts/` named `YYYY-MM-DD-title.md`
2. Add frontmatter (same as essays)
3. Write content in markdown
4. Commit and push

## File Structure

```
_essays/              → Long-form essays (markdown)
_posts/               → Short posts (markdown, named YYYY-MM-DD-title.md)
_layouts/             → Jekyll layouts (default, essay, post)
fonts/et-book/        → Self-hosted ET Book font files
index.html            → Homepage (auto-lists essays & posts)
archive.html          → Archive page (auto-lists all content)
style.css             → All styling
theme.js              → Dark mode toggle
_config.yml           → Jekyll configuration
```

## Local Development

To preview locally before pushing:

```bash
bundle install
bundle exec jekyll serve
```

Visit http://localhost:4000

## GitHub Pages Deployment

GitHub Pages automatically builds Jekyll sites. Just push to `main` branch:

```bash
git add .
git commit -m "Add new essay"
git push
```

GitHub builds and deploys within 1-2 minutes.

## Custom Domain Setup

The `CNAME` file configures `decentreliability.com`.

**DNS Configuration** (at your domain registrar):

Add four A records for the root domain:

| Type | Host | Value |
|------|------|-------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

Add CNAME for www:

| Type | Host | Value |
|------|------|-------|
| CNAME | www | raconger.github.io |

**GitHub Settings:**

1. Go to Settings → Pages
2. Under Custom domain, verify `decentreliability.com`
3. Wait for DNS check (a few minutes to 24 hours)
4. Enable "Enforce HTTPS" once verified

## Font

**ET Book** - the typeface Edward Tufte commissioned for his books. Self-hosted (no CDN dependency).

- License: MIT (Dave Liepmann / Edward Tufte)
- Only three weights included: regular, italic, bold
- Uses `font-display: swap` for instant text rendering
- Total size: ~370 KB

## Markdown Support

Full markdown support in essays and posts:

- Headings (`##`, `###`)
- **Bold** and *italic*
- Links
- Lists (bulleted and numbered)
- Code blocks
- Blockquotes
- Horizontal rules

## Theme

Colors switch automatically based on system preference and persist via localStorage:

- Light mode: cream `#f0ebdd` / ink `#17140f`
- Dark mode: `#1a1712` / `#f0ebdd`
- Respects `prefers-reduced-motion`
