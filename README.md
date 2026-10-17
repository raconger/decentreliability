# Decent Reliability

The website for the *Decent Reliability* podcast — the science, art, and history of reliability management — at **https://decentreliability.com**.

It's a Jekyll site hosted free on **GitHub Pages**. Every push to the `main` branch of `github.com/raconger/decentreliability` rebuilds and redeploys the site within a minute or two. There is no server to maintain.

---

## Quick reference

| I want to… | Do this |
|---|---|
| Publish a new episode on the site | Nothing — publish it on JustCast and the site picks it up daily at 15:00 UTC. [Details](#publishing-a-new-episode) |
| Get a new episode on the site *right now* | GitHub → **Actions** → **Import podcast episodes** → **Run workflow** |
| Change which episode is featured on the home page | Edit `featured:` in `_config.yml`, commit, push. [Details](#the-featured-episode) |
| Fix an episode description | Edit it in JustCast *and* in `_episodes/NN-….md`. [Details](#editing-episode-descriptions) |
| Add an Apple Podcasts / Spotify button | Fill in `apple:` / `spotify:` in `_config.yml`. [Details](#podcast-directories-apple-spotify) |
| See who signed up by email | Log in to Formspree (form `xaewbzyl`). [Details](#email-signups) |
| Preview the site on my computer | `bundle exec jekyll serve`. [Details](#previewing-locally) |
| Check whether the site deployed | GitHub → **Actions** → "pages build and deployment" |

---

## Publishing a new episode

**Normal workflow: publish on JustCast and you're done.**

A GitHub Action (`.github/workflows/import-episodes.yml`) runs every day at **15:00 UTC** (11am Eastern in summer, 10am in winter). It reads the JustCast RSS feed, creates a page for any episode the site doesn't have yet, commits it, and the site redeploys. On days with no new episode it does nothing.

Each new episode automatically gets:

- its own page at `/episodes/NN-episode-title/` with an audio player, MP3 download, show notes, subscribe links, and previous/next links
- a spot at the top of **All episodes** on the home page and in the archive

It does **not** become the featured episode on the home page — see [the featured episode](#the-featured-episode).

**Tips**

- **Write the full description in JustCast before publishing.** The site copies the description from the feed, so writing it once in JustCast keeps podcast apps and the website identical.
- The import only sees episodes that are actually *published* in the feed, not scheduled ones.
- If you can't wait for the daily run: GitHub → **Actions** → **Import podcast episodes** → **Run workflow** (green button). The site updates about two minutes later.

**Doing it by hand** (if the Action is ever broken):

```bash
cd ~/src/decentreliability
git pull
python3 scripts/import_episodes.py
git add _episodes && git commit -m "Add episode N" && git push
```

---

## The featured episode

The home page highlights one episode in a box with a player. It's set in `_config.yml`:

```yaml
podcast:
  featured: 7                          # episode number to highlight
  featured_label: Most popular episode # heading above it
```

- **Change the episode:** change the number.
- **Show the newest episode instead:** delete the `featured:` line. The heading automatically becomes "Latest episode" and updates itself with each new release.
- If the number doesn't match any episode, the site falls back to the newest one rather than breaking.

Currently featured: **Episode 7, "Healthcare as an analogy to APM"** — chosen because it has gotten the most attention.

---

## Editing episode descriptions

Each episode is a file in `_episodes/`, like `_episodes/07-healthcare-as-an-analogy-to-apm-….md`. The top section (between the `---` lines) holds the details; everything below it is the show notes shown on the page.

```yaml
---
title: "Healthcare as an analogy to APM - …"
episode: 7
date: 2024-08-23 12:43:00 +0000
duration: "16:26"
audio_url: "https://backend-api.justcast.com/…/602538.mp3"
summary: "One-paragraph summary used on the home page and in search results"
---
<p>Show notes go here…</p>
```

There are **two copies** of every description — one in JustCast (what podcast apps show) and one in the file (what the website shows). The import never overwrites a file that already exists, so to change a description:

1. **Edit it in JustCast** so podcast apps get it, **and**
2. **Edit the file** in `_episodes/` (both the `summary:` line and the notes below the `---`), then commit and push.

Or do step 1 only and then regenerate every page from the feed:

```bash
python3 scripts/import_episodes.py --force
git add _episodes && git commit -m "Refresh episode descriptions" && git push
```

> ⚠️ `--force` replaces **every** episode file with whatever is in JustCast. Any edits made only on the website are lost. See [open items](#open-items) — episodes 6, 7, and 9 currently have website-only edits.

---

## Podcast directories (Apple, Spotify)

| | |
|---|---|
| **Podcast host** | JustCast |
| **RSS feed** (give this to any directory) | `https://feed.justcast.com/shows/05554e06be7642a6f4acd5fa420f56a6081dc1a8/audioposts.rss` |
| **Apple Podcasts listing** | https://podcasts.apple.com/us/podcast/decent-reliability/id6801299399 |
| **Apple Podcasts Connect** (to manage it) | https://podcastsconnect.apple.com |
| **Feed owner email** (Apple may verify with it) | conger@hey.com |

**Showing directory buttons on the site.** The home page and every episode page show subscribe links. Only the RSS link appears until you add others in `_config.yml`:

```yaml
podcast:
  apple: "https://podcasts.apple.com/us/podcast/decent-reliability/id6801299399"
  spotify: ""   # paste the Spotify show URL here once it's listed
```

An empty value (`""`) hides that button.

**If you ever move podcast hosts again:** don't submit the new feed as a new show — that creates a duplicate listing and strands your followers. Instead, in Podcasts Connect open the existing show, replace the RSS feed URL, save, and click **Refresh Feed**. Status shows "Processing" for a while; the public listing can take several more hours to catch up. Then update `FEED_URL` in `scripts/import_episodes.py` and `feed:` in `_config.yml`.

**History:** the show was briefly hosted on rss.com in mid-2026, and the Apple listing was created from that feed. When hosting moved back to JustCast, the rss.com feed started returning 404 and Apple was stuck showing 3 old episodes. On 2026-10-17 the Apple feed URL was switched to JustCast in Podcasts Connect.

---

## Email signups

The "Get new episodes by email" form appears on the home page and on every episode page. It's one shared file: `_includes/signup.html`.

- Submissions go to **Formspree**, form ID **`xaewbzyl`** (`https://formspree.io/f/xaewbzyl`). Log in at formspree.io to see and export the list of addresses.
- Formspree only collects addresses; it doesn't send newsletters. When you email subscribers, you send it yourself (or import the list into a newsletter tool).
- People who signed up on the old "coming soon" page were promised one launch email.

To change the wording, edit `_includes/signup.html`. The heading and note text are at the top.

---

## Logo and cover art

| File | Used for |
|---|---|
| `assets/cover.jpg` | Original artwork (dark navy, bright orange), shown in **dark mode** and used as the preview image when links are shared |
| `assets/cover-light.png` | Light version (cream circle, darker orange `#c06a00`), shown in **light mode** |

The site swaps between them automatically with the light/dark toggle. The light version was made from the 3000×3000 original on JustCast by recoloring it, so the curve and lettering are pixel-identical in shape. The orange was darkened because the original `#ffa332` is hard to read on the cream page.

The cover art in podcast apps is separate — it's whatever is uploaded to JustCast.

---

## Previewing locally

```bash
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000. Changes to files reload automatically (except `_config.yml`, which needs a restart).

**If you get `cannot load such file -- erb`:** newer Ruby versions (3.4+) no longer bundle some gems Jekyll needs. Add these lines to `Gemfile` and run `bundle install` again:

```ruby
gem "erb"
gem "logger"
gem "csv"
gem "base64"
gem "bigdecimal"
```

This only affects your computer — GitHub Pages builds the live site with its own setup.

---

## Troubleshooting

**A new episode isn't on the site.**
1. Is it published (not scheduled) in JustCast? Open the RSS feed URL in a browser and look for it.
2. Has the daily run happened yet? It runs at 15:00 UTC. Run it by hand from GitHub → Actions → **Import podcast episodes** → **Run workflow**.
3. Did the run fail? GitHub emails you when a workflow fails; open the run under Actions to see the log.

**`git push` is rejected with "fetch first" / "non-fast-forward".**
The daily Action committed a new episode since you last pulled. Run `git pull`, then push again.

**I pushed but the site didn't change.**
GitHub → **Actions** → "pages build and deployment" shows each deploy. A deploy marked *cancelled* is normal when two pushes land close together — the newer one replaces it. Look for the latest one marked successful. Browsers also cache aggressively; try a private window.

**The site is down or shows a certificate error.**
Check GitHub → repo **Settings → Pages**. The custom domain should read `decentreliability.com` with "Enforce HTTPS" checked. The `CNAME` file in the repo must exist and contain `decentreliability.com` — deleting it disconnects the domain.

---

## How the site is built

```
index.html            → Home page: logo, featured episode, all episodes, email signup
archive.html          → /archive/ — every episode, essay, and post
_episodes/            → One file per podcast episode (created by the importer)
_layouts/episode.html → Template for episode pages
_layouts/default.html → Shared page frame: header, theme toggle, footer
_includes/signup.html → Email signup form
_includes/subscribe-links.html → RSS / Apple / Spotify links
scripts/import_episodes.py      → Reads the RSS feed, writes _episodes/ files
.github/workflows/import-episodes.yml → Runs the importer daily
assets/               → Logo / cover art
_config.yml           → Site settings, podcast settings, featured episode
style.css             → All styling (colors are defined at the top)
theme.js              → Light/dark toggle
CNAME                 → Custom domain — don't delete
```

The site also supports **essays** (`_essays/`, long-form) and **posts** (`_posts/YYYY-MM-DD-title.md`, short). Neither has any content right now; if you add some, they appear on the archive page. Each needs a header like:

```yaml
---
title: "Your Title"
dek: "Optional subtitle"
date: 2026-01-15
---
```

---

## Hosting and domain

- **Host:** GitHub Pages, building from the root of `main` ("legacy" Jekyll build — no workflow file needed for the site itself).
- **Domain:** `decentreliability.com`, set by the `CNAME` file. HTTPS is enforced; GitHub renews the certificate automatically.
- **DNS** (at the domain registrar): four `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`, and a `CNAME` for `www` → `raconger.github.io`.

---

## Design

- **Font:** ET Book (the typeface Edward Tufte commissioned for his books), self-hosted in `fonts/et-book/`, MIT licensed.
- **Colors:** light mode cream `#f0ebdd` with ink `#17140f`; dark mode `#1a1712` with `#f0ebdd`. Defined at the top of `style.css`.
- The light/dark choice follows the visitor's system setting until they use the toggle, then it's remembered.

---

## Open items

As of 2026-10-17:

- [ ] **Apple Podcasts** — feed URL switched to JustCast and refreshed; status was "Processing". Once the listing shows all 9 episodes, add the Apple URL to `apple:` in `_config.yml`.
- [ ] **Paste website-only description edits into JustCast**, so podcast apps match the site (and so `--force` is safe again):
  - [x] Episode 7 — new description (done; feed matches the site)
  - [ ] Episode 6 — the feed only has the first paragraph; add the second one from `_episodes/06-….md`
  - [ ] Episode 9 — feed still says "In 30 minutes"; change to "In 13 minutes"
  - To check: run `python3 scripts/import_episodes.py --force`, then `git diff _episodes`. No diff means they match; `git checkout -- _episodes` undoes the test either way.
- [ ] **Spotify** — if the show is listed there, add the URL to `spotify:` in `_config.yml`.
- [ ] Consider sending the promised launch email to the people who signed up on the coming-soon page.
