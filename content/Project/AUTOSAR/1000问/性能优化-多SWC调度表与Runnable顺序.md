# AUTOSAR 性能优化 Q2：多 SW-C 调度表与 Runnable 顺序

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0OTY4MzU0

AUTOSAR 性能优化 Q2：ECU 部署 50+ 个 SW-C——RTE 生成的 Schedule Table 什么样？Runnable 顺序怎么保证实时性？

先明确：Schedule Table 是 OS 层的调度机制，RTE（SchM）负责把 runnable 组织进 Task。所以它不是「每个 SW-C 一个表项」，而是按 Task 组织 + 时间轴排布。

Schedule Table 长什么样：

- RTE 把大量 runnable 映射到若干 Task（同周期的 runnable 常并进同一个 Task，减少上下文切换）。
- 调度表按时间轴把一个超周期（如 20ms / 100ms）的启动点排出来，每个到期点（Expiry Point）激活对应 Task，Task 里跑一组 runnable。
- SW-C 一多，调度表就「变大变密」：超周期内 Task 和到期点增多，形成按周期对齐的网状时间轴。

怎么保证实时性：

1. Task 优先级 + 抢占调度：高实时 runnable 放高优先级 Task，OS 抢占保证先跑。
2. runnable → Task 映射：按周期 / 实时性把 runnable 分组进合适 Task，减少切换和 jitter。
3. 超周期对齐：把周期不同的 runnable（10ms / 20ms / 100ms）排进同一个超周期，让启动时机相对固定、可预测。
4. 数据依赖顺序：RTE 按 runnable 间数据依赖排执行次序，保证先生产后消费。
5. 时间保护（Time Protection）：OS 监控每个 Task / ISR 执行上限，超时上报，防止单个 runnable 拖垮整体。
6. 多核同步：用 Schedule Table 同步（基于 StbM 全局时间）对齐各核调度。

SW-C 特别多时的挑战：单核上超周期变长、主循环负载高，需要更细地拆 Task、均衡分配，避免太多 runnable 挤进一个 Task 造成抖动；可考虑多核部署分散。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0OTY0ODc2><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR

## 调度机制边界补充

不要把“RTE 生成 Runnable 调度”与“OS 一定使用 Schedule Table”画等号。Runnable 通常通过 RTE 的 Event-to-Task Mapping 映射到 OS Task；OS Task 可以由 Alarm、Schedule Table 或其他 OS 机制激活，具体取决于项目设计与 OS 配置。

Runnable 的执行顺序必须从 RTE 生成代码、Task 内部调用序列、Event 配置和数据一致性语义确认，不能笼统认为 RTE 会自动按数据依赖排序。若多个 Runnable 写读同一数据，需明确 implicit/explicit communication、采样时刻、buffering 和执行顺序。

多核调度同步也不能简单归因于 StbM：OS 多核调度、Schedule Table synchronization 和 AUTOSAR 全局时间同步是不同机制，是否使用 StbM 取决于具体架构。