---
title: 工具链自动化构建 Q1 AUTOSAR 配置工具（Davinci / EB）和代码构建（make/cmake）怎么衔接？怎么跟 CI 集成？有没有 headless 模式？
tags:
  - AUTOSAR
  - 1000问
---

# 工具链自动化构建 Q1：AUTOSAR 配置工具（Davinci / EB）和代码构建（make/cmake）怎么衔接？怎么跟 CI 集成？有没有 headless 模式？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1MjU1MzM1

工具链自动化构建 Q1：AUTOSAR 配置工具（Davinci / EB）和代码构建（make/cmake）怎么衔接？怎么跟 CI 集成？有没有 headless 模式？

答案：有，大多数工具支持命令行 / 无头模式（headless / CLI），这是配置生成能进 CI 的关键。

衔接思路（三步）：

1. 用工具的 headless 命令行生成代码：
   - EB tresos：通过 ebtresos 命令行 + project 文件，用生成参数（如 -g）跑配置生成。
   - Davinci Configurator：用命令行 / batch mode（CLI），提供工程 + 生成动作。
   - 具体命令因工具和版本而异，核心是「给工程文件 \+ 指定生成动作」的命令行入口，能脱离 GUI。
2. 把生成命令封装成一键命令 / make target：如 make generate（先调工具 headless 生成）→ 再 make build（make / cmake 编译）。

3. CI 流水线串起来：拉取配置工程 → 调工具 headless 生成 → 调 make / cmake 编译 → 跑测试 / 静态检查。配置 arxml / dpa 变更才重新生成（用时间戳 / hash 判断），避免每次都全量生成。


关键注意点：

- headless 是核心：没有它，只能靠 GUI 自动化（脆弱、不稳定），进不了 CI。
- 版本锁定：工具版本 \+ 插件版本要固定。
- 生成是「覆盖式」：会覆盖生成目录，所以生成代码目录不要手动改，改动要回到配置。
- 运行环境：CI 容器里 headless 模式要能跑（可能要 license server / VM 环境）。
- 可复现性：输入配置要确定、可重复生成。

一句话：工具链自动化靠「工具 headless 命令行 + make 封装 + CI 流水线」——配置变才生成、生成完接编译测试，生成目录不手动改，版本和许可在 CI 里锁好。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU1MjU1Mjgw><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR