---
title: AUTOSAR 与 J1939 集成 Q2：J1939 的 BAM / CMDT 多帧传输和 AUTOSAR CanTp 的机制差异？同时跑 J1939 和 UDS 会冲突吗？
tags:
  - AUTOSAR
  - 1000问
---

# AUTOSAR 与 J1939 集成 Q2：J1939 的 BAM / CMDT 多帧传输和 AUTOSAR CanTp 的机制差异？同时跑 J1939 和 UDS 会冲突吗？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1MjU1MDA4

AUTOSAR 与 J1939 集成 Q2：J1939 的 BAM / CMDT 多帧传输和 AUTOSAR CanTp 的机制差异？同时跑 J1939 和 UDS 会冲突吗？

J1939 多帧传输（两种方式）：

- BAM（广播公告消息）：用于广播 / 全局地址（DA=255）。发送方先发一个连接管理消息（TYPE=32）宣布大包，然后按固定间隔（约 50ms）把所有数据帧（TP.DT）依次广播出去，接收方不确认、不建点对点连接。

- CMDT（点对点数据传输）：用于指定目的地址。发送方发请求发送 RTS（TYPE=16），接收方回准备接收 CTS（TYPE=17），建立连接，按接收方节奏（CTS 控制帧数 / 间隔）传输，最后结束确认（TYPE=19）。

- 数据帧：每个 TP.DT 是 8 字节标准 CAN 帧，第 1 字节序号 + 7 字节数据，最多约 1785 字节（255 帧）。


AUTOSAR CanTp（ISO 15765-2 / ISO-TP）：

- First Frame（FF）带总长度 → 接收方回 Flow Control（FC，含窗口 Block Size + 帧间隔 STmin）→ 发送方按窗口连续发 Consecutive Frames（CF）→ 循环到结束。
- 机制：点对点、有流控确认，同一通道（CAN ID）上同一时刻只有一个 ISO-TP 传输。

两者差异：

1. 连接建立：J1939 CMDT 用 RTS / CTS 握手 + 序号流控；ISO-TP 用 FF / FC 流控（接收方主动控制窗口）。

2. 广播 vs 点对点：J1939 支持 BAM（广播、无确认）和 CMDT（点对点、确认）；ISO-TP 基本是点对点。

3. 数据上限：J1939 约 1785 字节；ISO-TP 常规约 4095 字节（扩展更长）。

4. 确认 / 流控：ISO-TP 用 FC（BS + STmin）精确控；J1939 CMDT 用 CTS；BAM 无流控、固定间隔。

5. 寻址：J1939 用 PGN + SA / DA；ISO-TP 用 CAN ID + 地址。


会冲突吗？不会直接冲突：

- 两者是独立的多帧协议，各用自己的 CAN ID 号段（ISO-TP 用诊断类 ID 如 0x7E0/0x7E8；J1939 用专门的连接管理 PGN 和 TP 报文）。从 CAN 网络看是两个不同的 ID 空间，物理层交错帧正常。
- AUTOSAR 里 J1939Tp 和 CanTp / CanIf 是独立模块，CanIf / PduR 按 PDU（PGN）路由到不同 Tp 模块，协议栈互不干扰。
- 潜在冲突点只在网络负载 / 优先级竞争（靠 CAN 仲裁用 ID 优先级解决），以及「同一 ID 上不能混两种协议」——只要 ID 不重叠、每个 ID 只跑一种协议，就不冲突。

一句话：J1939（BAM/CMDT）和 CanTp（ISO-TP）是两套独立多帧协议，寻址和 ID 号段不同、模块也不同，同时跑不冲突；真正的约束是一个 CAN ID 只承载一种协议，其余只是总线负载竞争。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU1MjU0OTM2><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR