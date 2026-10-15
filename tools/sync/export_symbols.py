#!/usr/bin/env python3
"""IDB から symbols/<ビルド>/ へ書き出す（利用者が付けた物だけ）。idalib の python で実行する。

対象: 関数の名前・プロトタイプ（利用者が設定した物だけ）・大きさ、大域の名前と型、vtable（`vtbl_` で始まる名前）、
関数・行・繰り返しのコメント、利用者が変えたローカル変数、ローカルの型。
IDA の自動の名前（sub_・loc_・unk_・dword_ ...）とローダーが付けた名前（start）は書かない。

Thumb の関数は、アドレスの最下位ビットを 1 にして書く（ARM の慣習: 0x00123457）。
"""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import idacommon as ic  # noqa: E402
import symlib as sl  # noqa: E402

# 新しい IDB が最初から持っている型（ARM の NEON など）。利用者の型ではないので書かない。
BUILTIN_TYPES = frozenset()  # create_idb 後に builtin_types.txt から読む
VTABLE_PREFIX = "vtbl_"
MAX_VTABLE_SLOTS = 1024


def _builtin_types() -> frozenset:
    p = Path(__file__).resolve().parent / "builtin_types.txt"
    if p.exists():
        return frozenset(l.strip() for l in p.read_text(encoding="utf-8").splitlines() if l.strip())
    return frozenset()


# ---- 型の文字列 ----

def tinfo_text(tif) -> str:
    import ida_typeinf

    if tif is None or tif.empty():
        return ""
    s = tif._print(None, ida_typeinf.PRTYPE_1LINE)
    return s or ""


def user_tinfo(ea: int):
    """利用者が設定した型（無ければ None）。"""
    import ida_nalt
    import ida_typeinf

    if not ida_nalt.is_userti(ea):
        return None
    tif = ida_typeinf.tinfo_t()
    if not ida_nalt.get_tinfo(tif, ea):
        return None
    return tif


def user_type(ea: int) -> str:
    return tinfo_text(user_tinfo(ea))


def thumb_at(ea: int) -> bool:
    import ida_idp
    import ida_segregs

    return ida_segregs.get_sreg(ea, ida_idp.str2reg("T")) == 1


# ---- 各表 ----

def export_functions(comment_refs: dict[int, list[str]], commented: set[int]) -> list[dict]:
    import ida_bytes
    import ida_funcs
    import ida_name
    import idautils

    rows = []
    for ea in idautils.Functions():
        f = ida_funcs.get_func(ea)
        name = ida_name.get_name(ea)
        fl = ida_bytes.get_flags(ea)
        uname = name if (ida_bytes.has_user_name(fl) and sl.is_user_name(name)) else ""
        proto = user_type(ea)
        if not uname and not proto and ea not in commented:
            continue
        addr = ea | 1 if thumb_at(ea) else ea
        rows.append({"address": sl.fmt_addr(addr), "size": str(f.end_ea - f.start_ea), "name": uname,
                     "prototype": proto, "confidence": "", "source": "", "refs": sl.join_refs(comment_refs.get(ea, [])),
                     "clone_of": ""})
    return rows


def _func_start(ea: int) -> bool:
    import ida_funcs

    f = ida_funcs.get_func(ea)
    return f is not None and f.start_ea == ea


def export_globals(vtbl_addrs: set[int], comment_refs: dict[int, list[str]]) -> list[dict]:
    import ida_bytes
    import ida_name
    import idautils

    rows = []
    for ea, name in idautils.Names():
        if ea in vtbl_addrs or _func_start(ea):
            continue
        fl = ida_bytes.get_flags(ea)
        uname = name if (ida_bytes.has_user_name(fl) and sl.is_user_name(name)) else ""
        tif = user_tinfo(ea)
        typ = tinfo_text(tif)
        if not uname and not typ:
            continue
        size = tif.get_size() if typ else 0
        if not size or size == 0xFFFFFFFF:
            size = ida_bytes.get_item_size(ea)
        rows.append({"address": sl.fmt_addr(ea), "size": str(size), "name": uname, "type": typ,
                     "confidence": "", "source": "", "refs": sl.join_refs(comment_refs.get(ea, []))})
    return rows


def export_vtables() -> list[dict]:
    import ida_bytes
    import ida_name
    import ida_segment
    import idautils

    names = [(ea, n) for ea, n in idautils.Names() if n.startswith(VTABLE_PREFIX)]
    named = {ea for ea, n in idautils.Names() if ida_bytes.has_user_name(ida_bytes.get_flags(ea))}
    text = None
    rows = []
    for ea, n in names:
        seg = ida_segment.getseg(ea)
        count = 0
        a = ea
        while count < MAX_VTABLE_SLOTS and seg is not None and a + 4 <= seg.end_ea:
            if count > 0 and a in named:
                break
            v = ida_bytes.get_dword(a)
            s = ida_segment.getseg(v & ~1)
            if s is None or not (s.perm & ida_segment.SEGPERM_EXEC):
                break
            count += 1
            a += 4
        rows.append({"address": sl.fmt_addr(ea), "class": n[len(VTABLE_PREFIX):], "count": str(count)})
    return rows


def is_arg_comment(ea: int, text: str) -> bool:
    """呼び出し直前の命令に付く、識別子 1 語のコメントで、直後の呼び出し先の引数名と一致する物。

    IDA が関数の型から自動で入れる引数名のコメントで、利用者のコメントではない。
    """
    import ida_funcs
    import ida_idp
    import ida_nalt
    import ida_typeinf
    import ida_ua
    import ida_xref
    import idautils

    if not sl.ARG_COMMENT_RE.match(text):
        return False
    cur = ea
    for _ in range(40):
        insn = ida_ua.insn_t()
        if not ida_ua.decode_insn(insn, cur):
            return False
        is_call = ida_idp.is_call_insn(insn)
        for x in idautils.XrefsFrom(cur, ida_xref.XREF_FAR):
            # 呼び出し、または別の関数の先頭への分岐（末尾呼び出し）
            if x.type in (ida_xref.fl_CN, ida_xref.fl_CF) and is_call or (
                    x.type in (ida_xref.fl_JN, ida_xref.fl_JF) and _func_start(x.to)
                    and ida_funcs.get_func(cur) is not None and ida_funcs.get_func(cur).start_ea != x.to):
                t = ida_typeinf.tinfo_t()
                if ida_nalt.get_tinfo(t, x.to) or ida_typeinf.guess_tinfo(t, x.to) == ida_typeinf.GUESS_FUNC_OK:
                    fd = ida_typeinf.func_type_data_t()
                    if t.get_func_details(fd) and text in [a.name for a in fd]:
                        return True
                return False
        if is_call:
            return False
        cur = insn.ea + insn.size
    return False


def export_comments() -> tuple[list[dict], dict[int, list[str]], set[int]]:
    import ida_bytes
    import ida_funcs
    import ida_segment
    import idc

    rows = []
    refs: dict[int, list[str]] = {}

    def add(ea: int, kind: str, text: str):
        if sl.is_auto_comment(text):
            return
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        rows.append({"address": sl.fmt_addr(ea), "kind": kind, "text": text})
        for r in sl.extract_refs(text):
            lst = refs.setdefault(ea, [])
            if r not in lst:
                lst.append(r)

    seen_rpt_func = set()
    func_level: set[int] = set()
    for i in range(ida_segment.get_segm_qty()):
        seg = ida_segment.getnseg(i)
        ea = seg.start_ea
        while ea != idc.BADADDR and ea < seg.end_ea:
            fl = ida_bytes.get_flags(ea)
            if ida_bytes.has_cmt(fl):
                c = ida_bytes.get_cmt(ea, False)
                if c and not is_arg_comment(ea, c):
                    add(ea, "line", c)
                r = ida_bytes.get_cmt(ea, True)
                if r:
                    add(ea, "repeatable", r)
                    seen_rpt_func.add(ea)
            ea = ida_bytes.next_head(ea, seg.end_ea)
    import idautils

    for ea in idautils.Functions():
        f = ida_funcs.get_func(ea)
        c = ida_funcs.get_func_cmt(f, False)
        if c:
            add(ea, "func", c)
            func_level.add(ea)
        r = ida_funcs.get_func_cmt(f, True)
        if r:
            func_level.add(ea)
            if ea not in seen_rpt_func:
                add(ea, "repeatable", r)
    return rows, refs, func_level


def lvar_location(ll) -> str:
    loc = ll.location
    if loc.is_stkoff():
        s = "stk:%d" % loc.stkoff()
    elif loc.is_reg1():
        s = "reg:%d" % loc.reg1()
    elif loc.is_reg2():
        s = "reg2:%d:%d" % (loc.reg1(), loc.reg2())
    else:
        s = "loc:%s" % loc.dstr()
    return "%s@%s" % (s, sl.fmt_addr(ll.defea))


def export_lvars() -> list[dict]:
    import ida_hexrays
    import idautils

    rows = []
    ida_hexrays.init_hexrays_plugin()
    for ea in idautils.Functions():
        lv = ida_hexrays.lvar_uservec_t()
        if not ida_hexrays.restore_user_lvar_settings(lv, ea):
            continue
        fa = sl.fmt_addr(ea | 1 if thumb_at(ea) else ea)
        for l in lv.lvvec:
            name = l.name or ""
            typ = tinfo_text(l.type)
            if not name and not typ:
                continue
            rows.append({"function": fa, "name": name, "type": typ, "location": lvar_location(l.ll)})
    return rows


def export_types() -> str:
    """ローカルの型を C 宣言にする。決定的にするため、名前順（依存する型を先）に並べ、通し番号は書かない。"""
    import ida_typeinf
    import re

    til = ida_typeinf.get_idati()
    builtin = _builtin_types()
    ords = {}
    kinds = {}
    for o in range(1, ida_typeinf.get_ordinal_limit()):
        n = ida_typeinf.get_numbered_type_name(til, o)
        if not n or n in builtin or "$" in n:  # `$` を含む名前は無名の入れ子の型（親の宣言に含まれる）
            continue
        t = ida_typeinf.tinfo_t()
        if not t.get_numbered_type(til, o):
            continue
        ords[n] = o
        kinds[n] = "struct" if t.is_struct() else "union" if t.is_union() else "enum" if t.is_enum() else "typedef"
    if not ords:
        return ""

    class Sink(ida_typeinf.text_sink_t):
        def __init__(self):
            super().__init__()
            self.buf = []

        def _print(self, text):
            self.buf.append(text)
            return 0

    sink = Sink()
    flags = ida_typeinf.PDF_INCL_DEPS
    ida_typeinf.print_decls(sink, til, sorted(ords.values()), flags)
    text = "".join(sink.buf)
    num2name = {o: n for n, o in ords.items()}
    blocks: dict[str, str] = {}
    cur = None
    lines: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^/\* (\d+) \*/$", line)
        if m:
            if cur is not None:
                blocks[cur] = "\n".join(lines).strip("\n")
            cur = num2name.get(int(m.group(1)))
            lines = []
        elif cur is not None or line.strip():
            lines.append(line)
    if cur is not None:
        blocks[cur] = "\n".join(lines).strip("\n")
    # 依存で出てきた組み込み型のブロックは捨てる
    blocks = {n: sl.name_unnamed_members(b) for n, b in blocks.items() if n in ords}
    out = ["// ローカルの型（IDA の print_decls の出力を、名前順・依存順に並べた物）", ""]
    fwd = [n for n in sorted(blocks) if kinds[n] in ("struct", "union")]
    for n in fwd:
        out.append("%s %s;" % (kinds[n], n))
    out.append("")
    for n in sl.order_type_blocks(blocks):
        out.append("// type: %s" % n)
        out.append(blocks[n])
        out.append("")
    return "\n".join(out)


# ---- 本体 ----

def export_all(build: str, outdir: Path, source: str = "analysis", console: bool = False) -> dict:
    import ida_nalt
    import ida_segment

    outdir = Path(outdir)
    old = sl.read_all(outdir)
    comments, refs, commented = export_comments()
    vtables = export_vtables()
    vaddrs = {sl.parse_addr(r["address"]) for r in vtables}
    funcs = export_functions(refs, commented)
    globs = export_globals(vaddrs, refs)
    lvars = export_lvars()
    for r in funcs:
        r["source"] = ""
    funcs = sl.carry_over("functions", funcs, old["functions"], source)
    globs = sl.carry_over("globals", globs, old["globals"], source)
    types_text = export_types()

    tables = {"functions": funcs, "globals": globs, "comments": comments, "vtables": vtables, "lvars": lvars}
    segments = [(ida_segment.getnseg(i).start_ea, ida_segment.getnseg(i).end_ea)
                for i in range(ida_segment.get_segm_qty())]
    retained = 0
    for t, rows in tables.items():
        tables[t], count = sl.retain_outside_segments(t, rows, old[t], segments)
        retained += count
    for t, rows in tables.items():
        sl.write_csv(outdir / (t + ".csv"), t, rows)
    tdir = outdir / "types"
    if types_text:
        tdir.mkdir(parents=True, exist_ok=True)
        (tdir / "local_types.h").write_text(types_text, encoding="utf-8", newline="\n")
    elif (tdir / "local_types.h").exists():
        (tdir / "local_types.h").unlink()
    info = ic.load_builds().get(build, {})
    idb_sha = ida_nalt.retrieve_input_file_sha256()
    idb_sha = idb_sha.hex() if idb_sha else ""
    meta = {
        "build": build,
        "source": source,
        "idb_input_sha256": idb_sha,
        "code_sha256": info.get("code_sha256", ""),
        "idb_input_is_code_bin": idb_sha == info.get("code_sha256", "?"),
        "ida_version": ic.ida_version(),
        "tool_version": sl.TOOL_VERSION,
        "exported_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "counts": {t: len(r) for t, r in tables.items()} | {"types": types_text.count("// type: ")},
    }
    (outdir / "meta.toml").write_text(sl.dumps_meta(meta), encoding="utf-8", newline="\n")
    return meta["counts"] | {"retained": retained, "build": build}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--idb", required=True, help="書き出し元の .i64（保存しない。旧 IDB は写しを渡す）")
    ap.add_argument("--build", required=True, help="builds.toml のビルド名")
    ap.add_argument("--out", required=True, help="書き出し先 symbols/<ビルド>")
    ap.add_argument("--source", default="analysis", help="新しい行の source（既定 analysis。旧 IDB なら legacy-idb）")
    a = ap.parse_args(argv)
    with ic.OpenDb(a.idb, save=False) as _:
        counts = export_all(a.build, Path(a.out), a.source)
    print("書き出し:", ", ".join("%s=%s" % kv for kv in counts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
