---
title: SOMEIPTransformer
tags:
  - Project
  - AUTOSAR
  - CP
---

**SOME/IP Transformer** 是 CP 的转换器（Transformer）规范，负责把数据**线性化为 SOME/IP 的线上（on-the-wire）格式**，为嵌入式环境提供一套面向服务的客户端 / 服务器通信机制。注意：唯一正确的写法是 **SOME/IP**（`Some/IP` 等写法是错的）。

> [!info] 一句话定位
> 让 CP 也能「面向服务」：把 C 数据结构序列化成 SOME/IP 报文，跨 ECU 传服务调用与事件。

## 规范信息

| 项目 | 内容 |
| --- | --- |
| 平台 | CP |
| 类别 | SWS — 软件模块规范（Software Specification） |
| UID | 660 |
| 版本 | R25-11 |
| 本地 PDF | [AUTOSAR_CP_SWS_SOMEIPTransformer.pdf](file:///F:/Work/Standards/01_Sources/CP_SWS_SOMEIPTransformer_660/AUTOSAR_CP_SWS_SOMEIPTransformer.pdf) |
| 纯文本全文 | [CP_SWS_SOMEIPTransformer.complete.txt](file:///F:/Work/Standards/01_Sources/CP_SWS_SOMEIPTransformer_660/zzgen/CP_SWS_SOMEIPTransformer.complete.txt) |

## 核心要点

- **为什么要「再造一套」**：不使用现成中间件的目的是得到一种技术，它同时满足：
  - 满足嵌入式世界对**资源消耗**的硬性要求；
  - 尽可能**兼容**大量用例与通信伙伴；
  - 提供汽车用例所需的特性；
  - 可从极小平台**伸缩**到大型平台；
  - 可实现在不同操作系统（AUTOSAR、GENIVI、OSEK）乃至无 OS 的嵌入式设备上。
- **职责**：把数据按 SOME/IP 线上格式线性化，实现客户端 / 服务器通信。
- **依赖**：必须有 [[RTE]] 存在才能执行该转换器。

## 依赖关系

- 依赖 [[RTE]]；协议本体见 FO 文档 [SOMEIPProtocol](file:///F:/Work/AUTOSAR_Module_Notes/FO/PRS/SOMEIPProtocol.md)。

## 相关

- [[RTE]]
- [[TcpIp]]
- [[CommunicationManagement]]
- [[FO]]
- [[CP]]
- [[规范模块]]
