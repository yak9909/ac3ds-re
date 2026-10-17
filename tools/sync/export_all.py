#!/usr/bin/env python3
"""IDB の読むための書き出し（idalib Python）。IDB は保存しない。

--build BUILD --idb COPY.i64 --symbols-commit COMMIT [--out DIR]
--only NAME_OR_ADDRESS を繰り返すと、その関数と直接の呼び出し元だけ更新する。
索引の symbols_commit は行ごとの生成時点。部分更新では他の行の古さを残す。
正本のロック・写しの作成は呼び出し元 orch.py の責任。
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import idacommon as ic
import symlib as sl

NOTE = "生成物。編集しない（orch.py export が作り直す）"
FIELDS = ["name", "address", "file", "decompile", "symbols_commit"]


def function_path(ea: int, name: str) -> str:
    safe = re.sub(r'[^\w.-]', '_', name)[:100].rstrip('. ')
    return f"functions/{ea // sl.RANGE_SIZE * sl.RANGE_SIZE:08X}/{ea:08X}_{safe or 'unnamed'}.txt"


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(NOTE + "\n" + text.rstrip() + "\n", encoding="utf-8", newline="\n")


def index_text(rows: list[dict], sha: str, commit: str, partial: bool) -> str:
    buf = io.StringIO(newline="")
    buf.write(f"idb_input_sha256: {sha}\nsymbols_commit: {commit}\n")
    buf.write(f"mode: {'partial; see per-function symbols_commit' if partial else 'full'}\n")
    writer = csv.DictWriter(buf, FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(sorted(rows, key=lambda r: int(r['address'], 16)))
    return buf.getvalue()


def read_index(path: Path) -> tuple[str, list[dict]]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if len(lines) < 5 or lines[0].strip() != NOTE:
        raise ValueError("既存の索引の形式が違う")
    return lines[1].strip().removeprefix("idb_input_sha256: "), list(csv.DictReader(lines[4:], delimiter="\t"))


def clean_comment(text: str | None) -> str:
    return text if text and not sl.is_auto_comment(text) else ""


def split_comment(line: str, marker: str) -> tuple[str, str]:
    """引用符の外にあるコメントだけ分ける（文字列内の ; や // を保つ）。"""
    quote = ""
    escaped = False
    for i, char in enumerate(line):
        if escaped:
            escaped = False
        elif quote and char == "\\":
            escaped = True
        elif quote:
            if char == quote:
                quote = ""
        elif char in ('"', "'"):
            quote = char
        elif line.startswith(marker, i):
            return line[:i].rstrip(), line[i + len(marker):].strip()
    return line, ""


def clean_pseudocode(line: str) -> str:
    code, comment = split_comment(line, "//")
    return code if sl.is_auto_comment(comment) else line


class IdaReader:
    def __init__(self):
        self.hexrays = None
        self.can_decompile = False
        self.decompiler_error = "Hex-Rays unavailable"
        try:
            import ida_hexrays
            self.hexrays = ida_hexrays
            self.can_decompile = ida_hexrays.init_hexrays_plugin()
        except Exception as exc:
            self.decompiler_error += ": " + " ".join(str(exc).split())

    def name(self, ea):
        import ida_name
        return ida_name.get_name(ea) or ""

    def reference(self, ea):
        return f"{sl.fmt_addr(ea)} {self.name(ea)}"

    def comments(self, ea):
        import ida_bytes
        from export_symbols import is_arg_comment
        result = []
        for rep in (False, True):
            c = clean_comment(ida_bytes.get_cmt(ea, rep))
            if c and (rep or not is_arg_comment(ea, c)):
                result.append(c)
        return result

    def data(self, ea):
        import ida_bytes
        import ida_nalt
        import ida_typeinf
        tif = ida_typeinf.tinfo_t()
        typ = str(tif) if ida_nalt.get_tinfo(tif, ea) else ""
        if not typ:
            ida_typeinf.guess_tinfo(tif, ea)
            typ = str(tif) if not tif.empty() else "unknown"
        text = f"{self.reference(ea)} size={ida_bytes.get_item_size(ea)} type={typ}"
        if ida_bytes.is_strlit(ida_bytes.get_flags(ea)):
            raw = ida_bytes.get_strlit_contents(ea, -1, ida_nalt.get_str_type(ea))
            text += " string=" + repr(raw.decode("utf-8", "backslashreplace") if raw else "")
        for c in self.comments(ea):
            text += "\n  ; " + c.replace("\n", "\n  ; ")
        return text

    def edges(self, ea):
        """呼び出しと別関数先頭への末尾分岐。間接呼び出しは IDA の xref がある物だけ。"""
        import ida_funcs
        import ida_xref
        import idautils
        for item in idautils.FuncItems(ea):
            for x in idautils.XrefsFrom(item, ida_xref.XREF_FAR):
                target = ida_funcs.get_func(x.to)
                if x.type in (ida_xref.fl_CN, ida_xref.fl_CF) or (
                    x.type in (ida_xref.fl_JN, ida_xref.fl_JF) and target
                    and target.start_ea == x.to and x.to != ea
                ):
                    yield item, x.to

    def function(self, ea, callers, callees):
        import ida_bytes
        import ida_funcs
        import ida_idp
        import ida_lines
        import ida_segregs
        import idautils
        f = ida_funcs.get_func(ea)
        lines = [self.reference(ea), "", "[function comments]"]
        for rep in (False, True):
            c = clean_comment(ida_funcs.get_func_cmt(f, rep))
            if c:
                lines.append(c)
        for title, edges in (("callers", callers), ("callees", callees)):
            lines += ["", f"[{title}]"]
            for site, target in sorted(set(edges)):
                lines.append(f"{self.reference(target)} at {sl.fmt_addr(site)}")
        lines += ["", "[disassembly]"]
        refs = set()
        for item in idautils.FuncItems(ea):
            flags = ida_bytes.get_flags(item)
            thumb = ida_segregs.get_sreg(item, ida_idp.str2reg("T")) == 1
            mode = ("Thumb" if thumb else "ARM") if ida_bytes.is_code(flags) else "data"
            # GENDSM_REMOVE_TAGS と通常の出力（GENDSM_MULTI_LINE を付けない）。
            dis = ida_lines.tag_remove(ida_lines.generate_disasm_line(item, 0) or "")
            # IDA の自動注釈・xref 行は使わず、保存されたコメントを別に読む。
            dis = split_comment(dis, ";")[0]
            lines.append(f"{sl.fmt_addr(item)} {mode:5} {self.name(item)}: {dis}")
            for c in self.comments(item):
                lines.append("  ; " + c.replace("\n", "\n  ; "))
            refs.update(idautils.DataRefsFrom(item))
        lines += ["", "[referenced data and strings]"]
        lines += [self.data(ref) for ref in sorted(refs)]
        status = "ok"
        try:
            if not self.can_decompile:
                raise RuntimeError(self.decompiler_error)
            cf = self.hexrays.decompile(ea, flags=self.hexrays.DECOMP_NO_CACHE)
            if cf is None:
                raise RuntimeError("Hex-Rays returned no function")
            pseudo = [ida_lines.tag_remove(line.line) for line in cf.get_pseudocode()]
            lines += ["", "[pseudocode]"]
            # コメント文字列内の // は壊さず、コメントだけの行の自動注釈を除く。
            lines += [clean_pseudocode(s) for s in pseudo if clean_pseudocode(s).strip()]
        except Exception as exc:
            status = "failed: " + " ".join(str(exc).split())
            lines += ["", "[pseudocode unavailable] " + status]
        return "\n".join(lines), status


def export(build: str, out: Path, commit: str, only: list[str]) -> dict:
    import ida_auto
    import ida_bytes
    import ida_funcs
    import ida_name
    import ida_nalt
    import ida_idaapi
    import idautils
    ida_auto.auto_wait()
    sha = ida_nalt.retrieve_input_file_sha256()
    sha = sha.hex() if sha else ""
    old = []
    if only and (out / "index.txt").exists():
        old_sha, old = read_index(out / "index.txt")
        if old_sha != sha:
            raise ValueError("部分更新の元の IDB 入力 SHA256 が違う")
    reader = IdaReader()
    functions = list(idautils.Functions())
    incoming = {ea: [] for ea in functions}
    outgoing = {}
    for ea in functions:
        outgoing[ea] = list(reader.edges(ea))
        for site, target in outgoing[ea]:
            incoming.setdefault(target, []).append((site, ea))
    selected = set(functions)
    if only:
        selected = set()
        for token in only:
            try:
                addr = int(token, 0) & ~1
            except ValueError:
                addr = ida_name.get_name_ea(ida_idaapi.BADADDR, token)
            f = ida_funcs.get_func(addr)
            if f is None:
                raise ValueError(f"関数がない: {token}")
            selected.add(f.start_ea)
        selected.update(target for ea in list(selected) for _, target in incoming.get(ea, []))
    rows = {int(r['address'], 16): r for r in old}
    for count, ea in enumerate(sorted(selected), 1):
        name = reader.name(ea)
        rel = function_path(ea, name)
        body, status = reader.function(ea, incoming.get(ea, []), outgoing[ea])
        write_text(out / rel, body)
        rows[ea] = dict(name=name, address=sl.fmt_addr(ea), file=rel, decompile=status, symbols_commit=commit)
        if count % 1000 == 0:
            print(f"functions: {count}/{len(selected)}", flush=True)
    # 古い名前のファイルと削除された関数を除く（専用の生成先の中だけ）。
    keep = {r['file'] for r in rows.values()}
    for path in (out / "functions").glob("*/*.txt"):
        if path.relative_to(out).as_posix() not in keep:
            path.unlink()
    write_text(out / "index.txt", index_text(list(rows.values()), sha, commit, bool(only)))
    failures = [r for r in rows.values() if r['decompile'] != 'ok']
    write_text(out / "decompile_failures.txt", index_text(failures, sha, commit, bool(only)))
    # データと文字列の一覧は部分更新でも現在の IDB 全体から生成する。
    with (out / "data.txt").open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(NOTE + "\n")
        for ea in idautils.Heads():
            if ida_bytes.is_data(ida_bytes.get_flags(ea)):
                stream.write(reader.data(ea) + "\n")
    with (out / "strings.txt").open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(NOTE + "\n")
        for ea in idautils.Heads():
            if ida_bytes.is_strlit(ida_bytes.get_flags(ea)):
                stream.write(reader.data(ea) + "\n")
    return dict(build=build, functions=len(rows), updated=len(selected), decompile_failures=len(failures))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--idb", required=True, type=Path)
    ap.add_argument("--symbols-commit", required=True)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--only", action="append", default=[])
    a = ap.parse_args(argv)
    ic.build_info(a.build)
    out = a.out or ic.build_dir(a.build) / "export"
    started = time.monotonic()
    with ic.OpenDb(a.idb, save=False):
        result = export(a.build, out, a.symbols_commit, a.only)
    files = list(out.rglob("*.txt"))
    result.update(files=len(files), bytes=sum(p.stat().st_size for p in files), seconds=round(time.monotonic() - started, 3))
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
