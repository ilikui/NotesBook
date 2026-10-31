---
title: AUTOSAR MCAL 配置说明 · 模块⑮ Mpu（可选）
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑮ Mpu（可选）

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1Njg3

**AUTOSAR MCAL 配置说明 · 模块⑮ Mpu（可选）**

Mpu（内存保护单元）驱动是 **可选模块**，用于功能安全 / 内存隔离。它配置 MPU 硬件，为不同分区设定内存访问权限（读 / 写 / 执行），防止非法访问，支撑 AUTOSAR 的 Memory Protection 与 Freedom from Interference。

**核心职责**：内存区域访问权限配置、区域启停、配合 OS 上下文切换。

**关键配置项**：

- MpuRegionConfiguration：内存区域配置（基地址、大小、编号、优先级）。
- MpuRegionAccessPermissions：访问权限（读 / 写 / 执行）。
- MpuRegionBaseAddress / MpuRegionSize：区域基地址与大小。
- MpuConfiguration：整体配置（如 MpuNumberOfRegions）。
- MpuInstructionAccess / MpuDataAccess：指令 / 数据访问权限。
- MpuEndianness：字节序。

**常用 API**：Mpu\_Init、Mpu\_SetRegion（设置区域权限）、Mpu\_EnableRegion / DisableRegion、Mpu\_Reset、Mpu\_SetDataAccess / Mpu\_SetInstructionAccess。

**配置思路**：

1. 确定要保护的内存区域（代码段、数据段、堆栈、外设寄存器）。
2. 给每区域配访问权限（读 / 写 / 执行）。
3. 配区域优先级、大小、基地址。
4. 运行时配合 OS 上下文切换启用 / 禁用区域。

**常见坑**：

- 区域基地址 / 大小配错 → 保护范围不对（漏保护或误锁）。
- 权限配错 → 非法访问或被错误拦截。
- 区域优先级没配好 → 区域覆盖冲突。
- 与 OS 内存保护配合：Mpu 区域通常在上下文切换时更新，配合 OS 内存分区实现 Freedom from Interference。
- 外设寄存器区域要正确授权，否则驱动无法访问。

📎 上一个（Wdg）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY1NjY2><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL