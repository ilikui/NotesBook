---
title: 专栏⑳·第8篇：功能安全——ISO 26262、ASIL、冗余设计
tags:
  - 自动驾驶
  - 专题系列
---

# 专栏⑳·第8篇：功能安全——ISO 26262、ASIL、冗余设计

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjUyMTU1OTU4

**专栏⑳·第8篇：功能安全——ISO 26262、ASIL、冗余设计**

▎ **为什么自动驾驶是功能安全的重灾区**<br>
L3+ 系统接管驾驶，软件 / 硬件故障 = 直接人身伤害风险——ISO 26262 从「道路车辆电子电气系统功能安全」角度约束整个开发链。

▎ **ASIL 等级**

- 由危害分析（HARA）评定：S（严重度）× E（暴露概率）× C（可控性）→ ASIL A/B/C/D
- ASIL D 最高（制动 / 转向），QM 最低（不涉及安全）
- 自动驾驶典型分配：感知融合 ASIL B/C、决策规划 ASIL C、执行层 ASIL D

▎ **安全机制（你 AUTOSAR 里天天见的）**

- 硬件：锁步核（Lockstep）、ECC（内存纠错）、看门狗（WdgM）、电压 / 时钟监控（EcuM 的 MCU 故障检测）
- 软件：程序流监控（WdgM 的 Alive / Supervision）、内存分区（MPU）、运行时自检（BIST）
- 你的看门狗、ECC 笔记——全是功能安全的落地

▎ **冗余设计（L3+ 硬要求）**

- 异构冗余：不同实现算同一个结果（双 MCU 互检）——防共因失效
- 降级策略：单点失效 → 降级（限速 / 安全停车）而不是失控
- 安全状态（Safe State）：出问题去哪——停车 / 靠边 / 保持

▎ **三个坑**

1. 把 ASIL D 当口号：ASIL 分解（D = B(D)+B(D)）是架构工具，不是测试免责
2. 冗余做成同构：双份一模一样的代码 / 芯片——共因失效，同一个 bug 两份都炸
3. 安全机制不监控：装了看门狗 / ECC 但没在运行时验证它们在工作——安全机制本身要自检

▎ **一句话**：功能安全 = HARA 定 ASIL + 安全机制落地 + 冗余防共因失效；你 AUTOSAR 里的看门狗、ECC、EcuM 监控全是功能安全的日常，L3+ 的差异在「冗余 + 降级 + 安全状态」这套系统设计。

📎 专栏⑮·补充四 看门狗 → [https://v.flomoapp.com/mine/?memo\_id=MjUxMjA1MTM5](https://v.flomoapp.com/mine/?memo_id=MjUxMjA1MTM5)<br>
📎 嵌入式导航（ECC）→ [https://v.flomoapp.com/mine/?memo\_id=MjQ1NzMzNDk3](https://v.flomoapp.com/mine/?memo_id=MjQ1NzMzNDk3)<br>
📎 第7篇：计算平台 → [https://v.flomoapp.com/mine/?memo\_id=MjUyMTU1ODc3](https://v.flomoapp.com/mine/?memo_id=MjUyMTU1ODc3)

**专栏⑳进度：8/10篇**

#Area/技术/自动驾驶