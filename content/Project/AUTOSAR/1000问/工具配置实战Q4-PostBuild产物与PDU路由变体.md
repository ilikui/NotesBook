# 工具配置实战 Q4：PostBuild 生成 .c 还是 .arxml？运行时改 PDU 路由，PreCompile 还是 PostBuild 支持？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzcyOTgx

工具配置实战 Q4：PostBuild 生成 .c 还是 .arxml？运行时改 PDU 路由，PreCompile 还是 PostBuild 支持？

PostBuild 生成的产物：既有 .c/.h，也有 .arxml。关键区别不在文件格式，而在「配置是静态定死还是运行时可变」。

- PreCompile：编译前把配置全部定死，生成的是静态常量配置代码（.c/.h）——改动要重新生成 + 重编译 + 重烧。
- PostBuild：配置以「可变配置数据 / 多个变体」存在，启动时由 EcuM/BswM 选择加载。生成的配置结构体放进可写数据区，支持运行时标定 / 刷新改变值，不用重新编译。PostBuild 再细分 Loadable（加载变体）和 Selectable（启动时可选多个变体）。

运行时修改某个 PDU 的路由：

- PostBuild 支持。路由参数（PDU 映射、routing path）若纳入 PostBuild 范围，就能在运行时/启动时改变——通过标定、诊断刷新，或切换 PostBuild 变体。不用改代码重新编译。
- PreCompile 不支持：路由是编译期定死，要改就得改配置 → 重新生成 → 重编译 → 重烧。

补充：配置变体（Pre-compile / Post-build variant）和路由是否可运行时改是两件事——即使 PostBuild 能力在，PDU 路由具体能否运行时改，取决于当初是否把路由参数划进了 PostBuild 可变范围。

一句话：PostBuild 的关键是「配置可作为变体在运行时选/改」，所以运行时改 PDU 路由选 PostBuild；PreCompile 是静态定死，改一次烧一次。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzcyNjgw><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR