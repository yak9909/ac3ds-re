#!/usr/bin/env python3
"""symbols/<ビルド>/ を IDB へ取り込む。idalib の python で実行する。

順番: 型 → 関数（作成・名前・プロトタイプ）→ 大域（名前・型）→ vtable → コメント → ローカル変数。
失敗した物は件数と例を表示し、全部の結果を --report の JSON に書く。最後に保存して閉じる。
Thumb の関数はアドレスの最下位ビットが 1（0x00123457）。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import idacommon as ic  # noqa: E402
import symlib as sl  # noqa: E402


class Report:
    def __init__(self):
        self.sections: dict[str, dict] = {}

    def sec(self, name: str) -> dict:
        return self.sections.setdefault(name, {"total": 0, "ok": 0, "skipped": 0, "failed": []})

    def ok(self, name: str, n: int = 1):
        s = self.sec(name)
        s["total"] += n
        s["ok"] += n

    def fail(self, name: str, key: str, reason: str):
        s = self.sec(name)
        s["total"] += 1
        s["failed"].append({"key": key, "reason": reason})

    def skip(self, name: str, n: int):
        s = self.sec(name)
        s["total"] += n
        s["skipped"] += n

    def print(self, examples: int = 3):
        for name, s in self.sections.items():
            print("%-10s 全部 %6d  成功 %6d  対象外 %6d  失敗 %5d" %
                  (name, s["total"], s["ok"], s["skipped"], len(s["failed"])))
            for f in s["failed"][:examples]:
                print("    失敗例: %s: %s" % (f["key"], f["reason"]))

    def dump(self) -> dict:
        return self.sections


# ---- 型の解釈 ----

def parse_type(text: str):
    """型の文字列（`int __fastcall(int a)`・`const float[3]` など）を tinfo にする。失敗は None。"""
    import ida_typeinf as T

    til = T.get_idati()
    cands = [text.strip() + ";"]
    # 名前の無い関数型は、最初の '(' の前に仮の名前を入れて解釈する
    i = text.find("(")
    if i > 0:
        cands.append(text[:i].rstrip() + " __f" + text[i:] + ";")
    for c in cands:
        t = T.tinfo_t()
        if T.parse_decl(t, til, c, T.PT_SIL | T.PT_TYP) is not None and not t.empty():
            return t
    return None


# ---- 型の取り込み ----

def import_types(symdir: Path, rep: Report):
    import ida_typeinf as T

    til = T.get_idati()
    flags = T.HTI_DCL | T.HTI_PAKDEF if hasattr(T, "HTI_PAKDEF") else T.HTI_DCL
    blocks = {}
    for h in sorted((symdir / "types").glob("*.h")) if (symdir / "types").is_dir() else []:
        text = h.read_text(encoding="utf-8")
        head = text.split("// type: ", 1)[0]
        fwd = [l for l in head.splitlines() if l.strip() and not l.startswith("//")]
        if fwd:
            T.parse_decls(til, "\n".join(fwd) + "\n", None, flags)
        blocks.update(sl.split_type_blocks(text))
    for name in sl.order_type_blocks(blocks):
        errs = T.parse_decls(til, blocks[name] + "\n", None, flags)
        if errs:
            rep.fail("types", name, "C 宣言の解釈で %d 件の誤り" % errs)
        else:
            rep.ok("types")


# ---- 関数 ----

def _set_name(ea: int, name: str) -> str | None:
    import ida_name

    if ida_name.get_name(ea) == name:
        return None
    ok = ida_name.set_name(ea, name, ida_name.SN_NOCHECK | ida_name.SN_NOWARN | ida_name.SN_NON_AUTO)
    if not ok:
        return "名前を付けられない（重複か不正）"
    return None


SOFT = "\x00"  # 先頭にあれば、名前・プロトタイプは続けて付ける失敗


def _ensure_function(ea: int, size: int, thumb: bool) -> str | None:
    import ida_bytes
    import ida_funcs
    import ida_idp
    import ida_segregs
    import ida_ua

    want = 1 if thumb else 0
    treg = ida_idp.str2reg("T")
    end = ea + size if size > 0 else 0xFFFFFFFF
    cmts = None
    # get_func() はテールの所有者を返すため、チャンクを調べて全所有者から外す。
    pos = ea
    while pos < (end if size > 0 else ea + 1):
        chunk = ida_funcs.get_fchunk(pos)
        if chunk is None:
            nxt = ida_funcs.get_next_fchunk(pos)
            if nxt is None or size <= 0 or nxt.start_ea >= end:
                break
            pos = nxt.start_ea
            continue
        start, stop = chunk.start_ea, chunk.end_ea
        if chunk.flags & ida_funcs.FUNC_TAIL:
            parents = list(ida_funcs.func_parent_iterator_t(chunk))
            for parent in parents:
                if not ida_funcs.remove_func_tail(ida_funcs.get_func(parent), start):
                    return "共有テール 0x%X を外せない" % start
            if start < ea:
                for parent in parents:
                    if not ida_funcs.append_func_tail(ida_funcs.get_func(parent), start, ea):
                        return "テールの前半 0x%X を残せない" % start
        elif start < ea:
            if not ida_funcs.set_func_end(start, ea):
                return "別の関数 0x%X を手前で終わらせられない" % start
        elif start != ea:
            if not ida_funcs.del_func(start):
                return "重複する関数 0x%X を除けない" % start
        pos = stop
    f = ida_funcs.get_func(ea)
    if f is not None and f.start_ea != ea:
        # 自動解析が作った関数の途中から始まる関数: 手前の関数を ea で切る
        if not ida_funcs.set_func_end(f.start_ea, ea):
            return "別の関数 0x%X の途中（切れない）" % f.start_ea
        f = ida_funcs.get_func(ea)
    if f is not None and ida_segregs.get_sreg(ea, treg) != want:
        # 自動解析が違う命令セット（ARM/Thumb）で作った関数: 消して作り直す
        ida_funcs.del_func(ea)
        ida_bytes.del_items(ea, ida_bytes.DELIT_SIMPLE, max(size, 2))
        f = None
    if f is not None:
        if size > 0 and f.end_ea != ea + size:
            if not ida_funcs.set_func_end(ea, ea + size):
                # 間違った命令長などで境界が項目の途中にある場合は再作成する。
                cmts = [ida_funcs.get_func_cmt(f, repeat) for repeat in (False, True)]
                ida_funcs.del_func(ea)
                ida_bytes.del_items(ea, ida_bytes.DELIT_SIMPLE, size)
                f = None
            else:
                return None
        else:
            return None
    if ida_segregs.get_sreg(ea, treg) != want:
        prev_end = ida_segregs.get_sreg(end, treg) if size > 0 else None
        ida_segregs.split_sreg_range(ea, treg, want, ida_segregs.SR_user)
        if prev_end is not None and ida_segregs.get_sreg(end, treg) != prev_end:
            ida_segregs.split_sreg_range(end, treg, prev_end, ida_segregs.SR_user)
    if not ida_funcs.add_func(ea, end):
        ida_bytes.del_items(ea, ida_bytes.DELIT_SIMPLE, max(size, 2))
        ida_ua.create_insn(ea)
        if not ida_funcs.add_func(ea, end):
            return "関数を作れない"
    f = ida_funcs.get_func(ea)
    if cmts is not None:
        for repeat, cmt in zip((False, True), cmts):
            if cmt:
                ida_funcs.set_func_cmt(f, cmt, repeat)
    if size > 0 and f.end_ea != end:
        if not ida_funcs.set_func_end(ea, end):
            return SOFT + "関数の終わりを 0x%X にできない（今は 0x%X）" % (end, f.end_ea)
    return None


def _import_function_row(r: dict) -> tuple[str, str] | None:
    """1 行を取り込む。失敗なら (キー, 理由)。"""
    import ida_typeinf as T

    key = r["address"]
    a = sl.parse_addr(r["address"])
    ea, thumb = a & ~1, bool(a & 1)
    soft = None
    err = _ensure_function(ea, int(r["size"] or 0), thumb)
    if err and err.startswith(SOFT):
        soft, err = (key, err[len(SOFT):]), None
    if err:
        return key, err
    if r["name"]:
        err = _set_name(ea, r["name"])
        if err:
            return key + " " + r["name"], err
    if r["prototype"]:
        t = parse_type(r["prototype"])
        if t is None:
            return key + " " + r["name"], "プロトタイプを解釈できない: " + r["prototype"][:100]
        if not T.apply_tinfo(ea, t, T.TINFO_DEFINITE):
            return key + " " + r["name"], "プロトタイプを適用できない: " + r["prototype"][:100]
    return soft


def import_functions(rows: list[dict], rep: Report):
    """2 回通す。自動解析（auto_wait）が、呼び出し先の ARM/Thumb を後から書き換えることがあるため、
    1 回目の後に解析を待ち、2 回目で直す（2 回目の結果を採る）。"""
    import ida_auto

    for r in rows:
        _import_function_row(r)
    ida_auto.auto_wait()
    for r in rows:
        res = _import_function_row(r)
        if res:
            rep.fail("functions", *res)
        else:
            rep.ok("functions")


# ---- 大域 ----

def _define_data(ea: int, size: int) -> str | None:
    """型の無い名前の大きさを合わせる（1/2/4/8 バイトは単独のデータ、他はバイト列）。コードの上では何もしない。"""
    import ida_bytes

    fl = ida_bytes.get_flags(ea)
    if ida_bytes.is_code(fl) or ida_bytes.get_item_size(ea) == size and ida_bytes.is_data(fl):
        return None
    flag = {2: ida_bytes.FF_WORD, 4: ida_bytes.FF_DWORD, 8: ida_bytes.FF_QWORD}.get(size)
    ida_bytes.del_items(ea, ida_bytes.DELIT_SIMPLE, size)
    if flag is not None:
        ok = ida_bytes.create_data(ea, flag, size, 0xFFFFFFFF)
    else:
        ok = ida_bytes.create_data(ea, ida_bytes.FF_BYTE, size, 0xFFFFFFFF)
    return None if ok else "大きさ %d のデータを作れない" % size


def import_globals(rows: list[dict], rep: Report):
    import ida_typeinf as T

    for r in rows:
        key = r["address"]
        ea = sl.parse_addr(r["address"])
        _make_head(ea)
        if r["name"]:
            err = _set_name(ea, r["name"])
            if err:
                rep.fail("globals", key + " " + r["name"], err)
                continue
        if r["type"]:
            t = parse_type(r["type"])
            if t is None:
                rep.fail("globals", key + " " + r["name"], "型を解釈できない: " + r["type"][:100])
                continue
            if not T.apply_tinfo(ea, t, T.TINFO_DEFINITE):
                rep.fail("globals", key + " " + r["name"], "型を適用できない: " + r["type"][:100])
                continue
        elif int(r["size"] or 0) >= 1:
            err = _define_data(ea, int(r["size"]))
            if err:
                rep.fail("globals", key + " " + r["name"], err)
                continue
        rep.ok("globals")


# ---- vtable ----

def import_vtables(rows: list[dict], rep: Report):
    import ida_bytes
    import ida_nalt
    import ida_offset
    import ida_segment
    import ida_typeinf

    for r in rows:
        ea = sl.parse_addr(r["address"])
        name = "vtbl_" + r["class"]
        err = _set_name(ea, name)
        if err:
            rep.fail("vtables", r["address"] + " " + name, err)
            continue
        n = int(r["count"] or 0)
        # globals から復元した vtable 構造体を dword に分解しない。
        tif = ida_typeinf.tinfo_t()
        if ida_nalt.is_userti(ea) and ida_nalt.get_tinfo(tif, ea) and tif.is_struct():
            if n and tif.get_size() != n * 4:
                rep.fail("vtables", r["address"], "構造体型のサイズが slot 数と一致しない")
            else:
                rep.ok("vtables")
            continue
        bad = None
        for i in range(n):
            a = ea + 4 * i
            if not ida_bytes.is_dword(ida_bytes.get_flags(a)):
                if not ida_bytes.create_dword(a, 4, True):
                    bad = "スロット %d (0x%X) を dword にできない" % (i, a)
                    break
            if ida_segment.getseg(ida_bytes.get_dword(a) & ~1) is not None and not ida_bytes.is_off(ida_bytes.get_flags(a), 0):
                ida_offset.op_offset(a, 0, ida_nalt.REF_OFF32)
        if bad:
            rep.fail("vtables", r["address"] + " " + name, bad)
        else:
            rep.ok("vtables")


# ---- コメント ----

def _make_head(ea: int):
    """名前・コメントを付ける場所を、項目の先頭にする（大きな項目の途中なら項目を壊す）。
    実行できる場所なら命令、そうでなければバイトにする。"""
    import ida_bytes
    import ida_segment
    import ida_ua

    fl = ida_bytes.get_flags(ea)
    if ida_bytes.is_head(fl):
        return
    seg = ida_segment.getseg(ea)
    if seg is None:
        return
    if ida_bytes.is_tail(fl):
        ida_bytes.del_items(ea, ida_bytes.DELIT_SIMPLE, 1)
    if seg.perm & ida_segment.SEGPERM_EXEC:
        ida_ua.create_insn(ea)
    elif ida_bytes.is_unknown(ida_bytes.get_flags(ea)):
        ida_bytes.create_byte(ea, 1, True)


def import_comments(rows: list[dict], rep: Report):
    import ida_bytes
    import ida_funcs

    for r in rows:
        ea = sl.parse_addr(r["address"])
        key = "%s %s" % (r["address"], r["kind"])
        if r["kind"] == "func":
            f = ida_funcs.get_func(ea)
            if f is None:
                rep.fail("comments", key, "関数が無い")
            elif ida_funcs.set_func_cmt(f, r["text"], False):
                rep.ok("comments")
            else:
                rep.fail("comments", key, "関数のコメントを付けられない")
        elif r["kind"] == "repeatable" and ida_funcs.get_func(ea) is not None and ida_funcs.get_func(ea).start_ea == ea:
            # 関数の先頭の繰り返しコメントは、関数の繰り返しコメントとして付ける
            if ida_funcs.set_func_cmt(ida_funcs.get_func(ea), r["text"], True):
                rep.ok("comments")
            else:
                rep.fail("comments", key, "関数の繰り返しコメントを付けられない")
        elif r["kind"] in ("line", "repeatable"):
            _make_head(ea)
            if ida_bytes.set_cmt(ea, r["text"], r["kind"] == "repeatable"):
                rep.ok("comments")
            else:
                rep.fail("comments", key, "コメントを付けられない")
        else:
            rep.fail("comments", key, "未知の kind: " + r["kind"])


# ---- ローカル変数 ----

def _parse_location(s: str):
    """`stk:-20@0x00123456` / `reg:3@0x...` → (種類, 値, defea)"""
    loc, _, d = s.partition("@")
    kind, _, val = loc.partition(":")
    return kind, val, sl.parse_addr(d) if d else 0


def import_lvars(rows: list[dict], rep: Report):
    import ida_funcs
    import ida_hexrays

    ida_hexrays.init_hexrays_plugin()
    by_func: dict[int, list[dict]] = {}
    for r in rows:
        by_func.setdefault(sl.parse_addr(r["function"]) & ~1, []).append(r)
    for fea, lst in sorted(by_func.items()):
        if ida_funcs.get_func(fea) is None:
            for r in lst:
                rep.fail("lvars", r["function"] + " " + r["name"], "関数が無い")
            continue
        lv = ida_hexrays.lvar_uservec_t()
        ida_hexrays.restore_user_lvar_settings(lv, fea)
        for r in lst:
            key = "%s %s" % (r["function"], r["location"])
            kind, val, defea = _parse_location(r["location"])
            vd = ida_hexrays.vdloc_t()
            if kind == "stk":
                vd.set_stkoff(int(val))
            elif kind == "reg":
                vd.set_reg1(int(val))
            else:
                rep.fail("lvars", key, "未対応の場所: " + r["location"])
                continue
            ll = ida_hexrays.lvar_locator_t(vd, defea)
            target = None
            for e in lv.lvvec:
                if e.ll == ll:
                    target = e
                    break
            if target is None:
                target = ida_hexrays.lvar_saved_info_t()
                target.ll = ll
                lv.lvvec.push_back(target)
                target = lv.lvvec.back()
            if r["name"]:
                target.name = r["name"]
            if r["type"]:
                t = parse_type(r["type"])
                if t is None:
                    rep.fail("lvars", key, "型を解釈できない: " + r["type"][:100])
                    continue
                target.type = t
            rep.ok("lvars")
        ida_hexrays.save_user_lvar_settings(fea, lv)


# ---- 本体 ----

def import_all(symdir: Path, report: Path | None = None) -> Report:
    import ida_auto
    import ida_segment

    t = sl.read_all(symdir)
    rep = Report()
    segments = [(ida_segment.getnseg(i).start_ea, ida_segment.getnseg(i).end_ea)
                for i in range(ida_segment.get_segm_qty())]
    for table, rows in t.items():
        t[table], outside = sl.split_by_segments(table, rows, segments)
        rep.skip(table, len(outside))
    t0 = time.time()
    import_types(symdir, rep)
    import_functions(t["functions"], rep)
    ida_auto.auto_wait()
    import_globals(t["globals"], rep)
    import_vtables(t["vtables"], rep)
    ida_auto.auto_wait()
    import_comments(t["comments"], rep)
    import_lvars(t["lvars"], rep)
    ida_auto.auto_wait()
    rep.sections["_meta"] = {"seconds": round(time.time() - t0, 1)}
    if report:
        Path(report).parent.mkdir(parents=True, exist_ok=True)
        Path(report).write_text(json.dumps(rep.dump(), ensure_ascii=False, indent=1), encoding="utf-8")
    return rep


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--idb", required=True, help="取り込み先の .i64（保存して閉じる）")
    ap.add_argument("--symbols", required=True, help="symbols/<ビルド>")
    ap.add_argument("--report", help="全部の結果を書く JSON")
    a = ap.parse_args(argv)
    with ic.OpenDb(a.idb, save=True) as _:
        rep = import_all(Path(a.symbols), Path(a.report) if a.report else None)
    rep.sections.pop("_meta", None)
    rep.print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
