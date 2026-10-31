---
title: AUTOSAR MCAL 配置说明 · 模块⑬ Eep
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑬ Eep

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1NjEz

**AUTOSAR MCAL 配置说明 · 模块⑬ Eep**

Eep 是 EEPROM 驱动（MCAL 层），负责 MCU 内部 / 外部 EEPROM 的读、写、擦除。它是存储栈的驱动层，上层接 NvM。

**核心职责**：EEPROM 分区读写、擦除、异步 job 管理。

**关键配置项**：

- EepSectorConfiguration：扇区配置（EEPROM 分区地址、大小、数量）。
- EepRead / EepWrite / EepErase：读、写、擦配置。
- EepJobConfiguration：job 配置（读写 / 擦除最大长度、时间）。
- EepGeneralConfiguration：整体配置（如 EepMaxReadTime、EepMaxWriteTime 等）。
- EepProcessingType：中断 / 轮询模式。
- EepVirtualSector：虚拟扇区（可选）。

**常用 API**：Eep\_Init、Eep\_SetMode、Eep\_Read / Eep\_Write / Eep\_Erase、Eep\_GetJobResult / GetStatus / GetJobError、Eep\_Cancel、Eep\_MainFunction（轮询）。

**配置思路**：

1. 确定 EEPROM 分区布局（地址、大小、数量）。
2. 配读写 / 擦除的长度与时间。
3. 配处理方式（中断 / 轮询）。
4. 配 job 配置。

**常见坑**：

- EEPROM 地址 / 大小配错 → 读写 / 擦到错误区域。
- 超时设置不当 → job 卡住。
- 轮询模式没周期调用 Eep\_MainFunction → job 不完成。
- EEPROM 写寿命有限（擦写次数）——过度频繁写会耗尽寿命，注意写周期策略。
- 与 NvM 配合：NvM 分配块到 EEPROM 分区，配置错会导致存储错误。

**Eep 与 Fls 区别**：Eep 是 EEPROM 驱动（独立 EEPROM 或内部模拟），Fls 是 Flash 驱动；二者都是存储栈的 MCAL 驱动层，上层都接 NvM（通过 Fee 或直接）。

📎 上一个（Fls）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY1NDE3><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL