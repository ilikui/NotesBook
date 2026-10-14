#!/usr/bin/env python3
"""Read-only AUTOSAR ARXML inventory and reference-audit helper.

This tool is a practical triage aid, not an AUTOSAR XSD validator. It uses only
Python's standard library and deliberately reports unresolved references as
findings rather than assuming every external reference is invalid.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

SIGNAL_TYPES = {
    "I-SIGNAL",
    "I-SIGNAL-I-PDU",
    "I-SIGNAL-TO-I-PDU-MAPPING",
    "SYSTEM-SIGNAL",
}
REF_SUFFIXES = ("-REF", "-REFS")
OBJECT_NAME = "SHORT-NAME"


def lname(tag: str) -> str:
    """Return an XML local name, ignoring an optional namespace."""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def child_text(node: ET.Element, name: str) -> str:
    for child in list(node):
        if lname(child.tag) == name:
            return (child.text or "").strip()
    return ""


def refs_in(node: ET.Element) -> List[Tuple[str, str]]:
    found = []
    for item in node.iter():
        kind = lname(item.tag)
        if kind.endswith(REF_SUFFIXES):
            value = (item.text or "").strip()
            if value:
                found.append((kind, value))
    return found


def xml_path_map(root: ET.Element) -> Dict[ET.Element, str]:
    paths = {root: "/" + lname(root.tag)}
    for parent in root.iter():
        for child in list(parent):
            paths[child] = paths[parent] + "/" + lname(child.tag)
    return paths


def walk_package(package: ET.Element, parent_path: str, source: str,
                 objects: List[dict], path_index: Dict[str, List[dict]]) -> None:
    package_name = child_text(package, OBJECT_NAME)
    package_path = parent_path.rstrip("/") + "/" + package_name if package_name else parent_path
    elements = next((c for c in list(package) if lname(c.tag) == "ELEMENTS"), None)
    subpackages = next((c for c in list(package) if lname(c.tag) == "AR-PACKAGES"), None)

    if elements is not None:
        for obj in list(elements):
            name = child_text(obj, OBJECT_NAME)
            if not name:
                continue
            kind = lname(obj.tag)
            full_path = package_path.rstrip("/") + "/" + name
            row = {
                "source_file": source,
                "object_type": kind,
                "short_name": name,
                "autosar_path": full_path,
                "xml_path": "",
                "start_position": child_text(obj, "START-POSITION"),
                "packing_byte_order": child_text(obj, "PACKING-BYTE-ORDER"),
                "length": child_text(obj, "LENGTH"),
                "references": refs_in(obj),
            }
            objects.append(row)
            path_index[full_path].append(row)
            # A package may contain nested AR-PACKAGE nodes in vendor variants.
            if kind == "AR-PACKAGE":
                walk_package(obj, package_path, source, objects, path_index)

    if subpackages is not None:
        for subpackage in list(subpackages):
            if lname(subpackage.tag) == "AR-PACKAGE":
                walk_package(subpackage, package_path, source, objects, path_index)


def parse_inputs(inputs: Iterable[Path]) -> Tuple[List[dict], List[dict], Dict[str, List[dict]]]:
    objects: List[dict] = []
    all_refs: List[dict] = []
    path_index: Dict[str, List[dict]] = defaultdict(list)

    for file_path in inputs:
        try:
            root = ET.parse(file_path).getroot()
        except (ET.ParseError, OSError) as exc:
            all_refs.append({
                "severity": "ERROR",
                "rule": "XML_PARSE",
                "source_file": str(file_path),
                "object_path": "",
                "reference_type": "",
                "reference": "",
                "message": str(exc),
            })
            continue

        paths = xml_path_map(root)
        before = len(objects)
        # Standard AUTOSAR structure: AR-PACKAGES / AR-PACKAGE / ELEMENTS.
        for node in root.iter():
            if lname(node.tag) == "AR-PACKAGE":
                parent = next((p for p in root.iter() if node in list(p)), None)
                if parent is not None and lname(parent.tag) == "AR-PACKAGES":
                    walk_package(node, "", str(file_path), objects, path_index)
        for obj in objects[before:]:
            # xml_path is a navigational hint; canonical matching uses AUTOSAR path.
            obj["xml_path"] = paths.get(root, "/" + lname(root.tag))
        for node in root.iter():
            owner = child_text(node, OBJECT_NAME)
            for ref_type, ref_value in refs_in(node):
                all_refs.append({
                    "severity": "INFO",
                    "rule": "REFERENCE",
                    "source_file": str(file_path),
                    "object_path": owner,
                    "reference_type": ref_type,
                    "reference": ref_value,
                    "message": "Reference discovered; resolution is checked after all input files are indexed.",
                })

    # Deduplicate package walks when a parser encounters nested package containers.
    unique = {}
    for obj in objects:
        key = (obj["source_file"], obj["autosar_path"], obj["object_type"])
        unique[key] = obj
    objects = list(unique.values())
    return objects, all_refs, path_index


def audit(objects: List[dict], refs: List[dict], path_index: Dict[str, List[dict]]) -> List[dict]:
    findings: List[dict] = []
    name_counts = Counter((o["object_type"], o["short_name"]) for o in objects)
    for obj in objects:
        if name_counts[(obj["object_type"], obj["short_name"])] > 1:
            findings.append({
                "severity": "WARN", "rule": "DUPLICATE_SHORT_NAME",
                "source_file": obj["source_file"], "object_path": obj["autosar_path"],
                "reference_type": "", "reference": obj["short_name"],
                "message": "同类型对象的 SHORT-NAME 在输入集合中重复；请结合包路径判断是否冲突。",
            })
        if obj["object_type"] in SIGNAL_TYPES and not obj["short_name"]:
            findings.append({
                "severity": "WARN", "rule": "MISSING_SHORT_NAME",
                "source_file": obj["source_file"], "object_path": obj["autosar_path"],
                "reference_type": "", "reference": "",
                "message": "信号相关对象缺少直接 SHORT-NAME。",
            })

    for ref in refs:
        value = ref["reference"]
        if not value or not value.startswith("/"):
            continue
        if value not in path_index:
            findings.append({
                "severity": "WARN", "rule": "UNRESOLVED_REFERENCE",
                "source_file": ref["source_file"], "object_path": ref["object_path"],
                "reference_type": ref["reference_type"], "reference": value,
                "message": "在本次输入文件集合建立的对象索引中未找到该绝对引用；可能是缺少依赖 ARXML，也可能是路径/模型变体不同。",
            })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory common AUTOSAR objects and audit references across ARXML files.")
    parser.add_argument("inputs", nargs="+", help="ARXML files or directories")
    parser.add_argument("-o", "--output", default="arxml_signal_audit.csv", help="Output file path")
    parser.add_argument("--format", choices=("csv", "json"), default="csv", help="Report format")
    parser.add_argument("--fail-on-warn", action="store_true", help="Return exit code 1 if warnings/errors are found")
    args = parser.parse_args()

    files: List[Path] = []
    for item in args.inputs:
        path = Path(item)
        if path.is_dir():
            files.extend(sorted(path.rglob("*.arxml")))
        elif path.is_file() and path.suffix.lower() == ".arxml":
            files.append(path)
        else:
            print(f"Warning: skipped unsupported or missing input: {path}", file=sys.stderr)
    files = list(dict.fromkeys(p.resolve() for p in files))
    if not files:
        parser.error("No ARXML files found.")

    objects, refs, path_index = parse_inputs(files)
    findings = audit(objects, refs, path_index)
    result = {
        "summary": {
            "files_scanned": len(files),
            "objects_indexed": len(objects),
            "references_discovered": len(refs),
            "findings": len(findings),
            "signal_related_objects": sum(o["object_type"] in SIGNAL_TYPES for o in objects),
        },
        "objects": [
            {**o, "references": [{"type": t, "value": v} for t, v in o["references"]]}
            for o in objects
        ],
        "findings": findings,
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.format == "json":
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        columns = ["record_type", "severity", "rule", "source_file", "object_type",
                   "short_name", "autosar_path", "start_position", "packing_byte_order",
                   "length", "reference_type", "reference", "message"]
        with output.open("w", newline="", encoding="utf-8-sig") as stream:
            writer = csv.DictWriter(stream, fieldnames=columns)
            writer.writeheader()
            for obj in objects:
                writer.writerow({
                    "record_type": "OBJECT", "source_file": obj["source_file"],
                    "object_type": obj["object_type"], "short_name": obj["short_name"],
                    "autosar_path": obj["autosar_path"], "start_position": obj["start_position"],
                    "packing_byte_order": obj["packing_byte_order"], "length": obj["length"],
                    "message": "对象盘点记录；字段只读取对象的直接子元素。",
                })
            for item in findings:
                writer.writerow({"record_type": "FINDING", **item})

    print("Scanned {files} file(s); indexed {objects} object(s); found {findings} finding(s).".format(
        files=len(files), objects=len(objects), findings=len(findings)))
    print(f"Report: {output}")
    if args.fail_on_warn and findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
