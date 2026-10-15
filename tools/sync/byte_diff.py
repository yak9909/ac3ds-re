#!/usr/bin/env python3
"""2 つ（IDB と IDB、または IDB と code.bin）のバイトの違いを、セグメントごとに一覧にする（.bss は除く）。

出力 CSV: address,length,a_bytes,b_bytes,a_name
  a_name は a の IDB で、その番地を含む関数または大域の名前（無ければ空）。長い違いは、バイト列を先頭 32 バイトで切る。
IDB は開くだけで保存しない（念のため作業用の写しを開く。--no-copy で写さない）。idalib の python で実行する。
"""
from __future__ import annotations

import argparse
import csv
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import idacommon as ic  # noqa: E402

SEGS = (".text", ".rodata", ".data")
SHOW = 32


def dump_idb(path: Path, copy: bool) -> dict[str, tuple[int, bytes]]:
    tmp = None
    p = path
    if copy:
        tmp = Path(tempfile.mkdtemp(prefix="bytediff_", dir=str(ic.data_dir() / "scratch")))
        p = tmp / path.name
        shutil.copy2(path, p)
    try:
        out = {}
        with ic.OpenDb(p, save=False):
            import ida_bytes
            import ida_segment

            for n in SEGS:
                s = ida_segment.get_segm_by_name(n)
                out[n] = (s.start_ea, ida_bytes.get_bytes(s.start_ea, s.end_ea - s.start_ea))
        return out
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def dump_code_bin(path: Path, build: str) -> dict[str, tuple[int, bytes]]:
    info = ic.build_info(build)
    r = ic.seg_ranges(info)
    data = path.read_bytes()
    base = r["text"][0]
    return {n: (r[n[1:]][0], data[r[n[1:]][0] - base:r[n[1:]][1] - base]) for n in SEGS}


def diff_runs(a: bytes, b: bytes, start: int) -> list[tuple[int, int]]:
    """違うバイトの連続した範囲 (アドレス, 長さ) の列。"""
    runs = []
    n = min(len(a), len(b))
    step = 1 << 16
    i = 0
    while i < n:
        j = min(i + step, n)
        if a[i:j] != b[i:j]:
            k = i
            while k < j:
                if a[k] != b[k]:
                    m = k
                    while m < n and a[m] != b[m]:
                        m += 1
                    runs.append((start + k, m - k))
                    k = m
                else:
                    k += 1
        i = j
    return runs


def hexs(bs: bytes) -> str:
    h = bs[:SHOW].hex(" ").upper()
    return h + (" ..." if len(bs) > SHOW else "")


def run(a_path: Path, b_path: Path, build: str, out: Path, copy: bool = True) -> list[dict]:
    if b_path.suffix.lower() in (".i64", ".idb"):
        b = dump_idb(b_path, copy)
    else:
        b = dump_code_bin(b_path, build)
    rows = []
    tmp = None
    p = a_path
    if copy:
        tmp = Path(tempfile.mkdtemp(prefix="bytediff_", dir=str(ic.data_dir() / "scratch")))
        p = tmp / a_path.name
        shutil.copy2(a_path, p)
    try:
        with ic.OpenDb(p, save=False):
            import ida_bytes
            import ida_funcs
            import ida_name
            import ida_segment

            for n in SEGS:
                s = ida_segment.get_segm_by_name(n)
                a = ida_bytes.get_bytes(s.start_ea, s.end_ea - s.start_ea)
                bstart, bb = b[n]
                if bstart != s.start_ea or len(bb) != len(a):
                    raise SystemExit("%s の範囲が違う: a=%#x+%#x b=%#x+%#x" % (n, s.start_ea, len(a), bstart, len(bb)))
                for addr, ln in diff_runs(a, bb, s.start_ea):
                    off = addr - s.start_ea
                    f = ida_funcs.get_func(addr)
                    if f is not None:
                        name = ida_name.get_name(f.start_ea)
                    else:
                        name = ida_name.get_name(ida_bytes.get_item_head(addr))
                    rows.append({"address": "0x%08X" % addr, "length": ln, "a_bytes": hexs(a[off:off + ln]),
                                 "b_bytes": hexs(bb[off:off + ln]), "a_name": name})
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, ["address", "length", "a_bytes", "b_bytes", "a_name"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--a", required=True, help="a の .i64")
    ap.add_argument("--b", required=True, help="b の .i64 または code.bin")
    ap.add_argument("--build", required=True, help="builds.toml のビルド名（code.bin の配置に使う）")
    ap.add_argument("--out", required=True, help="出力 CSV")
    ap.add_argument("--no-copy", action="store_true", help="IDB の写しを作らず直接開く")
    a = ap.parse_args(argv)
    rows = run(Path(a.a), Path(a.b), a.build, Path(a.out), not a.no_copy)
    total = sum(r["length"] for r in rows)
    print("違う箇所 %d、バイト数 %d → %s" % (len(rows), total, a.out))
    for r in sorted(rows, key=lambda r: -r["length"])[:5]:
        print("  %s +%d %s" % (r["address"], r["length"], r["a_name"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
