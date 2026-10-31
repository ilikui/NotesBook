# 专栏⑮·补充二：DMA——数据搬运不占 CPU 的隐形引擎

> 来源：Flomo 原始笔记｜[查看原笔记](https://v.flomoapp.com/mine/?memo_id=MjUxMjA1MDkw)｜迁移日期：2026-10-31

**专栏⑮·补充二：DMA——数据搬运不占 CPU 的隐形引擎**

▎ **为什么嵌入式高性能离不开 DMA**<br>
UART 收一串不定长数据、ADC 连续采样 1024 点、SPI 读 Flash 一页——这些如果全用中断逐字节搬，CPU 全耗在搬运上，实时性崩。DMA 把「从外设搬到内存」这件事外包给硬件，搬完再打断你。

▎ **DMA 是什么**

- 直接内存访问：独立于 CPU 的搬运引擎，一条总线主设备
- 搬运描述：源地址 \+ 目的地址 \+ 长度 \+ 触发源（外设事件）
- 搬完回调：传输完成中断（TC）通知 CPU

▎ **三种搬运模式**

1. 内存→内存：Mem2Mem（批量拷贝，比 memcpy 省 CPU）
2. 外设→内存：Periph2Mem（ADC 采样、UART 接收、SPI 读）
3. 内存→外设：Mem2Periph（UART 发送、SPI 写、DAC）

▎ **经典场景**

- UART 接收：IDLE 中断 + DMA 环形缓冲区——不定长数据一条链搞定
- ADC 多通道连续采样：DMA 直接把结果搬进数组，CPU 只做数据处理
- SPI Flash 读：DMA 搬一页（256B），CPU 同时干别的
- 显示器/传感器高频刷新

▎ **DMA 与缓存（有 Cache 的 MCU 必看）**

- 数据一致性：DMA 写内存，CPU 读的是 Cache 旧数据——需要 Clean/Invalidate
- 场景：DMA 收完数据 → CPU 读之前要 Invalidate（让 Cache 失效重新读内存）
- DMA 发数据 → CPU 写完后要 Clean（把 Cache 刷回内存）
- 多核 \+ DMA 更要注意（接 C语言补充三 barrier）

▎ **三个坑**

1. 环形缓冲边界：DMA 指针回绕，处理时小心撕裂——按块处理或双缓冲（Ping-Pong）
2. 搬运一半改配置：DMA 正在搬，你改了长度/地址——传输错乱，停用再改
3. 数据一致性：有 Cache 的核上忘记 Invalidate/Clean——读到旧数据的经典疑难杂症

▎ **一句话**：DMA 是把搬运外包给硬件——三种模式（内存/外设双向）覆盖 UART/ADC/SPI 所有高频场景；有 Cache 的 MCU 记住「收完 Invalidate、发前 Clean」，一致性是唯一的深坑。

📎 第3篇：PWM 与定时器 → [https://v.flomoapp.com/mine/?memo\_id=MjQ2MzYzNjk0](https://v.flomoapp.com/mine/?memo_id=MjQ2MzYzNjk0)<br>
📎 C语言补充三：并发与原子性（barrier）→ [https://v.flomoapp.com/mine/?memo\_id=MjUxMjA0Mjc0](https://v.flomoapp.com/mine/?memo_id=MjUxMjA0Mjc0)<br>
📎 专栏⑮导航 → [https://v.flomoapp.com/mine/?memo\_id=MjQ1NzMzNDk3](https://v.flomoapp.com/mine/?memo_id=MjQ1NzMzNDk3)

**专栏⑮进度：10/10 + 补充二**

#Area/技术/嵌入式
