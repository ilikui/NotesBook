---
title: AUTOSAR MCAL 配置说明 · 模块④ Adc
tags:
  - AUTOSAR
  - MCAL
---

# AUTOSAR MCAL 配置说明 · 模块④ Adc

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1NzIxMDU1

**AUTOSAR MCAL 配置说明 · 模块④ Adc**

Adc 是 ADC（模数转换）驱动模块，把模拟信号转成数字量。管采样通道、转换组、触发源、分辨率、采样时间、结果读取。

**核心职责**：配置 ADC 通道与转换组、启动转换、读取转换结果。

**关键配置项**：

- AdcChannelConfiguration：通道，映射到具体 ADC 输入通道。
- AdcGroup：转换组，同一次触发采样的多个通道归一组。
- AdcGroupConversionMode：转换模式（单次 / 连续 / 组转换）。
- AdcGroupTriggerSource：触发源（软件 / 硬件触发，如定时器触发）。
- AdcStreamingNumSamples：流式采样次数（连续转换）。
- AdcResolution：分辨率（如 8 / 10 / 12 / 16 bit）。
- AdcConversionTime / AdcSampleTime：采样时间、转换时间。
- AdcResultAlignment：结果对齐（左 / 右对齐）。
- AdcGroupPriority：组优先级。
- AdcReadingGroup：读取方式（组读取 / 通道读取）。

**常用 API**：Adc\_SetupResultBuffer、Adc\_StartGroupConversion、Adc\_ReadGroup、Adc\_GetGroupStatus。

**配置思路**：

1. 确定哪些通道要采样，按触发时机分组（同一次触发的通道放一组）。
2. 配触发源（软件触发 / 定时器硬触发）。
3. 配分辨率、采样时间、转换模式。
4. 配结果缓冲和结果对齐，读取结果。

**常见坑**：

- 采样时间配太短 → 高阻抗源采样不准，需要更长采样时间。
- 触发源配错 → 组转换不启动。
- 分辨率 / 对齐配错 → 读到的数值范围不对。
- 多组同时转换 → 要配优先级，注意资源冲突。
- 结果缓冲没配 / 没读 → 结果丢失或读到旧值。
- ADC 时钟没在 Mcu 里配好 → ADC 根本不工作。

📎 上一个（Dio）：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIxMDA2><br>
📎 总览：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwNjEy><br>
📎 专题入口：<https://v.flomoapp.com/mine/?memo_id=MjU1NzIwMTcx>

#Area/技术/AUTOSAR/MCAL