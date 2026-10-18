#!/usr/bin/env python3
"""全関数の逆アセンブルから同じ形の関数を探す（IDA 不要）。

例: clones.py --build acnl_jpn_v15 [--export DIR] [--out FILE]
    [--min-instructions 5] [--update-symbols] [--symbols DIR]
--symbols はビルド単位の symbols ディレクトリ。
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "sync"))
import idacommon as ic
import symlib as sl

LINE = re.compile(r"^0x[0-9A-Fa-f]+\s+(ARM|Thumb|data)\s+.*?:[ \t]+(.*)$")
CONDITION = r"(?:EQ|NE|CS|HS|CC|LO|MI|PL|VS|VC|HI|LS|GE|LT|GT|LE|AL)?"
BRANCH = re.compile(r"(?:B|BL|BX|BLX)" + CONDITION + r"$")
REGISTER = re.compile(r"(?:R(?:1[0-5]|[0-9])|SP|LR|PC|SB|SL|FP|IP|[SDQ]\d+|C\d+|P\d+|"
                      r"APSR(?:_\w+)?|CPSR(?:_\w+)?|SPSR(?:_\w+)?|FPSCR|FPEXC)$", re.I)
WORDS = {"LSL", "LSR", "ASR", "ROR", "RRX", "UXTB", "UXTH", "SXTB", "SXTH",
         "SY", "ST", "ISH", "ISHST", "NSH", "NSHST", "OSH", "OSHST", "AIF", "IF", "I", "F", "A",
         "EQ", "NE", "CS", "HS", "CC", "LO", "MI", "PL", "VS", "VC", "HI", "LS", "GE", "LT", "GT", "LE", "AL"}
# 数値は名前より先に読む。文字リテラル内の字も名前として消さない。
TOKEN = re.compile(r"'(?:\\.|[^'\\])*'|0[xX][0-9A-Fa-f]+|\d+(?:\.\d+)?(?:[Ee][+-]?\d+)?|"
                   r"[A-Za-z_$?][\w$?:.@]*", re.UNICODE)


def operands(text: str) -> list[str]:
    """レジスタリスト・メモリ式・引用符内のコンマは分割しない。"""
    result, start, depth, quote, escape = [], 0, 0, "", False
    for i, char in enumerate(text):
        if escape:
            escape = False
        elif quote:
            if char == "\\":
                escape = True
            elif char == quote:
                quote = ""
        elif char in "\"'":
            quote = char
        elif char in "[{(":
            depth += 1
        elif char in "]})":
            depth -= 1
        elif char == "," and depth == 0:
            result.append(text[start:i].strip())
            start = i + 1
    result.append(text[start:].strip())
    return result


@lru_cache(maxsize=65536)
def normalize_instruction(text: str) -> str:
    # export はコメントを除去済み。手製の小さな入力でも ; 以降を無視する。
    text = text.split(";", 1)[0].strip()
    parts = text.split(None, 1)
    if not parts:
        raise ValueError("空の命令")
    mnemonic = parts[0].upper()
    base = mnemonic.split(".", 1)[0]
    args = operands(parts[1]) if len(parts) > 1 else []

    def token(match):
        word = match[0]
        if word.startswith("'"):
            return word
        if word[0].isdigit():
            # 10進と16進の表示差も揃える（浮動小数は表記を残す）。
            if re.fullmatch(r"0[xX][0-9a-fA-F]+|\d+", word):
                return str(int(word, 16 if word.lower().startswith("0x") else 10))
            return word.lower()
        upper = word.upper()
        return upper if REGISTER.fullmatch(word) or upper in WORDS else "<address>"

    normalized = []
    for i, arg in enumerate(args):
        # =値 は数値定数でも全体を伏せる。ADR と直接分岐も番地を伏せる。
        target = ((BRANCH.fullmatch(base) and i == 0) or
                  (base in {"CBZ", "CBNZ"} and i == 1) or
                  (re.fullmatch("ADR" + CONDITION, base) and i == 1))
        if arg.startswith("="):
            value = "=<literal>"
        elif target and not REGISTER.fullmatch(arg):
            value = "<address>"
        elif re.match(r"#?:?(?:LOWER16|UPPER16):", arg, re.I):
            value = "<address>"
        elif re.search(r"\[\s*PC\s*,\s*#", arg, re.I):
            # リテラルプールまでの距離は関数の形に含めない。
            value = TOKEN.sub(token, arg)
            value = re.sub(r"(\[\s*PC\s*,\s*)#[^\]]+", r"\1<address>", value, flags=re.I)
        elif (base.startswith(("LDR", "STR", "VLDR", "VSTR")) and i == len(args) - 1
              and re.fullmatch(r"(?:0x[0-9a-f]+|[0-9]+)", arg, re.I)):
            # ロード・ストアの裸の数値オペランドは絶対番地。
            value = "<address>"
        else:
            value = TOKEN.sub(token, arg)
        normalized.append(re.sub(r"\s+", "", value))
    return mnemonic + (" " + ",".join(normalized) if normalized else "")


def instruction_sequence(text: str) -> tuple[tuple[str, str], ...]:
    if "[disassembly]\n" not in text:
        raise ValueError("[disassembly] がない")
    section = text.split("[disassembly]\n", 1)[1]
    result = []
    for line in section.splitlines():
        if line.startswith("["):
            break
        if not line.strip() or line.lstrip().startswith(";"):
            continue
        match = LINE.fullmatch(line)
        if not match:
            raise ValueError(f"逆アセンブルの行を読めない: {line}")
        mode, instruction = match.groups()
        if mode != "data":
            result.append((mode, normalize_instruction(instruction)))
    return tuple(result)


@dataclass(frozen=True)
class Function:
    address: int  # Thumb は下位ビット 1
    name: str
    count: int
    digest: str
    mode: str

    @property
    def named(self):
        return sl.is_user_name(self.name)


def read_functions(export: Path, symbols: list[dict], minimum: int) -> list[Function]:
    lines = (export / "index.txt").read_text(encoding="utf-8").splitlines(keepends=True)
    header = next((i for i, line in enumerate(lines) if line.startswith("name\taddress\tfile\t")), None)
    if header is None:
        raise ValueError("index.txt のヘッダーがない")
    names = {sl.parse_addr(r["address"]): r["name"] for r in symbols}
    result, seen = [], set()
    for count, row in enumerate(csv.DictReader(io.StringIO("".join(lines[header:])), delimiter="\t"), 1):
        address = int(row["address"], 16) & ~1
        if address in seen:
            raise ValueError(f"索引の番地が重複: {sl.fmt_addr(address)}")
        seen.add(address)
        if count % 5000 == 0:
            print(f"functions: {count}", file=sys.stderr, flush=True)
        path = (export / row["file"]).resolve()
        if not path.is_relative_to((export / "functions").resolve()):
            raise ValueError(f"functions の外を指す索引: {row['file']}")
        try:
            seq = instruction_sequence(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise ValueError(f"{path}: {exc}") from exc
        if len(seq) < minimum:
            continue
        address |= int(seq[0][0] == "Thumb")
        name = names.get(address, row["name"])
        digest = hashlib.sha256(json.dumps(seq, ensure_ascii=False).encode("utf-8")).hexdigest()
        mode = "/".join(dict.fromkeys(m for m, _ in seq))
        result.append(Function(address, name, len(seq), digest, mode))
    return result


def group_functions(functions: list[Function]) -> list[list[Function]]:
    groups: dict[str, list[Function]] = {}
    for function in functions:
        groups.setdefault(function.digest, []).append(function)
    # 先頭が代表。名前が付いた関数を優先し、その中で最小番地を使う。
    result = [sorted(g, key=lambda f: (not f.named, f.address)) for g in groups.values() if len(g) > 1]
    return sorted(result, key=lambda g: g[0].address)


def update_symbols(directory: Path, rows: list[dict], groups: list[list[Function]]) -> int:
    targets = {f.address: ("" if f == group[0] else sl.fmt_addr(group[0].address))
               for group in groups for f in group if f.named}
    changed = 0
    for row in rows:
        address = sl.parse_addr(row["address"])
        if sl.is_user_name(row["name"]) and address in targets and row["clone_of"] != targets[address]:
            row["clone_of"] = targets[address]
            changed += 1
    if changed:
        sl.write_table(directory, "functions", rows)
    return changed


def run(build: str, export: Path, out: Path, symbols: Path, minimum: int = 5,
        update: bool = False) -> dict:
    if minimum < 1:
        raise ValueError("最小命令数は 1 以上にする")
    started = time.monotonic()
    rows = sl.read_table(symbols, "functions")
    groups = group_functions(read_functions(export, rows, minimum))
    text = ["生成物。編集しない（tools/clones.py が作り直す）",
            f"build: {build}", f"min_instructions: {minimum}", ""]
    for group in groups:
        representative = group[0]
        text.append(f"clone {representative.digest} mode={representative.mode} "
                    f"instructions={representative.count} representative={sl.fmt_addr(representative.address)}")
        for f in sorted(group, key=lambda f: f.address):
            text.append(f"  {sl.fmt_addr(f.address)}\t{f.name}\tinstructions={f.count}")
        text.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(text) + "\n", encoding="utf-8", newline="\n")
    changed = update_symbols(symbols, rows, groups) if update else 0
    return dict(build=build, groups=len(groups), functions=sum(map(len, groups)),
                named_groups=sum(any(f.named for f in g) for g in groups),
                symbols_updated=changed, seconds=round(time.monotonic() - started, 3), out=str(out))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--export", type=Path, help="書き出しのディレクトリ（index.txt のある場所）")
    ap.add_argument("--out", type=Path, help="clones.txt の出力ファイル")
    ap.add_argument("--symbols", type=Path, help="ビルドの symbols ディレクトリ")
    ap.add_argument("--min-instructions", type=int, default=5)
    ap.add_argument("--update-symbols", action="store_true")
    args = ap.parse_args(argv)
    ic.build_info(args.build)
    export = args.export or ic.build_dir(args.build) / "export"
    try:
        result = run(args.build, export, args.out or export / "clones.txt",
                     args.symbols or ic.REPO / "symbols" / args.build,
                     args.min_instructions, args.update_symbols)
    except (OSError, ValueError, KeyError) as exc:
        ap.error(str(exc))
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
