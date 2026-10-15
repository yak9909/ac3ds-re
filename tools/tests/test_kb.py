import json
import os
import subprocess
import sys
from pathlib import Path

import kb

TOOLS = Path(kb.__file__).resolve().parent


def run(*args):
    return kb.main(list(args))


def new(scope="acnl", cat="item", title="t"):
    return run("new", "--scope", scope, "--category", cat, "--title", title)


def recpath(repo, rid, scope="acnl"):
    n = int(rid.split("F")[1])
    return repo / "findings" / scope / kb.folder_for(n) / (rid + ".md")


def edit(repo, rid, old, new_, scope="acnl"):
    p = recpath(repo, rid, scope)
    t = p.read_text(encoding="utf-8")
    assert old in t, old
    p.write_text(t.replace(old, new_), encoding="utf-8", newline="\n")


def test_new_template_and_sequence(repo):
    assert new(title='あ"い') == 0
    p1 = recpath(repo, "ACNL-F0001")
    assert p1.exists() and p1.parent.name == "0000-0099"
    text = p1.read_text(encoding="utf-8")
    assert text.startswith("---\nid: ACNL-F0001\naliases: []\n")
    assert "confidence: LOW          # LOW / MEDIUM / HIGH" in text
    assert 'superseded_by: ""\ncorrected_by: []\n' in text
    assert "build: acnl_jpn_v15" in text
    assert "\r" not in text
    new()
    assert recpath(repo, "ACNL-F0002").exists()
    new("hhd")
    assert "build: hhd_jpn_v11" in recpath(repo, "HHD-F0001", "hhd").read_text(encoding="utf-8")
    assert kb.Rec(p1, "acnl").meta["title"] == 'あ"い'


def test_new_bad_category(repo):
    assert new(cat="nope") == 2
    assert new("3ds", "item") == 2
    assert new("3ds", "sdk") == 0
    assert new("acnl", "_triage") == 0


def test_numbering_repo_max_and_ledger(repo, tmp_path):
    new()
    d = repo / "findings/acnl/0400-0499"
    d.mkdir(parents=True)
    src = recpath(repo, "ACNL-F0001").read_text(encoding="utf-8")
    (d / "ACNL-F0412.md").write_text(src.replace("F0001", "F0412"), encoding="utf-8")
    new()
    assert recpath(repo, "ACNL-F0413").exists()
    (tmp_path / "state" / "ids.json").write_text(json.dumps({"acnl": 900}))
    new()
    assert recpath(repo, "ACNL-F0901").exists()
    assert recpath(repo, "ACNL-F0901").parent.name == "0900-0999"


def test_concurrent_numbering(repo):
    procs = [subprocess.Popen([sys.executable, str(TOOLS / "kb.py"), "new", "--scope", "acnl", "--category", "item",
                               "--title", "c"], env=dict(os.environ), stdout=subprocess.PIPE) for _ in range(8)]
    for p in procs:
        p.communicate()
        assert p.returncode == 0
    files = sorted((repo / "findings/acnl").rglob("*.md"))
    assert [f.stem for f in files] == ["ACNL-F%04d" % i for i in range(1, 9)]


def test_index_deterministic(repo):
    new()
    new(cat="ui")
    run("index")
    snap = {p: p.read_bytes() for p in (repo / "findings").rglob("*.md") if "-F0" not in p.name}
    assert snap
    run("index")
    assert snap == {p: p.read_bytes() for p in snap}
    for b in snap.values():
        assert b.decode("utf-8").split("\n")[0] == kb.GENERATED_NOTE
    assert (repo / "findings/acnl/by-category/item.md").exists()
    idx = (repo / "findings/INDEX.md").read_text(encoding="utf-8")
    assert "| acnl | 2 | 2 |" in idx and "未レビュー" in idx


def test_index_duplicates_and_unrated(repo):
    new()
    new()
    for i in (1, 2):
        edit(repo, "ACNL-F000%d" % i, "addresses: []", "addresses: [0x1000]")
        edit(repo, "ACNL-F000%d" % i, "by: auto", "by: gpt-6")
    run("index")
    idx = (repo / "findings/INDEX.md").read_text(encoding="utf-8")
    assert "0x00001000: ACNL-F0001, ACNL-F0002" in idx
    assert "- ACNL-F0001" in idx.split("要再解析")[1].split("未レビュー")[0]


def test_search_synonyms(repo, capsys):
    new(title="x")
    edit(repo, "ACNL-F0001", "## 結論\n", "## 結論\nSWKBD を呼ぶ\n")
    new(title="y")
    capsys.readouterr()
    run("search", "keyboard")
    out = capsys.readouterr().out
    assert "ACNL-F0001" in out and "ACNL-F0002" not in out and "SWKBD" in out
    run("search", "キーボード", "--scope", "hhd")
    assert capsys.readouterr().out == ""


def test_show_alias_and_tier(repo, capsys):
    new()
    edit(repo, "ACNL-F0001", "aliases: []", "aliases: [OLD-1]")
    capsys.readouterr()
    assert run("show", "OLD-1") == 0
    assert capsys.readouterr().out.startswith("格付け: 未記入")
    edit(repo, "ACNL-F0001", "by: auto", "by: claude-sonnet-5-5")
    run("show", "ACNL-F0001")
    assert capsys.readouterr().out.startswith("格付け: A")
    edit(repo, "ACNL-F0001", "by: claude-sonnet-5-5", "by: mystery")
    run("show", "ACNL-F0001")
    assert capsys.readouterr().out.startswith("格付け: C")
    assert run("show", "NOPE") == 1


def test_addr(repo, capsys, tmp_path):
    new()
    edit(repo, "ACNL-F0001", "addresses: []", "addresses: [0x100010]")
    capsys.readouterr()
    run("addr", "0x100020")
    out = capsys.readouterr().out
    assert "symbols に該当なし" in out and "ACNL-F0001" not in out
    sym = repo / "symbols/acnl_jpn_v15"
    sym.mkdir(parents=True)
    (sym / "functions.csv").write_text("address,size,name,prototype,confidence,source,refs,clone_of\n"
                                       "0x00100000,0x40,Foo_Bar,void f(),,analysis,,\n", encoding="utf-8")
    (sym / "globals.csv").write_text("address,size,name,type,confidence,source,refs\n"
                                     "0x00900000,4,g_X,int,,analysis,\n", encoding="utf-8")
    (tmp_path / "state" / "issues.json").write_text(json.dumps([
        {"number": 7, "title": "open", "body": "see 0x00100020 here", "state": "open"},
        {"number": 8, "title": "closed", "body": "0x100020", "state": "closed"}]), encoding="utf-8")
    run("addr", "0x100020")
    out = capsys.readouterr().out
    assert "Foo_Bar" in out and "ACNL-F0001" in out and "#7" in out and "#8" not in out
    run("addr", "0x100040")
    assert "Foo_Bar" not in capsys.readouterr().out
    run("addr", "0x900002")
    assert "g_X" in capsys.readouterr().out


def lint_out(capsys):
    capsys.readouterr()
    rc = run("lint")
    return rc, capsys.readouterr().out


def test_lint_clean_and_errors(repo, capsys):
    new(title="x")
    new(title="b")
    run("index")
    rc, out = lint_out(capsys)
    assert rc == 0, out
    cases = [
        ("category: item", "category: bogus", "category が台帳に無い"),
        ("build: acnl_jpn_v15", "build: zzz", "build が台帳に無い"),
        ("tags: []", "tags: [nosuchtag]", "tag が台帳に無い"),
        ("confidence: LOW ", "confidence: MAYBE ", "confidence の値が不正"),
        ("by: auto", "by: nobody", "by が models.toml に無い"),
        ("state: active", "state: superseded", "superseded_by が空"),
        ("supersedes: []", "supersedes: [ACNL-F0999]", "参照先が無い"),
        ('duplicate_of: ""', "duplicate_of: ACNL-F0999", "参照先が無い"),
        ("addresses: []", "addresses: [abc]", "整数でない"),
        ('title: "x"', "title:", "空（null）"),
        ("aliases: []", "aliases: [ACNL-F0002]", "重複"),
        ("id: ACNL-F0001", "id: ACNL-F0003", "ID"),
    ]
    for old, nw, msg in cases:
        edit(repo, "ACNL-F0001", old, nw)
        rc, out = lint_out(capsys)
        assert rc == 1 and msg in out, (nw, out)
        edit(repo, "ACNL-F0001", nw, old)
    rc, out = lint_out(capsys)
    assert rc == 0, out


def test_consolidated_into_topic_or_record(repo, capsys):
    new(title="first")
    new(title="second")
    topic = repo / "topics/acnl/item.md"
    topic.parent.mkdir(parents=True)
    topic.write_text("# item\n", encoding="utf-8")
    edit(repo, "ACNL-F0001", "state: active ", "state: consolidated ")
    edit(repo, "ACNL-F0001", 'consolidated_into: ""', "consolidated_into: topics/acnl/item.md")
    run("index")
    assert run("lint", "--strict") == 0
    capsys.readouterr()
    assert run("show", "ACNL-F0001") == 0
    assert "統合先: topics/acnl/item.md" in capsys.readouterr().out
    for path in (repo / "findings/acnl/INDEX.md", repo / "findings/acnl/by-category/item.md"):
        assert "| ACNL-F0001 | first |" in path.read_text(encoding="utf-8")
        assert "| topics/acnl/item.md |" in path.read_text(encoding="utf-8")

    edit(repo, "ACNL-F0001", "topics/acnl/item.md", "ACNL-F0002")
    assert lint_out(capsys)[0] == 0
    edit(repo, "ACNL-F0001", "ACNL-F0002", "ACNL-F0999")
    rc, out = lint_out(capsys)
    assert rc == 1 and "consolidated_into の参照先が無い: ACNL-F0999" in out
    edit(repo, "ACNL-F0001", "ACNL-F0999", "topics/acnl/missing.md")
    rc, out = lint_out(capsys)
    assert rc == 1 and "consolidated_into の参照先が無い: topics/acnl/missing.md" in out
    (repo / "outside.md").write_text("outside\n", encoding="utf-8")
    edit(repo, "ACNL-F0001", "topics/acnl/missing.md", "topics/../outside.md")
    assert "consolidated_into の参照先が無い" in lint_out(capsys)[1]
    edit(repo, "ACNL-F0001", "topics/../outside.md", '""')
    rc, out = lint_out(capsys)
    assert rc == 1 and "state consolidated なのに consolidated_into が空" in out


def test_lint_missing_field_and_source_blank(repo, capsys):
    new()
    run("index")
    edit(repo, "ACNL-F0001", "confidence: LOW ", 'confidence: "" ')
    rc, out = lint_out(capsys)
    assert rc == 1 and "confidence" in out
    edit(repo, "ACNL-F0001", "tool: IDA\n", "tool: IDA\nsource: old.md:10\n")
    rc, out = lint_out(capsys)
    assert rc == 0, out
    edit(repo, "ACNL-F0001", "tool: IDA\n", "")
    rc, out = lint_out(capsys)
    assert rc == 1 and "必須項目が無い: tool" in out


def test_lint_stale_generated(repo, capsys):
    new()
    rc, out = lint_out(capsys)
    assert rc == 0 and "生成物が古い" in out
    assert run("lint", "--strict") == 1
    run("index")
    rc, out = lint_out(capsys)
    assert rc == 0 and "古い" not in out


def test_stamp_overwrites_and_restores(repo, capsys):
    new()
    edit(repo, "ACNL-F0001", "by: auto", "by: forged")
    edit(repo, "ACNL-F0001", 'original_by: ""', "original_by: me")
    edit(repo, "ACNL-F0001", "reviewed_by: []", "reviewed_by: [opus-5.5]")
    edit(repo, "ACNL-F0001", "state: active ", "state: superseded ")
    p = recpath(repo, "ACNL-F0001")
    assert run("stamp", "--model", "claude-sonnet-5-5", str(p)) == 0
    t = p.read_text(encoding="utf-8")
    assert "by: sonnet-5.5\n" in t and 'original_by: ""' in t and "reviewed_by: []" in t
    assert "state: active            # active / consolidated" in t
    assert "管理項目" in capsys.readouterr().err
    assert run("stamp", "--model", "unknown-model", str(p)) == 2
    os.environ["AC3DS_MODEL"] = "opus-5.5"
    try:
        run("stamp", "--self", str(p))
    finally:
        del os.environ["AC3DS_MODEL"]
    assert "by: opus-5.5\n" in p.read_text(encoding="utf-8")


def test_stamp_skips_legacy_source(repo, capsys):
    new()
    new()
    edit(repo, "ACNL-F0001", "tool: IDA\n", "tool: IDA\nsource: old.md:10\n")
    edit(repo, "ACNL-F0001", "by: auto", "by: forged")
    edit(repo, "ACNL-F0001", 'original_by: ""', "original_by: me")
    edit(repo, "ACNL-F0001", "state: active ", "state: superseded ")
    p1, p2 = recpath(repo, "ACNL-F0001"), recpath(repo, "ACNL-F0002")
    before = p1.read_text(encoding="utf-8")
    capsys.readouterr()
    assert run("stamp", "--model", "claude-sonnet-5-5", str(p1), str(p2)) == 0
    assert p1.read_text(encoding="utf-8") == before
    out, err = capsys.readouterr()
    assert "ACNL-F0001.md 旧記録のため飛ばした（by は forged のまま）" in out
    assert "管理項目" not in err
    assert "by: sonnet-5.5\n" in p2.read_text(encoding="utf-8")


def test_stamp_untracked_autodetect(repo):
    g = os.environ.get("AC3DS_GIT") or "git"
    subprocess.run([g, "init", "-q"], cwd=repo, check=True)
    new()
    run("stamp", "--model", "opus-5.5")
    assert "by: opus-5.5\n" in recpath(repo, "ACNL-F0001").read_text(encoding="utf-8")


def test_tags_and_stubs(repo, capsys):
    assert run("tags") == 0
    assert "keyboard" in capsys.readouterr().out
    assert run("impact", "X") == 0
    assert "段階1b" in capsys.readouterr().out


def test_corrected_by_lint_and_display(repo, capsys):
    new(title="first")
    new(title="second")
    edit(repo, "ACNL-F0001", "corrected_by: []", "corrected_by: [ACNL-F0002]")
    run("index")
    assert lint_out(capsys)[0] == 0
    run("show", "ACNL-F0001")
    assert capsys.readouterr().out.startswith("訂正: ACNL-F0002\n格付け:")
    run("search", "first")
    assert "ACNL-F0001  [未記入/active] 訂正あり" in capsys.readouterr().out
    for path in (repo / "findings/acnl/INDEX.md", repo / "findings/acnl/by-category/item.md"):
        assert "| ACNL-F0001 | first |" in path.read_text(encoding="utf-8")
        assert "訂正あり |" in path.read_text(encoding="utf-8")
    edit(repo, "ACNL-F0001", "corrected_by: [ACNL-F0002]", "corrected_by: [ACNL-F0999]")
    assert "corrected_by の参照先が無い" in lint_out(capsys)[1]
    edit(repo, "ACNL-F0001", "corrected_by: [ACNL-F0999]", "corrected_by: [ACNL-F0001]")
    assert "自分自身" in lint_out(capsys)[1]
    edit(repo, "ACNL-F0001", "corrected_by: [ACNL-F0001]\n", "")
    assert lint_out(capsys)[0] == 0


def test_relate_partial_full_dry_run_and_conflict(repo, tmp_path, capsys):
    for _ in range(4):
        new()
    p = recpath(repo, "ACNL-F0001")
    edit(repo, "ACNL-F0001", "corrected_by: []\n", "")
    edit(repo, "ACNL-F0001", 'superseded_by: ""', 'superseded_by: "" # keep')
    before = p.read_text(encoding="utf-8")
    tsv = tmp_path / "relations.tsv"
    tsv.write_text("before\tafter\tkind\nACNL-F0001\tACNL-F0002\tpartial\n"
                   "ACNL-F0001\tACNL-F0002\tpartial\nACNL-F0003\tACNL-F0004\tfull\n", encoding="utf-8")
    capsys.readouterr()
    assert run("relate", "--file", str(tsv), "--dry-run") == 0
    assert "ACNL-F0001: 訂正: ACNL-F0002" in capsys.readouterr().out
    assert p.read_text(encoding="utf-8") == before
    assert run("relate", "--file", str(tsv)) == 0
    assert 'superseded_by: "" # keep\ncorrected_by: ["ACNL-F0002"]\n---' in p.read_text(encoding="utf-8")
    assert "state: active" in p.read_text(encoding="utf-8")
    p3 = recpath(repo, "ACNL-F0003")
    assert "state: superseded " in p3.read_text(encoding="utf-8")
    assert "superseded_by: ACNL-F0004" in p3.read_text(encoding="utf-8")
    run("index")
    assert lint_out(capsys)[0] == 0
    capsys.readouterr()
    assert run("relate", "--file", str(tsv)) == 0
    assert capsys.readouterr().out == ""
    tsv.write_text("before\tafter\tkind\nACNL-F0003\tACNL-F0002\tfull\n", encoding="utf-8")
    assert run("relate", "--file", str(tsv)) == 0
    assert "既に" in capsys.readouterr().err
    assert "superseded_by: ACNL-F0004" in p3.read_text(encoding="utf-8")
    run("show", "ACNL-F0003")
    assert capsys.readouterr().out.startswith("置き換え: ACNL-F0004")


def test_relate_invalid_input_is_atomic(repo, tmp_path, capsys):
    new()
    new()
    p = recpath(repo, "ACNL-F0001")
    before = p.read_bytes()
    tsv = tmp_path / "bad.tsv"
    for bad in ("ACNL-F0999\tpartial", "ACNL-F0001\tpartial", "ACNL-F0002\tunknown"):
        tsv.write_text("before\tafter\tkind\nACNL-F0001\tACNL-F0002\tpartial\n"
                       "ACNL-F0001\t" + bad + "\n", encoding="utf-8")
        assert run("relate", "--file", str(tsv)) == 1
        assert p.read_bytes() == before
        capsys.readouterr()
