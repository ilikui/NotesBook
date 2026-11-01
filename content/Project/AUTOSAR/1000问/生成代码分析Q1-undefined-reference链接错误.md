# 生成代码分析与集成 Q1：编译报「undefined reference」——模块没配全还是链接脚本没加源文件？第一步查什么？

原始 Flomo：https://v.flomoapp.com/mine/?memo_id=MjU0NzczMDU5

生成代码分析与集成 Q1：编译报「undefined reference」——模块没配全还是链接脚本没加源文件？第一步查什么？

undefined reference 通常两类来源：

1. 配置 / 生成问题：生成代码引用了某个函数 / 变量，但配置没配全，导致那个符号根本没被生成——比如某模块的源文件没生成、某个配置未启用（对应函数没被编译进去）。

2. 链接 / 编译清单问题：符号确实生成了，但对应的 .c 文件没被加进编译链接清单，或链接脚本没把该部分纳入。


第一步查什么：先确认「这个符号是谁生成的、定义在哪个生成源文件里」——生成代码是有规律的，符号定义位置通常能对应到某个配置。

- 用 linker map 文件搜符号：它在 map 里吗？不在 → 没生成。
- 在生成代码目录 grep 该符号定义：它存在于生成文件里吗？

判断逻辑：

- 生成目录里根本找不到该符号定义所在源文件 → 配置没生成全（模块未启用 / 某个 Option 没配置）。
- 符号定义在某个 .c 里、但链接仍报 undefined → 编译清单 / 链接脚本漏了这个 .c，或链接脚本区域问题。
- 符号定义在某个条件编译宏里、而对应配置参数的宏是 DISABLED → 模块没配全（函数体没被编译）。

常见坑：生成代码的 .c 文件清单（Makefile 里引用的生成文件列表）漏了刚新增的文件；或某模块 GenerateCode 没勾选。先看 map + 生成目录，能在几分钟内区分是「没生成」还是「没链接」。

上一题：<https://v.flomoapp.com/mine/?memo_id=MjU0NzcyOTgx><br>
总表：<https://v.flomoapp.com/mine/?memo_id=MjMxMTQ2NDk4>

#Area/技术/AUTOSAR

## 排障边界修订

链接脚本（linker script）主要定义存储区域、段布局和链接符号；它通常不是把某个 .c 文件加入编译清单的地方。遇到 undefined reference，优先区分“符号没有定义/没有编译进目标文件”和“符号名称/链接属性不匹配”，不要先改链接脚本。

推荐顺序：
1. 从链接器报错确认未定义符号的精确拼写和引用目标文件。
2. 用 nm/readelf/objdump 搜索所有 .o/.a 中是否存在定义（注意 C++ name mangling、weak/strong、static/internal linkage）。
3. 检查该源文件是否进入编译命令、是否因条件宏被裁掉、是否被打包进正确静态库。
4. 检查库链接顺序、链接器 --whole-archive 等选项、ABI/编译选项和符号可见性。
5. 只有当报错涉及段/地址/存储区域或链接脚本符号时，再检查 linker script 和 map 文件。

“map 里没有符号”只能作为线索：某些未解析符号不会出现在最终 map 中，应该结合目标文件符号表和完整 linker command 判断。