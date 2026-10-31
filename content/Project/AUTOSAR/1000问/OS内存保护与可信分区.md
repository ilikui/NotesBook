# AUTOSAR OS 内存保护与可信分区

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzcxMDUx

AUTOSAR OS 的 Memory Protection（MPU 配置）与 Trusted / Non-Trusted 差异

MPU 怎么配：

- AUTOSAR OS 用 MPU 实现内存分区（Memory Partitioning），跟 OS-Application 绑定。每个 OS-Application 分到一个或多个内存分区，各分区有自己的代码 / 数据 / 堆栈段。
- OS 为每个任务 / ISR、每个 OS-Application 维护一组访问权限，翻译成 MPU 寄存器配置（region + 权限：RW / RO / 无访问）。
- 上下文切换时 OS 同步切 MPU 上下文，保证任务只能访问自己所属分区。
- 访问违例触发保护异常，被 OS 捕获，通常走 ErrorHook / ProtectionHook，终止或恢复出错的实体。

Trusted vs Non-Trusted Function：

- 有的 OS-Application 是 trusted，有的是 non-trusted。
- Trusted 运行在特权级，访问权限最大：可访问所有内存分区、可执行特权指令（MSR / 特权寄存器 / 直接配 MPU）。通常放 OS 核心、复杂驱动、需要直操硬件或 OS 服务的函数。
- Non-Trusted 运行在受限态，被 MPU 约束：只能访问自己分区，不能碰其他 OS-Application，不能直接执行特权指令，不能直接调用受保护 OS 服务——要调服务得走受信任层做 gateway（System Call / Trap 代理）。

具体内存访问差异（三点）：

1. 可访问区域：trusted = 全地址空间（或多个分区）；non-trusted = 仅自己所在分区。
2. 特权指令：trusted 可执行；non-trusted 执行即触发异常。
3. OS 服务调用：trusted 直接调；non-trusted 只能通过 System Call / Trap 进入可信层代理。

这正是 AUTOSAR 满足 Freedom from Interference（免受干扰）的方式——靠内存分区 + MPU + 时间保护，让不同 ASIL 的应用互不干扰。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzcwOTYw><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR