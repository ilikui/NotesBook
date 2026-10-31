---
title: 变体管理 Q2：PreCompile / Link / PostBuild 三种变体处理——什么阶段决定变体？实车上靠诊断指令切换变体，选哪种？
tags:
  - AUTOSAR
  - 1000问
---

# 变体管理 Q2：PreCompile / Link / PostBuild 三种变体处理——什么阶段决定变体？实车上靠诊断指令切换变体，选哪种？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0OTY4ODUx

变体管理 Q2：PreCompile / Link / PostBuild 三种变体处理——什么阶段决定变体？实车上靠诊断指令切换变体，选哪种？

三种方式按「决定变体的阶段」区分：

1. PreCompile：编译前定死。生成代码 / 配置时按某个变体解析，后续不可换。适合变体早已确定、无需运行时切换的场景（按车型硬件固化）。

2. Link：链接阶段决定。生成代码把多个变体都编进去，链接时只选中一个（排除不需要的符号 / 联动选段）。适合编译单元统一、但不同产品线链接不同配置。

3. PostBuild：运行时 / 启动时决定。把多个变体都放进固件，启动时按某条件（标定 / 诊断 / NVM 标记 / 硬件识别 / 变体 ID）选择加载哪个变体。


「决策只能在实车上通过诊断指令切换」→ 选 PostBuild：

- PostBuild 允许 ECU 烧录后、运行中，通过诊断指令（或标定 / NVM 里的变体标记）选择某个变体生效，不需重新编译 / 重新烧录。
- 这正是 PostBuild 的设计目的——把「变成哪个变体」推迟到运行时，能在产线 / 实车 / 售后灵活切换。
- PreCompile 和 Link 都无法运行时切换：变体在编译或链接阶段就定死了。

一句话：PreCompile 编译前定、Link 链接时定、PostBuild 运行时定。要实车诊断指令切换，只能是 PostBuild。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0OTY4NzU2><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR