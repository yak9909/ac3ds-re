import json

import pytest
import yaml

import audit
import kb


DRAFT = """---
title: "下書き"
summary: "結論"
date: 2026-11-09
category: item
build: acnl_jpn_v15
confidence: MEDIUM
tool: Ghidra (WebChat)
addresses: [0x100000]
tags: []
supersedes: []
---
## 結論

本文

## 根拠

## 反証条件・未確認点
"""


def draft(repo, name="1", text=DRAFT, issue="125"):
    p = repo / "inbox" / "webchat" / issue / (name + ".md")
    kb.write_text(p, text)
    return p


def snapshot(repo):
    return {p.relative_to(repo).as_posix(): p.read_bytes()
            for p in repo.rglob("*") if p.is_file()}


@pytest.mark.parametrize("confidence", ["MEDIUM", "LOW"])
def test_draft_valid(repo, confidence):
    draft(repo, text=DRAFT.replace("confidence: MEDIUM", "confidence: " + confidence))
    assert kb.main(["lint"]) == 0
    assert kb.main(["lint", str(repo / "inbox/webchat/125/1.md")]) == 0


@pytest.mark.parametrize("old,new,message", [
    ('title: "下書き"\n', '', "必須項目が無い: title"),
    ('title: "下書き"', 'id: ACNL-F0001\ntitle: "下書き"', "下書きの鍵と並び"),
    ('title: "下書き"', 'by: gpt-6-sol\ntitle: "下書き"', "下書きの鍵と並び"),
    ('title: "下書き"\nsummary: "結論"', 'summary: "結論"\ntitle: "下書き"', "下書きの鍵と並び"),
    ('title: "下書き"', 'title: "重複"\ntitle: "下書き"', "下書きの鍵と並び"),
    ('category: item', 'category: unknown', "category が台帳に無い"),
    ('build: acnl_jpn_v15', 'build: unknown', "build が台帳に無い"),
    ('tags: []', 'tags: [unknown]', "tag が台帳に無い"),
    ('tags: []', 'tags: [{}]', "tag が台帳に無い"),
    ('addresses: [0x100000]', 'addresses: [true]', "addresses に整数でない値"),
    ('supersedes: []', 'supersedes: [ACNL-F9999]', "supersedes の参照先が無い"),
    ('confidence: MEDIUM', 'confidence: HIGH', "confidence の値が不正"),
    ('tags: []', 'tags:', "tags の型が違う"),
    ('## 結論', '', "本文の見出しが無い: ## 結論"),
    ('## 根拠', '', "本文の見出しが無い: ## 根拠"),
    ('## 反証条件・未確認点', '', "本文の見出しが無い: ## 反証条件・未確認点"),
])
def test_draft_invalid_is_atomic(repo, tmp_path, capsys, old, new, message):
    draft(repo)
    draft(repo, "2", DRAFT.replace(old, new))
    capsys.readouterr()
    assert kb.main(["lint", "--quiet"]) == 1
    lint_errors = capsys.readouterr().out
    assert message in lint_errors
    before = snapshot(repo)
    ledger = tmp_path / "state/ids.json"
    kb.write_text(ledger, json.dumps({"acnl": 42}))
    ledger_before = ledger.read_bytes()
    assert kb.main(["intake", "--issue", "125"]) == 1
    assert capsys.readouterr().out == lint_errors
    assert snapshot(repo) == before
    assert ledger.read_bytes() == ledger_before


@pytest.mark.parametrize("by", [None, "opus-5.5"])
def test_intake_sequence_cleanup_and_metadata(repo, tmp_path, capsys, by):
    for name in ("10", "2", "1"):
        draft(repo, name, DRAFT.replace('title: "下書き"', 'title: "' + name + '"'))
    draft(repo, issue="126")
    ledger = tmp_path / "state/ids.json"
    kb.write_text(ledger, json.dumps({"acnl": 98}))
    args = ["intake", "--issue", "125"] + (["--by", by] if by else [])
    assert kb.main(args) == 0
    assert capsys.readouterr().out.splitlines()[-3:] == ["ACNL-F0099", "ACNL-F0100", "ACNL-F0101"]
    records = kb.load_records()
    assert [r.get("title") for r in records] == ["1", "2", "10"]
    expected = yaml.safe_load(kb.FM_RE.match(kb.TEMPLATE.format(
        id="ACNL-F0099", title='""', date="2026-11-09", category="item",
        build="acnl_jpn_v15", tool="IDA")).group(1))
    for r in records:
        assert list(r.meta) == list(expected)
        assert r.get("by") == (by or "gpt-6-sol")
        assert r.get("addresses") == [0x100000]
        assert r.get("state") == "active"
        assert "本文" in r.raw
        assert r.path.parent.name == kb.folder_for(int(r.id.split("F")[1]))
    assert not (repo / "inbox/webchat/125").exists()
    assert (repo / "inbox/webchat/126/1.md").exists()
    assert kb.main(["lint", "--strict"]) == 0
    assert kb.main(["intake", "--issue", "126"]) == 0
    assert not (repo / "inbox").exists()


@pytest.mark.parametrize("path", ["inbox/1.md", "inbox/other/125/1.md", "inbox/webchat/x/1.md",
                                   "inbox/webchat/125/x.md", "inbox/webchat/125/1.txt",
                                   "inbox/webchat/125/deep/1.md"])
def test_inbox_paths(repo, path, capsys):
    assert audit.scan_file(path, DRAFT.encode(), [])
    kb.write_text(repo / path, DRAFT)
    assert kb.main(["lint"]) == 1
    assert "inbox/ に許可されていないファイル" in capsys.readouterr().out


def test_audit_valid_inbox():
    assert not audit.scan_file("inbox/webchat/125/1.md", DRAFT.encode(), [])


def test_intake_build_scope_and_invalid_by(repo, capsys):
    p = draft(repo, text=DRAFT.replace("acnl_jpn_v15", "hhd_jpn_v11"))
    before = snapshot(repo)
    assert kb.main(["intake", "--issue", "125", "--by", "not-a-registered-test-model"]) == 1
    assert snapshot(repo) == before
    assert kb.main(["intake", "--issue", "../125"]) == 1
    assert snapshot(repo) == before
    assert kb.main(["intake", "--issue", "125"]) == 0
    assert not p.exists()
    r, = kb.load_records()
    assert r.id == "HHD-F0001" and r.scope == "hhd"
    assert kb.main(["lint", "--strict"]) == 0
