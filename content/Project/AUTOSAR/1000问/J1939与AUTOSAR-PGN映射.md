---
title: AUTOSAR 与 J1939 集成 Q1：J1939 的 PGN 对应 AUTOSAR 的哪个概念？在 COM 层兼容还是应用层另写？
tags:
  - AUTOSAR
  - 1000问
---

# AUTOSAR 与 J1939 集成 Q1：J1939 的 PGN 对应 AUTOSAR 的哪个概念？在 COM 层兼容还是应用层另写？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1MjU0OTM2

AUTOSAR 与 J1939 集成 Q1：J1939 的 PGN 对应 AUTOSAR 的哪个概念？在 COM 层兼容还是应用层另写？

答：J1939 的 PGN 概念上对应 AUTOSAR 的 **PDU**（协议数据单元）。

分层对应：

- J1939 的 SPN（信号参数号）≈ AUTOSAR 的 Signal。
- J1939 的 PGN（参数组）≈ AUTOSAR 的 PDU（一个 PGN 封装一组 SPN 信号）。
- J1939 的优先权 / DA / SA ≈ CAN 优先级、节点寻址（PduR 路由 / 地址）。
- 每个 PGN 有 PGN 号、优先权、SA/DA、数据长度。

在 COM 层兼容还是应用层另写？两种做法：

1. 走 AUTOSAR 的 J1939 栈（推荐）：用 J1939 模块（J1939Tp + J1939 NM 寻址），把 PGN 建模成 COM 层的 PDU、SPN 映射成 Signal。这样能复用 AUTOSAR 的配置 / 生成 / 路由机制，跟 UDS 等其他 CAN 通信统一管理，也支持大包多帧传输。

2. 应用层另写：把 J1939 当一串原始 CAN 帧，在 SW-C / CDD 里直接解析 PGN / SPN。适合少量、特殊或定制场景，但牺牲 AUTOSAR 配置化的好处，链路更手工。


推荐：走 AUTOSAR 的 J1939 通信栈，在 COM 层把 PGN 当 PDU、SPN 当 Signal 建模——因为 PGN 本质就是「一组相关信号的编组」，概念跟 AUTOSAR PDU 高度对应，发送 / 接收路由也基于 PDU（PGN）级别。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU1MjU0ODUx><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR