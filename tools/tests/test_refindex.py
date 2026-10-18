import csv
from pathlib import Path

import pytest

import kb
import refindex


def test_gateway_write_and_control_codes():
    text = ("[sample]\n00100000 AABBCCDD\n10100002 00001234\n20100004 00000056\n"
            "D2000000 00000000\nDD000000 00000001\n30100008 00000001\n"
            "50100008 00000001\nB0100008 00000000\nC0000000 00000001\n"
            "E0100010 00000009\n00123456 00000000\n00123458 00000000\n"
            "00100020 11223344\n[0x00100030]\n")
    assert list(refindex.addresses(text, gateway=True)) == [
        (0x100000, 2), (0x100002, 3), (0x100004, 4), (0x100020, 14)]


def test_hex_notation():
    assert list(refindex.addresses(
        "a=0x00100000; b=0x100020u; c=0x00100000;\n"
        "0x1000 0x123456789 bad0x100000 0x100000xyz\n")) == [
            (0x100000, 1), (0x100020, 1)]


def test_address_range_hex():
    assert list(refindex.addresses(
        "0x00000000 0x000000FF 0x000FFFFF 0x00100000 "
        "0x3FFFFFFF 0x40000000 0xFFFFFFFF\n")) == [
            (0x00100000, 1), (0x3FFFFFFF, 1)]


def test_address_range_gateway():
    assert list(refindex.addresses(
        "00000000 00000000\n000000FF 00000000\n000FFFFF 00000000\n"
        "100FFFFF 00000000\n200FFFFF 00000000\n00100000 00000000\n"
        "10100000 00000000\n20100000 00000000\n0FFFFFFF 00000000\n"
        "40000000 00000000\n", gateway=True)) == [
            (0x00100000, 6), (0x00100000, 7), (0x00100000, 8), (0x0FFFFFFF, 9)]


def sample(repo):
    refs = repo / "_local/refs"
    (repo / "meta/references.toml").write_text('''
[refs.CHEATS]
path = "v1/CHEATS"
build = "acnl_jpn_v15"
[refs.CTRPF_PROJECTS]
path = "v1/CTRPF PROJECTS"
[refs.TEXTS]
path = "v1/TEXTS"
[refs.IDS]
path = "v1/IDS"
''', encoding="utf-8")
    files = {
        "CHEATS/sample.txt": "[secret cheat name]\n00100000 DEADBEEF\nD2000000 00000000\n000000FF 00000000\n",
        "CHEATS/INDEX.md": "0x00100000 duplicated index\n",
        "CHEATS/note.cpp": "auto p = 0x00100004; // secret comment\n",
        "CTRPF PROJECTS/any.cpp": "auto p = 0x00100000;\n",
        "CTRPF PROJECTS/hhd_jpn_v11/known.hpp": "auto p = 0x00100000;\n",
        "TEXTS/memo.txt": "日本語 0x00100008\n0x00000000 0x000000FF 0x40000000\n",
        "IDS/list.txt": "0x00100000 secret ID list\n",
    }
    for name, text in files.items():
        path = refs / "v1" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8-sig")
    (refs / "v1/TEXTS/image.png").write_bytes(b"0x00100010")
    (refs / "v1/TEXTS/binary.txt").write_bytes(b"\0 0x00100010")
    (refs / "v1/TEXTS/cp932.txt").write_bytes("日本語 0x0010000C\n".encode("cp932"))
    return refs


def test_generate_and_lookup(repo):
    refs = sample(repo)
    output = refindex.index_dir(repo)
    assert refindex.main(["--refs-root", str(refs), "--output-dir", str(output)]) == 0
    index = output / "addresses.tsv"
    original = index.read_bytes()
    assert refindex.generate(repo, refs, output) == 6
    assert index.read_bytes() == original
    text = original.decode("utf-8")
    assert "DEADBEEF" not in text and "secret" not in text and "IDS" not in text
    assert "D2000000" not in text and "binary.txt" not in text and "image.png" not in text
    rows = list(refindex.lookup(output, 0x100000, "acnl_jpn_v15"))
    assert {row["key"] for row in rows} == {"CHEATS", "CTRPF_PROJECTS"}
    assert {row["build"] for row in rows} == {"acnl_jpn_v15", "unknown"}
    assert all(row["line"] in {"1", "2"} for row in rows)
    other = list(refindex.lookup(output, 0x100000, "hhd_jpn_v11"))
    assert {row["build"] for row in other} == {"hhd_jpn_v11", "unknown"}
    with index.open(encoding="utf-8", newline="") as stream:
        assert set(next(csv.DictReader(stream, delimiter="\t"))) == set(refindex.FIELDS)


def test_addr_with_and_without_index(repo, capsys):
    assert kb.main(["addr", "0x100000"]) == 0
    assert "参考資料" not in capsys.readouterr().out
    refs = sample(repo)
    refindex.generate(repo, refs, refindex.index_dir(repo))
    assert kb.main(["addr", "0x100000"]) == 0
    out = capsys.readouterr().out
    assert "記録:" in out and "参考資料（LOW、一次証拠ではない）:" in out
    assert "CHEATS v1/CHEATS/sample.txt:2（build=acnl_jpn_v15）" in out
    assert "any.cpp:1（build=不明）" in out
    assert "known.hpp" not in out and "DEADBEEF" not in out and "secret" not in out
    assert kb.main(["addr", "0x100000", "--build", "hhd_jpn_v11"]) == 0
    out = capsys.readouterr().out
    assert "known.hpp:1（build=hhd_jpn_v11）" in out and "sample.txt" not in out
    assert kb.main(["addr", "0x999999"]) == 0
    assert "参考資料" not in capsys.readouterr().out


@pytest.mark.parametrize("count, options, shown", [
    (20, [], 20), (21, [], 20), (25, [], 20),
    (25, ["--ref-limit", "2"], 2), (25, ["--ref-limit", "0"], 0),
])
def test_addr_reference_limit(repo, capsys, count, options, shown):
    refs = sample(repo)
    (refs / "v1/CTRPF PROJECTS/any.cpp").write_text(
        "auto p = 0x00100000;\n" * (count - 1), encoding="utf-8")
    refindex.generate(repo, refs, refindex.index_dir(repo))
    assert kb.main(["addr", "0x100000", *options]) == 0
    out = capsys.readouterr().out.split("参考資料（LOW、一次証拠ではない）:\n", 1)[1]
    assert out.count("（build=") == shown
    if count > shown:
        assert "ほか %d 件" % (count - shown) in out
    else:
        assert "ほか" not in out


def test_addr_negative_reference_limit(repo, capsys):
    assert kb.main(["addr", "0x100000", "--ref-limit", "-1"]) == 2
    assert "--ref-limit は0以上" in capsys.readouterr().err


def test_local_dir_worktree_and_workspace(tmp_path, monkeypatch):
    monkeypatch.delenv("AC3DS_WORKSPACE", raising=False)
    workspace = tmp_path / "workspace"
    local = workspace / "_local"
    repo = local / "worktrees/ac3ds-re/94"
    repo.mkdir(parents=True)
    assert refindex.local_dir(repo) == local
    monkeypatch.setenv("AC3DS_WORKSPACE", str(workspace))
    assert refindex.local_dir(Path("unrelated")) == local
