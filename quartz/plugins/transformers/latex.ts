import remarkMath from "remark-math"
import rehypeKatex from "rehype-katex"
import rehypeMathjax from "rehype-mathjax/svg"
//@ts-ignore
import rehypeTypst from "@myriaddreamin/rehype-typst"
import { QuartzTransformerPlugin } from "../types"
import { KatexOptions } from "katex"
import { Options as MathjaxOptions } from "rehype-mathjax/svg"
//@ts-ignore
import { Options as TypstOptions } from "@myriaddreamin/rehype-typst"

interface Options {
  renderEngine: "katex" | "mathjax" | "typst"
  customMacros: MacroType
  katexOptions: Omit<KatexOptions, "macros" | "output">
  mathJaxOptions: Omit<MathjaxOptions, "macros">
  typstOptions: TypstOptions
}

interface MacroType {
  [key: string]: string
}

/**
 * remark-math only understands `$...$` / `$$...$$`. Notes written in Obsidian (or
 * pasted from LaTeX docs) often use `\(...\)` and `\[...\]` instead, which markdown
 * happily renders as literal `(` / `[` plus raw LaTeX source.
 *
 * Rewrite those delimiters into dollar form before parsing, while leaving fenced code
 * blocks and inline code untouched. `\[ ... \]` is only treated as math when it spans
 * whole lines or its content actually looks like LaTeX — prose such as the shell test
 * `\[ -d build \]` must stay text.
 */
const MATH_HINT = /\\[a-zA-Z]+|[_^]|=/

function convertDelimiters(text: string): string {
  return (
    text
      // 整行独立的 \[ ... \] 视为块级公式
      .replace(/^(\s*)\\\[[ \t]*$/g, (_all, indent: string) => `${indent}$$`)
      .replace(/^(\s*)\\\][ \t]*$/g, (_all, indent: string) => `${indent}$$`)
      // 行内 \( ... \)
      .replace(
        /(?<!\\)\\\((.+?)(?<!\\)\\\)/g,
        (_all, body: string) => (body.trim() === "" ? _all : `$${body}$`),
      )
      // 行内 \[ ... \]，只在内容确实像公式时转换
      .replace(/(?<!\\)\\\[(.+?)(?<!\\)\\\]/g, (all, body: string) =>
        MATH_HINT.test(body) ? `$$${body}$$` : all,
      )
  )
}

function normalizeMathDelimiters(src: string): string {
  const lines = src.split("\n")
  const out: string[] = []
  let fence: string | undefined

  for (const line of lines) {
    const marker = line.match(/^\s*(`{3,}|~{3,})/)
    if (marker) {
      const char = marker[1][0]
      if (fence === undefined) {
        fence = char
      } else if (fence === char) {
        fence = undefined
      }
      out.push(line)
      continue
    }
    if (fence !== undefined) {
      out.push(line)
      continue
    }

    // keep inline code spans intact, convert only the surrounding text
    out.push(
      line
        .split(/(`+[^`]*`+)/g)
        .map((segment, index) => (index % 2 === 1 ? segment : convertDelimiters(segment)))
        .join(""),
    )
  }

  return out.join("\n")
}

export const Latex: QuartzTransformerPlugin<Partial<Options>> = (opts) => {
  const engine = opts?.renderEngine ?? "katex"
  const macros = opts?.customMacros ?? {}
  return {
    name: "Latex",
    textTransform(_ctx, src) {
      if (engine === "katex" || engine === "mathjax") {
        return normalizeMathDelimiters(src)
      }
      return src
    },
    markdownPlugins() {
      return [remarkMath]
    },
    htmlPlugins() {
      switch (engine) {
        case "katex": {
          return [[rehypeKatex, { output: "html", macros, ...(opts?.katexOptions ?? {}) }]]
        }
        case "typst": {
          return [[rehypeTypst, opts?.typstOptions ?? {}]]
        }
        case "mathjax": {
          return [[rehypeMathjax, { macros, ...(opts?.mathJaxOptions ?? {}) }]]
        }
        default: {
          return [[rehypeMathjax, { macros, ...(opts?.mathJaxOptions ?? {}) }]]
        }
      }
    },
    externalResources() {
      switch (engine) {
        case "katex":
          return {
            // Bundled locally (copied from node_modules/katex/dist into quartz/static/katex)
            // so formulas still render when the jsDelivr CDN is slow or blocked.
            css: [{ content: "/static/katex/katex.min.css" }],
            js: [
              {
                // fix copy behaviour: https://github.com/KaTeX/KaTeX/blob/main/contrib/copy-tex/README.md
                src: "/static/katex/contrib/copy-tex.min.js",
                loadTime: "afterDOMReady",
                contentType: "external",
              },
            ],
          }
      }
    },
  }
}
