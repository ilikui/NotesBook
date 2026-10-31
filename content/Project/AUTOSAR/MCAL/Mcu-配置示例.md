---
title: AUTOSAR MCAL 配置示例 · 深化篇① Mcu（通用骨架，按芯片调整）
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置示例 · 深化篇① Mcu（通用骨架，按芯片调整）

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1NzU0

**AUTOSAR MCAL 配置示例 · 深化篇① Mcu（通用骨架，按芯片调整）**

给 Mcu 一份带具体参数值的配置示例，方便对照实际工程。

**示例（以某 32 位 MCU 为例，仅供参考）**：

1. 时钟源：外部晶振 20MHz（或内部 RC）。

2. PLL 倍频分频：
   - VCO 倍频到 320MHz。
   - 主时钟 160MHz（VCO ÷2）。
   - 系统总线 80MHz（÷4）、外设总线 40MHz（÷8）。
   - CAN 模块时钟 80MHz、ADC 时钟 40MHz。
3. 复位：上电复位 \+ 引脚复位 \+ 看门狗复位都开启；复位后应用默认时钟。

4. RAM 段：主数据段 + 堆栈段，启动时初始化，开启 ECC。

5. 功耗模式：
   - RUN：全时钟。
   - HALT / STOP：关外设时钟，保留唤醒源时钟。
   - SLEEP：关主时钟，靠唤醒源唤醒。
6. McuModuleConfiguration：进入 RUN 时应用默认时钟设置。


**提示**：按你手上的芯片（如 TC3xx）实际 PLL 结构与频率上限会不同，这里只是骨架。配之前先看芯片手册的时钟树，确认倍频/分频系数和最大频率。

📎 模块卡（Mcu）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwODI0><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL