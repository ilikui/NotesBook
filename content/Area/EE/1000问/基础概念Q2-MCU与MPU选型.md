# 嵌入式 1000问 · 基础概念Q2：MCU 和 MPU 的核心区别是什么？什么时候该选 MCU，什么时候该选 MPU？

> 来源：Flomo 原始笔记｜[查看原笔记](https://v.flomoapp.com/mine/?memo_id=MjU2NDUxOTQx)｜迁移日期：2026-10-31

**嵌入式 1000问 · 基础概念Q2：MCU 和 MPU 的核心区别是什么？什么时候该选 MCU，什么时候该选 MPU？**

▎ 五大学习法：西蒙学习法——把「MCU vs MPU」钻透

**一句话区别**

- MCU（Microcontroller Unit，微控制器）：把 CPU + Flash + RAM + 外设集成在一颗芯片里，本质是「一台完整的计算机」，上电就能跑程序。
- MPU（Microprocessor Unit，微处理器）：通常只给 CPU 内核（+ 缓存 + 内存控制器），要外挂 RAM 和存储，本质是「一台计算机的大脑」，得配上内存、Flash 才能跑。

**几个维度对比**

1. 集成度：MCU 高度集成（片上 Flash / SRAM / 外设）；MPU 只有 CPU 核，内存 / 存储外接。
2. 性能：MCU 通常几 MHz几百 MHz（Cortex-M、RISC-V）；MPU 动辄几百 MHzGHz（Cortex-A）。
3. 内存与保护：MCU 片上 RAM 几 KB~几 MB、无 MMU（常用 MPU 内存保护单元）；MPU 外接 DDR、有 MMU，能跑 Linux / Android。
4. 操作系统：MCU 跑裸机 / RTOS；MPU 跑 Linux、QNX、Android 等通用 OS。
5. 功耗：MCU 低（µAmA，适合电池）；MPU 高（几百 mAA）。
6. 启动：MCU 上电即跑；MPU 要 BootROM → Bootloader → 内核 → 用户空间，启动慢。
7. 实时性：MCU 确定性强、中断延迟低；MPU 因 OS 调度、cache、MMU，实时性差（靠 PREEMPT\_RT 等补救）。
8. 成本 / 生态：MCU 便宜、BOM 简单；MPU 外围内存 / 电源 / PCB 更复杂。

**名字的坑（MPU 有两个意思）**

- 这里说的 MPU = 微处理器（跑 Linux 那种）。
- ARM 语境里，MPU 还指「Memory Protection Unit」（内存保护单元），是 MCU 上做内存区域权限保护的一块硬件。
- 同名不同物，别混。

**什么时候选 MCU**

- 实时控制（电机、PWM、传感器采样、汽车 ECU）、低功耗 / 电池、成本敏感、任务固定、不需要复杂 OS。
- 典型：STM32、S32K、TC3xx、ESP32。

**什么时候选 MPU**

- 要跑 Linux / 复杂应用、网络、图形界面、文件系统；要大内存高算力（网关、HMI、AI 推理、域控）；要丰富生态（Python、数据库、容器）。
- 典型：树莓派、i.MX、TI Sitara、瑞萨 RZ。

**混合趋势**

- 现代 SoC 常是「MPU + MCU」组合：A 核跑 Linux 做应用，M 核或独立 MCU 跑实时控制（回看自动驾驶第 23 题「SoC + MCU」）。
- 也有「MPU 里带 MCU 子系统」的异构芯片。

一句话：MCU 是「把整台计算机塞进一颗芯片」——省电省成本、实时确定、上电即跑；MPU 只给 CPU 核、要外挂内存和 OS——算力强、能跑 Linux；选谁看你要「实时省电的专用控制」还是「复杂应用的通用计算」，很多场景干脆两者组合。

📎 问题库（专栏⑮导航）→ [https://v.flomoapp.com/mine/?memo\_id=MjQ1NzMzNDk3](https://v.flomoapp.com/mine/?memo_id=MjQ1NzMzNDk3)

📎 基础概念Q1（嵌入式 vs 通用机）→ [https://v.flomoapp.com/mine/?memo\_id=MjU2NDUxODUy](https://v.flomoapp.com/mine/?memo_id=MjU2NDUxODUy)

#Area/技术/嵌入式
