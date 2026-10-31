---
title: AUTOSAR MCAL 配置说明 · 模块⑩ CanTrcv
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑩ CanTrcv

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1Mzk1

**AUTOSAR MCAL 配置说明 · 模块⑩ CanTrcv**

CanTrcv 是 CAN 收发器驱动，管理收发器硬件（如 TJA1041 / TJA1145 / TJA1043 等），负责显性/隐性电平转换、总线唤醒、故障检测、模式切换。

**核心职责**：收发器模式管理、总线唤醒、故障检测（Bus-off / TXD 超时 / GND 断开）。

**关键配置项**：

- CanTrcvHardwareObject：收发器硬件对象（映射到具体收发器）。
- CanTrcvController：绑定到对应 CAN 控制器。
- CanTrcvMode：模式——Normal / Standby / Sleep / Listen-only 等。
- CanTrcvWakeUpMode：唤醒能力（可否被总线唤醒、唤醒源）。
- CanTrcvBaudRateConfig：波特率。
- CanTrcvFailureMode：故障模式（GND 断开、TXD 超时、Bus-off）。
- CanTrcvWakeUpSupport / BusOffDetection / TransceiverType：唤醒与故障检测配置。

**常用 API**：CanTrcv\_Init、CanTrcv\_SetMode（Normal / Sleep / Standby）、CanTrcv\_GetMode、CanTrcv\_GetBusState / CheckWakeup、CanTrcv\_MainFunction\_HandleTimeout。

**配置思路**：

1. 选收发器型号 \+ 绑定到 CAN 控制器。
2. 配模式（Normal / Standby / Sleep）和唤醒能力。
3. 配故障检测（TXD 超时、Bus-off、GND 断开）。
4. 配波特率。

**常见坑**：

- 模式切换不当 → 收发 / 唤醒异常（没进 Normal 无法通信）。
- 唤醒配置错 → 总线唤醒不生效或误唤醒。
- 故障检测配置不当 → 检测不到 Bus-off / TXD 超时。
- 波特率 / 收发器类型不匹配 → 通信问题。
- CanTrcv\_MainFunction\_HandleTimeout 没周期调用 → 故障 / 超时处理失效。

**CanTrcv 与 Can 分工**：Can 管控制器（协议层），CanTrcv 管收发器（物理层：电平、唤醒、故障）。两者配合实现 CAN 通信 + 低功耗唤醒。

📎 上一个（Can）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY1Mzc5><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL