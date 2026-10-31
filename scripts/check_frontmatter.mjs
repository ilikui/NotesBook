#!/usr/bin/env node
/**
 * 预检 content/ 下所有 Markdown 的 frontmatter 是否为合法 YAML。
 *
 * Quartz 构建时若 frontmatter 解析失败会直接抛错中断，但报错只给出行列号，
 * 很难定位到具体文件。这个脚本在构建前把问题一次性列出来。
 *
 * 常见元凶：从外部工具导入的笔记里键名前多了一个空格（" tags:"），
 * 或者含半角冒号的值没有加引号。
 *
 * 用法：node scripts/check_frontmatter.mjs [content 目录，默认 content]
 */
import fs from "node:fs"
import path from "node:path"
import yaml from "js-yaml"

const root = process.argv[2] ?? "content"

/** 递归收集所有 .md 文件 */
function collect(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) collect(full, out)
    else if (entry.name.endsWith(".md")) out.push(full)
  }
  return out
}

/** 取出 frontmatter 的行区间；没有 frontmatter 则返回 null */
function frontmatterBlock(text) {
  if (!text.startsWith("---")) return null
  const lines = text.split("\n")
  if (lines[0].trim() !== "---") return null
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === "---") return { lines, start: 1, end: i }
  }
  return null
}

if (!fs.existsSync(root)) {
  console.error(`目录不存在：${root}`)
  process.exit(1)
}

const files = collect(root).sort()
const problems = []

for (const file of files) {
  const text = fs.readFileSync(file, "utf8")
  const block = frontmatterBlock(text)
  if (!block) continue

  const body = block.lines.slice(block.start, block.end)
  try {
    yaml.load(body.join("\n"))
  } catch (err) {
    // js-yaml 的 mark.line 是相对 frontmatter 内容的 0 基行号
    const line = (err.mark?.line ?? 0) + block.start + 1
    problems.push({
      file,
      line,
      message: err.reason ?? err.message.split("\n")[0],
      snippet: (block.lines[line - 1] ?? "").replace(/\t/g, "→"),
    })
  }
}

if (problems.length === 0) {
  console.log(`frontmatter 检查通过：${files.length} 个文件`)
  process.exit(0)
}

console.error(`frontmatter 检查失败：${problems.length} 个文件存在非法 YAML\n`)
for (const p of problems) {
  console.error(`  ${p.file}:${p.line}`)
  console.error(`    ${p.message}`)
  console.error(`    > ${p.snippet}`)
  if (/^\s+\S/.test(p.snippet) && !/^\s+-\s/.test(p.snippet)) {
    console.error(`    提示：键名前的空格会导致 YAML 解析失败，请顶格书写`)
  }
  console.error("")
}
process.exit(1)
