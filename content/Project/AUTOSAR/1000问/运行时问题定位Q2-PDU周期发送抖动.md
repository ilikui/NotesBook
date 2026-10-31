# 运行时问题定位 Q2：PDU 配了周期发送 100ms，但示波器看实际间隔是乱的——可能原因？从哪查？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzczMjcw

运行时问题定位 Q2：PDU 配了周期发送 100ms，但示波器看实际间隔是乱的——可能原因？从哪查？

关键认知：COM 的周期发送靠 Com\_MainFunction 被周期调度来推进。所以「配置的 100ms」是 COM 内部发送节拍，不等于总线上严格 100ms。实际间隔 = COM 节拍 × 发送时机 × 总线仲裁的叠加。

可能原因（按概率）：

1. Com\_MainFunction 的调用周期不稳：周期发送依赖 MainFunction 被固定周期调用；若调度它的 OS Task 周期不是 100ms 的整数倍、或该 Task 抖动大（被高优先级/长任务/中断抢占），发送节拍就乱。

2. COM 发送周期与 MainFunction 周期没对齐：如 MainFunction 100ms、PDU 配 50ms，实际只能按 100ms 对齐，间隔看着就不规律。

3. 总线竞争 / 仲裁延迟：同一时刻多报文抢总线，低优先级被推迟，间隔被挤乱。看总线负载和报文优先级。

4. 发送失败：Bus-off、发送队列满、PDU 被丢弃，导致某几个周期没发出来，间隔看起来「乱」。

5. 信号更新 / 发送时机：Com 内部 shadow signal 更新与发送时机若配置不当（update bit / 周期不同步）也会影响。


从哪开始查：先查 COM 的 MainFunction 调度（OS Task 周期 + 抖动），再核对 COM 周期配置与 MainFunction 周期的倍数关系，接着看总线负载/仲裁（示波器 + 报文优先级），最后排查 Bus-off / 发送失败。

一句话：COM 周期发送是「尽力而为」的——只能保证每个 MainFunction 周期尝试发一次，无法保证总线上严格等间隔。间隔乱，十有八九是 MainFunction 调度或总线仲裁的问题。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzczMjE3><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR