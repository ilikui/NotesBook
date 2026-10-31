#!/usr/bin/env python3
"""检查构建产物 public/ 中是否有指向不存在文件的站内链接。

Quartz 生成的链接是相对且不带 .html 后缀的（例如 `../../Area/EE/工具`），
在 GitHub Pages 上由服务器补全扩展名。本脚本按同样的规则判断链接是否有效：

- `foo`        -> `foo` 或 `foo.html` 或 `foo/index.html`
- `/foo`       -> 站点根目录下的同样规则
- 外部 URL、纯锚点、mailto/data 链接会跳过

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
SKIP_PREFIXES = ("http:", "https:", "//", "#", "mailto:", "data:", "javascript:", "tel:")


def is_page_candidate(path: str) -> bool:
    return any(
        os.path.exists(candidate)
        for candidate in (path, path + ".html", os.path.join(path, "index.html"))
    )


def page_link_base(page: str, dirpath: str, site_root: str) -> str:
    """返回 Quartz 生成相对链接时使用的页面基准目录。

    Quartz 的 FolderPage 会把目录页写入 folder/index.html，但链接是按
    目录 slug（folder）计算的，而不是按物理文件所在目录（folder/index.html）
    计算。若直接使用 dirpath，会多算一层目录，造成静态资源和站内链接误报。
    tags.html 同样对应 tags 这个虚拟 slug。
    """
    name = os.path.basename(page)
    if name == "index.html":
        return os.path.dirname(dirpath)
    if name == "tags.html":
        return os.path.join(site_root, "tags")
    return dirpath


def resolve(base_dir: str, url_path: str, site_root: str) -> str:
    """把链接解析成文件系统路径。"""
    target = urllib.parse.unquote(url_path)
    if target.startswith("/"):
        return os.path.normpath(os.path.join(site_root, target.lstrip("/")))
    return os.path.normpath(os.path.join(base_dir, target))


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else "public"
    if not os.path.isdir(root):
        print(f"目录不存在：{root}")
        return 2

    site_root = os.path.abspath(root)
    broken: Counter[str] = Counter()
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
                # 去掉锚点与查询串，只看文件本身
                url_path = url.split("#")[0].split("?")[0]
                if not url_path:
                    continue
                base_dir = page_link_base(page, dirpath, site_root)
                target_path = resolve(base_dir, url_path, site_root)
                if is_page_candidate(target_path):
                    continue
                broken[url_path] += 1
                examples.setdefault(url_path, os.path.relpath(page, root))

    print(f"检查页面数：{pages}")
    if not broken:
        print("站内链接全部有效 ✅")
        return 0

    print(f"失效链接：{sum(broken.values())} 处，共 {len(broken)} 个不同目标 ❌")
    for url, count in broken.most_common():
        print(f"  {count:>3}  {url}    （例如出现在 {examples[url]}）")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
