---
title: "微信读书"
description: "从微信读书自动同步的个人书架与阅读记录索引。"
tags:
  - 阅读
  - 微信读书
---

# 微信读书

这里将自动同步微信读书中的书籍目录、划线与个人想法。首次同步成功后，会生成书架索引与每本书的独立页面。

- 数据来源：[ilikui/WeRead](https://github.com/ilikui/WeRead)
- 自动同步：每天定时运行，也支持 GitHub Actions 手动触发。
- 隐私默认值：只公开书籍元数据和记录数量；划线与批注默认不公开。

首次配置时，需要在 NotesBook 仓库的 **Settings → Secrets and variables → Actions** 中添加 `WEREAD_API_KEY`。如需在网站上公开具体划线和批注，再将仓库变量 `WEREAD_PUBLISH_NOTES` 设为 `true`。

## 同步入口

自动同步完成后，书架与每本书的阅读记录会出现在本页。详细的阅读方法见 [[Area/KM/渐进阅读]] 与 [[Area/KM/知识管理工作流]]。
