---
title: ObsidianFlavoredMarkdown
tags:
  - plugin/transformer
---

This plugin provides support for [[工业互联网]].

> [!note]
> For information on how to add, remove or configure plugins, see the [[configuration#Plugins|Configuration]] page.

This plugin accepts the following configuration options:

- `comments`: If `true` (default), enables parsing of `%%` style Obsidian comment blocks.
- `highlight`: If `true` (default), enables parsing of `==` style highlights within content.
- `wikilinks`:If `true` (default), turns [[处理器架构]] into regular links.
- `callouts`: If `true` (default), adds support for [[计算机组成原理|callout]] blocks for emphasizing content.
- `mermaid`: If `true` (default), enables [[RTOS|Mermaid diagram]] rendering within Markdown files.
- `parseTags`: If `true` (default), parses and links tags within the content.
- `parseArrows`: If `true` (default), transforms arrow symbols into their HTML character equivalents.
- `parseBlockReferences`: If `true` (default), handles block references, linking to specific content blocks.
- `enableInHtmlEmbed`: If `true`, allows embedding of content directly within HTML. Defaults to `false`.
- `enableYouTubeEmbed`: If `true` (default), enables the embedding of YouTube videos and playlists using external image Markdown syntax.
- `enableVideoEmbed`: If `true` (default), enables the embedding of video files.
- `enableCheckbox`: If `true`, adds support for interactive checkboxes in content. Defaults to `false`.
- `disableBrokenWikilinks`: If `true`, replaces links to non-existent notes with a dimmed, disabled link. Defaults to `false`.

> [!warning]
> Don't remove this plugin if you're using [[工业互联网|Obsidian]] to author the content!

## API

- Category: Transformer
- Function name: `Plugin.ObsidianFlavoredMarkdown()`.
- Source: [`quartz/plugins/transformers/ofm.ts`](https://github.com/jackyzha0/quartz/blob/v4/quartz/plugins/transformers/ofm.ts)
