# Spinlock 与 Mutex 的差异

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzcwOTYw

Spinlock 和 Mutex 都是互斥原语，差别在「拿不到锁时怎么等」。

Spinlock（自旋锁）：拿不到就原地忙等（busy-wait），不睡、不释放 CPU。适合临界区极短、等待时间可确定、等待方不能被调度的场景。

Mutex（互斥锁）：拿不到就阻塞/睡眠，把 CPU 让给别的任务，由调度器唤醒。适合临界区较长、可能触发阻塞操作（如访问慢速外设）、等待时间不可预估的场景。

多核场景怎么选：

- 短临界区（保护一条共享变量、一个寄存器、一段共享内存）→ Spinlock，等的时间短，忙等成本小于调度切换成本。
- 长临界区 / 可能阻塞 → Mutex（或 AUTOSAR 里的资源锁 + 优先级天花板 PCP），让出 CPU 更划算，避免占着核空转。

为什么 ISR 里不能等 Spinlock：

Spinlock 靠「持有者把它释放」——问题在于持有者能不能执行。ISR 优先级最高，若持有锁的是个普通任务，而它恰好被这个 ISR 抢占、一直没机会运行释放锁，ISR 里的自旋就永远等不到 → 死锁。

更直接地说：中断上下文无法被调度器让出，也没法「阻塞后睡一觉等别人唤醒」。所以 ISR 里不能用「等待型」的锁。要保护 ISR 里访问的共享资源，通常用「关中断 / 屏蔽同级中断」配合短临界区，而不是等 spinlock。

AUTOSAR 视角：OS 多核用 GetSpinlock / ReleaseSpinlock 这类 API 保护短暂共享资源；ISR（尤其 Cat 2）里避免调用可能阻塞的服务。核间长临界区尽量走 IOC 或事件机制，别在中断里自旋。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzcwODY4><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR

## 实时系统与 AUTOSAR 术语边界

AUTOSAR OS 的 Resource 与 Spinlock 不应简单等同于通用 OS 的 Mutex。Resource 常用于单核资源访问并配合优先级天花板协议；Spinlock 用于多核共享资源同步，持锁期间应极短且不得执行阻塞操作。是否允许特定 ISR 类别调用相关 API，必须查 AUTOSAR OS 一致性类和 OS 配置约束。

“ISR 里绝对不能使用 Spinlock”也过于绝对：不同 OS/架构对 ISR 类别和 API 调用有明确限制，某些场景可在受限规则下使用，但必须避免持锁者被无法恢复执行的高优先级上下文永久阻塞。设计优先考虑缩短临界区、关中断/中断屏蔽策略、IOC 或无锁消息传递，并分析最坏等待时间。