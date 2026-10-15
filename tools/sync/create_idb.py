#!/usr/bin/env python3
"""code.bin と ExHeader から、ARM（ARMv6K、リトルエンディアン）の IDB を新しく作る。

セグメントの置き方は v2 の ctr_loader.py（Kynex7510/3ds_ida。tools/sync/loaders/ に同梱）で、読み込みもそれが行う:
  .text=CODE(R-X)  .rodata=CONST(R--)  .data=DATA(RW-)  .bss=BSS(RW-)、32 ビット、エントリ `start`（.text の先頭）。
アドレス・大きさは builds.toml と ExHeader の両方で確かめる。code.bin の SHA256 が builds.toml と違えば止まる。
idalib の python で実行する。
"""
from __future__ import annotations

import argparse
import os
import struct
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import idacommon as ic  # noqa: E402


def read_layout(exheader: Path) -> dict:
    """ExHeader の SystemControlInfo.CodeSetInfo から (アドレス, ページ数, 大きさ) を読む。"""
    e = exheader.read_bytes()
    out = {}
    for off, name in ((0x10, "text"), (0x20, "rodata"), (0x30, "data")):
        a, pages, size = struct.unpack_from("<III", e, off)
        out[name] = (a, size)
    out["bss_size"] = struct.unpack_from("<I", e, 0x3C)[0]
    return out


def plan_segments(info: dict, layout: dict) -> list[dict]:
    """builds.toml と ExHeader を突き合わせ、置くセグメントの一覧を返す。"""
    r = ic.seg_ranges(info)
    text_base = r["text"][0]
    for n in ("text", "rodata", "data"):
        a, size = layout[n]
        if (a, a + size) != r[n]:
            raise SystemExit("ExHeader と builds.toml が違う: %s exheader=%#x..%#x builds=%#x..%#x"
                             % (n, a, a + size, *r[n]))
    if r["bss"][0] != r["data"][1] or r["bss"][1] - r["bss"][0] != layout["bss_size"]:
        raise SystemExit("bss が ExHeader と違う")
    segs = []
    for name, cls, perm in ((".text", "CODE", 5), (".rodata", "CONST", 4), (".data", "DATA", 6), (".bss", "BSS", 6)):
        s, e = r[name[1:]]
        segs.append({"name": name, "start": s, "end": e, "class": cls, "perm": perm,
                     "file_off": None if name == ".bss" else s - text_base})
    return segs


def install_loader() -> None:
    """同梱の ctr_loader.py（Kynex7510/3ds_ida。ExHeader を環境変数で渡せるよう 1 か所だけ直した物）を IDAUSR に置く。"""
    import shutil

    ic.init_ida()
    dst = Path(os.environ["IDAUSR"]) / "loaders" / "ctr_loader.py"
    src = ic.HERE / "loaders" / "ctr_loader.py"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or dst.read_bytes() != src.read_bytes():
        shutil.copy2(src, dst)


def create(build: str, out: Path, wait: bool = True, quiet: bool = False) -> dict:
    """ctr_loader で code.bin を読み込み（読み込み時の解析の予約を含めて v2 と同じ手順）、自動解析を最後まで行う。"""
    info = ic.build_info(build)
    code = ic.code_bin_path(build)
    sha = ic.sha256_file(code)
    if sha != info.get("code_sha256"):
        raise SystemExit("code.bin の SHA256 が builds.toml と違う: %s != %s" % (sha, info.get("code_sha256")))
    exh = ic.exheader_path(build)
    layout = read_layout(exh)
    segs = plan_segments(info, layout)
    data = code.read_bytes()
    out = Path(out)
    if out.exists() or out.with_suffix(".id0").exists():
        raise SystemExit("出力先が既にある（上書きしない）: %s" % out)
    out.parent.mkdir(parents=True, exist_ok=True)
    install_loader()
    os.environ["AC3DS_EXHEADER"] = str(exh)

    t0 = time.time()
    with ic.OpenDb(code, save=True, auto=wait, args='-c -o"%s"' % out, console=not quiet) as _:
        import ida_auto
        import ida_bytes
        import ida_funcs
        import ida_segment

        t1 = time.time()
        ida_auto.auto_wait()
        # 読み込み結果を builds.toml・ExHeader・code.bin と突き合わせる
        for sg in segs:
            s = ida_segment.get_segm_by_name(sg["name"])
            if s is None or (s.start_ea, s.end_ea, s.perm) != (sg["start"], sg["end"], sg["perm"]):
                raise SystemExit("セグメントが期待と違う: %s" % sg["name"])
            if sg["file_off"] is not None:
                n = sg["end"] - sg["start"]
                if ida_bytes.get_bytes(sg["start"], n) != data[sg["file_off"]:sg["file_off"] + n]:
                    raise SystemExit("バイトが code.bin と違う: %s" % sg["name"])
        t2 = time.time()
        res = {"build": build, "idb": str(out), "code_sha256": sha, "functions": ida_funcs.get_func_qty(),
               "load_seconds": round(t1 - t0, 1), "auto_seconds": round(t2 - t1, 1),
               "processor": ic.processor_info(), "ida": ic.ida_version()}
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True, help="builds.toml のビルド名（例 acnl_jpn_v15）")
    ap.add_argument("--out", required=True, help="作る .i64 のパス（既にあれば止まる）")
    ap.add_argument("--no-auto", action="store_true", help="読み込み時の自動解析を待たない（試験用）")
    ap.add_argument("--json", help="結果（設定・セグメント）を書く JSON")
    a = ap.parse_args(argv)
    res = create(a.build, Path(a.out), wait=not a.no_auto)
    if a.json:
        import json

        Path(a.json).write_text(json.dumps(res, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    print("作成: %s 関数 %d 件、読み込み %.1f 秒、自動解析 %.1f 秒" % (res["idb"], res["functions"], res["load_seconds"],
                                                           res["auto_seconds"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
