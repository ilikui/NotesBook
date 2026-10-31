#!/usr/bin/env python3
"""Generate vercel.json with lowercase -> canonical redirects.

Background: the site used to live on Netlify, whose "Pretty URLs" setting
301-redirects every path to its lowercase form. Browsers cache 301s forever,
so visitors who ever opened /Archive/Archive keep requesting /archive/archive.
Vercel serves a case-sensitive filesystem, so those cached redirects land on a
404 (Quartz's "私有笔记或笔记不存在" page).

This script scans the build output and emits a redirect map so the lowercase
paths keep working: /archive/archive -> 301 -> /Archive/Archive.

Usage:
    python scripts/gen_vercel_redirects.py [build_dir] [-o vercel.json]

Run it after `npx quartz build`, before deploying.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

# Vercel caps the redirects array; stay well below the limit.
MAX_REDIRECTS = 900


def collect_pages(build_dir: str) -> list[str]:
    """Return canonical URL paths for every emitted HTML page."""
    pages: list[str] = []
    for root, _dirs, files in os.walk(build_dir):
        for name in files:
            if not name.endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(root, name), build_dir).replace("\\", "/")
            if rel.endswith("index.html"):
                url = "/" + rel[: -len("index.html")]
            else:
                url = "/" + rel[: -len(".html")]
            pages.append(url)
    return sorted(set(pages))


def build_redirects(pages: list[str]) -> list[dict]:
    redirects: list[dict] = []
    seen: set[str] = set()

    def add(source: str, destination: str) -> None:
        if source in seen or source == destination:
            return
        seen.add(source)
        redirects.append({"source": source, "destination": destination, "permanent": True})

    for page in pages:
        lower = page.lower()
        if lower == page:
            continue
        is_folder = page.endswith("/")
        add(lower, page)
        if is_folder:
            # trailingSlash normalisation can hand us either form
            add(lower.rstrip("/"), page)
            add(page.rstrip("/").lower() + "/", page)

    redirects.sort(key=lambda r: r["source"])
    if len(redirects) > MAX_REDIRECTS:
        print(f"warning: {len(redirects)} redirects exceeds {MAX_REDIRECTS}", file=sys.stderr)
        redirects = redirects[:MAX_REDIRECTS]
    return redirects


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("build_dir", nargs="?", default="public")
    parser.add_argument("-o", "--output", default="vercel.json")
    args = parser.parse_args()

    if not os.path.isdir(args.build_dir):
        print(f"error: build dir not found: {args.build_dir}", file=sys.stderr)
        return 1

    pages = collect_pages(args.build_dir)
    redirects = build_redirects(pages)

    config = {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "cleanUrls": True,
        "trailingSlash": True,
        "redirects": redirects,
    }
    with open(args.output, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(config, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    print(f"pages scanned: {len(pages)}")
    print(f"redirects written: {len(redirects)} -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
