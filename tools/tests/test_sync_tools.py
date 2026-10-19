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
    sl.write_table(a, "functions", rows)
    sl.write_table(b, "functions", [dict(rows[0], confidence="", source="y")])
    res, ok = restore_test.compare_dirs(a, b)
    assert ok  # confidence/source/refs は比べない
    sl.write_table(b, "functions", [dict(rows[0], name="G")])
    res, ok = restore_test.compare_dirs(a, b)
    assert not ok and "name" in res["functions"]["changed"]
    (a / "types").mkdir()
    (a / "types" / "local_types.h").write_text("// type: A\nstruct A { int x; };\n", encoding="utf-8")
    sl.write_table(b, "functions", rows)
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

def test_compare_all_type_headers(tmp_path):
    a, b = tmp_path / 'a', tmp_path / 'b'
    for root in (a, b):
        (root / 'types').mkdir(parents=True)
    (a / 'types' / 'extra.h').write_text('// type: Extra\nstruct Extra { int x; };\n')
    res, ok = restore_test.compare_dirs(a, b)
    assert not ok and res['types']['only_a'] == ['Extra']
    (b / 'types' / 'local_types.h').write_text('// type: Extra\nstruct Extra { int x; };\n')
    assert restore_test.compare_dirs(a, b)[1]


def test_import_types_cross_header_dependencies(tmp_path, monkeypatch):
    from types import SimpleNamespace
    (tmp_path / 'types').mkdir()
    (tmp_path / 'types' / 'a.h').write_text('struct Dependency;\n// type: Owner\nstruct Owner { Dependency d; };\n')
    (tmp_path / 'types' / 'z.h').write_text('// type: Dependency\nstruct Dependency { int x; };\n')
    parsed = []
    monkeypatch.setitem(sys.modules, 'ida_typeinf', SimpleNamespace(
        get_idati=lambda: None, HTI_DCL=1,
        parse_decls=lambda til, text, printer, flags: parsed.append(text) or 0))
    rep = import_symbols.Report()
    import_symbols.import_types(tmp_path, rep)
    assert parsed == ['struct Dependency;\n', 'struct Dependency { int x; };\n',
                      'struct Owner { Dependency d; };\n']
    assert rep.sections['types']['ok'] == 2


def test_export_unnamed_typed_global(monkeypatch):
    from types import SimpleNamespace as NS
    import export_symbols as ex
    ea = 0x955FF4
    monkeypatch.setitem(sys.modules, 'ida_name', NS(get_name=lambda addr: 'stru_955FF4'))
    monkeypatch.setitem(sys.modules, 'ida_nalt', NS(is_userti=lambda addr: addr == ea))
    monkeypatch.setitem(sys.modules, 'ida_bytes', NS(
        get_flags=lambda addr: 0, is_code=lambda flags: False, has_user_name=lambda flags: False))
    monkeypatch.setitem(sys.modules, 'idautils', NS(Names=lambda: [], Heads=lambda: [ea]))
    monkeypatch.setattr(ex, '_func_start', lambda addr: False)
    monkeypatch.setattr(ex, 'user_tinfo', lambda addr: NS(get_size=lambda: 4))
    monkeypatch.setattr(ex, 'tinfo_text', lambda tif: 'struct ItemID')
    rows = ex.export_globals(set(), {})
    assert len(rows) == 1
    assert (rows[0]['address'], rows[0]['name'], rows[0]['type']) == ('0x00955FF4', '', 'struct ItemID')


@pytest.mark.parametrize('structured,expected', [(True, 1), (False, 0)])
def test_export_vtable_preserves_only_user_struct_type(monkeypatch, structured, expected):
    from types import SimpleNamespace as NS
    import export_symbols as ex
    ea = 0x8FC17C
    monkeypatch.setitem(sys.modules, 'ida_name', NS(get_name=lambda addr: 'vtbl_DrawInfo'))
    monkeypatch.setitem(sys.modules, 'ida_nalt', NS(is_userti=lambda addr: True))
    monkeypatch.setitem(sys.modules, 'ida_bytes', NS(
        get_flags=lambda addr: 0, is_code=lambda flags: False, has_user_name=lambda flags: True))
    monkeypatch.setitem(sys.modules, 'idautils', NS(Names=lambda: [(ea, 'vtbl_DrawInfo')], Heads=lambda: [ea]))
    monkeypatch.setattr(ex, '_func_start', lambda addr: False)
    monkeypatch.setattr(ex, 'user_tinfo', lambda addr: NS(is_struct=lambda: structured, get_size=lambda: 8))
    monkeypatch.setattr(ex, 'tinfo_text', lambda tif: 'DrawInfoVtable')
    rows = ex.export_globals({ea}, {ea: ['ACNL-F0712']})
    assert len(rows) == expected
    if expected:
        assert (rows[0]['type'], rows[0]['size'], rows[0]['refs']) == ('DrawInfoVtable', '8', 'ACNL-F0712')


@pytest.mark.parametrize('size,failed', [(8, False), (4, True)])
def test_import_vtable_keeps_struct_and_rejects_size_mismatch(monkeypatch, size, failed):
    from types import SimpleNamespace as NS
    monkeypatch.setattr(import_symbols, '_set_name', lambda *args: None)
    monkeypatch.setitem(sys.modules, 'ida_bytes', NS())  # 構造体をdwordへ作り直す呼出しがあれば失敗する
    monkeypatch.setitem(sys.modules, 'ida_offset', NS())
    monkeypatch.setitem(sys.modules, 'ida_segment', NS())
    monkeypatch.setitem(sys.modules, 'ida_nalt', NS(is_userti=lambda ea: True, get_tinfo=lambda tif, ea: True))
    monkeypatch.setitem(sys.modules, 'ida_typeinf', NS(
        tinfo_t=lambda: NS(is_struct=lambda: True, get_size=lambda: size)))
    rep = import_symbols.Report()
    import_symbols.import_vtables([{'address': '0x008FC17C', 'class': 'DrawInfo', 'count': '2'}], rep)
    result = rep.sections['vtables']
    assert bool(result['failed']) == failed
    assert result['ok'] == (0 if failed else 1)


@pytest.mark.parametrize('case,thumb', [('extend', False), ('shrink', False), ('tail', False),
                                       ('middle', False), ('new', True), ('wrong_mode', True)])
def test_function_boundaries(monkeypatch, case, thumb):
    from types import SimpleNamespace as NS
    ea, end = 0x1000, 0x1010
    funcs = {}
    tails = {}
    modes = {ea: 0, end: 0}
    def add(start, stop):
        funcs[start] = NS(start_ea=start, end_ea=stop, flags=0)
        return True
    if case == 'extend':
        add(ea, ea + 4)
        add(ea + 4, end)
    elif case == 'shrink':
        add(ea, end + 2)
    elif case == 'middle':
        add(ea - 4, end)
    elif case == 'tail':
        add(ea - 0x100, ea - 0xF0)
        tails[ea] = NS(start_ea=ea, end_ea=end, flags=1)
    elif case == 'wrong_mode':
        add(ea, end)
    def chunk(addr):
        return next((f for f in [*funcs.values(), *tails.values()]
                     if f.start_ea <= addr < f.end_ea), None)
    def get_func(addr):
        f = chunk(addr)
        return funcs[ea - 0x100] if f and f.flags else f
    def set_end(start, stop):
        f = funcs[start]
        # 拡張時の別関数と、命令途中の縮小を IDA と同様に拒む。
        if any(g.start_ea != start and start < g.start_ea < stop for g in funcs.values()):
            return False
        if case == 'shrink' and f.end_ea == end + 2:
            return False
        f.end_ea = stop
        return True
    def delete(start):
        return funcs.pop(start, None) is not None
    def remove_tail(f, start):
        return tails.pop(start, None) is not None
    monkeypatch.setitem(sys.modules, 'ida_funcs', NS(
        FUNC_TAIL=1, get_fchunk=chunk, get_func=get_func,
        get_next_fchunk=lambda addr: next(iter(sorted(
            (f for f in [*funcs.values(), *tails.values()] if f.start_ea > addr),
            key=lambda f: f.start_ea)), None),
        func_parent_iterator_t=lambda f: [ea - 0x100], remove_func_tail=remove_tail,
        append_func_tail=lambda *a: True, set_func_end=set_end, del_func=delete, add_func=add,
        get_func_cmt=lambda *a: 'preserved', set_func_cmt=lambda *a: True))
    monkeypatch.setitem(sys.modules, 'ida_idp', NS(str2reg=lambda name: 0))
    monkeypatch.setitem(sys.modules, 'ida_segregs', NS(
        SR_user=1, get_sreg=lambda addr, reg: modes.get(addr, 0),
        split_sreg_range=lambda addr, reg, val, source: modes.__setitem__(addr, val)))
    monkeypatch.setitem(sys.modules, 'ida_bytes', NS(DELIT_SIMPLE=0, del_items=lambda *a: True))
    monkeypatch.setitem(sys.modules, 'ida_ua', NS(create_insn=lambda ea: True))
    assert import_symbols._ensure_function(ea, end - ea, thumb) is None
    assert (get_func(ea).start_ea, get_func(ea).end_ea) == (ea, end)
    assert modes[ea] == int(thumb)
    if case == 'middle':
        assert funcs[ea - 4].end_ea == ea
    if case == 'tail':
        assert not tails
