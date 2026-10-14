#!/usr/bin/env python3
"""Import WeRead export JSON into the Quartz digital garden."""
from __future__ import annotations
import hashlib, json, os, re, sys, unicodedata
from datetime import datetime, timezone
from pathlib import Path

def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKC", str(value or "book")).strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s-]+", "-", value).strip("-")
    return value[:64] or "book"

def yaml_string(value: object) -> str:
    return json.dumps(str(value if value is not None else ""), ensure_ascii=False)

def markdown_quote(value: str) -> str:
    value = (value or "").strip()
    return "\n".join("> " + line if line else ">" for line in value.splitlines()) if value else ""

def format_date(value: object) -> str:
    if value in (None, ""): return ""
    try:
        number = float(value)
        if number > 10_000_000_000: number /= 1000
        return datetime.fromtimestamp(number, timezone.utc).strftime("%Y-%m-%d")
    except (ValueError, TypeError, OSError, OverflowError):
        return str(value)[:32]

def render_book(book: dict, publish_notes: bool) -> str:
    title = str(book.get("title") or "未命名书籍").strip()
    author = str(book.get("author") or "作者未知").strip()
    cover = str(book.get("cover") or "").strip()
    category = str(book.get("category") or "").strip()
    notes = book.get("notes") or []
    count = int(book.get("note_count") or len(notes))
    lines = [
        "---", f"title: {yaml_string(title)}", f"author: {yaml_string(author)}",
        f"book_id: {yaml_string(book.get('book_id', ''))}", f"cover: {yaml_string(cover)}",
        f"category: {yaml_string(category)}", f"note_count: {count}", "tags:",
        "  - 微信读书", "  - 阅读记录", "---", "", f"# {title}", "",
        f"- **作者：** {author}", f"- **分类：** {category or '未分类'}",
        f"- **个人划线与想法：** {count} 条",
    ]
    if cover: lines += ["", f"![《{title}》封面]({cover})"]
    lines += ["", "## 阅读记录", ""]
    if not publish_notes:
        lines += [
            f"当前页面同步书籍信息与记录数量（共 {count} 条），未公开原始划线和个人批注。", "",
            "如需在公开网站展示具体记录，请在仓库 Settings → Secrets and variables → Actions → Variables 中将 WEREAD_PUBLISH_NOTES 设置为 true。开启后，个人划线和批注会公开发布。",
        ]
    elif not notes:
        lines.append("这本书目前没有可导出的划线或批注。")
    else:
        for i, note in enumerate(notes, 1):
            chapter = str(note.get("chapter") or "未标注章节").strip()
            created = format_date(note.get("created_at"))
            lines += [f"### {i}. {chapter}", ""]
            if created: lines += [f"<small>记录日期：{created}</small>", ""]
            highlight = markdown_quote(str(note.get("highlight") or ""))
            comment = str(note.get("comment") or "").strip()
            if highlight: lines += ["**划线**", "", highlight, ""]
            if comment: lines += ["**想法 / 批注**", "", comment, ""]
            lines += ["---", ""]
    lines += ["", "来源：[微信读书](https://weread.qq.com/)", ""]
    return "\n".join(lines)

def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: import_weread_to_quartz.py INPUT_JSON OUTPUT_DIR", file=sys.stderr); return 2
    source, output = Path(sys.argv[1]), Path(sys.argv[2])
    books_dir = output / "书籍"
    if not source.is_file():
        print(f"导出 JSON 不存在：{source}", file=sys.stderr); return 2
    data = json.loads(source.read_text(encoding="utf-8"))
    books = data.get("books") or []
    if not books:
        print("导出数据中没有书籍；为避免误删现有记录，停止同步。", file=sys.stderr); return 3
    publish_notes = os.getenv("WEREAD_PUBLISH_NOTES", "false").strip().lower() in {"1", "true", "yes", "on"}
    books_dir.mkdir(parents=True, exist_ok=True)
    meta = data.get("meta") or {}
    total_notes = int(meta.get("total_notes") or sum(int(b.get("note_count") or 0) for b in books))
    index_lines = [
        "---", 'title: "微信读书"', 'description: "从微信读书自动同步的个人书架与阅读记录索引。"',
        "tags:", "  - 阅读", "  - 微信读书", "---", "", "# 微信读书", "",
        "> 本页面由自动同步脚本生成。源数据来自个人微信读书账号。", "",
        f"- **书籍数量：** {len(books)}", f"- **划线与批注总数：** {total_notes}",
        f"- **最近同步：** {meta.get('generated_at', '未知')}",
        f"- **记录公开模式：** {'公开划线与批注' if publish_notes else '仅公开书籍元数据'}",
        "", "## 书架", "", "| 书籍 | 作者 | 分类 | 记录数 |", "| --- | --- | --- | ---: |",
    ]
    expected_files: set[str] = set()
    for book in sorted(books, key=lambda item: str(item.get("title") or "").casefold()):
        title = str(book.get("title") or "未命名书籍").strip()
        book_id = str(book.get("book_id") or title)
        suffix = hashlib.sha1(book_id.encode("utf-8")).hexdigest()[:8]
        filename = f"{slugify(title)}-{suffix}.md"
        expected_files.add(filename)
        (books_dir / filename).write_text(render_book(book, publish_notes), encoding="utf-8")
        link_title = title.replace("|", "\\|")
        rel_link = f"[[Resource/微信读书/书籍/{filename[:-3]}|{link_title}]]"
        author = str(book.get("author") or "作者未知").replace("|", "\\|")
        category = str(book.get("category") or "未分类").replace("|", "\\|")
        count = int(book.get("note_count") or len(book.get("notes") or []))
        index_lines.append(f"| {rel_link} | {author} | {category} | {count} |")
    index_lines += [
        "", "## 同步说明", "",
        "- 由 ilikui/WeRead 仓库的微信读书导出脚本获取数据。",
        "- GitHub Actions 每天自动同步，也可在 Actions 中手动运行。",
        "- 默认只公开书籍元数据；原始划线与个人批注需显式开启公开模式。",
        "- 书籍详情页由脚本生成，请勿直接编辑生成文件；需要沉淀的独立观点建议另写永久笔记并链接到本页。",
        "", "相关主题：[[Area/KM/渐进阅读]] · [[Area/KM/知识管理工作流]] · [[Resource/index|资源总览]]", "",
    ]
    (output / "index.md").write_text("\n".join(index_lines), encoding="utf-8")
    for existing in books_dir.glob("*.md"):
        if existing.name not in expected_files: existing.unlink()
    print(f"已导入 {len(books)} 本书；公开模式={'全文记录' if publish_notes else '仅书籍元数据'}；生成目录：{output}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
