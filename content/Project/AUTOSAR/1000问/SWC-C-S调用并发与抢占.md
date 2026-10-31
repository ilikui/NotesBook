# SW-C 设计与应用层实践 Q3：Client-Server 并发与抢占

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0OTY0Nzcw

SW-C 设计与应用层实践 Q3：Client 调了 Server 的 Operation，Server 还没返回时 Client 被抢占——会不会出问题？

先区分两种 C/S 调用语义：

1. 同步（synchronous）：Rte\_Call 是阻塞调用，Client 发起后挂起，等 Server 完成才返回结果，RTE 保证结果正确传回。

2. 异步（asynchronous）：发起后不等结果，Client 继续执行，结果通过 Rte\_Result / Buffer 读取。「Server 没返回时 Client 还在跑」是设计预期，不是 bug。


所以「被抢占」会不会出问题，取决于调用模式和并发模型：

- 同一核、同一任务上下文：同步调用等价于函数调用，顺序执行，不存在被抢占问题——Server 执行完才回到 Client。

- 同步 \+ 跨任务 / 跨核：Rte\_Call 会让 Client 等待 Server 完成（挂起 / 阻塞）。此时真正的风险不是「数据损坏」，而是：


a. 优先级反转：Server 优先级低于等待它的高优 Client，需要 PCP（优先级天花板）或合理优先级配置。

b. 非重入 / 共享状态：Server 执行体若用了共享全局变量，且等待期间另一个 Client 又调进来，会互相干扰——需要 Server 可重入或用锁。

c. 同步超时 / 卡死：Server 依赖的资源不满足，Client 会一直等，可能导致任务卡死、触发看门狗。

- 异步 C/S：Client 不等结果继续跑是正常的，只要正确用 Rte\_Result 拿结果、不依赖未就绪的数据就行。

一句话：标准同步 C/S 下「Client 被抢占」通常不是数据损坏——RTE 保证返回值正确，风险在并发访问 Server 内部状态（非重入）和调度/优先级（反转、卡死）。不想等，就用异步 C/S。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0OTY0NjUx><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR