---
title: ARXML 解析与自动化脚本 Q2：两个版本 ARXML 做 diff——哪些是真正影响行为的「语义差异」？怎么在 CI 里自动检测？
tags:
  - AUTOSAR
  - 1000问
---

# ARXML 解析与自动化脚本 Q2：两个版本 ARXML 做 diff——哪些是真正影响行为的「语义差异」？怎么在 CI 里自动检测？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU1MjU0ODUx

ARXML 解析与自动化脚本 Q2：两个版本 ARXML 做 diff——哪些是真正影响行为的「语义差异」？怎么在 CI 里自动检测？

文本 diff（git diff）看到的是行级变化，但 ARXML 大量是引用、顺序、结构——很多行变不改变行为，很多隐藏语义变化却看不出。

真正影响行为的语义差异：

1. 引用（REF）指向的目标变了：某个 REF 从指向 A 变成指向 B——只是路径字符串变化，行为完全改变。

2. 配置关键值变了：CAN ID、DLC、周期、超时、波特率等数值变化。

3. 存在性（增删）变化：PDU / 信号 / SW-C / 端口被添加或删除。

4. 结构 / 归属变化：一个信号从 PDU A 移到 PDU B；PDU 传输属性改变；runnable 被重新映射到别的 Task。

5. 类型 / 属性变化：信号数据类型、字节序、长度、E2E 保护配置变化。

6. 默认值 / 初始值变化：文本上不易察觉，行为影响大。

7. 端口映射 / 连接变化：两个 SW-C 的连接断开或改成别的连接。


怎么在 CI 里自动检测：

1. 先把 ARXML 解析成「结构化对象」再比较：用 lxml / XML 库把对象（按类型 + 唯一标识）解析成键值对 / 树，做对象级 diff——忽略格式、顺序、行号差异。

2. 比较「引用目标」而非「引用字符串」：把 REF 解析成目标对象，比较目标是否变了。

3. 生成「语义快照」：把配置导出成规范化中间表示（JSON / 关键字段列表：所有 PDU 的 CAN ID、DLC、周期；所有 SW-C 端口映射；所有 REF 指向），对快照 diff。

4. 用 XPath / 查询提取关键配置项，两版本各提一份对比。

5. 依赖 AUTOSAR Meta Model 做语义化比较（PDU、Signal、SW-C Port、Runnable Mapping、E2E）。

6. CI 门禁：语义 diff 脚本发现关键差异（CAN ID 变、PDU 增减、引用断链）就 fail。


一句话：别用文本 diff。先把 ARXML 解析成「对象 + 引用目标」的结构化快照再 diff——比较引用目标、关键值和存在性，才能抓到真正的语义变化。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU1MjU0NzY2><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR