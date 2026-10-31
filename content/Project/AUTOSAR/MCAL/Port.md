---
title: AUTOSAR MCAL 配置说明 · 模块② Port
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块② Port

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzIwOTQ1

**AUTOSAR MCAL 配置说明 · 模块② Port**

Port 是配置 MCU 引脚的模块——管每根引脚的复用功能、方向、初始电平、上拉下拉。它是最贴近硬件引脚的"配置层"，决定引脚用哪个功能。

**核心职责**：引脚复用（MUX）、方向、上拉/下拉、初始电平、是否允许运行时改方向/模式。

**关键配置项**：

- PortPinConfiguration：每根引脚的配置（引脚编号、方向、复用模式、上下拉、初始电平）。
- PortPinDirection：输入 / 输出。
- PortPinMode：引脚功能——普通 GPIO 还是复用给外设（如 CAN、ADC、SPI、UART 引脚）。
- PortPinLevelValue：初始输出电平（HIGH / LOW）。
- PortPinType：引脚类型（如是否 ADC 通道、是否为模拟/数字引脚）。
- PortPinModeChangeable / DirectionChangeable：运行时是否允许改模式 / 方向。
- PortPinIndex：引脚编号（对应芯片引脚）。

**配置思路**：

1. 按硬件设计（引脚图）确定每根引脚功能：普通 GPIO 还是复用外设。
2. 配方向（输入/输出）、上下拉（上拉/下拉/浮空）、初始电平。
3. 配复用功能（注意：Port 只配 MUX，真正的外设功能由对应驱动模块如 Can / Spi / Adc 各自配置）。
4. 若运行时需改方向（如 one-wire、I2C 总线切换），把 DirectionChangeable / ModeChangeable 设为 TRUE。

**常见坑**：

- 引脚 MUX 配错 → 引脚功能不对（想当 CAN 用却配成 GPIO）。
- 复用引脚只在 Port 配了、没在外设驱动里配 → 外设不工作。
- 初始电平 / 上下拉配错 → 上电瞬间引脚状态异常，可能影响外设或负载。
- Port 是静态配置，常在 EcuM 启动早期 Port\_Init 完成。

**Port 与 Dio 关系**：Port 管「引脚如何配置」（方向、复用、上下拉）；Dio 管「引脚如何读写」（逻辑电平）。Port 只配不读写，Dio 只读写不配复用。

📎 上一个（Mcu）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwODI0><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL