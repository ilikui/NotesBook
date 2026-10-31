#!/usr/bin/env python3
"""检查构建产物 public/ 中是否有失效的站内链接与锚点。

Quartz 生成的链接是相对且不带 .html 后缀的（例如 `../../Area/EE/工具`），
在静态托管上由服务器补全扩展名。本脚本按同样的规则判断链接是否有效：

- `foo`        -> `foo` 或 `foo.html` 或 `foo/index.html`
- `/foo`       -> 站点根目录下的同样规则
- `#bar`       -> 当前页面的元素 id
- `foo#bar`    -> 目标页面里存在 id="bar"
- 外部 URL、mailto/data 链接会跳过

用法：
    python scripts/check_links.py            # 检查 public/
    python scripts/check_links.py public     # 指定目录
"""

from __future__ import annotations

import os
import re
import sys
import urllib.parse
from collections import Counter

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')
ID_RE = re.compile(r'\bid="([^"]+)"')
SKIP_PREFIXES = ("http:", "https:", "//", "#", "mailto:", "data:", "javascript:", "tel:")


def page_candidates(path: str) -> list[str]:
    return [path, path + ".html", os.path.join(path, "index.html")]


def resolve_page(path: str) -> str | None:
    for candidate in page_candidates(path):
        if os.path.isfile(candidate):
            return candidate
    return None


def resolve(base_dir: str, url_path: str, site_root: str) -> str:
    """把链接解析成文件系统路径。"""
    target = urllib.parse.unquote(url_path)
    if target.startswith("/"):
        return os.path.normpath(os.path.join(site_root, target.lstrip("/")))
    return os.path.normpath(os.path.join(base_dir, target))


def collect_ids(root: str) -> dict[str, set[str]]:
    """收集每个页面里所有元素 id，用于校验锚点。"""
    ids: dict[str, set[str]] = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if not name.endswith(".html"):
                continue
            page = os.path.join(dirpath, name)
            with open(page, encoding="utf-8", errors="replace") as handle:
                html = handle.read()
            ids[page] = set(ID_RE.findall(html))
    return ids


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else "public"
    if not os.path.isdir(root):
        print(f"目录不存在：{root}")
        return 2

    site_root = os.path.abspath(root)
    ids_by_page = collect_ids(root)

    broken: Counter[str] = Counter()
    bad_anchors: Counter[str] = Counter()
    examples: dict[str, str] = {}
    pages = 0

    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            if not name.endswith(".html"):
                continue
            pages += 1
            page = os.path.join(dirpath, name)
            with open(page, encoding="utf-8", errors="replace") as handle:
                html = handle.read()

            for match in LINK_RE.finditer(html):
                url = match.group(1)
                if url.startswith(SKIP_PREFIXES):
                    continue

                url_path, _, fragment = url.partition("#")
                url_path = url_path.split("?")[0]

                if not url_path:
                    # 纯锚点：检查当前页面
                    if fragment and urllib.parse.unquote(fragment) not in ids_by_page.get(page, set()):
                        bad_anchors[f"#{fragment}"] += 1
                        examples.setdefault(f"#{fragment}", os.path.relpath(page, root))
                    continue

                target = resolve(dirpath, url_path, site_root)
                resolved = resolve_page(target)
                if resolved is None:
                    key = urllib.parse.unquote(url_path)
                    broken[key] += 1
                    examples.setdefault(key, os.path.relpath(page, root))
                    continue

                if fragment and resolved.endswith(".html"):
                    anchor = urllib.parse.unquote(fragment)
                    if anchor and anchor not in ids_by_page.get(resolved, set()):
                        key = f"{urllib.parse.unquote(url_path)}#{fragment}"
                        bad_anchors[key] += 1
                        examples.setdefault(key, os.path.relpath(page, root))

    print(f"检查页面数：{pages}")
    ok = True

    if broken:
        ok = False
        print(f"失效链接：{sum(broken.values())} 处，共 {len(broken)} 个不同目标 ❌")
        for url, count in broken.most_common():
            print(f"  {count:>3}  {url}    （例如出现在 {examples[url]}）")

    if bad_anchors:
        ok = False
        print(f"失效锚点：{sum(bad_anchors.values())} 处，共 {len(bad_anchors)} 个不同目标 ❌")
        for url, count in bad_anchors.most_common():
            print(f"  {count:>3}  {url}    （例如出现在 {examples[url]}）")

    if ok:
        print("站内链接与锚点全部有效 ✅")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
