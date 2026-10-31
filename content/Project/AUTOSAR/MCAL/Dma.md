---
title: AUTOSAR MCAL Dma 配置说明
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块⑯ Dma（可选）

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzY1NzE2

**AUTOSAR MCAL 配置说明 · 模块⑯ Dma（可选）**

Dma（直接内存访问）驱动是 **可选模块**，配置 DMA 硬件实现数据在内存与外设、内存与内存之间的直接传输，减轻 CPU 负担。常用于 ADC 采样数据搬移、SPI/串口收发缓冲、内存拷贝。

**核心职责**：DMA 通道启停、传输配置、完成中断回调。

**关键配置项**：

- DmaChannelConfiguration：DMA 通道配置（通道号）。
- DmaChannelMode：传输模式（单次 / 循环 / 周期）。
- DmaChannelSourceAddress / DestinationAddress：源 / 目的地址。
- DmaChannelSourceAddressIncrement / DestinationAddressIncrement：地址增量。
- DmaChannelTransferLength：传输长度（字节数）。
- DmaChannelTransferSize：传输宽度（byte / halfword / word）。
- DmaChannelPriority：通道优先级。
- DmaChannelNotification：传输完成中断回调。
- DmaChannelRequestSource：请求源（外设请求 / 软件）。

**常用 API**：Dma\_Init / Dma\_DeInit、Dma\_StartChannel / Dma\_StopChannel、Dma\_GetChannelStatus / GetStatus、Dma\_ResetChannel、Dma\_SetTransferData / SetupTransfer。

**配置思路**：

1. 确定要搬移的数据（源 / 目的地址、长度、宽度）。
2. 配传输模式（单次 / 循环）、地址增量。
3. 配通道优先级（冲突资源调度）。
4. 配完成中断回调。

**常见坑**：

- 源 / 目的地址或长度配错 → 搬移错误数据 / 越界。
- 地址增量配错 → 数据覆盖或错位。
- 优先级没配好 → 多通道资源冲突、丢数据。
- 完成回调没配 / 没开 → 数据搬完没通知。
- 与外设配合：DMA 请求源要跟外设触发正确匹配（如 ADC 转换完成触发 DMA）。
- 循环模式缓冲区边界处理不当 → 数据覆盖。

📎 上一个（Mpu）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzY1Njg3><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL