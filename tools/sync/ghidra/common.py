"""Ghidra に依存しない入力の検証と比較。"""
from __future__ import annotations

import csv
import hashlib
import re
import tomllib
from pathlib import Path

LANGUAGE = "ARM:LE:32:v6"
COMPILER = "default"


def plan_segments(info: dict, data: bytes) -> list[dict]:
    if hashlib.sha256(data).hexdigest() != info["code_sha256"]:
        raise ValueError("code.bin の SHA256 が builds.toml と違う")
    if len(data) != info["code_size"]:
        raise ValueError("code.bin のサイズが builds.toml と違う")
    ranges = {k: tuple(int(x, 0) for x in v) for k, v in info["segments"].items()}
    base = ranges["text"][0]
    out = []
    previous = base
    for name in ("text", "rodata", "data", "bss"):
        start, end = ranges[name]
        offset = start - base
        if start < previous or end <= start or (name != "bss" and end - base > len(data)):
            raise ValueError("セグメントの範囲が不正: " + name)
        out.append(dict(name="." + name, start=start, end=end,
                        offset=None if name == "bss" else offset,
                        read=True, write=name in ("data", "bss"), execute=name == "text"))
        previous = end
    if ranges["bss"][0] != ranges["data"][1]:
        raise ValueError("bss は data の直後でない")
    return out


def function_range(row: dict) -> tuple[int, int, bool]:
    raw = int(row["address"], 0)
    start = raw & ~1
    size = int(row["size"], 0)
    if size <= 0:
        raise ValueError("関数サイズは正数が必要")
    return start, start + size - 1, bool(raw & 1)


def normalize_c(text: str) -> str:
    # IDA の整数・呼出規約の表記のみ置換。未知の宣言は推測せず失敗として報告する。
    text = re.sub(r"\bunsigned\s+__int64\b", "unsigned long long", text)
    text = re.sub(r"\b__int64\b", "long long", text)
    for old, new in (("__int8", "char"), ("__int16", "short"), ("__int32", "int"),
                     ("_BYTE", "unsigned char"), ("_WORD", "unsigned short"),
                     ("_DWORD", "unsigned int"), ("_QWORD", "unsigned long long")):
        text = re.sub(r"\b" + old + r"\b", new, text)
    return re.sub(r"\b__(?:fastcall|cdecl|stdcall|thiscall|noreturn|restrict|bitmask)\b", "", text)


def prototype_declaration(text: str, name: str) -> str:
    text = normalize_c(text).strip().rstrip(";")
    pos = text.find("(")
    if pos < 0:
        raise ValueError("関数宣言に引数リストがない")
    # symbols は名前のない関数型。戻り値に含まれるポインタも保持する。
    return text[:pos].rstrip() + " " + name + text[pos:] + ";"


def ida_starts(path: Path, expected_sha: str) -> set[int]:
    with path.open(encoding="utf-8") as f:
        lines = iter(f)
        header = []
        for line in lines:
            if line.startswith("name\taddress\t"):
                columns = line.rstrip().split("\t")
                break
            header.append(line.strip())
        else:
            raise ValueError("IDA index にヘッダーがない")
        if "idb_input_sha256: " + expected_sha not in header:
            raise ValueError("IDA index の入力ハッシュが code.bin と違う")
        return {int(r["address"], 0) & ~1 for r in csv.DictReader(lines, fieldnames=columns, delimiter="\t")}


def compare_starts(ida: set[int], ghidra: set[int]) -> dict:
    return {"ida_count": len(ida), "ghidra_count": len(ghidra), "common": len(ida & ghidra),
            "ida_only_count": len(ida - ghidra), "ghidra_only_count": len(ghidra - ida),
            "ida_only": [f"0x{x:08X}" for x in sorted(ida - ghidra)],
            "ghidra_only": [f"0x{x:08X}" for x in sorted(ghidra - ida)]}


def type_units(text: str) -> list[tuple[str, str]]:
    """IDA の export の // type: を保って型ごとに診断する。通常の C ヘッダーも受ける。"""
    parts = re.split(r"(?m)^// type: ([^\n]+)\n", text.replace("\r\n", "\n"))
    if len(parts) == 1:
        return [("header", text)]
    units = [("forward_declarations", parts[0])] if parts[0].strip() else []
    units.extend((parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2))
    return units


def resolve_target(target: str, rows: list[dict], native_names=()) -> int:
    try:
        return int(target, 0) & ~1
    except ValueError:
        matches = {int(r["address"], 0) & ~1 for r in rows if r["name"] == target}
        matches.update(at for name, at in native_names if name == target)
        if len(matches) != 1:
            raise ValueError("関数名が一意でない、または存在しない: " + target)
        return matches.pop()


def global_type_expression(text: str) -> str:
    # Ghidra の DataType に C の cv 修飾はない。基底型・ポインタ・配列の形は保存する。
    text = re.sub(r"\b(?:const|volatile|restrict)\b", "", normalize_c(text))
    return re.sub(r"\b(?:struct|enum|union)\s+", "", text).strip()



def enum_declaration(text: str) -> tuple[str, int | None]:
    text = normalize_c(text)
    match = re.search(r"\benum\s+(\w+)\s*:\s*([^{}]+)\{", text)
    if match is None:
        return text, None
    sizes = {"unsigned char": 1, "char": 1, "signed char": 1, "short": 2,
             "unsigned short": 2, "int": 4, "unsigned int": 4,
             "long long": 8, "unsigned long long": 8}
    base = " ".join(match[2].split())
    if base not in sizes:
        raise ValueError("列挙型の基底型に対応していない: " + base)
    return text[:match.start()] + "enum " + match[1] + " {" + text[match.end():], sizes[base]


def discover_workspace(repo: Path, explicit: Path | None = None) -> Path:
    if explicit is not None:
        return Path(explicit).resolve()
    for parent in Path(repo).resolve().parents:
        if (parent / "workspace.toml").is_file():
            return parent
    raise FileNotFoundError("workspace.toml のある作業場が見つからない。--workspace を指定する")


def discover_ghidra(workspace: Path, explicit: Path | None = None) -> Path:
    if explicit is not None:
        return Path(explicit).resolve()
    with (workspace / "scripts/third_party.toml").open("rb") as stream:
        version = tomllib.load(stream)["tools"]["ghidra"]["version"]
    base = workspace / "_local/tools/ghidra" / version
    candidates = sorted({p.parent.parent for p in base.rglob("application.properties")
                         if p.parent.name == "Ghidra"})
    if len(candidates) != 1:
        raise ValueError(f"Ghidra {version} の導入先が一意でない（{len(candidates)} 件）: {base}。--ghidra を指定する")
    return candidates[0]


def target_mode(target: str, requested: int, rows: list[dict], explicit: str | None = None) -> str:
    if explicit is not None:
        if explicit not in ("arm", "thumb"):
            raise ValueError("ARM/Thumb の指定が不正")
        return explicit
    try:
        if int(target, 0) & 1:
            return "thumb"
    except ValueError:
        pass
    modes = {"thumb" if int(row["address"], 0) & 1 else "arm"
             for row in rows if int(row["address"], 0) & ~1 == requested}
    if len(modes) > 1:
        raise ValueError("symbols の ARM/Thumb が曖昧。--mode を指定する")
    return next(iter(modes), "arm")
