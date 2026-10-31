---
title: MATLAB与Simulink
tags:
  - MATLAB
  - Simulink
---

# MATLAB 与 Simulink

按 MATLAB 语言基础、矩阵运算、数据处理、可视化、Simulink 建模、Stateflow、Simscape、控制系统、代码生成和 Model-Based Design 组织。

## 10000问逐题解答

- [[10000问/基础语法矩阵与Simulink建模]] —— MATLAB 语法、矩阵运算、脚本/函数、数据容器、绘图和求解器。
- [[10000问/矩阵可视化数值计算与信号处理]] —— 矩阵变形、逻辑索引、数值求解、FFT、时频分析与滤波器。
- [[10000问/Simulink建模控制系统与物理仿真]] —— Subsystem、代数环、控制系统、PID、Stateflow、Simscape 与 Model Reference。
- [[10000问/代码生成验证定点与实时HIL]] —— Embedded Coder、MIL/SIL/PIL/HIL、Polyspace、实时仿真、AUTOSAR Blockset 和定点数。
- [[10000问/OOP并行图像深度学习与测试]] —— MATLAB OOP、App Designer、GPU、图像、深度学习、系统辨识、测试和 Variant。

~~~~mermaid
flowchart TD
  A[MATLAB / Simulink] --> B[语言与矩阵]
  A --> C[数据处理与可视化]
  A --> D[Simulink / Stateflow]
  A --> E[代码生成与验证]
  B --> F[10000问逐题解答]
  C --> F
  D --> F
  E --> F
~~~~
