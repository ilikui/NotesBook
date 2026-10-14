---
title: COM 配置参数与 ARXML 信号映射实战
tags:
  - Project
  - AUTOSAR
  - ARXML
  - COM
  - Python
---

# COM 配置参数与 ARXML 信号映射实战

> [!info] 本文目标
> 把 COM 配置从“工具界面里找参数”变成可追溯的模型检查：从 ARXML 中提取 I-Signal、I-Signal-I-PDU、映射引用、起始位、端序等信息，再与通信矩阵和 CANoe Trace 对照。示例脚本用于审查与盘点，不代替 AUTOSAR XSD 校验或供应商配置验证。

## 1. 从逻辑信号到总线帧：对象关系

~~~mermaid
flowchart TD
    A["SWC DataElement"] --> B["System Signal / Mapping"]
    B --> C["I-Signal"]
    C --> D["I-Signal-I-PDU"]
    D --> E["PduR Routing"]
    E --> F["CanIf Tx / Rx PDU"]
    F --> G["CAN ID / Controller"]
~~~

具体模型引用会随 AUTOSAR Release、System Description 内容、工具链和项目方法论变化。上图是帮助追踪的逻辑关系，不意味着每个项目都以单个 ARXML 文件或完全相同的引用链表达。

## 2. 建议检查的字段

| 对象 / 配置 | 关注字段 | 检查目的 |
| --- | --- | --- |
| I-Signal | SHORT-NAME、长度、数据类型或相关引用 | 确认信号身份和数据定义 |
| I-Signal-I-PDU | SHORT-NAME、长度、发送 / 接收方向相关配置 | 确认信号所属 PDU |
| I-Signal-To-I-PDU-Mapping | I-SIGNAL-REF、START-POSITION、PACKING-BYTE-ORDER 等 | 确认信号如何放入 PDU |
| System Signal / Mapping | 引用关系、映射对象 | 追踪应用语义与通信信号关联 |
| ECUC / COM 配置 | 发送模式、超时、初始值、过滤、更新指示 | 确认运行时行为 |
| PduR / CanIf 配置 | 源 / 目标 PDU、路由与硬件映射 | 确认 PDU 能到达正确通信接口 |

不要假定 START-POSITION 在所有工具中都以相同的位编号方式展示，尤其是 Motorola / Big Endian 信号。审查报告应保留原始字段，最后用项目工具和已知测试向量交叉验证。

## 3. 用 Python 盘点 ARXML 中的信号与映射

以下脚本仅使用 Python 标准库，具备这些能力：

- 支持一个或多个 ARXML 输入文件。
- 按 XML local-name 处理带命名空间的文档。
- 提取 I-Signal、I-Signal-I-PDU 和 I-Signal-To-I-PDU-Mapping。
- 为映射对象输出直接子字段及引用文本，避免把不同层级的 SHORT-NAME 混成一个值。
- 生成 CSV 报告，便于在 Excel 中筛选、对比版本或与通信矩阵核对。

保存为 `arxml_signal_report.py`：

~~~python
#!/usr/bin/env python3
"""Read-only ARXML inventory report; not an XSD or ECUC validator."""

import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


TARGETS = {
    "I-SIGNAL",
    "I-SIGNAL-I-PDU",
    "I-SIGNAL-TO-I-PDU-MAPPING",
    "SYSTEM-SIGNAL",
}


def local_name(tag):
    """Remove an optional XML namespace from a tag."""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def direct_child_text(element, wanted_name):
    """Return text from a direct child only, not a nested descendant."""
    for child in list(element):
        if local_name(child.tag) == wanted_name:
            return (child.text or "").strip()
    return ""


def descendant_refs(element):
    """Collect reference-like elements while preserving their XML paths."""
    refs = []
    for node in element.iter():
        name = local_name(node.tag)
        if name.endswith("-REF") or name.endswith("-REFS"):
            value = (node.text or "").strip()
            if value:
                refs.append(f"{name}={value}")
    return " | ".join(refs)


def element_path(element):
    """Build a readable local-name path; useful for report triage."""
    names = []
    node = element
    while node is not None:
        names.append(local_name(node.tag))
        node = parent_map.get(node)
    return "/" + "/".join(reversed(names))


def inspect_file(file_path):
    global parent_map
    tree = ET.parse(file_path)
    root = tree.getroot()

    parent_map = {child: parent for parent in root.iter() for child in parent}

    for element in root.iter():
        kind = local_name(element.tag)
        if kind not in TARGETS:
            continue

        row = {
            "source_file": str(file_path),
            "object_type": kind,
            "short_name": direct_child_text(element, "SHORT-NAME"),
            "start_position": direct_child_text(element, "START-POSITION"),
            "packing_byte_order": direct_child_text(element, "PACKING-BYTE-ORDER"),
            "length": direct_child_text(element, "LENGTH"),
            "references": descendant_refs(element),
            "xml_path": element_path(element),
        }
        yield row


def main():
    parser = argparse.ArgumentParser(
        description="Create a read-only inventory of common AUTOSAR signal objects."
    )
    parser.add_argument("inputs", nargs="+", help="ARXML files or directories")
    parser.add_argument("-o", "--output", default="arxml_signal_report.csv")
    args = parser.parse_args()

    files = []
    for item in args.inputs:
        path = Path(item)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.arxml")))
        elif path.is_file() and path.suffix.lower() == ".arxml":
            files.append(path)
        else:
            print(f"Warning: skipped unsupported or missing input: {path}", file=sys.stderr)

    # Keep a stable order and avoid processing the same path twice.
    files = list(dict.fromkeys(p.resolve() for p in files))
    if not files:
        parser.error("No ARXML files found.")

    columns = [
        "source_file", "object_type", "short_name", "start_position",
        "packing_byte_order", "length", "references", "xml_path",
    ]
    count = 0
    with open(args.output, "w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for file_path in files:
            try:
                for row in inspect_file(file_path):
                    writer.writerow(row)
                    count += 1
            except (ET.ParseError, OSError) as exc:
                print(f"Error reading {file_path}: {exc}", file=sys.stderr)

    print(f"Scanned {len(files)} ARXML file(s); wrote {count} object row(s) to {args.output}")


if __name__ == "__main__":
    main()
~~~

### 运行方式

~~~bash
# 扫描单个文件
python arxml_signal_report.py path/to/System.arxml

# 递归扫描目录
python arxml_signal_report.py path/to/arxml_dir -o signal_report.csv

# 同时扫描多个文件或目录
python arxml_signal_report.py System.arxml EcuExtract.arxml Ecuc -o signal_report.csv
~~~

### 报告怎么读

| 列 | 解释 |
| --- | --- |
| object_type | 对象的 XML local-name |
| short_name | 当前对象的直接 SHORT-NAME |
| start_position | 若当前对象直接包含 START-POSITION，则输出该值 |
| packing_byte_order | 若当前对象直接包含 PACKING-BYTE-ORDER，则输出原始枚举文本 |
| length | 若当前对象直接包含 LENGTH，则输出该值 |
| references | 当前对象内部发现的引用元素和值 |
| xml_path | 由 XML 层级构建的定位路径 |

**边界说明：** 这是通用盘点脚本，不会自动把分散在多个 ARXML 中的引用全部解析成闭合模型，也不保证字段对每个 AUTOSAR Release 或工具输出都相同。它不会校验 XSD、引用目标是否存在、ECUC 参数是否合法，也不会自动计算 Motorola 位布局。对大型文件应先在副本上运行，并用项目工具进行模型校验。

### 3.1 仓库内可复用的审查脚本

上面的简化示例用于解释字段提取思路。仓库还提供了独立 CLI 工具：[scripts/arxml_signal_audit.py](https://github.com/ilikui/NotesBook/blob/main/scripts/arxml_signal_audit.py)。它可跨多个 ARXML 文件建立对象路径索引，导出对象盘点和引用审查结果；同时尝试从 I-SIGNAL-TO-I-PDU-MAPPING 的父级对象与 I-SIGNAL-REF 提取映射链路。CSV 中会出现 OBJECT、SIGNAL_MAPPING、FINDING 三类记录，JSON 则单独提供 signal_mappings 数组。该链路提取依赖常见 ARXML 嵌套结构，仍需用实际项目模型复核。工具还可选用警告作为 CI 失败条件。

~~~bash
# 输出 CSV，方便在 Excel 中筛选
python scripts/arxml_signal_audit.py ./path/to/arxml -o reports/arxml-audit.csv

# 输出 JSON，方便后续自动化处理
python scripts/arxml_signal_audit.py ./path/to/arxml --format json -o reports/arxml-audit.json

# 存在审查发现时返回非零退出码，可接入 CI
python scripts/arxml_signal_audit.py ./path/to/arxml --fail-on-warn
~~~

该 CLI 同样是只读审查工具。引用解析仅对本次输入文件中已建立的 AUTOSAR 对象路径进行匹配；未解析项可能意味着依赖文件未提供、路径不一致或工具变体差异，不应直接认定为规范错误。建议先用项目的完整 ARXML 输入集合运行，再人工复核告警。
## 4. 从报告到可验证结论

~~~mermaid
flowchart TD
    A["读取 ARXML"] --> B["生成 CSV 盘点"]
    B --> C["筛选 I-Signal / I-PDU / Mapping"]
    C --> D["核对引用与位布局"]
    D --> E["与通信矩阵 / 工具界面对照"]
    E --> F["CANoe 已知测试向量"]
    F --> G["记录差异与配置版本"]
~~~

建议对每个关键信号维护以下记录：

| 字段 | 示例内容 |
| --- | --- |
| Signal / I-PDU | 填写实际 SHORT-NAME |
| ARXML 来源 | 文件名、提交号或配置版本 |
| Mapping | 起始位、长度、端序原始枚举 |
| 数值定义 | 符号属性、Factor、Offset、单位、无效值 |
| 路由 | PduR 源 / 目标 PDU、CanIf PDU |
| 测试向量 | 原始字节、预期 Raw、预期 Physical |
| 验证结果 | CANoe Trace、ECU 变量、偏差说明 |

## 5. 常见误区

- **ARXML 能解析就代表配置合法。** XML 语法正确不等于 XSD、元模型约束、引用关系或 ECUC 约束正确。
- **只按 SHORT-NAME 连接对象。** 同名对象可能出现在不同包路径中；应使用完整引用路径和模型上下文。
- **把 PDU ID 当成 CAN ID。** PDU 标识与总线 CAN Identifier 属于不同层次，需要经配置映射追踪。
- **直接按 Start Bit 手算 Motorola 信号。** 先确认通信矩阵格式与工具位编号约定，再用已知字节向量验证。
- **报告没有某字段就认为项目没配置。** 字段可能在另一个对象、引用目标或 ECUC 参数容器中；本脚本只读取指定对象的直接子字段。
- **用脚本报告代替生成器检查。** 报告用于缩小排查范围，最终仍需项目工具校验、生成日志、编译结果和总线证据。

## 6. 评审检查清单

- [ ] 输入 ARXML 文件与变体、Release、工具版本已记录。
- [ ] CSV 中的对象名称与完整引用路径可回溯到原文件。
- [ ] Signal、I-Signal、I-PDU、PduR、CanIf 关系已人工核对。
- [ ] 位布局、端序、符号属性、Factor、Offset 和无效值已核验。
- [ ] 使用最小值、最大值、边界值和无效值测试向量验证。
- [ ] 与 CANoe Trace 和 ECU 内部观测点交叉验证。
- [ ] 差异、修复、回归结果与配置版本一并归档。

## 相关笔记

- [[COM 信号编码与发送接收机制]]
- [[通信栈工程实战与 CANoe 验证]]
- [[ARXML 与 RTE 代码生成实战]]
- [[规范模块/COM]]
- [[规范模块/PDURouter]]
- [[规范模块/CANInterface]]
