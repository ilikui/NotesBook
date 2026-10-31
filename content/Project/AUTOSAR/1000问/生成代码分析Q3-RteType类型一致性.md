# 生成代码分析与集成 Q3：Rte\_Type.h 定义了哪些类型？应用层类型和 RTE 生成类型不一致，谁说了算？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzczMTY2

生成代码分析与集成 Q3：Rte\_Type.h 定义了哪些类型？应用层类型和 RTE 生成类型不一致，谁说了算？

Rte\_Type.h 是 RTE 生成的头文件，主要包含：

1. 数据建模导出的 C 类型：AUTOSAR 系统描述里的 Application Data Type / Implementation Data Type 被映射成 C 类型（primitive、array、record、union），这些 typedef 就在 Rte\_Type.h 里。
2. RTE 内部工作类型：Rte\_ServiceType、Rte\_ModeType、Rte\_Entry / Instance 相关类型等。
3. 基础类型：如 uint8 / uint16 等平台标准类型。

类型不一致时谁说了算：RTE 说了算。

原因：

- RTE 是通信中间层，生成的类型是从系统描述（ADT / IDT）派生出的唯一权威映射，用于定义端口、接口和函数签名。
- 应用层 SW-C 应 include Rte\_Type.h、用 RTE 生成类型，而不是自己重复 typedef。
- 应用层若自己定义了不同或同名类型（比如自己 typedef 一个整数但 RTE 用不同宽度），会类型不匹配——编译期函数签名冲突、指针类型不合，或运行时数据解释错误。

正确做法：应用层自定义类型要在 AUTOSAR 的 SW-C 描述里定义（Implementation Data Type），让 RTE 生成对应类型；应用代码一律引用 Rte\_Type.h 里的。若不一致，应用层要改到与 RTE 一致，而不是反过来改 RTE。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzczMTI5><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR