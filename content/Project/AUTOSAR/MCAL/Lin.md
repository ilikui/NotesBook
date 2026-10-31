---
title: AUTOSAR MCAL 配置说明 · 模块⑪ Lin
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑪ Lin

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1NDA3

**AUTOSAR MCAL 配置说明 · 模块⑪ Lin**

Lin 是 LIN 通信驱动，管理 LIN 通道的收发、主/从节点、帧调度。LIN 是单线、低成本、低速率（常见 9600 / 19200 bps 级）的局部互联总线，常用于车身（车窗、雨刮、灯光等）。

**核心职责**：通道收发、主/从节点角色、帧调度、唤醒/休眠。

**关键配置项**：

- LinChannel：LIN 通道（控制器）。
- LinChannelBaudRate：波特率（如 9600 / 19200）。
- LinNodeType：节点类型——主节点（Master）/ 从节点（Slave）。
- LinScheduler：帧调度表（主节点：调度哪些帧、时间槽）。
- LinFrame / FrameType：帧配置（帧 ID、类型：无条件帧 / 事件触发帧 / 点对点帧、数据长度）。
- LinWakeUp：唤醒配置。
- LinProcessingType：中断 / 轮询。
- LinHwIndependentConfig：波特率、唤醒、识别位等。

**常用 API**：Lin\_Init、Lin\_LinChannelInit、Lin\_SendFrame / Lin\_ReceiveFrame、Lin\_MainFunction\_Read / Write（轮询）、Lin\_GoToSleep / Lin\_Wakeup、Lin\_GetState / GetStatus、Lin\_ScheduleRequest（主节点请求调度）。

**配置思路**：

1. 配 LIN 通道 + 波特率。
2. 确定节点类型（主 / 从），配节点模式。
3. 主节点配调度表（帧 \+ 时间槽）；从节点配帧 ID 与接收。
4. 配唤醒、中断 / 轮询。

**常见坑**：

- 波特率配错 → 通信失败。
- 主 / 从角色配错 → 调度 / 收发异常。
- 主节点调度表没配帧 → 帧不发送。
- 从节点帧 ID 配错 → 无法响应主节点。
- 轮询模式没周期调用 MainFunction → 不收发。
- LIN 唤醒 / 休眠配置不当 → 无法进出休眠。

📎 上一个（CanTrcv）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY1Mzk1><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL