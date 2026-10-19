import os
import subprocess

import audit


def reasons(text, path="docs/a.md", allow=()):
    return [p.reason for p in audit.scan_text(path, text, list(allow))]


def test_personal_paths():
    assert any("Windows" in r for r in reasons("see C:" + "\\Users\\alice\\x"))
    assert any("Windows" in r for r in reasons("D:/" + "Users/bob/x"))
    assert any("/home" in r for r in reasons("at /home/" + "carol/x"))
    assert any("/Users" in r for r in reasons("at /Users/" + "dave/x"))
    assert not reasons("C:" + "\\Users\\Public\\x and C:\\Users\\<name>\\x and /home/<user>/")
    assert not reasons("see ~/x and /usr/home")


def test_email():
    assert reasons("mail " + "bob" + "@" + "gmail.com")
    assert not reasons("noreply" + "@anthropic.com a@users.noreply.github.com b@example.com c@example.org")


def test_ipv4():
    assert reasons("host 192.168." + "1.20 ok")
    assert reasons("203.0." + "113.5")
    assert not reasons("0x1234ABCD 0x12345678 0.0.0.0 127.0.0.1 255.255.255.255")
    assert not reasons("v1.3.0.0 and version 10.20.30.40 and a1.2.3.4 and 1.3.0.0")
    assert not reasons("1.2.3.4.5")
    assert not reasons("999.1.1.1")


def test_long_lines_are_fast():
    import time
    n = 40000
    lines = ["a" * n + "@" + "b" * n, "a" * (2 * n), "a@" * n, "a." * n + "@" + "b." * n,
             "x:" + "/" * n, "1." * n, "192.168." + "1.1 " + " " * n, "sk-" + "a" * n, "A" * n + "1" * n,
             "/hom" + "e/" + "a" * n, ("a" * 10 + "@") * 4000]
    for t in lines:
        s = time.perf_counter()
        audit.scan_text("docs/a.md", t, [])
        assert time.perf_counter() - s < 1.0, t[:20]
    assert reasons("mail " + "bob" + "@" + "gmail.com.")
    assert not reasons("x@" + "b" * 100)


def test_serial():
    assert reasons("SN: " + "CTR" + "123456789")
    assert not reasons("ABCDEFGH123456789")


def test_secrets_not_echoed():
    secret = "ghp_" + "a" * 30
    ps = audit.scan_text("docs/a.md", "tok=" + secret, [])
    assert ps and "ghp_" not in str(ps[0])
    for s in ("sk-ant-" + "x" * 12, "sk-" + "A" * 24, "AKIA" + "A" * 16, "github_pat_" + "a" * 25,
              "-----BEGIN RSA PRIVATE" + " KEY-----"):
        assert any("秘密" in r for r in reasons(s)), s
    assert not reasons("sk-short and ghp_x")


def test_allow_list():
    t = "C:" + "\\Users\\alice\\x"
    allow = [{"path": "docs/*.md", "pattern": "alice", "reason": "t"}]
    assert not reasons(t, allow=allow)
    assert reasons(t, path="tools/a.py", allow=allow)
    assert reasons("C:" + "\\Users\\bob\\x", allow=allow)


def test_decompiler_output():
    call = "int __" + "fastcall f(void)"
    local_reg = "  _" + "BYTE *v2; // r9"
    local_stack = "  int v5; // [sp+4h] [bp-1Ch]"
    macro = "LOB" + "YTE(v2) = 1;"
    assert not reasons("\n".join((call, local_reg)))
    for lines in ((call, local_reg, local_stack),
                  ("_" + "DWORD x;", "_" + "WORD y;", "__" + "int8 z;"),
                  (macro, macro, macro)):
        ps = audit.scan_text("findings/acnl/a.md", "\n".join(lines), [])
        assert len(ps) == 1
        assert ps[0].line == 1
        assert "3 行" in ps[0].reason
        assert "_DWORD" not in str(ps[0])
    assert reasons("\n".join(("| " + macro[:-5] + " |",) * 3))
    assert file_reasons("docs/a.json", "\n".join((call, local_reg, local_stack)).encode("utf-8"))
    assert not reasons("\n".join(("0x001000,4,F," + call,) * 3), path="symbols/acnl/functions.csv")
    assert len(audit.scan_text("docs/a.md", call + " " + macro + " " + local_reg, [])) == 0
    allow = [{"path": "findings/*", "pattern": "疑似C", "reason": "quoted example"}]
    assert not reasons("\n".join((call, local_reg, local_stack)), path="findings/acnl/a.md", allow=allow)
    assert reasons("\n".join((call, local_reg, local_stack)), path="docs/a.md", allow=allow)
    digest = audit.scan_text("docs/a.md", "\n".join((call, local_reg, local_stack)), [])[0].match
    exact = [{"path": "findings/*", "pattern": "^" + digest + "$", "reason": "old quote"}]
    assert not reasons("\n".join((call, local_reg, local_stack)), path="findings/acnl/a.md", allow=exact)
    assert reasons("\n".join((call, local_reg, local_stack, macro)), path="findings/acnl/a.md", allow=exact)
    fields = "  unsigned __" + "int8 mode;\n  signed __" + "int8 state;\n  __" + "int8 value;\n"
    assert not reasons(fields, path="symbols/acnl_jpn_v15/types/local_types.h")
    assert reasons(fields, path="docs/a.md")
    assert reasons("\n".join((call, local_reg, macro)), path="symbols/acnl_jpn_v15/types/local_types.h")


def file_reasons(path, data, **kw):
    return [p.reason for p in audit.scan_file(path, data, [], **kw)]


def test_forbidden_and_location():
    assert any("禁止" in r for r in file_reasons("docs/a.bin", b"x"))
    assert any("1MB" in r for r in file_reasons("docs/a.txt", b"a" * (1024 * 1024 + 1)))
    assert any("許可された場所の外" in r for r in file_reasons("scratch/a.md", b"x\n"))
    assert any("許可された場所の外" in r for r in file_reasons("other.md", b"x\n"))
    assert not file_reasons("README.md", b"x\n")
    assert not file_reasons("tools/audit.py", b"x\n")
    assert any(".task" in r for r in file_reasons(".task/report.md", b"x\n", main_mode=True))
    assert not file_reasons(".task/report.md", b"x\n")


def test_task_files():
    for path in (".task/notes.md", ".task/report.md"):
        assert not file_reasons(path, b"x" * (64 * 1024))
        assert any("64KB" in r for r in file_reasons(path, b"x" * (64 * 1024 + 1)))
    for path in (".task/dump.c", ".task/sub/report.md", ".task/notes.txt"):
        assert any("許可されていない" in r for r in file_reasons(path, b"x\n"))


def test_encoding():
    assert any("BOM" in r for r in file_reasons("docs/a.md", b"\xef\xbb\xbfhi\n"))
    assert any("CRLF" in r for r in file_reasons("docs/a.md", b"a\r\nb\r\n"))
    assert any("UTF-8" in r for r in file_reasons("docs/a.md", b"\xff\xfe"))
    assert any("CRLF" in r for r in file_reasons("LICENSE", b"a\r\n"))
    assert not file_reasons("docs/a.png", b"\x89\xff\r\n")


def test_size_limits():
    assert any("AGENTS" in r for r in file_reasons("AGENTS.md", b"a" * (16 * 1024 + 1)))
    assert not file_reasons("AGENTS.md", b"a" * (16 * 1024))
    assert any("SKILL" in r for r in file_reasons("skills/x/SKILL.md", b"a" * (8 * 1024 + 1)))


def test_generated_note():
    note = audit.GENERATED_NOTE.encode("utf-8")
    assert not file_reasons("findings/INDEX.md", note + b"\nx\n")
    assert any("生成物" in r for r in file_reasons("findings/acnl/INDEX.md", b"# x\n"))
    assert any("生成物" in r for r in file_reasons("findings/acnl/by-category/item.md", b"# x\n"))


def test_vtable_function_pointer_members_are_type_data():
    members = '\n'.join(f'  void (__fastcall *method_{i})(Pane *pane);' for i in range(3))
    assert not audit.scan_text('symbols/acnl_jpn_v15/types/local_types.h', members, [])
    # 宣言の置き場を変える、または本体を含める場合は引き続き検出する。
    assert audit.scan_text('docs/example.md', members, [])
    bodies = '\n'.join('int __fastcall method(void) { return 1; }' for _ in range(3))
    assert audit.scan_text('symbols/acnl_jpn_v15/types/local_types.h', bodies, [])


def test_modes(repo, monkeypatch, capsys):
    g = os.environ.get("AC3DS_GIT") or "git"
    monkeypatch.delenv("GITHUB_REF", raising=False)

    def git(*a):
        subprocess.run([g, *a], cwd=repo, check=True, capture_output=True)

    git("init", "-q")
    (repo / "README.md").write_text("ok\n", encoding="utf-8")
    (repo / "docs").mkdir()
    (repo / "docs/a.md").write_text("C:" + "\\Users\\zed\\x\n", encoding="utf-8")
    git("add", "README.md", "docs/a.md")
    assert audit.main(["--staged"]) == 1
    assert "docs/a.md:1" in capsys.readouterr().out
    (repo / "docs/a.md").write_text("clean\n", encoding="utf-8")
    assert audit.main(["--staged"]) == 1  # ステージ済みの内容を見る
    git("add", "-A")
    assert audit.main(["--staged"]) == 0
    assert audit.main(["--ci"]) == 0
    (repo / ".task").mkdir()
    (repo / ".task/report.md").write_bytes(b"x\n")
    assert audit.main([]) == 0
    (repo / ".task/dump.txt").write_bytes(b"x\n")
    assert audit.main([]) == 1
    (repo / ".task/dump.txt").unlink()
    assert audit.main(["--main"]) == 1
    monkeypatch.setenv("GITHUB_REF", "refs/heads/main")
    assert audit.main([]) == 1
