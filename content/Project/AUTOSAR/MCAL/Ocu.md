---
title: AUTOSAR MCAL 配置说明 · 模块⑥ Ocu
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑥ Ocu

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY0NTA5

**AUTOSAR MCAL 配置说明 · 模块⑥ Ocu**

Ocu（输出比较）驱动，在定时器计数值达到比较值时翻转 / 置位 / 清位输出引脚，产生精确边沿、脉冲、时基信号，也是 Pwm 的底层基础。

**核心职责**：定时器比较输出、边沿/脉冲产生、比较事件回调。

**关键配置项**：

- OcuChannelConfiguration：通道配置（映射到定时器比较通道 / 引脚）。
- OcuMode：比较模式——翻转 / 置位 / 清位 / 无操作，支持多比较值。
- OcuCompareValue / CompareValueList：比较值（一个或多个预定义比较点）。
- OcuInitialState：输出初始状态（翻转前的初始电平）。
- OcuNotification：比较值达到时的回调通知。
- OcuEnableDisableNotification：通知开关。
- OcuChannelClass：通道类别（单个比较 / 组合比较）。
- OcuPeriod：周期。

**常用 API**：Ocu\_StartChannel / Ocu\_StopChannel、Ocu\_SetCompareValue、Ocu\_EnableNotification / Ocu\_DisableNotification、Ocu\_GetState。

**配置思路**：

1. 确定输出行为：到达比较值时翻转 / 置位 / 清位。
2. 配比较值（一个或多个）\+ 初始状态。
3. 配通知回调（比较值达到时触发）。
4. 运行时 Ocu\_StartChannel + 设置比较值。

**常见坑**：

- 比较模式配错 → 输出行为不对（该翻转却置位）。
- 比较值 / 初始状态配错 → 第一段边沿不对。
- 通知回调没开 → 比较事件无响应。
- 定时器 / 时钟源没配好 → 输出不准。

**Ocu 与 Pwm 关系**：Ocu 是底层比较输出（产生边沿 / 脉冲）；Pwm 通常基于 Ocu 通道产生周期 + 占空比的波形。配 Pwm 前常先想清楚底层 Ocu 行为。

📎 上一个（Icu）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY0MTU2><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL