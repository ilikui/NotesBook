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


## MATLAB / Simulink 资源补充（来自 Flomo）

### 常用工具箱与建模库

Simulink 的基础库包括 Commonly Used Blocks、Continuous、Dashboard。按工程方向可进一步关注：

- 控制与系统：Control System Toolbox、Model Predictive Control Toolbox、Fuzzy Logic Toolbox。
- 汽车与自主系统：Automated Driving System Toolbox、Powertrain Blockset、Embedded Coder Support Package for AUTOSAR Standard。
- 信号与通信：DSP System Toolbox、Communications System Toolbox、Audio System Toolbox、Phased Array System Toolbox。
- 图像与视觉：Computer Vision System Toolbox、Image Acquisition Toolbox。
- 嵌入式与硬件：Embedded Coder、HDL Coder、HDL Verifier、HDL Verifier、Instrument Control Toolbox、Data Acquisition Toolbox。
- AI 与计算：Neural Network Toolbox，以及 MATLAB 的并行计算、AI/数据科学、数学优化等工具箱方向。

工具箱名称和授权随 MATLAB 版本变化，实际使用前应核对 MathWorks 当前版本、许可证和支持平台。

### MATLAB 软件工程与持续集成

MATLAB 工程可纳入常见 CI 工作流：

~~~~mermaid
flowchart TD
  A[功能分支提交] --> B[GitHub / GitLab 等远程仓库]
  B --> C[CI 触发]
  C --> D[启动 MATLAB / 测试环境]
  D --> E[运行单元测试与静态检查]
  E --> F[编译 MEX / 代码生成 / 打包]
  F --> G[归档测试报告与构建工件]
  G --> H{检查通过？}
  H -->|是| I[合并与发布]
  H -->|否| J[反馈失败并修复]
  J --> A
~~~~

CI 的核心价值是尽早发现跨平台、版本兼容、依赖和集成问题。可将 MATLAB 单元测试、代码生成、MEX 构建和工件归档纳入自动化流水线；Jenkins 等平台只是执行载体，关键是固定 MATLAB 版本、依赖和测试数据。

### 官方学习入口与功能地图

- 官方帮助文档：[MATLAB 文档](https://ww2.mathworks.cn/help/matlab/index.html?s_tid=hc_panel)。
- 快速入门：桌面、矩阵与数组、索引、工作区、数据类型、控制流、脚本与函数、二维/三维绘图。
- 软件开发：调试与性能、内存、工程、源代码管理、测试框架、编译自动化、持续集成、工具箱开发与验证。
- 应用方向：并行计算、AI/数据科学、数学优化、代码生成、信号处理、图像处理、控制系统、雷达、机器人与自主系统、汽车和航空航天。
- MATLAB 环境设置：桌面环境、编辑器与 App 设计工具、操作系统命令和设置 API。

### Flomo 原始资料

- [MATLAB 与 Simulink 10000 问导航](https://v.flomoapp.com/mine/?memo_id=MjQ2Mzc1Mzg4)
- [MATLAB 矩阵概念与名称来源](https://v.flomoapp.com/mine/?memo_id=MjQ2NTI3ODgx)
- [常用 Simulink 建模库](https://v.flomoapp.com/mine/?memo_id=ODU2MDgxOTk)
- [MATLAB 持续集成工作流](https://v.flomoapp.com/mine/?memo_id=ODM3MDU1OTY)
- [MATLAB 函数与环境设置](https://v.flomoapp.com/mine/?memo_id=ODM3MDIxOTA)
- [MATLAB 官方帮助文档目录](https://v.flomoapp.com/mine/?memo_id=ODM2OTY0NjE)
- [MATLAB / Simulink 工具箱与应用方向](https://v.flomoapp.com/mine/?memo_id=ODM2Njc1NTE)
