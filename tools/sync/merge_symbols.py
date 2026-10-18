#!/usr/bin/env python3
"""symbols の CSV を行の主キーで3方向統合する Git merge driver。IDA・外部依存なし。

merge_symbols.py %O %A %B %P --marker-size %L
結果は %A へ書く。終了値 0: 成功、1: 行の衝突、2: 入力・実行エラー。
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import symlib as sl


def _index(table: str, text: str) -> dict:
    # 新規ファイル同士の統合では Git が空の共通祖先を渡す。
    rows = sl.loads_csv(table, text) if text else []
    result = {}
    for row in rows:
        sl.range_name(table, row)  # 番地の妥当性も検査する。
        key = tuple(sl.parse_addr(row[c]) if c in ("address", "function") else row[c]
                    for c in sl.KEYS[table])
        if key in result:
            raise ValueError("%s: キーの重複: %r" % (table, key))
        result[key] = row
    return result


def merge_csv(table: str, base: str, ours: str, theirs: str, marker_size: int = 7) -> tuple[str, int]:
    """同じキーの双方の行が祖先と異なり、互いにも異なる場合だけ衝突する。"""
    if marker_size < 1:
        raise ValueError("marker-size は正の整数")
    ancestor, local, remote = (_index(table, text) for text in (base, ours, theirs))
    # 主キーを symlib の順序（数値番地・コメントの種類）で並べる。
    representatives = ancestor | local | remote
    ordered = sl.sort_rows(table, list(representatives.values()))
    output = [sl.dumps_csv(table, [])]
    conflicts = 0

    def row_text(row):
        return sl.dumps_csv(table, [row]).split("\n", 1)[1] if row is not None else ""

    for row in ordered:
        key = tuple(sl.parse_addr(row[c]) if c in ("address", "function") else row[c]
                    for c in sl.KEYS[table])
        b, a, c = ancestor.get(key), local.get(key), remote.get(key)
        if a == c:
            output.append(row_text(a))
        elif a == b:
            output.append(row_text(c))
        elif c == b:
            output.append(row_text(a))
        else:
            conflicts += 1
            output.extend(["<" * marker_size + " ours\n", row_text(a),
                           "|" * marker_size + " base\n", row_text(b),
                           "=" * marker_size + "\n", row_text(c),
                           ">" * marker_size + " theirs\n"])
    return "".join(output), conflicts


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("base", type=Path)
    ap.add_argument("ours", type=Path)
    ap.add_argument("theirs", type=Path)
    ap.add_argument("path", help="Git の %%P（表の判定用）")
    ap.add_argument("--marker-size", type=int, default=7)
    args = ap.parse_args(argv)
    try:
        table = Path(args.path).parent.name
        if table not in sl.COLUMNS:
            raise ValueError("symbols の表を判定できない: %s" % args.path)
        texts = []
        for path in (args.base, args.ours, args.theirs):
            with path.open(encoding="utf-8", newline="") as f:
                texts.append(f.read())
        merged, conflicts = merge_csv(table, *texts, marker_size=args.marker_size)
        with args.ours.open("w", encoding="utf-8", newline="") as f:
            f.write(merged)
        return int(bool(conflicts))
    except (OSError, ValueError, csv.Error) as exc:
        print("symbols merge: %s" % exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
