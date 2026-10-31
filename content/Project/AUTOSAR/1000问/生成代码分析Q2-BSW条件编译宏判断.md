# 生成代码分析与集成 Q2：BSW 生成代码用宏控制条件编译——怎么确定某配置参数对应宏是 ENABLED 还是 DISABLED？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzczMTI5

生成代码分析与集成 Q2：BSW 生成代码用宏控制条件编译——怎么确定某配置参数对应宏是 ENABLED 还是 DISABLED？

生成器把每个配置参数翻译成预处理器宏，命名有规律（如 XXX\_ENABLED / XXX\_ACTIVE / XXX\_USE\_...），值为 STD\_ON / STD\_OFF 或 TRUE / FALSE。

三个直接手段：

1. 看生成的配置头文件（\_Cfg.h）：在生成目录里搜宏名（如 Can\_Cfg.h、PduR\_Cfg.h），定位宏定义语句看值。这是最直接的。

2. 追踪宏在哪些 .c 里被引用：条件编译宏（if 宏）控住函数体，grep 宏在哪个文件被用，就知道它管哪段代码。

3. 生成预处理输出：让编译器输出预处理结果（-E），看宏最终展开成什么——避免宏被其他配置覆盖 / 再定义。


判断命名约定：宏名和配置工具里的参数名有对应关系（驼峰 / 下划线转换），大多带 \_ENABLED / \_ACTIVE 后缀、值用 STD\_ON / STD\_OFF。Davinci 和 EB 生成的宏命名略有差异，但规律一致。

最实用的一招：函数体里看到「if XXX\_ENABLED」就立刻明白——该参数决定这段代码要不要编译；去配置工具找到对应开关看值即可。注意别只信配置工具界面，生成的 \_Cfg.h 里的值是最终答案。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzczMDU5><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR