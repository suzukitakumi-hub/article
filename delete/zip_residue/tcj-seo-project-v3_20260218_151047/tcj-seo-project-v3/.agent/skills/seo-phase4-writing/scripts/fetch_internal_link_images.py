#!/usr/bin/env python3
"""
Resolve internal link card images from linked WordPress posts.

Usage:
  python fetch_internal_link_images.py <html_file>
"""

from __future__ import annotations

import json
import re
import sys
from html import escape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import urlopen


CARD_PATTERN = re.compile(
    r'(<a\s+href="(?P<href>[^"]+)"\s+class="tcj-blogcard-link"[^>]*>\s*'
    r'<img\s+[^>]*?src="(?P<src>[^"]*)"(?P<img_rest>[^>]*)>)',
    re.IGNORECASE | re.DOTALL,
)

PLACEHOLDER_PATTERNS = (
    "placehold.jp",
    "placeholder",
    "/site-logo.svg",
)


def fetch_json(url: str) -> dict | list | None:
    try:
        with urlopen(url, timeout=10) as res:
            return json.loads(res.read().decode("utf-8", errors="ignore"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None


def extract_slug(permalink: str) -> str | None:
    parsed = urlparse(permalink)
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) >= 2 and parts[-2] == "posts":
        return parts[-1]
    return parts[-1] if parts else None


def get_featured_image_url(permalink: str) -> str | None:
    parsed = urlparse(permalink)
    if not parsed.scheme or not parsed.netloc:
        return None

    slug = extract_slug(permalink)
    if not slug:
        return None

    base = f"{parsed.scheme}://{parsed.netloc}"
    post_api = (
        f"{base}/wp-json/wp/v2/posts?slug={quote(slug)}"
        "&_fields=featured_media,yoast_head_json,yoast_head"
    )
    posts = fetch_json(post_api)
    if not isinstance(posts, list) or not posts:
        return None

    post = posts[0]

    yoast_json = post.get("yoast_head_json") or {}
    og_images = yoast_json.get("og_image")
    if isinstance(og_images, list) and og_images:
        maybe = og_images[0].get("url")
        if maybe:
            return maybe

    featured_media = post.get("featured_media")
    if isinstance(featured_media, int) and featured_media > 0:
        media_api = f"{base}/wp-json/wp/v2/media/{featured_media}?_fields=source_url"
        media = fetch_json(media_api)
        if isinstance(media, dict) and media.get("source_url"):
            return media["source_url"]

    yoast_head = post.get("yoast_head") or ""
    m = re.search(r'"thumbnailUrl":"([^"]+)"', yoast_head)
    if m:
        return m.group(1).replace("\\/", "/")
    return None


def needs_replacement(src: str) -> bool:
    s = src.strip().lower()
    if not s:
        return True
    return any(token in s for token in PLACEHOLDER_PATTERNS)


def replace_img_src(anchor_and_img: str, new_src: str) -> str:
    return re.sub(
        r'src="[^"]*"',
        f'src="{escape(new_src, quote=True)}"',
        anchor_and_img,
        count=1,
        flags=re.IGNORECASE,
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python fetch_internal_link_images.py <html_file>")
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        return 2

    html = path.read_text(encoding="utf-8", errors="ignore")
    changed = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal changed
        href = m.group("href")
        src = m.group("src") or ""
        full = m.group(1)

        if not needs_replacement(src):
            return full

        resolved = get_featured_image_url(href)
        if not resolved:
            return full

        changed += 1
        return replace_img_src(full, resolved)

    updated = CARD_PATTERN.sub(repl, html)

    if updated != html:
        path.write_text(updated, encoding="utf-8")

    print(f"[INFO] Updated card images: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

