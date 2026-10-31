---
title: AUTOSAR MCAL 配置说明 · 模块⑫ Fls
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑫ Fls

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1NDE3

**AUTOSAR MCAL 配置说明 · 模块⑫ Fls**

Fls 是 Flash 驱动（MCAL 层），负责 MCU 内部 / 外部 Flash 的读、写、擦除、校验。它是存储栈最底层，上层是 Fee（Flash EEPROM 仿真）→ NvM。

**核心职责**：扇区擦除、写入、读取、校验，异步 job 管理。

**关键配置项**：

- FlsSectorConfiguration：扇区配置（起始地址、扇区大小、扇区数量）。
- FlsGeneralConfiguration：整体配置（FlsMaxRead / Write / Erase Normal Mode 等）。
- FlsProtection / SectorProtection：扇区写保护与擦除保护。
- FlsEraseWrite：擦写配置（最小擦写单位、擦写时间）。
- FlsReadConfiguration：读取配置。
- FlsConfigurationPointer / FlsCallCycle：轮询周期。

**常用 API**：Fls\_Init、Fls\_SetMode、Fls\_Erase、Fls\_Write、Fls\_Read、Fls\_GetJobResult / GetStatus、Fls\_Cancel、Fls\_MainFunction。

**配置思路**：

1. 确定 Flash 扇区布局（地址、大小、数量）。
2. 配读写 / 擦除的单位、擦除时间、校验。
3. 配扇区保护（关键区域防误写 / 误擦）。
4. 配轮询周期（MainFunction）。

**常见坑**：

- 扇区地址 / 大小配错 → 读写 / 擦除到错误区域。
- 擦写超时设置不当 → job 卡住或报错。
- 轮询模式没周期调用 Fls\_MainFunction → job 不完成。
- 扇区保护配错 → 关键区域被误擦写。
- 扇区是擦除最小单位——不能只擦一部分，理解错会导致擦除范围不对。
- Fls 是底层驱动，Fee / NvM 每次写入都经过它，配置错会波及上层存储。

📎 上一个（Lin）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY1NDA3><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL