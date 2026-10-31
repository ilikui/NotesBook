---
title: AUTOSAR MCAL 配置说明 · 模块⑭ Wdg
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑭ Wdg

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1NjY2

**AUTOSAR MCAL 配置说明 · 模块⑭ Wdg**

Wdg（看门狗驱动）负责看门狗硬件的超时、模式、喂狗。注意：MCAL 的 Wdg 只管驱动层，上层 WdgIf / WdgM 做看门狗管理与周期触发。

**核心职责**：看门狗超时配置、模式切换、触发条件（喂狗）。

**关键配置项**：

- WdgDevice：设备配置（映射到看门狗硬件）。
- WdgSettingConfiguration：设置——超时时间（WdgTimeout）、模式（WdgMode：Fast / Slow / Off）。
- WdgGeneralConfiguration：整体配置（如 WdgDefaultMode）。
- WdgSetMode / WdgSetTriggerCondition：模式与触发条件。

**常用 API**：Wdg\_Init、Wdg\_SetMode、Wdg\_SetTriggerCondition（喂狗 / 设置触发条件）、Wdg\_GetVersionInfo。

**配置思路**：

1. 选看门狗设备、确定超时。
2. 配模式（Fast / Slow / Off）和默认模式。
3. 配触发条件（喂狗周期）。
4. 运行时用 Wdg\_SetTriggerCondition 定时喂狗。

**常见坑**：

- 超时设太短 → 频繁误复位；设太长 → 系统挂死无法及时救。
- 模式切换不当 → 无法正常喂狗。
- 忘了喂狗（SetTriggerCondition 没按时调）→ 看门狗复位。
- 与 WdgM 配合：MCAL Wdg 只是驱动，WdgM 负责调度喂狗；WdgM 配置错会导致误触发。
- 低功耗 / 休眠时看门狗处理方式——有的要进特定模式，避免休眠时被复位。

📎 上一个（Eep）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY1NjEz><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL