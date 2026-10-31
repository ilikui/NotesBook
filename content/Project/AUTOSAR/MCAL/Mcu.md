---
title: AUTOSAR MCAL 配置说明 · 模块① Mcu
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块① Mcu

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzIwODI0

**AUTOSAR MCAL 配置说明 · 模块① Mcu**

Mcu 是 MCAL 最底层、第一个被初始化的 BSW 模块——管时钟、复位、功耗模式、RAM 段。EcuM 上电 Phase 0/1 就会 Init 它。

**核心职责**：时钟树（PLL）、复位源管理、功耗模式、RAM 段划分与初始化。

**关键配置项**：

- McuClockSettingConfig：时钟设置。选时钟源（外部晶振 / 内部 RC）、配 PLL 倍频 / 分频、定各总线时钟（Core clock、peripheral clock、Can / Adc 等外设时钟）。
- McuRamSectorSettingConfig：RAM 段设置。划分 RAM 段、是否初始化、ECC 开启与处理。
- McuResetSettingConfig：复位设置。复位源（上电复位、引脚复位、看门狗复位、软复位）检测与处理。
- McuModeSettingConfig：功耗模式设置。RUN / HALT / STOP / SLEEP 各模式下的时钟与功耗配置。
- McuModuleConfiguration：Mcu 整体配置（如进入 RUN 的默认时钟设置）。

**配置思路**：

1. 先定时钟树：外部晶振频率 → PLL 倍频分频 → 目标 Core clock / 各总线时钟。这是基础中的基础。
2. 再配复位：哪些复位源要检测、复位后的行为。
3. 配功耗模式：各模式下关哪些时钟、怎么进低功耗。
4. 配 RAM 段：启动时初始化哪些段、ECC 怎么处理。

**常见坑**：

- 时钟树配错（PLL 超范围、分频错）→ 系统跑不起来或频率不对。
- 外设时钟忘开 → 模块不工作（CAN 没时钟、ADC 不采样）。
- 功耗切换时时钟没恢复 → 唤醒后外设时钟缺失。
- Mcu 常在 EcuM Startup 早期就会 Init，配置错误影响后面所有模块。

📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL