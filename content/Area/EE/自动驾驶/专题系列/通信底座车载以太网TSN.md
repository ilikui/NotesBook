---
title: 专栏⑳·第6篇：通信底座——车载以太网、TSN、SOME-IP
tags:
  - 自动驾驶
  - 专题系列
---

# 专栏⑳·第6篇：通信底座——车载以太网、TSN、SOME-IP

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjUyMTU1ODc2

**专栏⑳·第6篇：通信底座——车载以太网、TSN、SOME-IP**

▎ **为什么自动驾驶要换通信底座**<br>
CAN 2.0 只有 1Mbps，连传感器原始数据都传不动（摄像头一帧就是 MB 级）。自动驾驶要三样：高带宽（传感器 / 地图 / 日志）、低延迟（实时控制）、确定性（时间同步）。

▎ **三件套**

1. 车载以太网（100BASE-T1 / 1000BASE-T1）：单对双绞线、高带宽——接通信专栏⑫补充四
2. TSN（时间敏感网络）：确定性调度——802.1AS 时间同步、802.1Qbv 门控调度、802.1CB 帧复制消除——接时间同步专题
3. SOME-IP：服务化通信——服务发现、订阅发布，接 AUTOSAR 服务层

▎ **通信架构**

- 域内：域控制器内部（PCIe / 以太网）
- 域间：主干以太网 \+ TSN 交换机（环形 / 星形）
- 传感器接入：GMSL / FPD-Link 串行链路（摄像头）→ 域控
- 关键：所有数据共享一个时间基准（StbM / gPTP）——感知融合、多 ECU 协同的前提

▎ **三个坑**

1. 带宽算错：8 路 1080p@30fps 原始数据是 GB 级——先压缩（H.264/H.265）或边缘处理再传
2. TSN 配置复杂：门控表（GCL）配置错，优先级反转——确定性变成不确定性
3. SOME-IP 服务发现抖动：多服务同时 Offer 造成 SD 报文风暴——要限速和抖动抑制

▎ **一句话**：通信底座三件套——以太网管带宽、TSN 管确定性、SOME-IP 管服务化；所有数据共享一个时间基准，是感知融合和多 ECU 协同的前提。

📎 通信专栏⑫·补充四 车载以太网 → [https://v.flomoapp.com/mine/?memo\_id=MjUxMDI5MjY2](https://v.flomoapp.com/mine/?memo_id=MjUxMDI5MjY2)<br>
📎 时间同步专题导航 → [https://v.flomoapp.com/mine/?memo\_id=MjUxMjAzOTEx](https://v.flomoapp.com/mine/?memo_id=MjUxMjAzOTEx)<br>
📎 专栏⑳导航 → [https://v.flomoapp.com/mine/?memo\_id=MjUyMDEzNTQx](https://v.flomoapp.com/mine/?memo_id=MjUyMDEzNTQx)

**专栏⑳进度：6/10篇**

#Area/技术/自动驾驶