"""番地範囲の分割・結合と、Git に渡す行単位の3方向統合。IDA は使わない。"""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sync"))
import merge_symbols as ms
import symlib as sl


def row(table, address=0x100000, value="old"):
    r = dict.fromkeys(sl.COLUMNS[table], "")
    r["function" if table == "lvars" else "address"] = sl.fmt_addr(address)
    r["text" if table == "comments" else "class" if table == "vtables" else "name"] = value
    if table == "comments":
        r["kind"] = "line"
    if table == "lvars":
        r["location"] = "stk:-20@0x00123456"
    return r


@pytest.mark.parametrize("table", sl.COLUMNS)
def test_split_join_and_overwrite(tmp_path, table):
    rows = [row(table, ea, '日本語, "引用"\n次の行')
            for ea in (0, 0xFFFFF, 0x100000, 0x1FFFFF, 0x200000, 0xFFFFFFFF)]
    sl.write_table(tmp_path, table, list(reversed(rows)))
    files = sorted((tmp_path / table).glob("*.csv"))
    assert [p.name for p in files] == ["00000000.csv", "00100000.csv", "00200000.csv", "FFF00000.csv"]
    assert sl.read_table(tmp_path, table) == rows
    for p in files:
        assert p.read_text(encoding="utf-8").splitlines()[0] == ",".join(sl.COLUMNS[table])
        assert not p.read_bytes().startswith(b"\xef\xbb\xbf")
        assert b"\r" not in p.read_bytes()
    # 古い行を残さず、空になった範囲のヘッダーは消さない。
    sl.write_table(tmp_path, table, rows[:1])
    assert sl.read_table(tmp_path, table) == rows[:1]
    assert all(p.exists() for p in files)
    joined = tmp_path / "joined.csv"
    sl.write_csv(joined, table, rows)
    assert sl.read_csv(joined, table) == rows


@pytest.mark.parametrize("table", sl.COLUMNS)
def test_empty_table(tmp_path, table):
    sl.write_table(tmp_path, table, [])
    assert (tmp_path / table / "00000000.csv").read_text() == ",".join(sl.COLUMNS[table]) + "\n"
    assert sl.read_table(tmp_path, table) == []


@pytest.mark.parametrize("table", sl.COLUMNS)
@pytest.mark.parametrize("case", ["different_rows", "same_change", "conflict", "add_delete",
                                  "both_delete", "delete_edit", "add_add_same", "add_add_conflict"])
def test_three_way(table, case):
    x, y, z = row(table), row(table, 0x100004), row(table, 0x100008)
    xa, xb = dict(x), dict(x)
    value = "text" if table == "comments" else "class" if table == "vtables" else "name"
    xa[value], xb[value] = '自分, "A"\n続き', "相手"
    ya = dict(y, **{value: "別の行"})
    base, ours, theirs, expected, conflicts = {
        "different_rows": ([x, y], [xa, y], [x, ya], [xa, ya], 0),
        "same_change": ([x], [xa], [xa], [xa], 0),
        "conflict": ([x], [xa], [xb], [], 1),
        "add_delete": ([x, y], [y], [x, y, z], [y, z], 0),
        "both_delete": ([x], [], [], [], 0),
        "delete_edit": ([x], [], [xb], [], 1),
        "add_add_same": ([], [xa], [xa], [xa], 0),
        "add_add_conflict": ([], [xa], [xb], [], 1),
    }[case]
    text, count = ms.merge_csv(table, *(sl.dumps_csv(table, r) for r in (base, ours, theirs)))
    assert count == conflicts
    if not conflicts:
        assert sl.loads_csv(table, text) == expected
        assert ms.merge_csv(table, *(sl.dumps_csv(table, r) for r in (base, theirs, ours)))[0] == text
    else:
        assert "<<<<<<< ours\n" in text and "||||||| base\n" in text
        assert "=======\n" in text and ">>>>>>> theirs\n" in text
        for r in (ours, base, theirs):
            if r:
                assert sl.dumps_csv(table, r).split("\n", 1)[1] in text


def test_different_fields_in_same_row_conflict():
    b = row("functions")
    text, count = ms.merge_csv("functions", sl.dumps_csv("functions", [b]),
                               sl.dumps_csv("functions", [dict(b, name="renamed")]),
                               sl.dumps_csv("functions", [dict(b, prototype="void f()")]))
    assert count == 1 and "<<<<<<<" in text


@pytest.mark.parametrize("table,field,other", [("comments", "kind", "repeatable"),
                                                 ("lvars", "location", "reg:0@0x00123456")])
def test_compound_keys(table, field, other):
    a = row(table)
    b = dict(a, **{field: other})
    text, count = ms.merge_csv(table, "", sl.dumps_csv(table, [a]), sl.dumps_csv(table, [b]))
    assert count == 0
    assert sl.loads_csv(table, text) == sl.sort_rows(table, [a, b])


def test_lvar_rename_is_same_key():
    b = row("lvars")
    renamed = dict(b, name="new")
    changed = dict(b, type="int")
    text, count = ms.merge_csv("lvars", *(sl.dumps_csv("lvars", r)
                                          for r in ([b], [renamed], [changed])))
    assert count == 1
    diff = sl.compare_tables("lvars", [b], [renamed])
    assert not diff["only_a"] and not diff["only_b"] and "name" in diff["changed"]


def test_conflict_keeps_clean_rows_and_marker_size():
    x, y = row("comments"), row("comments", 0x100004)
    text, count = ms.merge_csv("comments", sl.dumps_csv("comments", [x, y]),
                               sl.dumps_csv("comments", [dict(x, text="a"), y]),
                               sl.dumps_csv("comments", [dict(x, text="b"), dict(y, text="clean")]), 11)
    assert count == 1 and "<" * 11 + " ours\n" in text
    assert text.endswith("0x00100004,line,clean\n")


def test_driver_cli(tmp_path):
    files = [tmp_path / (s + " with space.csv") for s in ("base", "ours", "theirs")]
    x, y = row("comments"), row("comments", 0x100004)
    for path, rows in zip(files, ([x, y], [dict(x, text="a"), y], [x, dict(y, text="b")])):
        sl.write_csv(path, "comments", rows)
    cmd = [sys.executable, ms.__file__, *map(str, files), "symbols/test/comments/00100000.csv"]
    result = subprocess.run(cmd, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert sl.read_csv(files[1], "comments") == [dict(x, text="a"), dict(y, text="b")]
    sl.write_csv(files[2], "comments", [dict(x, text="other"), y])
    assert subprocess.run(cmd, capture_output=True).returncode == 1
    assert "<<<<<<<" in files[1].read_text()
    # 壊れた入力で ours を上書きしない。
    saved = files[1].read_bytes()
    files[0].write_text("wrong,header\n")
    assert subprocess.run(cmd, capture_output=True).returncode == 2
    assert files[1].read_bytes() == saved


@pytest.mark.parametrize("bad", ["address,kind,text\n0x00100000,line\n",
                                  "address,kind,text\n0x00100000,line,x,extra\n",
                                  'address,kind,text\n0x00100000,line,"unclosed',
                                  "bad,header\n"])
def test_malformed_csv_rejected(bad):
    import csv
    with pytest.raises((ValueError, csv.Error)):
        ms.merge_csv("comments", "", bad, sl.dumps_csv("comments", []))


def test_duplicate_key_rejected(tmp_path):
    x = row("lvars")
    rows = [x, dict(x, name="different_name")]
    with pytest.raises(ValueError, match="重複"):
        sl.write_table(tmp_path, "lvars", rows)
    text = sl.dumps_csv("lvars", rows)
    with pytest.raises(ValueError, match="重複"):
        ms.merge_csv("lvars", text, text, text)
    sl.write_csv(tmp_path / "lvars/00100000.csv", "lvars", rows)
    with pytest.raises(ValueError, match="重複"):
        sl.read_table(tmp_path, "lvars")


def test_wrong_range_and_legacy_rejected(tmp_path):
    sl.write_csv(tmp_path / "comments/00200000.csv", "comments", [row("comments")])
    with pytest.raises(ValueError, match="範囲外"):
        sl.read_table(tmp_path, "comments")
    sl.write_csv(tmp_path / "functions.csv", "functions", [])
    with pytest.raises(ValueError, match="旧形式"):
        sl.read_table(tmp_path, "functions")
