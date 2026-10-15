"""tools/sync の IDA を使わない部分（セグメントの計画・差分の走査・復元試験の比較）の試験。"""
import struct
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sync"))
import byte_diff  # noqa: E402
import create_idb  # noqa: E402
import idacommon as ic  # noqa: E402
import import_symbols  # noqa: E402
import restore_test  # noqa: E402
import symlib as sl  # noqa: E402


def _layout(info):
    r = ic.seg_ranges(info)
    return {"text": (r["text"][0], r["text"][1] - r["text"][0]),
            "rodata": (r["rodata"][0], r["rodata"][1] - r["rodata"][0]),
            "data": (r["data"][0], r["data"][1] - r["data"][0]), "bss_size": r["bss"][1] - r["bss"][0]}


@pytest.mark.parametrize("build", ["acnl_jpn_v15", "hhd_jpn_v11"])
def test_plan_segments(build):
    info = ic.build_info(build)
    segs = create_idb.plan_segments(info, _layout(info))
    assert [s["name"] for s in segs] == [".text", ".rodata", ".data", ".bss"]
    assert [s["perm"] for s in segs] == [5, 4, 6, 6]
    assert segs[0]["file_off"] == 0 and segs[3]["file_off"] is None
    assert segs[1]["file_off"] == segs[1]["start"] - segs[0]["start"]


def test_plan_segments_mismatch():
    info = ic.build_info("hhd_jpn_v11")
    lay = _layout(info)
    lay["text"] = (lay["text"][0], lay["text"][1] + 4)
    with pytest.raises(SystemExit):
        create_idb.plan_segments(info, lay)


def test_read_layout(tmp_path):
    e = bytearray(0x40)
    struct.pack_into("<III", e, 0x10, 0x100000, 3, 0x2100)
    struct.pack_into("<III", e, 0x20, 0x103000, 1, 0x800)
    struct.pack_into("<III", e, 0x30, 0x104000, 1, 0x10)
    struct.pack_into("<I", e, 0x3C, 0x500)
    p = tmp_path / "exheader.bin"
    p.write_bytes(bytes(e))
    assert create_idb.read_layout(p) == {"text": (0x100000, 0x2100), "rodata": (0x103000, 0x800),
                                         "data": (0x104000, 0x10), "bss_size": 0x500}


def test_diff_runs():
    a = bytearray(200000)
    b = bytearray(a)
    b[5] = 1
    b[6] = 2
    b[70000] = 9
    b[199999] = 7
    assert byte_diff.diff_runs(bytes(a), bytes(b), 0x1000) == [(0x1005, 2), (0x1000 + 70000, 1), (0x1000 + 199999, 1)]
    assert byte_diff.diff_runs(bytes(a), bytes(a), 0) == []
    assert byte_diff.hexs(bytes(range(40))).endswith("...")


def test_compare_dirs(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    rows = [{"address": "0x00100000", "size": "4", "name": "F", "prototype": "", "confidence": "HIGH",
             "source": "x", "refs": "R", "clone_of": ""}]
    sl.write_csv(a / "functions.csv", "functions", rows)
    sl.write_csv(b / "functions.csv", "functions", [dict(rows[0], confidence="", source="y")])
    res, ok = restore_test.compare_dirs(a, b)
    assert ok  # confidence/source/refs は比べない
    sl.write_csv(b / "functions.csv", "functions", [dict(rows[0], name="G")])
    res, ok = restore_test.compare_dirs(a, b)
    assert not ok and "name" in res["functions"]["changed"]
    (a / "types").mkdir()
    (a / "types" / "local_types.h").write_text("// type: A\nstruct A { int x; };\n", encoding="utf-8")
    sl.write_csv(b / "functions.csv", "functions", rows)
    res, ok = restore_test.compare_dirs(a, b)
    assert not ok and res["types"]["only_a"] == ["A"]


def test_import_report_skipped(capsys):
    rep = import_symbols.Report()
    rep.skip("functions", 2)
    rep.ok("functions")
    rep.fail("functions", "0x00001000", "bad")
    assert rep.dump()["functions"] == {"total": 4, "ok": 1, "skipped": 2,
                                       "failed": [{"key": "0x00001000", "reason": "bad"}]}
    rep.print()
    assert "対象外      2" in capsys.readouterr().out
