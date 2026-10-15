"""symbols/ の CSV・meta の読み書きと比較。IDA を使わない（pytest で試験できる）。

形式は docs/symbols.md。アドレスは 0x 付き大文字16進8桁、行はアドレス昇順、UTF-8（BOM なし）・LF。
"""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path

TOOL_VERSION = "1"

COLUMNS = {
    "functions": ["address", "size", "name", "prototype", "confidence", "source", "refs", "clone_of"],
    "globals": ["address", "size", "name", "type", "confidence", "source", "refs"],
    "comments": ["address", "kind", "text"],
    "vtables": ["address", "class", "count"],
    "lvars": ["function", "name", "type", "location"],
}
# 比較・並べ替えに使う主キー（address 以外の列）
KEYS = {
    "functions": ["address"],
    "globals": ["address"],
    "comments": ["address", "kind"],
    "vtables": ["address"],
    "lvars": ["function", "location", "name"],
}
COMMENT_KINDS = ["func", "line", "repeatable"]
# 引き継ぐ列（既存の行から）
CARRY = {
    "functions": ["confidence", "source", "refs", "clone_of"],
    "globals": ["confidence", "source", "refs"],
}

# IDA が自動で付ける名前（利用者の名前ではない）
_AUTO_RE = re.compile(
    r"^(?:j_)*(?:sub|loc|locret|unk|dword|word|byte|qword|off|stru|asc|flt|dbl|tbyte|oword|xmmword|"
    r"nullsub|def|jpt|algn|BYTE|WORD|DWORD)_[0-9A-Fa-f]+(?:_\d+)?$"
)
_LOADER_NAMES = {"start"}

_REF_RE = re.compile(r"\[((?:ACNL|HHD|3DS)-[A-Z]?\d{3,5})\]")


# ---- アドレス ----

def fmt_addr(a: int) -> str:
    return "0x%08X" % a


def parse_addr(s: str) -> int:
    return int(s, 16) if s.lower().startswith("0x") else int(s)


def addr_key(s: str) -> int:
    try:
        return parse_addr(s)
    except (ValueError, AttributeError):
        return -1


# ---- 名前 ----

def is_auto_name(name: str) -> bool:
    """IDA の自動の名前（sub_・loc_・unk_・dword_ など）か。空も自動扱い。"""
    if not name:
        return True
    return bool(_AUTO_RE.match(name))


def is_loader_name(name: str) -> bool:
    return name in _LOADER_NAMES


def is_user_name(name: str) -> bool:
    return not is_auto_name(name) and not is_loader_name(name)


# ---- コメント ----

_AUTO_CMT_RE = re.compile(
    r"^(?:"
    r"(?:unsigned |signed |const )*(?:char|short|int|long|float|double|bool|__int8|__int16|__int32|__int64|"
    r"_BYTE|_WORD|_DWORD|_QWORD|_OWORD)(?: ?\*)*"
    r"|switch jump|jump table for switch statement|indirect table for switch statement"
    r"|switch \d+ cases?(?: default)?|default"
    r"|jumptable [0-9A-Fa-f]+ .*"
    r"|reference to RTTI's type class|type descriptor name|offset to this|base class' type descriptor"
    r"|base class' attributes|attribute|count of base classes|(?:reference|pointer) to RTTI.*"
    r"|reference to (?:type's name|parent's type name)"
    r")$"
)
# 呼び出しの引数名として IDA が入れる、識別子 1 語のコメント
ARG_COMMENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def is_auto_comment(text: str) -> bool:
    """IDA が自動で入れるコメント（型名・switch の説明など）か。"""
    lines = [l.strip() for l in (text or "").splitlines() if l.strip()]
    return bool(lines) and all(_AUTO_CMT_RE.match(l) for l in lines)


# ---- refs ----

def extract_refs(text: str) -> list[str]:
    """文章の中の `[ACNL-F0412]` 形式の ID を、出てきた順に重複なしで返す。"""
    out: list[str] = []
    for m in _REF_RE.finditer(text or ""):
        if m.group(1) not in out:
            out.append(m.group(1))
    return out


def join_refs(ids: list[str]) -> str:
    return ";".join(sorted(set(ids)))


# ---- CSV ----

def sort_rows(table: str, rows: list[dict]) -> list[dict]:
    def key(r: dict):
        k = []
        for c in KEYS[table]:
            v = r.get(c, "")
            if c in ("address", "function"):
                k.append(addr_key(v))
            elif c == "kind":
                k.append(COMMENT_KINDS.index(v) if v in COMMENT_KINDS else 99)
            else:
                k.append(v)
        return k

    return sorted(rows, key=key)


def dumps_csv(table: str, rows: list[dict]) -> str:
    cols = COLUMNS[table]
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writerow(cols)
    for r in sort_rows(table, rows):
        w.writerow([_norm(r.get(c, "")) for c in cols])
    return buf.getvalue()


def _norm(v) -> str:
    s = "" if v is None else str(v)
    return s.replace("\r\n", "\n").replace("\r", "\n")


def write_csv(path: Path, table: str, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(dumps_csv(table, rows))


def loads_csv(table: str, text: str) -> list[dict]:
    cols = COLUMNS[table]
    r = csv.DictReader(io.StringIO(text, newline=""))
    rows = []
    for row in r:
        rows.append({c: (row.get(c) or "") for c in cols})
    return rows


def read_csv(path: Path, table: str) -> list[dict]:
    if not Path(path).exists():
        return []
    with open(path, "r", encoding="utf-8", newline="") as f:
        return loads_csv(table, f.read())


def read_all(d: Path) -> dict[str, list[dict]]:
    return {t: read_csv(Path(d) / (t + ".csv"), t) for t in COLUMNS}


# ---- IDB の範囲 ----

def split_by_segments(table: str, rows: list[dict], segments: list[tuple[int, int]]) -> tuple[list[dict], list[dict]]:
    """行を IDB のセグメント内と外に分ける。範囲の終わりは含まない。"""
    column = "function" if table == "lvars" else "address"
    inside, outside = [], []
    for row in rows:
        ea = parse_addr(row[column])
        if table in ("functions", "lvars"):
            ea &= ~1  # CSV の Thumb フラグは IDB の番地には含まれない
        (inside if any(start <= ea < end for start, end in segments) else outside).append(row)
    return inside, outside


def retain_outside_segments(table: str, new_rows: list[dict], old_rows: list[dict],
                            segments: list[tuple[int, int]]) -> tuple[list[dict], int]:
    """IDB に無い番地の既存行を、IDB から書き出した行へ加える。"""
    _, outside = split_by_segments(table, old_rows, segments)
    return sort_rows(table, new_rows + outside), len(outside)


# ---- 引き継ぎ ----

def carry_over(table: str, new_rows: list[dict], old_rows: list[dict], default_source: str = "analysis") -> list[dict]:
    """`confidence`・`source`・`refs`（functions は clone_of も）を、同じアドレス・同じ名前の既存の行から引き継ぐ。

    引き継げない行（新しい行）は source = default_source、refs = コメント由来の物（呼び出し側が入れた値）のまま。
    """
    cols = CARRY.get(table)
    if not cols:
        return new_rows
    old = {(r["address"], r["name"]): r for r in old_rows}
    out = []
    for r in new_rows:
        r = dict(r)
        o = old.get((r["address"], r["name"]))
        if o:
            for c in cols:
                r[c] = o.get(c, "")
        else:
            r.setdefault("source", "")
            if not r.get("source"):
                r["source"] = default_source
        out.append(r)
    return out


# ---- 比較 ----

def _rkey(table: str, r: dict) -> tuple:
    return tuple(r.get(c, "") for c in KEYS[table])


def compare_tables(table: str, a: list[dict], b: list[dict], ignore: tuple[str, ...] = ()) -> dict:
    """a と b を主キーで突き合わせる。

    返り値: {"only_a": [...], "only_b": [...], "changed": {列: [(キー, a の値, b の値), ...]}, "same": 件数}
    """
    da = {_rkey(table, r): r for r in a}
    db = {_rkey(table, r): r for r in b}
    only_a = [da[k] for k in sorted(da.keys() - db.keys())]
    only_b = [db[k] for k in sorted(db.keys() - da.keys())]
    changed: dict[str, list] = {}
    same = 0
    for k in sorted(da.keys() & db.keys()):
        diff = False
        for c in COLUMNS[table]:
            if c in KEYS[table] or c in ignore:
                continue
            if da[k].get(c, "") != db[k].get(c, ""):
                changed.setdefault(c, []).append((k, da[k].get(c, ""), db[k].get(c, "")))
                diff = True
        if not diff:
            same += 1
    return {"only_a": only_a, "only_b": only_b, "changed": changed, "same": same}


def summarize_compare(res: dict, limit: int = 3) -> list[str]:
    lines = []
    lines.append("same=%d only_a=%d only_b=%d" % (res["same"], len(res["only_a"]), len(res["only_b"])))
    for c, v in res["changed"].items():
        lines.append("changed[%s]=%d" % (c, len(v)))
        for k, x, y in v[:limit]:
            lines.append("  %s: %r -> %r" % ("/".join(k), x[:80], y[:80]))
    for r in res["only_a"][:limit]:
        lines.append("  only_a: %s" % dict(r))
    for r in res["only_b"][:limit]:
        lines.append("  only_b: %s" % dict(r))
    return lines


def tables_equal(res: dict) -> bool:
    return not res["only_a"] and not res["only_b"] and not res["changed"]


# ---- 型ファイル ----

def split_type_blocks(text: str) -> list[tuple[str, str]]:
    """`// type: 名前` で始まるブロックに分ける。返り値は (名前, 本文) の列。"""
    blocks: list[tuple[str, str]] = []
    cur_name = None
    cur: list[str] = []
    for line in text.splitlines():
        if line.startswith("// type: "):
            if cur_name is not None:
                blocks.append((cur_name, "\n".join(cur).strip("\n")))
            cur_name = line[len("// type: "):].strip()
            cur = []
        elif cur_name is not None:
            cur.append(line)
    if cur_name is not None:
        blocks.append((cur_name, "\n".join(cur).strip("\n")))
    return blocks


def order_type_blocks(blocks: dict[str, str]) -> list[str]:
    """名前順を基本に、他の型の名前を本文で使う型は、使われる型の後に並べる（循環は名前順で切る）。"""
    ident = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
    deps = {n: {t for t in ident.findall(body) if t in blocks and t != n} for n, body in blocks.items()}
    order: list[str] = []
    state: dict[str, int] = {}

    def visit(n: str):
        if state.get(n):
            return
        state[n] = 1
        for d in sorted(deps[n]):
            visit(d)
        state[n] = 2
        order.append(n)

    for n in sorted(blocks):
        visit(n)
    return order


_BASE_WORDS = {"unsigned", "signed", "int", "char", "short", "long", "float", "double", "const", "volatile",
               "__int8", "__int16", "__int32", "__int64", "bool"}


def name_unnamed_members(block: str) -> str:
    """IDA は名前の無い構造体メンバーを `unsigned int;` と出力するが、これは C として解釈できない。
    基本型だけの行に `__unnamed_<通し番号>` を補う（ブロックの中での出現順）。"""
    out = []
    n = 0
    for line in block.split("\n"):
        m = re.match(r"^(\s+)([A-Za-z_][A-Za-z0-9_ ]*?)\s*;$", line)
        if m and set(m.group(2).split()) <= _BASE_WORDS:
            n += 1
            line = "%s%s __unnamed_%d;" % (m.group(1), m.group(2), n)
        out.append(line)
    return "\n".join(out)


# ---- meta ----

def dumps_meta(data: dict) -> str:
    lines = []
    for k, v in data.items():
        if isinstance(v, dict):
            continue
        lines.append("%s = %s" % (k, _toml_val(v)))
    for k, v in data.items():
        if isinstance(v, dict):
            lines.append("")
            lines.append("[%s]" % k)
            for k2, v2 in v.items():
                lines.append("%s = %s" % (k2, _toml_val(v2)))
    return "\n".join(lines) + "\n"


def _toml_val(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    s = str(v).replace("\\", "\\\\").replace('"', '\\"')
    return '"%s"' % s
