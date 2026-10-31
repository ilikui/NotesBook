---
title: AUTOSAR MCAL 配置说明 · 模块③ Dio
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块③ Dio

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzIxMDA2

**AUTOSAR MCAL 配置说明 · 模块③ Dio**

Dio 是数字 I/O 的 **逻辑读写** 模块，面向「读一个引脚的逻辑电平 / 写一个引脚的逻辑电平」。它不配方向、不复用——那些是 Port 的事。

**核心职责**：单通道读写、整端口读写、翻转电平。

**关键配置项**：

- DioPort：端口定义，逻辑上把一批物理引脚归组。
- DioChannel：通道配置，把一个逻辑通道映射到具体物理引脚（通过底层 Port 分配）。
- DioPortDataPort / DioPortMask：端口数据访问与掩码。
- DioChannelGroup（可选）：多个通道合成的组合通道。

**常用 API**：

- Dio\_ReadChannel / Dio\_WriteChannel：读 / 写单通道逻辑电平。
- Dio\_ReadPort / Dio\_WritePort：整端口读写。
- Dio\_FlipChannel：翻转某通道。
- Dio\_GetVersionInfo：版本信息。

**配置思路**：

1. 定义逻辑通道（DioChannel）并映射到物理引脚（底层由 Port 分配引脚）。
2. 运行时用 Dio\_ReadChannel / Dio\_WriteChannel 读写逻辑电平。
3. 大量同组 I/O 时用整端口读写提高效率。

**常见坑**：

- Dio 通道没对应到正确引脚 → 读写的是别的引脚。
- 方向配错（Port 里配成输入，Dio 却想写）→ 写无效、读回还是输入状态。方向在 Port、读写才在 Dio。
- Dio\_WritePort 是整端口写——小心读改写破坏其他位。位操作与端口操作别混用。
- Dio 只管电平，不管复用。用了复用外设功能的引脚（如 CAN、ADC 引脚）别再用 Dio 读写。

**Dio 与 Port 区分**：Port = 配置层（方向、复用、上下拉）；Dio = 逻辑读写层（读电平、写电平）。Dio 不配引脚功能。

📎 上一个（Port）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwOTQ1><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL