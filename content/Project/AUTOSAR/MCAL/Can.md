---
title: AUTOSAR MCAL 配置说明 · 模块⑨ Can
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑨ Can

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1Mzc5

**AUTOSAR MCAL 配置说明 · 模块⑨ Can**

Can 是 CAN 通信驱动（MCAL 层），负责硬件 CAN 控制器的初始化、报文收发、控制器模式、Bus-off 处理。注意它只做帧级收发，上层 CAN 帧 ID 管理 / PDU 映射由 CanIf / CanNm / CanTp 等其他通信栈模块负责。

**核心职责**：控制器初始化、报文收发、模式切换、错误 / Bus-off 处理。

**关键配置项**：

- CanController：每个 CAN 控制器一个配置。
- CanControllerBaudRateConfig：波特率配置——仲裁段 + 数据段（CAN FD 时数据段更快），含预分频、采样点、SJW、Tseg1 / Tseg2。
- CanControllerMode：控制器模式（Normal / Sleep / Stop）。
- CanControllerActivation：激活 / 去激活。
- CanHardwareObject：硬件对象 / 邮箱（收发邮箱、标准 / 扩展 ID、DLC、FIFO 配置）。
- CanProcessingType：中断 / 轮询。
- CanControllerBusOff / State：Bus-off 与状态处理。

**常用 API**：Can\_Init、Can\_ControllerInit、Can\_Write（发送）、Can\_MainFunction\_Read / Write（轮询）、Can\_ControllerModeChange、Can\_EnableControllerInterrupts / Disable、Can\_GetControllerMode。

**配置思路**：

1. 配波特率（仲裁 / 数据段）\+ 位时序（采样点、SJW、Tseg）。
2. 配硬件对象（邮箱：标准 / 扩展 ID、DLC、方向）。
3. 配处理方式（中断 / 轮询）。
4. 配控制器模式与行为。

**常见坑**：

- 波特率 / 采样点配错 → 通信不了或误码。
- 硬件邮箱配错（ID、DLC、方向）→ 收发不到。
- Bus-off 处理配置不当 → 恢复失败或通信中断。
- 中断和轮询混用 → 收发异常。
- 轮询模式没周期调用 Can\_MainFunction → 不收发。
- CAN FD 的数据段波特率 / 采样点没单独配 → FD 通信失败。

📎 上一个（Gpt）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY1Mjc3><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL