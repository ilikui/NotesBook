# AUTOSAR 1000问 · PartialNetworkingQ1：Partial Networking（部分网络）解决了什么问题？为什么一个 ECU 在不该做某事的时候还要被唤醒是一种浪费？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzcwNDc5

**AUTOSAR 1000问 · PartialNetworkingQ1：Partial Networking（部分网络）解决了什么问题？为什么一个 ECU 在不该做某事的时候还要被唤醒是一种浪费？**

▎ 五大学习法：费曼——把 Partial Networking 讲成「按需叫醒，不叫无关的」

**解决的问题**：传统 CAN 网络的唤醒是「全网络唤醒」——只要有节点被唤醒，整个网络（包括所有节点的收发器）都被唤醒，即使某些节点对这些报文根本不关心。结果是大量无关的唤醒和功耗浪费。

**为什么「不该做某事却唤醒」是浪费**

1. 功耗：整车熄火 / 关机后，很多节点本可以休眠——但因为收到一条无关报文被唤醒，收发器 \+ CPU 都耗电，直接推高静态电流，影响蓄电池
2. 无关唤醒：一个 ECU 只关心某几个信号，却被网络上所有报文唤醒——大部分唤醒它是白醒的，白白耗电
3. 寿命 / 热管理：频繁无效唤醒增加收发器和 CPU 的负担

**Partial Networking 的价值**

- 允许节点「选择性唤醒」：只对「跟它相关的 PN 报文」响应 / 唤醒，对无关报文继续睡
- 按「报文相关性」决定要不要醒——让 ECU 只在「跟它有关的事发生」时才醒来
- 大幅降低整车休眠时的静态功耗，同时对本地感兴趣的报文保持实时响应

**一句话总结**：Partial Networking 解决的是「整车休眠时不必要的唤醒耗电」——传统 CAN 一节点醒、全网醒；PN 让节点只对跟自己相关的报文唤醒、无关报文继续睡。因为它按报文相关性选择性唤醒，所以一个 ECU「不该醒却被唤醒」就没必要了——省电、降低静态电流，这是 PN 的核心价值（结合网络管理 CanNm / ComM 的唤醒策略）。

📎 AUTOSAR 1000问总表 → [https://v.flomoapp.com/mine/?memo\_id=MjMxMTQ2NDk4](https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4)

#Area/技术/AUTOSAR