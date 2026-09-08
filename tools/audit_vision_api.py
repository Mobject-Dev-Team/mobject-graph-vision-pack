#!/usr/bin/env python3
"""Compare a local, untracked Vision API export with PLC sources and registration.

Run from any directory: python3 tools/audit_vision_api.py
Only writes docs/vision-api-5.10.2-audit/. No TwinCAT installation is required.
This is a structural inventory, not an ST compiler or a runtime correctness test.
"""

import argparse
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "Tc3_Vision_Api_5.10.2.html"
LIB = ROOT / "src/sln/lib/mobject-graph-vision-pack"
OUT = ROOT / "docs/vision-api-5.10.2-audit"


def text(element):
    return " ".join("".join(element.itertext()).split()) if element is not None else ""


def strip_comments(source):
    # Preserve quoted strings, including labels containing whitespace or '//'.
    pattern = r"'(?:\$[\s\S]|''|[^'])*'|//[^\n]*|\(\*[\s\S]*?\*\)"
    return re.sub(pattern, lambda m: m[0] if m[0].startswith("'") else " ", source)


def table_rows(table):
    if table is None:
        return []
    rows = table.findall("tr")
    headers = [text(cell) for cell in rows[0].findall("td")]
    return [dict(zip(headers, [text(c) for c in row.findall("td")])) for row in rows[1:]]


def read_api():
    root = ET.parse(API).getroot()
    types, functions, interfaces, blocks = {}, {}, {}, {}
    section, kind, current = "", "", None
    for element in root.find("body"):
        if element.tag == "h1":
            section, current = text(element), None
        elif element.tag == "h2":
            kind = text(element)
            if section in ("Interfaces", "FunctionBlocks"):
                current = {"name": kind, "description": [], "methods": [], "params": []}
                (interfaces if section == "Interfaces" else blocks)[kind] = current
        elif section == "Data Types" and element.tag == "table":
            for row in element.findall("tr"):
                cells = row.findall("td")
                name = text(cells[0].find("b"))
                assert name and name not in types, name
                types[name] = {
                    "name": name, "kind": kind,
                    "description": text(cells[0].find("i")),
                    "base": text(cells[1].find("i")),
                    "members": table_rows(row.find("./td/table")),
                }
        elif section.startswith("Functions (") and element.tag == "table":
            for row in element.findall("tr"):
                cells = row.findall("td")
                name = text(cells[0].find("b"))
                assert name and name not in functions, name
                functions[name] = {
                    "name": name, "description": text(cells[0]),
                    "return": text(cells[1]), "params": table_rows(cells[2].find("table")),
                }
            assert len(functions) == int(re.search(r"\((\d+)\)", section)[1])
        elif current is not None and element.tag == "i":
            current["description"].append(text(element))
        elif current is not None and element.tag == "table":
            if text(element.find("tr/td")) == "Parameter":
                current["params"].extend(table_rows(element))
            else:
                assert text(element.find("tr/td")) == "Method"
                for row in element.findall("tr")[1:]:
                    cells = row.findall("td")
                    current["methods"].append({
                        "name": text(cells[0].find("b")), "return": text(cells[1]),
                        "params": table_rows(cells[2].find("table")),
                    })
    assert len(types) == 209 and len(interfaces) == 113 and len(blocks) == 25
    assert all(t["members"] for t in types.values() if t["kind"] in ("Enums", "Structs"))
    return types, functions, interfaces, blocks


def read_sources():
    project = ET.parse(LIB / "mobject-graph-vision-pack.plcproj").getroot()
    compile_entries = {}
    for item in project.findall(".//{*}Compile"):
        path = item.get("Include").replace("\\", "/")
        assert path not in compile_entries, path
        assert (LIB / path).is_file(), path
        compile_entries[path] = item.findtext("{*}ExcludeFromBuild", "false").lower() != "true"
    sources = {}
    for path in sorted(LIB.rglob("*.TcPOU")):
        pou = ET.parse(path).getroot().find("POU")
        name = pou.get("Name")
        assert name.lower() not in sources, name
        source = strip_comments("\n".join(pou.itertext()))
        sources[name.lower()] = {
            "name": name, "path": path.relative_to(ROOT).as_posix(),
            "compiled": compile_entries.get(path.relative_to(LIB).as_posix(), False),
            "declaration": strip_comments(pou.findtext("Declaration", "")),
            "text": source,
            "methods": {m.get("Name"): strip_comments(m.findtext("Implementation/ST", ""))
                        for m in pou.findall("Method")},
            "calls": set(re.findall(r"\b(F_VN_\w+)\s*\(", source, re.I)),
        }
    return sources


def registrations(sources, pack, method, named=False):
    source = sources[pack.lower()]
    variables = {n.lower(): t.lower() for n, t in re.findall(
        r"\b(\w+)\s*:\s*(\w+)", source["declaration"])}
    prefix = r"\s*'([^']*)'\s*," if named else ""
    matches = re.findall(r"\." + method + r"\(" + prefix + r"\s*(\w+)\s*\)", source["text"], re.I)
    entries = {}
    for match in matches:
        label, variable = match if named else ("", match)
        name = variables[variable.lower()]
        assert name in sources and name not in entries, name
        assert sources[name]["compiled"], name
        entries[name] = label
    if named:
        assert len(entries.values()) == len(set(entries.values()))
    return entries


def status(source, registered):
    if source is None:
        return "missing"
    if not source["compiled"]:
        return "excluded_from_build"
    return "registered" if source["name"].lower() in registered else "unregistered"


def call_parameters(st, name):
    start = re.search(r"\b" + re.escape(name) + r"\s*\(", st, re.I)
    if start is None:
        return None
    end, depth = start.end(), 1
    while depth and end < len(st):
        depth += (st[end] == "(") - (st[end] == ")")
        end += 1
    assert depth == 0, name
    return {p.lower() for p in re.findall(r"\b(\w+)\s*(?::=|=>)", st[start.end():end - 1])}


def signature(params):
    return "; ".join(f"{p['Parameter']}: {p['Type']} [{p.get('Direction', '')}]"
                     + (f" = {p['Default']}" if p.get("Default") else "") for p in params)


def licence(description):
    match = re.search(r"Required License: (.*)", description)
    return match[1] if match else ""


def write_csv(name, fields, rows):
    with (OUT / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    global API
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api", type=Path, default=API,
                        help="Path to the local Tc3_Vision_Api_5.10.2.html export (never committed).")
    args = parser.parse_args()
    API = args.api.resolve()
    if not API.is_file():
        parser.error("The API export is a local-only reference. Supply it with --api PATH; "
                     "the committed coverage inventories remain readable without it.")
    types, functions, interfaces, blocks = read_api()
    sources = read_sources()
    node_regs = registrations(sources, "VisionNodePack", "AddNodeAsPrototype", True)
    datatype_regs = registrations(sources, "VisionDatatypePack", "RegisterDatatype")
    OUT.mkdir(parents=True, exist_ok=True)
    known_types = {n.lower(): n for n in list(types) + list(interfaces)}

    def dependencies(value):
        return sorted({known_types[t.lower()] for t in re.findall(r"\w+", value)
                       if t.lower() in known_types and types.get(known_types[t.lower()], {}).get("kind") != "Constants"})

    def unavailable(names):
        return [n for n in names if status(sources.get("_" + n.lower()), datatype_regs) != "registered"]

    function_rows, repairs = [], []
    for name, function in sorted(functions.items()):
        source = sources.get("node_" + name.lower())
        declared_types = dependencies(" ".join(p["Type"] for p in function["params"]))
        option_types = dependencies(" ".join(p.get("Comment", "") for p in function["params"]))
        called = call_parameters(source["methods"].get("OnExecute", ""), name) if source else None
        expected = {p["Parameter"].lower() for p in function["params"]}
        missing = [p["Parameter"] for p in function["params"] if called is not None and p["Parameter"].lower() not in called]
        extra = sorted(called - expected) if called is not None else []
        if source and (called is None or missing or extra):
            repairs.append({"kind": "function_parameters", "symbol": name,
                            "missing": "; ".join(missing), "extra": "; ".join(extra),
                            "path": source["path"]})
        function_rows.append({
            "api_function": name, "proposed_node": "Node_" + name,
            "status": status(source, node_regs), "licence": licence(function["description"]),
            "source": source["path"] if source else "",
            "graph_path": node_regs.get("node_" + name.lower(), ""),
            "required_api_types": "; ".join(declared_types),
            "unavailable_api_types": "; ".join(unavailable(declared_types)),
            "unavailable_types_in_comments": "; ".join(unavailable(option_types)),
            "external_interface_types": "; ".join(sorted({p["Type"] for p in function["params"] if "ITcUnknown" in p["Type"]})),
            "buffer_or_pointer_params": "; ".join(p["Parameter"] + ": " + p["Type"] for p in function["params"] if re.search(r"PVOID|Pointer To", p["Type"], re.I)),
            "other_call_sites": "; ".join(s["path"] for s in sources.values() if name in s["calls"] and s != source),
            "omitted_call_parameters": "; ".join(missing),
            "signature": signature(function["params"]),
        })
    write_csv("functions.csv", list(function_rows[0]), function_rows)

    datatype_rows, members = [], []
    for name, datatype in sorted(types.items()):
        is_constant = datatype["kind"] == "Constants"
        wrapper = ("Node_" if is_constant else "_") + name
        source = sources.get(wrapper.lower())
        declared_types = dependencies(datatype["base"] + " " + " ".join(p.get("Type", "") for p in datatype["members"]))
        datatype_rows.append({
            "api_type": name, "kind": datatype["kind"], "wrapper": wrapper,
            "status": status(source, node_regs if is_constant else datatype_regs),
            "base_type": datatype["base"], "source": source["path"] if source else "",
            "required_api_types": "; ".join(declared_types),
            "unavailable_api_types": "; ".join(unavailable(declared_types)),
        })
        label_key = "Value" if datatype["kind"] == "Enums" else "Parameter"
        method = "AddLocalEnumeration" if datatype["kind"] == "Enums" else "AddMember"
        registered_labels = set(re.findall(method + r"\(\s*'([^']*)'", source["text"], re.I)) if source else set()
        for member in datatype["members"]:
            label = member[label_key]
            member_status = "missing_wrapper" if not source else "present" if label in registered_labels else "missing_label"
            members.append({
                "api_type": name, "kind": datatype["kind"], "member": label,
                "type": member.get("Type", datatype["base"]), "default": member.get("Default", ""),
                "status": member_status, "comment": member.get("Comment", ""),
            })
            if member_status == "missing_label":
                repairs.append({"kind": "member_label", "symbol": name, "missing": label,
                                "extra": "; ".join(x for x in registered_labels if x.strip() == label), "path": source["path"]})
    write_csv("datatypes-and-constants.csv", list(datatype_rows[0]), datatype_rows)
    write_csv("datatype-members.csv", list(members[0]), members)
    write_csv("existing-wrapper-gaps.csv", ["kind", "symbol", "missing", "extra", "path"], repairs)

    interface_rows = []
    direct_interface_deps = {n for f in functions.values() for n in dependencies(" ".join(p["Type"] for p in f["params"]))}
    for name, interface in sorted(interfaces.items()):
        source = sources.get("_" + name.lower())
        if name.startswith(("ITcVnAccess_", "ITcVnRandomAccess_")):
            scope = "typed_access_adapter; most operations also exposed by F_VN nodes"
        elif name in direct_interface_deps:
            scope = "function_parameter; implement graph datatype for function coverage"
        elif name in ("ITcVnIteratorBase", "ITcVnIteratorCopyCreator", "ITcVnBidirectionalIterator"):
            scope = "iterator_foundation"
        else:
            scope = "advanced_device_export_or_interface_method_access"
        interface_rows.append({
            "api_interface": name, "wrapper": "_" + name, "status": status(source, datatype_regs),
            "scope": scope, "source": source["path"] if source else "",
            "description": "; ".join(interface["description"]),
            "methods": "; ".join(m["name"] + "(" + signature(m["params"]) + "): " + m["return"] for m in interface["methods"]),
        })
    write_csv("interfaces.csv", list(interface_rows[0]), interface_rows)

    block_rows = []
    for name, block in sorted(blocks.items()):
        source = sources.get("node_" + name.lower())
        block_rows.append({
            "api_function_block": name, "proposed_node_or_facade": "Node_" + name,
            "status": status(source, node_regs), "source": source["path"] if source else "",
            "licence": licence(" ".join(block["description"])),
            "parameters": signature(block["params"]),
            "methods": "; ".join(m["name"] + "(" + signature(m["params"]) + "): " + m["return"] for m in block["methods"]),
        })
    write_csv("function-blocks.csv", list(block_rows[0]), block_rows)
    assert any(b["parameters"] for b in block_rows) and any(b["methods"] for b in block_rows)

    registration_rows = []
    for source in sources.values():
        if source["name"].startswith("Node_") or ("/Datatypes/" in source["path"] and source["name"].startswith("_")):
            regs = node_regs if source["name"].startswith("Node_") else datatype_regs
            registration_rows.append({"symbol": source["name"], "status": status(source, regs),
                                      "source": source["path"], "graph_path": regs.get(source["name"].lower(), "")})
    write_csv("project-registration.csv", list(registration_rows[0]), registration_rows)

    summary = {
        "api_file": API.name,
        "api_sha256": hashlib.sha256(API.read_bytes()).hexdigest(),
        "functions": dict(Counter(r["status"] for r in function_rows)),
        "datatypes_and_constants": {kind: dict(Counter(r["status"] for r in datatype_rows if r["kind"] == kind)) for kind in sorted({r["kind"] for r in datatype_rows})},
        "interfaces": dict(Counter(r["status"] for r in interface_rows)),
        "function_blocks": dict(Counter(r["status"] for r in block_rows)),
        "missing_functions_by_licence": dict(Counter(r["licence"] for r in function_rows if r["status"] == "missing")),
        "registered_nodes": len(node_regs), "registered_datatypes": len(datatype_regs),
        "source_pous": len(sources), "existing_wrapper_gap_rows": len(repairs),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = ["# Complete list of missing function nodes", "",
             "Generated by `python3 tools/audit_vision_api.py`. Each entry needs `Node_<function>` unless the plan explicitly routes it through an existing extension. These are source absences, not a release-to-release API diff.", "",
             "See [functions.csv](functions.csv) for signatures, defaults, dependencies, pointer parameters, existing helper uses, and every implemented function. See [the implementation plan](../vision-api-5.10.2-plan.md) for sequencing and scope.", ""]
    for lic in sorted(summary["missing_functions_by_licence"]):
        rows = [r for r in function_rows if r["status"] == "missing" and r["licence"] == lic]
        lines += [f"## {lic} ({len(rows)})", ""]
        lines += ["- `" + r["api_function"] + "`" for r in rows]
        lines += [""]
    lines += ["## Existing but unavailable", ""]
    lines += ["- `" + r["proposed_node"] + "`: " + r["status"] for r in function_rows
              if r["status"] not in ("registered", "missing")]
    lines += ["",
              "Function blocks are inventoried separately in [function-blocks.csv](function-blocks.csv); their methods and asynchronous operation require facade design, so they are not counted as ordinary function nodes.", ""]
    (OUT / "missing-function-nodes.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
