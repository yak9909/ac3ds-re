"""tools/sync/symlib.py の試験（IDA を使わない部分）。"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sync"))
import symlib as sl  # noqa: E402


def test_addr_roundtrip():
    assert sl.fmt_addr(0x193764) == "0x00193764"
    assert sl.fmt_addr(0x193765) == "0x00193765"
    assert sl.parse_addr("0x00193764") == 0x193764
    assert sl.addr_key("zz") == -1


@pytest.mark.parametrize("name", [
    "sub_1A2B3C", "loc_100", "unk_9F0000", "dword_1234", "word_12", "byte_FF", "off_8E4880", "stru_1234",
    "nullsub_13", "j_j_nullsub_13_0", "locret_1000", "def_1234", "jpt_1234", "sub_100_0", "", "qword_8",
])
def test_auto_names(name):
    assert sl.is_auto_name(name)
    assert not sl.is_user_name(name)


@pytest.mark.parametrize("name", [
    "PlayerState_Enter", "g_PlayerManager", "vtbl_SelectBase", "vc_ISLPOINTER", "sub_Foo", "dword_table",
    "_ZN3Foo3barEv", "kItemParamTable", "unk_name",
])
def test_user_names(name):
    assert sl.is_user_name(name)


def test_loader_name_not_user():
    assert not sl.is_user_name("start")


def test_extract_refs():
    t = "判明 [ACNL-F0412] と [HHD-F0001]。[ACNL-F0412] 再掲。[x] [ACNL-F12]"
    assert sl.extract_refs(t) == ["ACNL-F0412", "HHD-F0001"]
    assert sl.extract_refs("") == []
    assert sl.join_refs(["B-1", "A-1", "A-1"]) == "A-1;B-1"


@pytest.mark.parametrize("text,auto", [
    ("int", True), ("unsigned int", True), ("_DWORD *", True), ("float", True), ("switch jump", True),
    ("jump table for switch statement", True), ("switch 12 cases", True), ("jumptable 00105070 default case, case 3", True),
    ("jumptable 001E9CAC default case\njumptable 001EA090 default case", True), ("offset to this", True),
    ("reference to RTTI's type class", True), ("type descriptor name", True),
    ("プレイヤーの位置を返す", False), ("int の最大値", False), ("", False), ("[ACNL-F0412] 根拠", False),
])
def test_auto_comment(text, auto):
    assert sl.is_auto_comment(text) is auto


def test_csv_roundtrip_and_determinism():
    rows = [
        {"address": "0x00000200", "kind": "line", "text": "二行目\n三行目, \"引用\""},
        {"address": "0x00000100", "kind": "repeatable", "text": "x"},
        {"address": "0x00000100", "kind": "func", "text": "y"},
        {"address": "0x00000100", "kind": "line", "text": "z"},
    ]
    a = sl.dumps_csv("comments", rows)
    b = sl.dumps_csv("comments", list(reversed(rows)))
    assert a == b
    assert "\r" not in a
    back = sl.loads_csv("comments", a)
    assert [(r["address"], r["kind"]) for r in back] == [
        ("0x00000100", "func"), ("0x00000100", "line"), ("0x00000100", "repeatable"), ("0x00000200", "line")]
    assert back[-1]["text"] == "二行目\n三行目, \"引用\""


def test_sort_numeric_not_lexical():
    rows = [{"address": "0x0000FFFF", "size": "4", "name": "b"}, {"address": "0x00010000", "size": "4", "name": "a"}]
    out = sl.sort_rows("functions", rows)
    assert [r["name"] for r in out] == ["b", "a"]


def test_write_read_file(tmp_path):
    p = tmp_path / "functions.csv"
    rows = [{"address": "0x00100000", "size": "8", "name": "F", "prototype": "int(int a, int b)", "confidence": "HIGH",
             "source": "analysis", "refs": "ACNL-F0001", "clone_of": ""}]
    sl.write_csv(p, "functions", rows)
    raw = p.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf") and b"\r" not in raw
    assert '"int(int a, int b)"' in raw.decode()
    assert sl.read_csv(p, "functions") == rows
    assert sl.read_csv(tmp_path / "nothing.csv", "functions") == []


def test_carry_over():
    old = [{"address": "0x00100000", "name": "F", "confidence": "HIGH", "source": "analysis", "refs": "ACNL-F0001",
            "clone_of": "0x00200000", "size": "8", "prototype": ""}]
    new = [
        {"address": "0x00100000", "name": "F", "size": "12", "prototype": "", "refs": "ACNL-F0999", "source": ""},
        {"address": "0x00100000", "name": "G", "size": "12", "prototype": "", "refs": "ACNL-F0412", "source": ""},
        {"address": "0x00100100", "name": "F", "size": "4", "prototype": "", "refs": "", "source": ""},
    ]
    out = sl.carry_over("functions", new, old, "legacy-idb")
    assert (out[0]["confidence"], out[0]["source"], out[0]["refs"], out[0]["clone_of"]) == \
        ("HIGH", "analysis", "ACNL-F0001", "0x00200000")
    assert out[0]["size"] == "12"  # 引き継ぐのは4列だけ
    assert (out[1]["source"], out[1]["refs"]) == ("legacy-idb", "ACNL-F0412")  # 名前が違えば新しい行
    assert out[2]["source"] == "legacy-idb"  # アドレスが違えば新しい行


@pytest.mark.parametrize("table,column", [
    ("functions", "address"), ("globals", "address"), ("comments", "address"),
    ("vtables", "address"), ("lvars", "function"),
])
def test_split_by_segments(table, column):
    rows = [{column: a, "name": str(i)} for i, a in enumerate([
        "0x00000FFF", "0x00001000", "0x000010FF", "0x00001100", "0x00B00000",
    ])]
    inside, outside = sl.split_by_segments(table, rows, [(0x1000, 0x1100)])
    assert [r["name"] for r in inside] == ["1", "2"]
    assert [r["name"] for r in outside] == ["0", "3", "4"]


def test_thumb_address_at_segment_end():
    rows = [{"address": "0x00001001"}, {"address": "0x00001101"}]
    inside, outside = sl.split_by_segments("functions", rows, [(0x1000, 0x1100)])
    assert inside == rows[:1]
    assert outside == rows[1:]


@pytest.mark.parametrize("table,column", [
    ("functions", "address"), ("globals", "address"), ("comments", "address"),
    ("vtables", "address"), ("lvars", "function"),
])
def test_retain_outside_segments(table, column):
    old = [{column: "0x00001000", "name": "deleted"},
           {column: "0x00B00000", "name": "ModuleIndoor", "text": "そのまま,\n保存"},
           {column: "0x00C00000", "name": "ModuleFtr"}]
    new = [{column: "0x00001004", "name": "from IDB"}]
    merged, retained = sl.retain_outside_segments(table, new, old, [(0x1000, 0x1100)])
    assert retained == 2
    assert merged == [new[0], old[1], old[2]]
    assert old[0] not in merged  # IDB 内で消された行は戻らない


def test_retained_csv_row_survives_write_and_read():
    old = [{"address": "0x00B00000", "kind": "line", "text": "CRO,\nコメント"}]
    new = [{"address": "0x00001000", "kind": "line", "text": "IDB のコメント"}]
    rows, retained = sl.retain_outside_segments("comments", new, old, [(0x1000, 0x1100)])
    assert retained == 1
    assert sl.loads_csv("comments", sl.dumps_csv("comments", rows)) == [new[0], old[0]]


def test_compare_tables():
    a = [{"address": "0x1", "size": "4", "name": "A", "prototype": "", "source": "x"},
         {"address": "0x2", "size": "4", "name": "B", "prototype": "", "source": "x"},
         {"address": "0x3", "size": "4", "name": "C", "prototype": "", "source": "x"}]
    b = [{"address": "0x1", "size": "4", "name": "A", "prototype": "", "source": "y"},
         {"address": "0x2", "size": "8", "name": "B", "prototype": "int()", "source": "y"},
         {"address": "0x4", "size": "4", "name": "D", "prototype": "", "source": "y"}]
    r = sl.compare_tables("functions", a, b, ignore=("source",))
    assert r["same"] == 1
    assert [x["address"] for x in r["only_a"]] == ["0x3"]
    assert [x["address"] for x in r["only_b"]] == ["0x4"]
    assert set(r["changed"]) == {"size", "prototype"}
    assert not sl.tables_equal(r)
    assert sl.tables_equal(sl.compare_tables("functions", a, a))
    lines = sl.summarize_compare(r)
    assert lines[0].startswith("same=1 only_a=1 only_b=1")


def test_type_blocks_and_order():
    text = ("// header\nstruct A;\n\n// type: B\nstruct B\n{\n  A *a;\n  C c;\n};\n\n"
            "// type: A\nstruct A\n{\n  int x;\n};\n\n// type: C\nstruct C\n{\n  int y;\n};\n")
    blocks = dict(sl.split_type_blocks(text))
    assert list(blocks) == ["B", "A", "C"]
    assert blocks["A"].startswith("struct A")
    order = sl.order_type_blocks(blocks)
    assert order == ["A", "C", "B"]  # 名前順。ただし B は A・C の後


def test_meta():
    s = sl.dumps_meta({"build": "x", "n": 3, "ok": True, "counts": {"functions": 2}})
    assert s == 'build = "x"\nn = 3\nok = true\n\n[counts]\nfunctions = 2\n'
    import tomllib

    assert tomllib.loads(s)["counts"]["functions"] == 2


def test_name_unnamed_members():
    src = "struct A\n{\n  u32 fsr;\n  unsigned int;\n  const char *p;\n  unsigned __int8;\n};"
    assert sl.name_unnamed_members(src) == (
        "struct A\n{\n  u32 fsr;\n  unsigned int __unnamed_1;\n  const char *p;\n  unsigned __int8 __unnamed_2;\n};")
