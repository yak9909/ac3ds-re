#!/usr/bin/env python3
"""code.bin のバイトを読む。例: codebytes.py --build acnl_jpn_v15 0x100000 16。IDA 不要。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "sync"))
import idacommon as ic


def file_offset(info: dict, address: int, length: int) -> int:
    """仮想番地を配置済み code.bin の位置へ変換。隙間と BSS は読まない。"""
    if length <= 0:
        raise ValueError("長さは正の整数にする")
    ranges = ic.seg_ranges(info)
    end = address + length
    cursor = address
    for start, stop in sorted(v for k, v in ranges.items() if k != "bss"):
        if start <= cursor < stop:
            cursor = min(end, stop)
            if cursor == end:
                return address - ranges["text"][0]
    raise ValueError("範囲が code.bin のセグメント外（隙間・BSS を含む）")


def read_bytes(path: Path, info: dict, address: int, length: int) -> bytes:
    offset = file_offset(info, address, length)
    with path.open("rb") as stream:
        stream.seek(offset)
        data = stream.read(length)
    if len(data) != length:
        raise ValueError("code.bin が指定範囲より短い")
    return data


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--build", required=True)
    ap.add_argument("--code", type=Path, help="既定の code.bin の代わりに読むファイル")
    ap.add_argument("address", type=lambda s: int(s, 0))
    ap.add_argument("length", type=lambda s: int(s, 0))
    args = ap.parse_args(argv)
    try:
        info = ic.build_info(args.build)
        data = read_bytes(args.code or ic.code_bin_path(args.build), info, args.address, args.length)
    except (ValueError, OSError) as exc:
        ap.error(str(exc))
    print(data.hex(" ").upper())
    return 0


if __name__ == "__main__":
    sys.exit(main())
