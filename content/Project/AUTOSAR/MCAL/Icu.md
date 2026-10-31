---
title: AUTOSAR MCAL 配置说明 · 模块⑤ Icu
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑤ Icu

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY0MTU2

**AUTOSAR MCAL 配置说明 · 模块⑤ Icu**

Icu（输入捕获）驱动，用来测量外部信号的边沿、周期、脉宽——比如测转速/轮速传感器信号、外设方波频率与占空比，提供测量完成的回调通知。

**核心职责**：边沿检测、信号周期/脉宽测量、时间戳、通知回调。

**关键配置项**：

- IcuChannelConfiguration：通道配置（映射到定时器输入捕获通道 / 引脚）。
- IcuMeasurementMode：测量模式（信号测量：周期 / 脉宽 / 两个边沿之间时间；边沿检测）。
- IcuSignalMeasurement：信号测量（测高/低电平时间、边沿间时间）。
- IcuEdgeDetection：边沿检测（上升沿 / 下降沿 / 任意边沿）。
- IcuInputPolarity / ActivationState：激活电平 / 极性。
- IcuNotification：测量完成中断回调（通知函数）。
- IcuTimestamp：时间戳。
- IcuWakeupCapability：唤醒能力（可选）。

**常用 API**：Icu\_StartTimestamp / Icu\_StopTimestamp、Icu\_GetTimestamp、Icu\_EnableNotification / DisableNotification、Icu\_StartSignalMeasurement / StopSignalMeasurement、Icu\_GetMeasurementValue、Icu\_SetActivationCondition。

**配置思路**：

1. 确定要测什么：信号周期、脉宽、两沿时间，还是简单边沿检测（计数 / 唤醒）。
2. 选测量模式 \+ 极性（上升 / 下降沿）。
3. 配通知回调（测量完成触发）。
4. 运行时用 Icu\_StartXYZ + 读结果或用回调。

**常见坑**：

- 测量模式与通道能力不匹配 → 测不出正确值。
- 极性配反 → 测到的是反边沿。
- 通知回调没配 / 没开 → 测量完成没响应。
- 时钟 / 定时器源没配好 → 时间戳不准。
- 唤醒能力配置不当 → 无法唤醒 CPU。

📎 上一个（Adc）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIxMDU1><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL