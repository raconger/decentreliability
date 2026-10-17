#!/usr/bin/env python3
"""Import podcast episodes from the RSS feed into the _episodes collection.

Usage:
  python3 scripts/import_episodes.py           # add new episodes only
  python3 scripts/import_episodes.py --force   # rewrite every episode file

Existing episode files are left alone unless --force is passed, so show notes
edited by hand in _episodes/ are preserved.
"""

import argparse
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED_URL = "https://feed.justcast.com/shows/05554e06be7642a6f4acd5fa420f56a6081dc1a8/audioposts.rss"
ITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
OUT_DIR = Path(__file__).resolve().parent.parent / "_episodes"


def slugify(text):
    text = text.lower().replace("’", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def clean_notes(raw):
    # JustCast stores empty descriptions as <p><br></p>
    notes = re.sub(r"<p>\s*(<br\s*/?>)?\s*</p>", "", (raw or "").strip())
    return notes.strip()


def summarize(notes):
    first = re.search(r"<(p|blockquote)>(.*?)</\1>", notes, re.S)
    text = first.group(2) if first else notes
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()


def yaml_str(value):
    # JSON strings are valid YAML scalars and handle all escaping
    return json.dumps(value, ensure_ascii=False)


def episode_file(item):
    title = item.findtext("title").strip()
    number = int(item.findtext(f"{ITUNES}episode"))
    date = parsedate_to_datetime(item.findtext("pubDate"))
    enclosure = item.find("enclosure")
    notes = clean_notes(item.findtext("description"))

    front = {
        "title": yaml_str(title),
        "episode": number,
        "season": int(item.findtext(f"{ITUNES}season") or 1),
        "date": date.strftime("%Y-%m-%d %H:%M:%S %z"),
        "duration": yaml_str(item.findtext(f"{ITUNES}duration").lstrip("0:") or "0"),
        "audio_url": yaml_str(enclosure.get("url")),
        "audio_length": int(enclosure.get("length") or 0),
        "summary": yaml_str(summarize(notes)),
        "justcast_url": yaml_str(item.findtext("link")),
    }
    lines = ["---"] + [f"{k}: {v}" for k, v in front.items()] + ["---", ""]
    body = "\n".join(lines) + (notes + "\n" if notes else "")
    return f"{number:02d}-{slugify(title)}.md", number, body


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="overwrite existing episode files")
    args = parser.parse_args()

    with urllib.request.urlopen(FEED_URL) as resp:
        channel = ET.fromstring(resp.read()).find("channel")

    OUT_DIR.mkdir(exist_ok=True)
    existing = {int(p.name.split("-", 1)[0]): p for p in OUT_DIR.glob("*.md")}
    added = 0
    for item in channel.findall("item"):
        name, number, body = episode_file(item)
        if number in existing and not args.force:
            continue
        if number in existing:
            existing[number].unlink()
        (OUT_DIR / name).write_text(body, encoding="utf-8")
        print(f"wrote _episodes/{name}")
        added += 1

    print(f"{added} episode(s) written", file=sys.stderr)


if __name__ == "__main__":
    main()
