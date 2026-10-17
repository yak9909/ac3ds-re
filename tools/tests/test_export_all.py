"""書き出しの形式・コメント・code.bin の位置計算（IDA 不要）。"""
import sys
from types import SimpleNamespace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "sync"))
import export_all as export
import codebytes
import idacommon as ic


def test_paths():
    assert export.function_path(0x123456, 'sub_123456') == 'functions/00100000/00123456_sub_123456.txt'
    path = export.function_path(0x200000, '../a<b>:c/日本語')
    assert Path(path).name.startswith('00200000_')
    assert '<' not in path and ':' not in path
    assert len(Path(export.function_path(1, 'a' * 200)).name) < 150


def test_comments():
    assert export.clean_comment('switch 4 cases') == ''
    assert export.clean_comment('人が書いた説明') == '人が書いた説明'
    assert export.clean_comment(None) == ''
    assert export.split_comment('DCB "a;b" ; unsigned int', ';') == ('DCB "a;b"', 'unsigned int')
    assert export.clean_pseudocode('  v = "https://x"; // unsigned int') == '  v = "https://x";'
    assert export.clean_pseudocode('  v = "a\\\"//b"; // 手書き') == '  v = "a\\\"//b"; // 手書き'


def test_hexrays_unavailable_still_outputs_disassembly(monkeypatch):
    def unavailable():
        raise RuntimeError('no license')
    modules = dict(
        ida_hexrays=SimpleNamespace(init_hexrays_plugin=unavailable),
        ida_bytes=SimpleNamespace(get_flags=lambda _: 1, is_code=lambda _: True, get_cmt=lambda *args: None),
        ida_funcs=SimpleNamespace(get_func=lambda _: object(), get_func_cmt=lambda *args: None),
        ida_idp=SimpleNamespace(str2reg=lambda _: 0),
        ida_lines=SimpleNamespace(tag_remove=lambda s: s, generate_disasm_line=lambda *args: 'BX LR ; unsigned int'),
        ida_segregs=SimpleNamespace(get_sreg=lambda ea, _: int(ea == 0x1004)),
        ida_name=SimpleNamespace(get_name=lambda ea: f'sub_{ea:X}'),
        idautils=SimpleNamespace(FuncItems=lambda _: [0x1000, 0x1004], DataRefsFrom=lambda _: []),
    )
    for name, module in modules.items():
        monkeypatch.setitem(sys.modules, name, module)
    # 引数コメントの判定用モジュールを実際の IDA なしで読み込める状態にする。
    import export_symbols
    monkeypatch.setattr(export_symbols, 'is_arg_comment', lambda *args: False)
    reader = export.IdaReader()
    body, status = reader.function(0x1000, [], [])
    assert status == 'failed: Hex-Rays unavailable: no license'
    assert '0x00001000 ARM' in body and '0x00001004 Thumb' in body
    assert 'BX LR' in body and 'unsigned int' not in body
    assert '[pseudocode unavailable]' in body


def test_index_roundtrip(tmp_path):
    rows = [dict(name='日本語\tname', address='0x00200000', file='a.txt', decompile='failed: error', symbols_commit='old'),
            dict(name='start', address='0x00100000', file='b.txt', decompile='ok', symbols_commit='new')]
    path = tmp_path / 'index.txt'
    export.write_text(path, export.index_text(rows, 'sha', 'new', True))
    sha, actual = export.read_index(path)
    assert sha == 'sha'
    assert actual == [rows[1], rows[0]]
    assert path.read_bytes().startswith(export.NOTE.encode() + b'\n')
    assert b'\r' not in path.read_bytes()


@pytest.mark.parametrize('build', ['acnl_jpn_v15', 'hhd_jpn_v11'])
def test_real_segment_offsets(build):
    info = ic.build_info(build)
    ranges = ic.seg_ranges(info)
    for name in ('text', 'rodata', 'data'):
        start, end = ranges[name]
        assert codebytes.file_offset(info, start, end - start) == start - ranges['text'][0]
    with pytest.raises(ValueError):
        codebytes.file_offset(info, ranges['bss'][0], 1)
    with pytest.raises(ValueError):
        codebytes.file_offset(info, ranges['text'][1] - 1, 2)


def test_byte_reads(tmp_path, capsys):
    info = dict(segments=dict(text=['0x1000', '0x1004'], data=['0x1008', '0x100C'], bss=['0x100C', '0x1010']))
    path = tmp_path / 'code.bin'
    path.write_bytes(bytes(range(12)))
    assert codebytes.read_bytes(path, info, 0x1008, 4) == bytes(range(8, 12))
    for addr, length in ((0xFFF, 1), (0x1003, 2), (0x1004, 1), (0x100C, 1), (0x1000, 0), (0x1000, -1)):
        with pytest.raises(ValueError):
            codebytes.read_bytes(path, info, addr, length)
    path.write_bytes(b'')
    with pytest.raises(ValueError, match='短い'):
        codebytes.read_bytes(path, info, 0x1000, 4)


def test_cli(tmp_path, capsys):
    path = tmp_path / 'code.bin'
    path.write_bytes(b'\x01\xAB\x00\xFF')
    assert codebytes.main(['--build', 'acnl_jpn_v15', '--code', str(path), '0x100000', '4']) == 0
    assert capsys.readouterr().out == '01 AB 00 FF\n'


def test_partial_export_keeps_old_provenance_and_removes_renamed_file(tmp_path, monkeypatch):
    names = {0x1000: 'first', 0x2000: 'caller', 0x3000: 'unrelated'}
    class Reader:
        name = staticmethod(lambda ea: names[ea])
        edges = staticmethod(lambda ea: [(ea, 0x1000)] if ea == 0x2000 else [])
        function = staticmethod(lambda ea, callers, callees: ('body', 'failed: test' if ea == 0x3000 else 'ok'))
    modules = dict(
        ida_auto=SimpleNamespace(auto_wait=lambda: None),
        ida_bytes=SimpleNamespace(),
        ida_funcs=SimpleNamespace(get_func=lambda ea: SimpleNamespace(start_ea=ea) if ea in names else None),
        ida_name=SimpleNamespace(get_name_ea=lambda _, name: next((ea for ea, n in names.items() if n == name), -1)),
        ida_nalt=SimpleNamespace(retrieve_input_file_sha256=lambda: b'\xAB'),
        ida_idaapi=SimpleNamespace(BADADDR=-1),
        idautils=SimpleNamespace(Functions=lambda: iter(names), Heads=lambda: iter(())),
    )
    for name, module in modules.items():
        monkeypatch.setitem(sys.modules, name, module)
    monkeypatch.setattr(export, 'IdaReader', Reader)
    export.export('test', tmp_path, 'old', [])
    first = tmp_path / export.function_path(0x1000, 'first')
    assert first.exists()
    names[0x1000] = 'renamed'
    result = export.export('test', tmp_path, 'new', ['0x1001'])
    assert result['updated'] == 2  # Thumb ポインタ指定を正規化し、直接の呼び出し元も更新。
    assert not first.exists()
    _, rows = export.read_index(tmp_path / 'index.txt')
    assert [r['symbols_commit'] for r in rows] == ['new', 'new', 'old']
    _, failures = export.read_index(tmp_path / 'decompile_failures.txt')
    assert len(failures) == 1 and failures[0]['name'] == 'unrelated'
    for path in tmp_path.rglob('*.txt'):
        assert path.read_text(encoding='utf-8').startswith(export.NOTE + '\n')
    modules['ida_nalt'].retrieve_input_file_sha256 = lambda: b'\xCD'
    with pytest.raises(ValueError, match='SHA256'):
        export.export('test', tmp_path, 'wrong', ['renamed'])
