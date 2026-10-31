---
title: Dcm 协议多路复用 Q2 用 DoIP 刷写和用 CAN TP 刷写同一个 ECU——Dcm 层处理逻辑一样吗？刷写速率谁快？CAN 路径断电接着刷，DoIP 支持同样的恢复吗？
tags:
  - AUTOSAR
  - 1000问
---

# Dcm 协议多路复用 Q2：用 DoIP 刷写和用 CAN TP 刷写同一个 ECU——Dcm 层处理逻辑一样吗？刷写速率谁快？CAN 路径断电接着刷，DoIP 支持同样的恢复吗？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1MjU1NTEz

Dcm 协议多路复用 Q2：用 DoIP 刷写和用 CAN TP 刷写同一个 ECU——Dcm 层处理逻辑一样吗？刷写速率谁快？CAN 路径断电接着刷，DoIP 支持同样的恢复吗？

Dcm 层处理逻辑一样吗？

- 上层 Dcm 的服务处理逻辑（会话、安全访问、0x34 请求下载、0x36 TransferData、0x37 请求退出传输、0x11 复位等刷写流程）是共享的、一样的。
- 不同的是传输层 / PDU 路由：CAN 走 CanTp（ISO-TP 多帧），DoIP 走 DoIP 模块（基于 TCP/IP、单消息承载大 payload）。同一个刷写服务，Dcm 层同一套，底层传输机制和分段方式不同。

刷写速率谁快？

- DoIP 明显更快。
- 原因：DoIP 基于 TCP/IP + 以太网（100M / 1000M），带宽远高于 CAN（500kbps）；DoIP 单消息 payload 大，不用像 ISO-TP 那样 8 字节一帧拆装、受 FC 流控（Block Size + STmin）限制。ISO-TP 每发一个窗口要等流控帧，吞吐受 STmin / BS 限制；DoIP 基本是高吞吐、低延迟。
- 实际 DoIP 可把刷写速率提升几个数量级（取决于以太网速率和数据块大小）。

CAN 路径断电接着刷，DoIP 支持同样的恢复吗？

- 先澄清：「断电接着刷」是刷写中断恢复机制（0x34 / 0x36 中掉电，重连后从断点或从头继续），通常靠 NvM 保存刷写进度 + 会话状态，不是传输协议本身。
- CAN 路径断电接着刷：通过诊断会话 + NvM 记录刷写状态（进度 / 块），重启后恢复——不是 CAN TP 独有，是「刷写应用 + NvM 持久化」提供的。
- DoIP 支持同样的恢复吗：支持。DoIP 只是传输通道，恢复逻辑同样在 Dcm / 刷写应用层（会话 + NvM 进度保存）。
- 补充：DoIP 走 TCP 有连接管理（keep-alive），重连后恢复会话通常更稳；但「能否断点续传」取决于 tester 和 ECU 的 Dcm 是否都实现了进度保存，而非协议本身决定。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU1MjU1NDE5><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR