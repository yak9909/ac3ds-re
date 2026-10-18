"""Ghidra を起動せず、入力検証と形式の変換を試験する。"""
import hashlib
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("ghidra_common", Path(__file__).parents[1] / "sync/ghidra/common.py")
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def image():
    data = bytes(range(32))
    info = {"code_sha256": hashlib.sha256(data).hexdigest(), "code_size": len(data),
            "segments": {"text": ["0x1000", "0x1008"], "rodata": ["0x1010", "0x1018"],
                         "data": ["0x1018", "0x1020"], "bss": ["0x1020", "0x1028"]}}
    return info, data


def test_memory_layout_uses_virtual_gaps_and_uninitialized_bss():
    info, data = image()
    segs = g.plan_segments(info, data)
    assert [(s["name"], s["offset"], s["write"], s["execute"]) for s in segs] == [
        (".text", 0, False, True), (".rodata", 16, False, False),
        (".data", 24, True, False), (".bss", None, True, False)]


def test_corrupted_image_rejected_before_ghidra():
    info, data = image()
    with pytest.raises(ValueError, match="SHA256"):
        g.plan_segments(info, b'X' + data[1:])
    info["code_size"] += 1
    with pytest.raises(ValueError, match="サイズ"):
        g.plan_segments(info, data)


@pytest.mark.parametrize("key,value", [("rodata", ["0x1004", "0x1010"]),
                                       ("data", ["0x1018", "0x1030"]),
                                       ("bss", ["0x1021", "0x1028"])])
def test_bad_ranges_rejected(key, value):
    info, data = image()
    info["segments"][key] = value
    with pytest.raises(ValueError):
        g.plan_segments(info, data)


def test_thumb_address_and_inclusive_end():
    assert g.function_range({"address": "0x00100001", "size": "12"}) == (0x100000, 0x10000B, True)
    with pytest.raises(ValueError):
        g.function_range({"address": "0x100000", "size": "0"})


def test_ida_c_conversion_preserves_signedness_and_pointer():
    assert g.prototype_declaration('unsigned __int64 *__fastcall(int x, unsigned __int16 *p)', 'test') == 'unsigned long long * test(int x, unsigned short *p);'
    assert '__usercall' in g.normalize_c('int __usercall(int a)')
    with pytest.raises(ValueError):
        g.prototype_declaration('int', 'test')


def test_function_start_comparison_does_not_pair_unrelated_functions():
    result = g.compare_starts({0x1000, 0x1010}, {0x1000, 0x1020})
    assert result["common"] == 1
    assert result["ida_only_count"] == result["ghidra_only_count"] == 1
    assert result["ida_only"] == ['0x00001010']


def test_export_index_requires_header_and_provenance(tmp_path):
    path = tmp_path / 'index.txt'
    path.write_text('idb_input_sha256: abc\nname\taddress\tfile\nfoo\t0x1001\tx.txt\n', encoding='utf-8')
    assert g.ida_starts(path, 'abc') == {0x1000}
    path.write_text('foo\t0x1000', encoding='utf-8')
    with pytest.raises(ValueError, match='ヘッダー'):
        g.ida_starts(path, 'abc')


def test_type_units_keep_pack_pragmas_and_forward_declarations():
    text = 'struct X;\n// type: X\n#pragma pack(push, 1)\nstruct X { int a; };\n#pragma pack(pop)\n// type: Y\ntypedef X Y;\n'
    units = g.type_units(text)
    assert [name for name, _ in units] == ['forward_declarations', 'X', 'Y']
    assert '#pragma pack(pop)' in units[1][1]
    assert g.type_units('typedef int Z;') == [('header', 'typedef int Z;')]


def test_export_index_with_other_build_is_rejected(tmp_path):
    path = tmp_path / 'index.txt'
    path.write_text('idb_input_sha256: other\nname\taddress\tfile\nfoo\t0x1000\tx.txt\n', encoding='utf-8')
    with pytest.raises(ValueError, match='ハッシュ'):
        g.ida_starts(path, 'expected')


def test_target_names_and_thumb_normalization():
    rows = [{"address": "0x1001", "name": "Alias"}]
    assert g.resolve_target('0x1001', []) == 0x1000
    assert g.resolve_target('Alias', rows) == 0x1000
    assert g.resolve_target('FUN_1000', [], [('FUN_1000', 0x1000)]) == 0x1000
    with pytest.raises(ValueError, match='一意'):
        g.resolve_target('Alias', rows, [('Alias', 0x2000)])
    with pytest.raises(ValueError):
        g.resolve_target('unknown', rows)


def test_global_cv_qualifiers_do_not_hide_array_or_pointer_shape():
    assert g.global_type_expression('const unsigned __int8[8]') == 'unsigned char[8]'
    assert g.global_type_expression('float * const') == 'float *'
    assert g.global_type_expression('MyconstType *') == 'MyconstType *'


def test_enum_bitmask_and_explicit_width():
    text, size = g.enum_declaration('enum __bitmask Flags { First = 1, Second = 32 };')
    assert '__bitmask' not in text and size is None
    declaration = 'enum Small : unsigned __int8 { One = 1 }'
    text, size = g.enum_declaration(declaration + ';')
    assert text == 'enum Small { One = 1 };' and size == 1
    assert g.global_type_expression('const struct ItemID *') == 'ItemID *'
    with pytest.raises(ValueError):
        g.enum_declaration('enum Strange : Missing { One = 1 };')


def test_workspace_discovery_for_checkout_and_nested_worktree(tmp_path, monkeypatch):
    workspace = tmp_path / 'workspace'
    workspace.mkdir()
    (workspace / 'workspace.toml').write_text('data="_local"', encoding='utf-8')
    checkout = workspace / 'ac3ds-re'
    worktree = workspace / '_local/worktrees/ac3ds-re/82'
    checkout.mkdir()
    worktree.mkdir(parents=True)
    assert g.discover_workspace(checkout) == workspace
    assert g.discover_workspace(worktree) == workspace
    assert g.discover_workspace(worktree, tmp_path / 'override') == tmp_path / 'override'
    with monkeypatch.context() as patch:
        patch.setattr(Path, 'is_file', lambda path: False)
        with pytest.raises(FileNotFoundError, match='workspace.toml'):
            g.discover_workspace(tmp_path / 'unrelated')


def test_ghidra_discovery_uses_catalog_version_and_explicit_override(tmp_path):
    (tmp_path / 'scripts').mkdir()
    (tmp_path / 'scripts/third_party.toml').write_text('[tools.ghidra]\nversion="12.1.4"\n', encoding='utf-8')
    for version in ('old', '12.1.4'):
        install = tmp_path / '_local/tools/ghidra' / version / 'distribution'
        (install / 'Ghidra').mkdir(parents=True)
        (install / 'Ghidra/application.properties').write_text('application.name=Ghidra', encoding='utf-8')
    expected = tmp_path / '_local/tools/ghidra/12.1.4/distribution'
    assert g.discover_ghidra(tmp_path) == expected
    assert g.discover_ghidra(tmp_path, tmp_path / 'custom') == tmp_path / 'custom'
    duplicate = expected.parent / 'another/Ghidra'
    duplicate.mkdir(parents=True)
    (duplicate / 'application.properties').write_text('', encoding='utf-8')
    with pytest.raises(ValueError, match='2 件'):
        g.discover_ghidra(tmp_path)
    (expected / 'Ghidra/application.properties').unlink()
    (duplicate / 'application.properties').unlink()
    with pytest.raises(ValueError, match='0 件'):
        g.discover_ghidra(tmp_path)


@pytest.mark.parametrize('target,rows,explicit,want', [
    ('0x1000', [], None, 'arm'),
    ('0x1001', [], None, 'thumb'),
    ('0x1000', [{'address':'0x1001'}], None, 'thumb'),
    ('Named', [{'address':'0x1000'}], None, 'arm'),
    ('Named', [{'address':'0x1001'}], None, 'thumb'),
    ('0x1001', [{'address':'0x1001'}], 'arm', 'arm'),
    ('0x1000', [{'address':'0x1000'}], 'thumb', 'thumb'),
])
def test_create_mode_precedence(target, rows, explicit, want):
    assert g.target_mode(target, 0x1000, rows, explicit) == want


def test_ambiguous_create_mode_requires_override():
    rows = [{'address':'0x1000'}, {'address':'0x1001'}]
    with pytest.raises(ValueError, match='曖昧'):
        g.target_mode('Named', 0x1000, rows)
    assert g.target_mode('Named', 0x1000, rows, 'thumb') == 'thumb'


@pytest.mark.parametrize('fail', [False, True])
def test_dump_copy_isolated_and_removed_even_on_error(tmp_path, monkeypatch, fail):
    import contextlib
    import sys
    from types import SimpleNamespace
    opened = []
    closed = []
    copied = []
    original = object()
    duplicate = object()
    copy_root = object()
    source = SimpleNamespace(copyTo=lambda root, monitor: copied.append(root))
    project = SimpleNamespace(getProjectData=lambda: SimpleNamespace(getFile=lambda name: source))
    copy_project = SimpleNamespace(getProjectData=lambda: SimpleNamespace(getRootFolder=lambda: copy_root),
                                   close=lambda: closed.append(True))

    def open_project(folder, name, create):
        opened.append(Path(folder))
        return copy_project

    @contextlib.contextmanager
    def program_context(owner, path):
        yield original if owner is project else duplicate

    monkeypatch.setitem(sys.modules, 'common', g)
    monkeypatch.setitem(sys.modules, 'pyghidra', SimpleNamespace(open_project=open_project,
                        program_context=program_context, task_monitor=lambda: None))
    backend_spec = importlib.util.spec_from_file_location('test_ghidra_backend',
                       Path(__file__).parents[1] / 'sync/ghidra/backend.py')
    backend = importlib.util.module_from_spec(backend_spec)
    backend_spec.loader.exec_module(backend)
    try:
        with backend.dump_program(project, 'independent', True, tmp_path) as program:
            assert program is duplicate and program is not original
            assert opened[0].is_dir()
            if fail:
                raise RuntimeError('decompiler failed')
    except RuntimeError:
        assert fail
    assert copied == [copy_root]
    assert closed == [True]
    assert not opened[0].exists()
