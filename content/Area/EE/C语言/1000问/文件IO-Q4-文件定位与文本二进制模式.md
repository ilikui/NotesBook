# C语言 1000问 · 文件I/O Q4：fseek / ftell / rewind 怎么用？文本模式和二进制模式下的定位有什么不同？

> 来源：Flomo 原始笔记｜[查看原笔记](https://v.flomoapp.com/mine/?memo_id=MjU2NDUwNTY4)｜迁移日期：2026-10-31

**C语言 1000问 · 文件I/O Q4：fseek / ftell / rewind 怎么用？文本模式和二进制模式下的定位有什么不同？**

▎ 五大学习法：西蒙学习法——把「文件定位」钻透

**三个基本定位函数**

- ftell(fp)：返回当前位置相对文件开头的偏移。常用于「记住当前位置，之后跳回来」。
- fseek(fp, offset, whence)：移动位置指针。
  - whence 三个取值：SEEK\_SET（文件开头，offset 非负）、SEEK\_CUR（当前位置，可正可负）、SEEK\_END（文件末尾，通常为负或 0）。
  - 返回 0 成功、非 0 失败。
- rewind(fp)：回到文件开头，等价 fseek(fp, 0, SEEK\_SET)，但它还会清除错误标志（feof / ferror）。

**典型用法**

- 求文件大小：fseek(fp, 0, SEEK\_END); n = ftell(fp); rewind(fp);
- 定位到第 k 条记录：fseek(fp, k \* sizeof(Record), SEEK\_SET);
- 回退到上一个位置：pos = ftell(fp); ...; fseek(fp, pos, SEEK\_SET);

**文本模式和二进制模式下的差别**

- 二进制模式：位置就是「真实的字节偏移」，定位精确、可任意跳转——推荐用二进制定位。
- 文本模式：因为换行翻译，ftell 返回的值不一定等于真实字节偏移（尤其 Windows 上 '\\r\\n' 与 '\\n' 互转）。标准只保证 ftell 的值能原样传给 fseek（同一文件、同一模式下）用。
- 文本模式下理论上只能 fseek 到「ftell 返回过的位置」或文件开头 / 末尾，不支持任意中间偏移。
- Unix 上文本模式不做翻译，两者基本一致；为可移植，做字节级定位就一律用二进制模式。

**几个坑**

- fseek 超出文件末尾不报错（可跳到末尾之后再写，中间成空洞、读为 0）。
- fseek 只适用于可定位流：管道、终端、socket 不能 fseek。
- 用 fseek 后缓冲状态会重置；"r+" 读写切换时中间必须有 fflush 或 fseek，否则未定义。
- rewind 会清除错误标志，想「复位又清错误」时方便，但想保留错误状态就别用。
- ftell 返回 long，超大文件（> 2GB）要用 fseeko / ftello（POSIX）或 \_fseeki64。

一句话：ftell 记位置、fseek 跳位置、rewind 回开头（还清错误标志）；二进制模式下位置就是真实字节偏移、可任意跳，文本模式因换行翻译只保证「fseek 到 ftell 给过的位置」——要精确字节定位就用二进制模式。

📎 问题库（专栏⑭导航）→ [https://v.flomoapp.com/mine/?memo\_id=MjQ1NzM0NTk5](https://v.flomoapp.com/mine/?memo_id=MjQ1NzM0NTk5)

📎 文件I/O Q3（feof 的坑）→ [https://v.flomoapp.com/mine/?memo\_id=MjU2NDUwNDg4](https://v.flomoapp.com/mine/?memo_id=MjU2NDUwNDg4)

#Area/技术/C语言
