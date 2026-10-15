#!/usr/bin/env python3
"""復元の試験: code.bin から空の IDB を作り、symbols を取り込み、もう一度書き出して、元の symbols と比べる。

一致しなければ終了コード 1。空の IDB は _local/builds/<ビルド>/ida/restore-test/ にキャッシュする（--fresh で作り直す）。
作業用の IDB・書き出しは --keep を付けたときだけ残す。idalib の python で実行する。
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import create_idb  # noqa: E402
import export_symbols  # noqa: E402
import idacommon as ic  # noqa: E402
import import_symbols  # noqa: E402
import symlib as sl  # noqa: E402

TABLES = ("functions", "globals", "comments", "vtables", "lvars")


def compare_dirs(a: Path, b: Path) -> tuple[dict, bool]:
    ta, tb = sl.read_all(a), sl.read_all(b)
    result = {}
    ok = True
    for t in TABLES:
        # confidence/source/refs/clone_of は IDB の外の情報なので比べない
        ign = ("confidence", "source", "refs", "clone_of")
        res = sl.compare_tables(t, ta[t], tb[t], ignore=ign)
        result[t] = res
        ok &= sl.tables_equal(res)
    ha, hb = a / "types" / "local_types.h", b / "types" / "local_types.h"
    ra = ha.read_text(encoding="utf-8") if ha.exists() else ""
    rb = hb.read_text(encoding="utf-8") if hb.exists() else ""
    ba = dict(sl.split_type_blocks(ra))
    bb = dict(sl.split_type_blocks(rb))
    tres = {"only_a": sorted(ba.keys() - bb.keys()), "only_b": sorted(bb.keys() - ba.keys()),
            "changed": sorted(k for k in ba.keys() & bb.keys() if ba[k] != bb[k]), "same": 0}
    tres["same"] = len(ba) - len(tres["changed"]) - len(tres["only_a"])
    result["types"] = tres
    ok &= not (tres["only_a"] or tres["only_b"] or tres["changed"])
    return result, ok


def run(build: str, symbols: Path, keep: bool = False, fresh: bool = False, report: Path | None = None) -> bool:
    cache = ic.build_dir(build) / "ida" / "restore-test"
    cache.mkdir(parents=True, exist_ok=True)
    base = cache / (build + "_empty.i64")
    if fresh and base.exists():
        base.unlink()
    if not base.exists():
        print("空の IDB を作る: %s" % base)
        create_idb.create(build, base, quiet=True)
    work_dir = Path(tempfile.mkdtemp(prefix="restore_", dir=str(cache)))
    work = work_dir / (build + ".i64")
    shutil.copy2(base, work)
    out = work_dir / "symbols"
    try:
        with ic.OpenDb(work, save=True) as _:
            rep = import_symbols.import_all(symbols, work_dir / "import_report.json")
        rep.sections.pop("_meta", None)
        rep.print()
        with ic.OpenDb(work, save=False) as _:
            export_symbols.export_all(build, out, "restore-test")
        res, ok = compare_dirs(symbols, out)
        for t, r in res.items():
            if t == "types":
                print("%-10s same=%d only_a=%d only_b=%d changed=%d" % (t, r["same"], len(r["only_a"]), len(r["only_b"]),
                                                                     len(r["changed"])))
                for k in ("only_a", "only_b", "changed"):
                    if r[k]:
                        print("    %s 例: %s" % (k, ", ".join(r[k][:3])))
            else:
                print("%-10s %s" % (t, sl.summarize_compare(r)[0]))
                for line in sl.summarize_compare(r)[1:]:
                    print("    " + line)
        if report:
            def conv(r):
                if "changed" in r and isinstance(r["changed"], dict):
                    return {"same": r["same"], "only_a": r["only_a"], "only_b": r["only_b"],
                            "changed": {c: [list(map(str, x)) for x in v] for c, v in r["changed"].items()}}
                return r
            report.write_text(json.dumps({t: conv(r) for t, r in res.items()}, ensure_ascii=False, indent=1),
                              encoding="utf-8")
        print("結果: %s" % ("一致" if ok else "不一致"))
        return ok
    finally:
        if not keep:
            shutil.rmtree(work_dir, ignore_errors=True)
        else:
            print("残した場所: %s" % work_dir)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--build", required=True)
    ap.add_argument("--symbols", required=True, help="symbols/<ビルド>")
    ap.add_argument("--keep", action="store_true", help="作業用の IDB と書き出しを残す")
    ap.add_argument("--fresh", action="store_true", help="キャッシュした空の IDB を作り直す")
    ap.add_argument("--report", help="差の詳細を書く JSON")
    a = ap.parse_args(argv)
    ok = run(a.build, Path(a.symbols), a.keep, a.fresh, Path(a.report) if a.report else None)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
