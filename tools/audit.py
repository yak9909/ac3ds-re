#!/usr/bin/env python3
"""公開前の検査。モジュールとしても使える（scan_text / scan_file）。"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import os
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

GENERATED_NOTE = "<!-- 生成物。編集しない（kb.py index が作り直す） -->"
FORBIDDEN_EXT = {".cia", ".3ds", ".cci", ".cxi", ".app", ".bin", ".elf", ".3gx", ".i64", ".idb", ".id0",
                 ".id1", ".id2", ".nam", ".til", ".gpr", ".rep", ".sav", ".dmp", ".zip", ".7z"}
TEXT_EXT = {".md", ".toml", ".py", ".yml", ".yaml", ".csv", ".h", ".txt", ".json", ".ps1"}
MAX_SIZE = 1024 * 1024
TASK_MAX_SIZE = 64 * 1024
TASK_FILES = {".task/notes.md", ".task/report.md"}
# .gitignore のホワイトリストと同じ一覧
ALLOWED_TOP_FILES = {".gitignore", ".gitattributes", "README.md", "AGENTS.md", "CLAUDE.md", "LICENSE"}
ALLOWED_TOP_DIRS = {".github", ".githooks", "skills", "meta", "findings", "topics", "symbols", "archive",
                    "docs", "tools", ".task"}


@dataclass
class Problem:
    path: str
    line: int
    reason: str
    match: str = ""

    def __str__(self) -> str:
        return "%s:%d: %s" % (self.path, self.line, self.reason)


def repo_root() -> Path:
    env = os.environ.get("AC3DS_REPO")
    return Path(env).resolve() if env else Path(__file__).resolve().parent.parent


def git(args: list[str]) -> bytes:
    r = subprocess.run([os.environ.get("AC3DS_GIT") or "git", "-c", "core.quotepath=off", *args],
                       cwd=repo_root(), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode("utf-8", "replace"))
    return r.stdout


def load_allow(root: Path | None = None) -> list[dict]:
    p = (root or repo_root()) / "meta" / "audit-allow.toml"
    if not p.exists():
        return []
    with open(p, "rb") as f:
        return tomllib.load(f).get("allow", [])


def is_allowed(path: str, match: str, allow: list[dict]) -> bool:
    for e in allow:
        if fnmatch.fnmatchcase(path, e.get("path", "")) and re.search(e.get("pattern", "$^"), match):
            return True
    return False


# ---------- 内容の検査 ----------
_NAME = r"[^\\/\s\"'<>|:*?]+"
WIN_USER = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+(?P<n>%s)" % _NAME)
# 自分のソースに一致しないよう、リテラルを分けて書く
HOME_USER = re.compile(r"(?<![\w:./\\])/hom" r"e/(?P<n>[^/\s\"'<>]+)")
MAC_USER = re.compile(r"(?<![\w:./\\])/User" r"s/(?P<n>[^/\s\"'<>]+)")
_LOCAL_CH = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._%+-")
_LOCAL_TAIL = re.compile(r"[A-Za-z0-9._%+-]{1,64}$")
_DOMAIN = re.compile(r"(?P<d>[A-Za-z0-9-]{1,63}(?:\.[A-Za-z0-9-]{1,63}){0,9}?\.[A-Za-z]{2,63})(?![A-Za-z0-9-]|\.[A-Za-z0-9])")


def _emails(line: str):
    """(アドレス, ドメイン) を返す。@ ごとに前後の限られた範囲だけを調べるので、行の長さに対して線形。"""
    i = line.find("@")
    while i != -1:
        if i > 0 and line[i - 1] in _LOCAL_CH and line.find(".", i + 1, i + 1 + 255) != -1:
            lm = _LOCAL_TAIL.search(line, max(0, i - 64), i)
            dm = _DOMAIN.match(line, i + 1, min(len(line), i + 1 + 255))
            if lm and dm:
                yield lm.group(0) + "@" + dm.group("d"), dm.group("d").lower()
        i = line.find("@", i + 1)
IPV4 = re.compile(r"(?<![0-9A-Za-z.])(?:25[0-5]|2[0-4]\d|1?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|1?\d?\d)){3}"
                  r"(?![0-9A-Za-z]|\.[0-9A-Za-z])")
SERIAL = re.compile(r"\b[A-Z]{2,3}\d{9,10}\b")
SECRETS = [
    (re.compile(r"\b(?:ghp|gho|ghu|ghs)_[A-Za-z0-9]{20,}"), "GitHub トークンらしい値"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}"), "GitHub トークンらしい値"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_-]{10,}"), "Anthropic の API キーらしい値"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}"), "API キーらしい値"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}"), "AWS のアクセスキーらしい値"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "秘密鍵"),
]
DECOMP_CALL = re.compile(r"\b__(?:fast" r"call|cdecl|stdcall|thiscall|usercall)\b")
DECOMP_TYPE = re.compile(r"\b(?:_(?:BYTE|WORD|DWORD|QWORD|OWORD)|__int(?:8|16|32|64))\b")
DECOMP_MACRO = re.compile(r"\b(?:LO|HI)(?:BYTE|WORD|DWORD)\s*\(")
DECOMP_LOCAL = re.compile(
    r"^\s*(?:(?:const|signed|unsigned)\s+)*(?:[A-Za-z_]\w*\s+)+\**\s*v\d+\s*(?:\[[^]]+\])?\s*;"
    r"\s*//\s*(?:r\d+\b|\[sp[^]]*\]\s*\[bp[^]]*\])"
)


def _name_ignored(n: str) -> bool:
    return n.lower() in ("public", "default") or n.startswith("<") or "…" in n


def scan_text(path: str, text: str, allow: list[dict] | None = None) -> list[Problem]:
    """テキストの内容（個人の情報・秘密）を検査する。秘密の値そのものは返さない。"""
    if allow is None:
        allow = load_allow()
    path = path.replace("\\", "/")
    out: list[Problem] = []
    decomp_lines: list[tuple[int, str]] = []

    def add(ln: int, reason: str, match: str) -> None:
        if not is_allowed(path, match, allow):
            out.append(Problem(path, ln, reason, match))

    for ln, line in enumerate(text.split("\n"), 1):
        # symbols の CSV は型・関数宣言、型ヘッダはフィールド定義を正規データとして持つ。
        csv_row = path.endswith(".csv") and re.match(r"^0x[0-9A-Fa-f]+,", line)
        type_hit = (DECOMP_TYPE.search(line) and ";" in line
                    and not fnmatch.fnmatchcase(path, "symbols/*/types/*.h") and not csv_row)
        macro_hit = DECOMP_MACRO.search(line)
        call_hit = DECOMP_CALL.search(line) and not csv_row
        if call_hit or macro_hit or DECOMP_LOCAL.search(line) or type_hit:
            decomp_lines.append((ln, line.strip()))
        for rx, label in ((WIN_USER, "Windows のユーザーのパス"), (HOME_USER, "/home のユーザーのパス"),
                          (MAC_USER, "/Users のユーザーのパス")):
            for m in rx.finditer(line):
                if not _name_ignored(m.group("n")):
                    add(ln, "個人の情報: " + label, m.group(0))
        for addr, d in _emails(line):
            if addr.lower() == "noreply@anthropic.com" or d.endswith("users.noreply.github.com") \
                    or d in ("example.com", "example.org"):
                continue
            add(ln, "個人の情報: メールアドレス", addr)
        for m in IPV4.finditer(line):
            s = m.group(0)
            octs = [int(x) for x in s.split(".")]
            if s in ("0.0.0.0", "127.0.0.1", "255.255.255.255") or all(o <= 9 for o in octs):
                continue  # 版番号らしい（全オクテットが一桁）
            if re.search(r"(?i)(?:version|ver\.?|v)\s{0,8}$", line[max(0, m.start() - 20):m.start()]):
                continue
            add(ln, "個人の情報: IPv4 アドレス", s)
        for m in SERIAL.finditer(line):
            add(ln, "個人の情報: 本体の製造番号らしい値", m.group(0))
        for rx, label in SECRETS:
            for m in rx.finditer(line):
                add(ln, "秘密: " + label, m.group(0))
    if len(decomp_lines) >= 3:
        digest = hashlib.sha256("\n".join(line for _, line in decomp_lines).encode("utf-8")).hexdigest()
        add(decomp_lines[0][0], "逆コンパイラの出力らしい行が %d 行" % len(decomp_lines), "疑似C:" + digest)
    return out


# ---------- ファイルの検査 ----------
def scan_file(path: str, data: bytes, allow: list[dict], main_mode: bool = False) -> list[Problem]:
    path = path.replace("\\", "/")
    out: list[Problem] = []

    def add(reason: str, ln: int = 0) -> None:
        if not is_allowed(path, path, allow):
            out.append(Problem(path, ln, reason, path))

    pp = PurePosixPath(path)
    ext = pp.suffix.lower()
    top = pp.parts[0]
    if ext in FORBIDDEN_EXT:
        add("禁止ファイル（拡張子 %s）" % ext)
    if len(data) > MAX_SIZE:
        add("1MB を超えるファイル（%d バイト）" % len(data))
    if len(pp.parts) == 1:
        if path not in ALLOWED_TOP_FILES:
            add("許可された場所の外のファイル")
    elif top not in ALLOWED_TOP_DIRS:
        add("許可された場所の外のファイル")
    if top == ".task":
        if path not in TASK_FILES:
            add(".task/ に許可されていないファイル")
        elif len(data) > TASK_MAX_SIZE:
            add(".task/ のファイルが 64KB を超えている")
    if main_mode and top == ".task":
        add(".task/ は main に置けない")
    # 大きさ
    if path == "AGENTS.md" and len(data) > 16 * 1024:
        add("AGENTS.md が 16KB を超えている")
    if fnmatch.fnmatchcase(path, "skills/*/SKILL.md") and len(data) > 8 * 1024:
        add("SKILL.md が 8KB を超えている")
    if ext in FORBIDDEN_EXT:
        return out
    is_text = ext in TEXT_EXT or ext == ""
    text = None
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        if is_text:
            add("UTF-8 として読めない")
    if text is not None and is_text:
        if text.startswith("﻿"):
            add("BOM がある")
        if "\r\n" in text:
            add("CRLF がある", text[:text.index("\r\n")].count("\n") + 1)
    # 生成物の注記
    if text is not None and (fnmatch.fnmatchcase(path, "findings/INDEX.md")
                             or fnmatch.fnmatchcase(path, "findings/*/INDEX.md")
                             or fnmatch.fnmatchcase(path, "findings/*/by-category/*.md")):
        if text.lstrip("﻿").split("\n", 1)[0].rstrip("\r") != GENERATED_NOTE:
            add("生成物の先頭行が注記ではない", 1)
    if text is not None:
        out += scan_text(path, text, allow)
    return out


# ---------- ファイルの列挙 ----------
def list_files(mode: str) -> list[tuple[str, bytes]]:
    root = repo_root()
    out = []
    if mode == "staged":
        names = git(["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"]).decode("utf-8").split("\0")
        for n in filter(None, names):
            out.append((n, git(["show", ":" + n])))
        return out
    names = git(["ls-files", "-z"]).decode("utf-8").split("\0")
    if mode == "default":
        names += git(["ls-files", "--others", "--exclude-standard", "-z"]).decode("utf-8").split("\0")
    tracked = set(filter(None, git(["ls-files", "-z"]).decode("utf-8").split("\0")))
    for n in sorted(set(filter(None, names))):
        p = root / n
        if n in tracked:
            out.append((n, git(["show", ":" + n])))  # 改行変換の影響を避け、インデックスの内容を見る
        elif p.is_file():
            out.append((n, p.read_bytes()))
    return out


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    ap = argparse.ArgumentParser(prog="audit.py")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--staged", action="store_true")
    g.add_argument("--ci", action="store_true")
    ap.add_argument("--main", action="store_true")
    a = ap.parse_args(argv)
    main_mode = a.main or os.environ.get("GITHUB_REF") == "refs/heads/main"
    mode = "staged" if a.staged else "ci" if a.ci else "default"
    allow = load_allow()
    problems: list[Problem] = []
    files = list_files(mode)
    for n, data in files:
        problems += scan_file(n, data, allow, main_mode)
    for p in problems:
        print(p)
    print("audit: %d ファイル、問題 %d 件" % (len(files), len(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
