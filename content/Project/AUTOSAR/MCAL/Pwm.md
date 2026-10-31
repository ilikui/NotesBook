---
title: AUTOSAR MCAL 配置说明 · 模块⑦ Pwm
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑦ Pwm

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1MjM2

**AUTOSAR MCAL 配置说明 · 模块⑦ Pwm**

Pwm 驱动，输出 PWM 波形（周期 + 占空比），常用于电机控制、LED 调光、加热控制、信号调制。通常基于定时器 PWM 通道实现（底层常借助 Ocu）。

**核心职责**：输出周期性 PWM、调整占空比、极性/空闲状态管理、更新通知。

**关键配置项**：

- PwmChannelConfiguration：通道配置（映射到定时器 PWM 通道 / 引脚）。
- PwmPeriod：PWM 周期（定时器计数上限）。
- PwmDutycycle：占空比（0-100%）。
- PwmPolarity：极性（高有效 / 低有效）。
- PwmIdleState：空闲状态（空闲时电平）。
- PwmNotification：周期完成 / 占空比更新通知回调。
- PwmEnableDisableNotification：通知开关。
- PwmChannelClass：通道类别。

**常用 API**：Pwm\_SetDutyCycle、Pwm\_SetPeriodAndDutyCycle、Pwm\_EnableNotification / DisableNotification、Pwm\_GetPeriod / GetDutyCycle、Pwm\_SetOutputToIdle、Pwm\_GetOutputState。

**配置思路**：

1. 确定 PWM 输出通道（映射到引脚）。
2. 配周期、占空比、极性、空闲状态。
3. 配通知回调（周期 / 占空比更新时）。
4. 运行时用 Pwm\_SetDutyCycle 调整占空比。

**常见坑**：

- 周期 / 占空比超范围 → 输出异常。
- 极性和空闲状态配错 → 输出反相、空闲电平不对。
- 通知回调没开 → 更新无响应。
- 底层定时器 / 时钟没配好 → 频率不对。
- Pwm 基于 Ocu：Ocu 底层配置不当会影响 Pwm。
- 占空比更新有时点要求（最好在周期边界），避免产生毛刺。

📎 上一个（Ocu）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY0NTA5><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL