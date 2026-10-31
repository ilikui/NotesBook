---
title: 专栏⑳·第7篇：计算平台——域控制器、SoC、Adaptive AUTOSAR
tags:
  - 自动驾驶
  - 专题系列
---

# 专栏⑳·第7篇：计算平台——域控制器、SoC、Adaptive AUTOSAR

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjUyMTU1ODc3

**专栏⑳·第7篇：计算平台——域控制器、SoC、Adaptive AUTOSAR**

▎ **在整条链路的位置**<br>
感知 / 融合 / 决策 / 规划全要算力——计算平台是自动驾驶的算力心脏。从分布式 ECU 到域控到中央计算（接第1篇架构演进）。

▎ **三层硬件**

1. SoC（自动驾驶芯片）：Orin（254 TOPS）/ Thor（2000 TOPS）/ 华为昇腾——GPU / NPU 加速神经网络
2. MCU（安全控制）：TC3xx / S32K——执行控制、功能安全（ASIL D）
3. 冗余设计：双 SoC / SoC+MCU 异构——一个负责 AI 计算、一个负责安全兜底

▎ **软件架构（Adaptive AUTOSAR）**

- 分层：OS（Linux / QNX / AUTOSAR OS）→ Adaptive 中间件（ara::com 通信、状态管理、执行管理）→ 应用（感知 / 融合 / 规划）
- Classic vs Adaptive：Classic 管实时确定性（MCU），Adaptive 管动态应用（SoC）——通过 RTE / IOC 桥接
- 执行管理（Execution Management）：应用生命周期管理、进程启动顺序

▎ **关键挑战**

- 算力分配：GPU / NPU / CPU 分工——神经网络上 NPU、逻辑上 CPU、图形上 GPU
- 功耗与散热：大算力 SoC 功耗数百瓦——液冷 / 热管理（接硬件专题）
- 安全隔离：ASIL D 功能安全 + 网络安全（HSM）——虚拟机 / 容器隔离

▎ **三个坑**

1. 只算 TOPS 不算功耗：账面 500 TOPS，车上散热装不下——选型看 TOPS/W
2. Classic / Adaptive 割裂：两套开发流程不打通——数据交互要提前定义（IOC / RTE 桥）
3. 安全功能放在 AI 芯片上：AI 推理不保证确定性——安全关键功能必须独立 MCU 兜底

▎ **一句话**：计算平台 = SoC（AI 算力）+ MCU（安全兜底）+ Adaptive 中间件（动态应用）；选型看 TOPS/W 不是裸 TOPS，安全关键功能永远不放在 AI 芯片上。

📎 第1篇：分级与系统架构 → [https://v.flomoapp.com/mine/?memo\_id=MjUyMDEzNTQy](https://v.flomoapp.com/mine/?memo_id=MjUyMDEzNTQy)<br>
📎 AUTOSAR 专栏⑩多核导航 → [https://v.flomoapp.com/mine/?memo\_id=MjQ5MDI0OTUz](https://v.flomoapp.com/mine/?memo_id=MjQ5MDI0OTUz)<br>
📎 专栏⑳导航 → [https://v.flomoapp.com/mine/?memo\_id=MjUyMDEzNTQx](https://v.flomoapp.com/mine/?memo_id=MjUyMDEzNTQx)

**专栏⑳进度：7/10篇**

#Area/技术/自动驾驶