---
title: AUTOSAR MCAL 模块配置说明 · 总览
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 模块配置说明 · 总览

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy

**AUTOSAR MCAL 模块配置说明 · 总览**

（专题起点，逐模块展开）

MCAL（微控制器抽象层）是 AUTOSAR 最底层、唯一碰寄存器/硬件寄存器的层——每个模块对应一类硬件外设。

**核心模块清单与配置要点**：

- Mcu：时钟（PLL）、复位、功耗模式、RAM 段——配好时钟树和复位源。
- Port：引脚复用/方向、初始电平、上拉下拉——每根引脚选功能、方向、上下拉。
- Dio：数字 I/O 读写，通道/端口——比 Port 上层，只管读写位。
- Adc：ADC 采样——通道、转换组、分辨率、触发、采样时间。
- Icu：输入捕获——边沿检测、信号/周期测量。
- Ocu：输出比较——输出翻转/置位，配合 PWM。
- Pwm：PWM 输出——通道、周期、占空比、极性。
- Gpt：通用定时器——通道、周期、计数、回调。
- Can：CAN 通信——控制器、波特率、帧、中断/轮询。
- CanTrcv：CAN 收发器——唤醒、故障检测、波特率。
- Lin：LIN 通信——通道、帧、主/从节点。
- Fls：Flash 驱动——扇区、读写、擦除。
- Eep：EEPROM 驱动——读/写、页。
- Wdg：看门狗驱动——喂狗、超时。
- Mpu：内存保护单元——内存访问权限分区（可选）。
- Dma：DMA 驱动——通道、传输、中断（可选）。

**配置思路**：每个模块先配「外设基础」（时钟、引脚、通道），再配「通信/业务参数」（波特率、帧、缓冲），最后配「中断和回调」。MCAL 配置一般来自芯片厂 MCAL 包（Infineon / NXP 等）+ EB tresos / 芯片工具。

📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL