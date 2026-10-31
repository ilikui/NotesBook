---
title: AUTOSAR MCAL 配置说明 · 模块⑧ Gpt
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑧ Gpt

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1Mjc3

**AUTOSAR MCAL 配置说明 · 模块⑧ Gpt**

Gpt（通用定时器）驱动，提供定时功能——周期性超时、单次定时、延时、时基，常用于产生周期中断或定时触发。

**核心职责**：启停定时、读取已过/剩余时间、定时超时回调。

**关键配置项**：

- GptChannelConfiguration：通道配置（映射到定时器通道）。
- GptChannelMode：通道模式——连续（循环）/ 单次模式。
- GptChannelTickFrequency：定时器 tick 频率。
- GptChannelTickValue：tick 值。
- GptChannelNotification：定时器超时回调（通知函数）。
- GptChannelAccess：通道访问类型（读 / 写）。
- GptWakeupCapability：唤醒能力（可选）。

**常用 API**：Gpt\_StartTimer / Gpt\_StopTimer、Gpt\_GetTimeElapsed / Gpt\_GetTimeRemaining、Gpt\_EnableNotification / Gpt\_DisableNotification、Gpt\_GetVersionInfo。

**配置思路**：

1. 选定时器通道 \+ 模式（连续 / 单次）。
2. 配 tick 频率 / 值，确定定时周期。
3. 配通知回调。
4. 运行时 StartTimer + 回调 / 读取状态。

**常见坑**：

- 通道模式配错（要循环却配单次）→ 只触发一次。
- tick 频率 / 值算错 → 定时不准。
- 通知回调没配 / 没开 → 无响应。
- 时钟源没配好 → 时基不准。
- 多个通道共用同一硬件定时器 → 资源冲突。
- 唤醒能力配置不当 → 定时唤醒失败。

📎 上一个（Pwm）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY1MjM2><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL