---
title: 嵌入式通信协议
tags:
  - EE
  - Communication
---

# 嵌入式通信协议

通信协议知识按基础概念、接口机制、驱动实现、故障排查和车载应用组织。

## 1000问逐题解答

- [[1000问/基础协议与四大协议]] —— 同步/异步、全/半双工、UART、SPI、I2C、RS-485、汽车 ECU 应用与故障定位。

~~~~mermaid
flowchart TD
  A[嵌入式通信] --> B[UART]
  A --> C[SPI]
  A --> D[I2C]
  A --> E[RS-485]
  A --> F[SENT / LIN / USB / SDIO / Ethernet]
  B --> G[驱动与验证]
  C --> G
  D --> G
  E --> G
  F --> G
  G --> H[波形分析 / 故障复现 / 回归测试]
~~~~

## CAN 基础

- [[1000问/CAN网络通用概念]]：CAN 总线基础概念，并链接到终端电阻、排查工具箱和通信栈分层实战。
