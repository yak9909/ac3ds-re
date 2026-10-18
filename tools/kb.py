#!/usr/bin/env python3
"""ac3ds-re の記録（findings）の道具。"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml
from filelock import FileLock

GENERATED_NOTE = "<!-- 生成物。編集しない（kb.py index が作り直す） -->"
PREFIX = {"acnl": "ACNL", "hhd": "HHD", "3ds": "3DS"}
ID_RE = re.compile(r"^(ACNL|HHD|3DS)-F(\d+)$")
FOLDER_RE = re.compile(r"^\d+-\d+$")
FM_RE = re.compile(r"\A---\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)

TEMPLATE = """---
id: {id}
aliases: []
title: {title}
summary: ""
date: {date}
category: {category}
build: {build}
confidence: LOW          # LOW / MEDIUM / HIGH
tool: {tool}
addresses: []
tags: []
supersedes: []
# ── 管理項目（編集しない。kb.py と仕上げが書く）──
by: auto
original_by: ""
reviewed_by: []
state: active            # active / consolidated / superseded / duplicate
consolidated_into: ""
duplicate_of: ""
superseded_by: ""
corrected_by: []
---
## 結論

## 根拠

## 反証条件・未確認点
"""

MANAGED_DEFAULTS = {
    "original_by": ('""', ""),
    "reviewed_by": ("[]", []),
    "state": ("active", "active"),
    "consolidated_into": ('""', ""),
    "duplicate_of": ('""', ""),
    "superseded_by": ('""', ""),
    "corrected_by": ("[]", []),
}
REQUIRED = {
    "id": str, "aliases": list, "title": str, "summary": str, "date": (datetime.date, str),
    "category": str, "build": str, "confidence": str, "tool": str, "addresses": list,
    "tags": list, "supersedes": list, "by": str, "original_by": str, "reviewed_by": list,
    "state": str, "consolidated_into": str, "duplicate_of": str, "superseded_by": str,
}
STATES = ("active", "consolidated", "superseded", "duplicate")


# ---------- 環境 ----------
def root() -> Path:
    env = os.environ.get("AC3DS_REPO")
    return Path(env).resolve() if env else Path(__file__).resolve().parent.parent


def git_cmd() -> str:
    return os.environ.get("AC3DS_GIT") or "git"


def run_git(args: list[str]) -> str:
    r = subprocess.run([git_cmd(), "-c", "core.quotepath=off", *args], cwd=root(),
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip())
    return r.stdout


def state_dir() -> Path:
    env = os.environ.get("AC3DS_STATE")
    if env:
        p = Path(env)
    elif (root().parent / "_local" / "state").is_dir():
        p = root().parent / "_local" / "state"
    else:
        p = root() / ".kb-state"
    p.mkdir(parents=True, exist_ok=True)
    return p


def load_toml(name: str) -> dict:
    p = root() / "meta" / name
    if not p.exists():
        return {}
    with open(p, "rb") as f:
        return tomllib.load(f)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def hexa(n: int) -> str:
    return "0x%08X" % n


# ---------- 記録 ----------
class Rec:
    def __init__(self, path: Path, scope: str):
        self.path = path
        self.scope = scope
        try:
            self.rel = path.relative_to(root()).as_posix()
        except ValueError:
            self.rel = path.as_posix()
        self.meta: dict = {}
        self.err = ""
        self.raw = path.read_text(encoding="utf-8", errors="replace")
        m = FM_RE.match(self.raw)
        if not m:
            self.err = "frontmatter が無い"
        else:
            try:
                d = yaml.safe_load(m.group(1))
                if isinstance(d, dict):
                    self.meta = d
                else:
                    self.err = "frontmatter が辞書ではない"
            except yaml.YAMLError as e:
                self.err = "frontmatter の YAML が読めない: %s" % str(e).splitlines()[0]

    @property
    def id(self) -> str:
        return str(self.meta.get("id") or self.path.stem)

    def get(self, k, default=""):
        v = self.meta.get(k, default)
        return default if v is None else v


def load_records() -> list[Rec]:
    out = []
    base = root() / "findings"
    if not base.is_dir():
        return out
    for sd in sorted(base.iterdir()):
        if not sd.is_dir():
            continue
        for fd in sorted(sd.iterdir()):
            if fd.is_dir() and FOLDER_RE.match(fd.name):
                for f in sorted(fd.glob("*.md")):
                    out.append(Rec(f, sd.name))
    return out


def folder_for(n: int) -> str:
    s = n // 100 * 100
    return "%04d-%04d" % (s, s + 99)


def max_number(scope: str, recs: list[Rec]) -> int:
    m = 0
    for r in recs:
        mm = ID_RE.match(r.path.stem)
        if mm and r.scope == scope:
            m = max(m, int(mm.group(2)))
    return m


def models_lookup(by: str, models: dict) -> str | None:
    """格付けを返す。未記入は None、未登録は C。"""
    if by in ("", "auto"):
        return None
    for name, v in models.get("models", {}).items():
        if by == name or by in v.get("aliases", []):
            return v.get("tier", "C")
    return "C"


def tier_label(by: str, models: dict) -> str:
    t = models_lookup(by, models)
    return "未記入" if t is None else t


def canonical_model(m: str, models: dict) -> str | None:
    for name, v in models.get("models", {}).items():
        if m == name or m in v.get("aliases", []):
            return name
    return None


# ---------- frontmatter の行編集 ----------
def set_field(text: str, key: str, value: str) -> str:
    m = FM_RE.match(text)
    assert m
    fm = m.group(1)
    pat = re.compile(r'^(%s:[ \t]*)(?:"[^"]*"|\[[^\]]*\]|[^#\n]*?)([ \t]+#.*)?$' % re.escape(key), re.M)
    if not pat.search(fm):
        raise ValueError("項目が無い: " + key)
    new = pat.sub(lambda mm: mm.group(1) + value + (mm.group(2) or ""), fm, count=1)
    return text[:m.start(1)] + new + text[m.end(1):]


def set_corrected_by(text: str, ids: list[str]) -> str:
    value = json.dumps(ids, ensure_ascii=False)
    fm = FM_RE.match(text)
    if re.search(r"^corrected_by:", fm.group(1), re.M):
        return set_field(text, "corrected_by", value)
    m = re.search(r"^superseded_by:[^\n]*", fm.group(1), re.M)
    if not m:
        raise ValueError("項目が無い: superseded_by")
    end = fm.start(1) + m.end()
    return text[:end] + "\ncorrected_by: " + value + text[end:]


# ---------- new ----------
def reserve_number(scope: str) -> int:
    sd = state_dir()
    with FileLock(str(sd / "ids.lock")):
        led_path = sd / "ids.json"
        led = {}
        if led_path.exists():
            try:
                led = json.loads(led_path.read_text(encoding="utf-8"))
            except ValueError:
                led = {}
        n = max(int(led.get(scope, 0)), max_number(scope, load_records())) + 1
        led[scope] = n
        tmp = sd / ("ids.json.tmp%d" % os.getpid())
        write_text(tmp, json.dumps(led, indent=1, sort_keys=True))
        os.replace(tmp, led_path)
        return n


def default_build(scope: str) -> str:
    for name, b in load_toml("builds.toml").get("builds", {}).items():
        if b.get("scope") == scope and "保管だけ" not in b.get("note", ""):
            return name
    return ""


def cmd_new(a) -> int:
    cats = load_toml("categories.toml")
    allowed = set(cats.get("scopes", {}).get(a.scope, {}).get("categories", [])) | set(
        cats.get("special", {}).get("categories", []))
    if a.category not in allowed:
        print("category が台帳に無い: %s（%s）" % (a.category, ", ".join(sorted(allowed))), file=sys.stderr)
        return 2
    if a.build and a.build not in load_toml("builds.toml").get("builds", {}):
        print("build が台帳に無い: " + a.build, file=sys.stderr)
        return 2
    build = a.build or default_build(a.scope)
    n = reserve_number(a.scope)
    rid = "%s-F%04d" % (PREFIX[a.scope], n)
    path = root() / "findings" / a.scope / folder_for(n) / (rid + ".md")
    write_text(path, TEMPLATE.format(
        id=rid, title=json.dumps(a.title, ensure_ascii=False), date=datetime.date.today().isoformat(),
        category=a.category, build=build, tool=a.tool))
    print(path)
    return 0


# ---------- index ----------
def cell(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def build_index(recs: list[Rec]) -> dict[str, str]:
    models = load_toml("models.toml")
    cats = load_toml("categories.toml")
    scopes = list(cats.get("scopes", {}).keys())
    good = sorted((r for r in recs if not r.err), key=lambda r: (r.scope, r.id))
    out: dict[str, str] = {}
    H = GENERATED_NOTE + "\n"

    def title(r):
        return str(r.get("title"))

    def correction(r):
        return "訂正あり" if r.get("corrected_by", []) else ""

    lines = [H, "# 記録の索引", "", "## スコープ別の件数", "", "| scope | 件数 | active |", "|---|---|---|"]
    for s in scopes:
        rs = [r for r in good if r.scope == s]
        lines.append("| %s | %d | %d |" % (s, len(rs), sum(1 for r in rs if r.get("state") == "active")))
    lines += ["", "## カテゴリ別の未消化（state active の件数）", ""]
    counts: dict[tuple, int] = {}
    for r in good:
        if r.get("state") == "active":
            k = (r.scope, str(r.get("category")))
            counts[k] = counts.get(k, 0) + 1
    if counts:
        lines += ["| scope | category | 件数 |", "|---|---|---|"]
        lines += ["| %s | %s | %d |" % (s, c, n) for (s, c), n in sorted(counts.items())]
    else:
        lines.append("なし")

    def lst(title_, items):
        lines.extend(["", "## " + title_, ""])
        lines.extend(items if items else ["なし"])

    lst("要再解析（by の格付けが ?）",
        ["- %s %s" % (r.id, title(r)) for r in good if models_lookup(str(r.get("by")), models) == "?"])
    lst("未レビュー（reviewed_by が空）",
        ["- %s %s" % (r.id, title(r)) for r in good if not r.get("reviewed_by")])
    groups: dict[tuple, list[str]] = {}
    for r in good:
        if r.get("state") == "active":
            for ad in r.get("addresses", []) or []:
                if isinstance(ad, int):
                    groups.setdefault((str(r.get("build")), ad), []).append(r.id)
    lst("重複候補（同じ addresses を持つ active の記録の組）",
        ["- %s %s: %s" % (b, hexa(ad), ", ".join(sorted(set(ids))))
         for (b, ad), ids in sorted(groups.items()) if len(set(ids)) > 1])
    lst("10件を超えた未消化カテゴリ",
        ["- %s/%s: %d件" % (s, c, n) for (s, c), n in sorted(counts.items()) if n > 10])
    out["findings/INDEX.md"] = "\n".join(lines) + "\n"

    for s in scopes:
        rs = [r for r in good if r.scope == s]
        t = [H, "# %s の記録" % s, "", "| ID | 題 | 確度 | 格付け | state | consolidated_into | 訂正 |", "|---|---|---|---|---|---|---|"]
        for r in rs:
            t.append("| %s | %s | %s | %s | %s | %s | %s |" % (r.id, cell(title(r)), r.get("confidence"),
                                                                tier_label(str(r.get("by")), models), r.get("state"),
                                                                cell(r.get("consolidated_into")), correction(r)))
        out["findings/%s/INDEX.md" % s] = "\n".join(t) + "\n"
        bycat: dict[str, list[Rec]] = {}
        for r in rs:
            bycat.setdefault(str(r.get("category")), []).append(r)
        for c, crs in sorted(bycat.items()):
            t = [H, "# %s / %s" % (s, c), "", "| ID | 題 | summary | 確度 | 格付け | consolidated_into | 訂正 |", "|---|---|---|---|---|---|---|"]
            for r in crs:
                t.append("| %s | %s | %s | %s | %s | %s | %s |" % (r.id, cell(title(r)), cell(r.get("summary")),
                                                                    r.get("confidence"), tier_label(str(r.get("by")), models),
                                                                    cell(r.get("consolidated_into")), correction(r)))
            out["findings/%s/by-category/%s.md" % (s, c)] = "\n".join(t) + "\n"
    return out


def generated_existing() -> set[str]:
    base = root() / "findings"
    found = set()
    if (base / "INDEX.md").exists():
        found.add("findings/INDEX.md")
    if base.is_dir():
        for sd in base.iterdir():
            if sd.is_dir():
                if (sd / "INDEX.md").exists():
                    found.add("findings/%s/INDEX.md" % sd.name)
                bc = sd / "by-category"
                if bc.is_dir():
                    found |= {"findings/%s/by-category/%s" % (sd.name, f.name) for f in bc.glob("*.md")}
    return found


def cmd_index(a) -> int:
    exp = build_index(load_records())
    for rel in generated_existing() - set(exp):
        (root() / rel).unlink()
    for rel, text in exp.items():
        write_text(root() / rel, text)
    print("生成: %d ファイル" % len(exp))
    return 0


# ---------- search / show ----------
def expand_terms(word: str, tags: dict) -> list[str]:
    w = word.lower()
    terms = {w}
    for tag, v in tags.get("tags", {}).items():
        syn = [s.lower() for s in v.get("synonyms", [])]
        if w == tag.lower() or w in syn:
            terms |= {tag.lower(), *syn}
    return sorted(terms)


def cmd_search(a) -> int:
    tags = load_toml("tags.toml")
    models = load_toml("models.toml")
    groups = [expand_terms(w, tags) for w in a.query]
    n = 0
    for r in load_records():
        if r.err or (a.scope and r.scope != a.scope) or (a.category and r.get("category") != a.category) \
                or (a.tag and a.tag not in (r.get("tags") or [])):
            continue
        low = r.raw.lower()
        if not all(any(t in low for t in g) for g in groups):
            continue
        terms = [t for g in groups for t in g]
        hits = [(i, ln) for i, ln in enumerate(r.raw.splitlines(), 1) if any(t in ln.lower() for t in terms)]
        mark = " 訂正あり" if r.get("corrected_by", []) else ""
        print("%s  [%s/%s]%s %s" % (r.id, tier_label(str(r.get("by")), models), r.get("state"), mark, r.get("title")))
        for i, ln in hits[:3]:
            print("    L%d: %s" % (i, ln.strip()))
        n += 1
        if n >= a.limit:
            break
    return 0


def find_rec(rid: str) -> Rec | None:
    for r in load_records():
        if r.id == rid or rid in (r.get("aliases") or []):
            return r
    return None


def cmd_show(a) -> int:
    r = find_rec(a.id)
    if not r:
        print("見つからない: " + a.id, file=sys.stderr)
        return 1
    by = str(r.get("by"))
    if r.get("corrected_by", []):
        print("訂正: %s" % ", ".join(r.get("corrected_by", [])))
    if r.get("superseded_by"):
        print("置き換え: %s" % r.get("superseded_by"))
    if r.get("consolidated_into"):
        print("統合先: %s" % r.get("consolidated_into"))
    print("格付け: %s（by: %s）" % (tier_label(by, load_toml("models.toml")), by or "-"))
    print(r.raw, end="" if r.raw.endswith("\n") else "\n")
    return 0


# ---------- relate ----------
def cmd_relate(a) -> int:
    recs = {r.id: r for r in load_records() if not r.err}
    try:
        with open(a.file, encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f, delimiter="\t")
            if not reader.fieldnames or not {"before", "after", "kind"} <= set(reader.fieldnames):
                raise ValueError("TSV に before, after, kind 列が必要")
            rows = list(reader)
        for i, row in enumerate(rows, 2):
            before, after, kind = (str(row.get(k) or "").strip() for k in ("before", "after", "kind"))
            if before not in recs or after not in recs:
                raise ValueError("%d 行目: 存在しない ID: %s %s" % (i, before, after))
            if before == after:
                raise ValueError("%d 行目: 自分自身を参照" % i)
            if kind not in ("full", "partial"):
                raise ValueError("%d 行目: kind は full か partial" % i)
        texts = {rid: r.raw for rid, r in recs.items()}
        states = {rid: r.get("state") for rid, r in recs.items()}
        superseded = {rid: r.get("superseded_by") for rid, r in recs.items()}
        corrected = {}
        for rid, r in recs.items():
            value = r.get("corrected_by", [])
            if not isinstance(value, list):
                raise ValueError("%s: corrected_by の型が違う" % rid)
            corrected[rid] = list(value)
        changes = []
        for row in rows:
            before, after, kind = (str(row.get(k) or "").strip() for k in ("before", "after", "kind"))
            if kind == "full":
                if states[before] == "superseded" and superseded[before] != after:
                    print("警告: %s は既に %s に置き換え済み" % (before, superseded[before]), file=sys.stderr)
                    continue
                changed = False
                if states[before] != "superseded":
                    texts[before] = set_field(texts[before], "state", "superseded")
                    states[before] = "superseded"
                    changed = True
                if superseded[before] != after:
                    texts[before] = set_field(texts[before], "superseded_by", after)
                    superseded[before] = after
                    changed = True
                if changed:
                    changes.append("%s: 置き換え: %s" % (before, after))
            elif after not in corrected[before]:
                corrected[before].append(after)
                texts[before] = set_corrected_by(texts[before], corrected[before])
                changes.append("%s: 訂正: %s" % (before, after))
    except (OSError, ValueError, csv.Error, TypeError) as e:
        print("エラー: " + str(e), file=sys.stderr)
        return 1
    for change in changes:
        print(change)
    for rid, r in recs.items():
        if texts[rid] != r.raw:
            if not a.dry_run:
                write_text(r.path, texts[rid])
    return 0


# ---------- addr ----------
def read_csv(p: Path):
    if not p.exists():
        return []
    with open(p, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def to_int(s):
    try:
        return int(str(s), 0)
    except ValueError:
        return None


def cmd_addr(a) -> int:
    addr = int(a.addr, 0)
    builds = load_toml("builds.toml").get("builds", {})
    build = a.build or next((n for n, b in builds.items() if "保管だけ" not in b.get("note", "")), "")
    sym = root() / "symbols" / build
    rng = (addr, addr + 1)
    found = False
    from sync import symlib

    for row in symlib.read_table(sym, "functions"):
        fa, sz = to_int(row.get("address")), to_int(row.get("size")) or 0
        if fa is not None and fa <= addr < fa + max(sz, 1):
            print("関数: %s %s size=0x%X %s" % (hexa(fa), row.get("name"), sz, row.get("prototype", "")))
            rng = (fa, fa + max(sz, 1))
            found = True
    for row in symlib.read_table(sym, "globals"):
        ga, sz = to_int(row.get("address")), to_int(row.get("size")) or 0
        if ga is not None and ga <= addr < ga + max(sz, 1):
            print("グローバル: %s %s size=0x%X %s" % (hexa(ga), row.get("name"), sz, row.get("type", "")))
            found = True
    if not found:
        print("symbols に該当なし（build=%s）" % build)
    print("記録:")
    n = 0
    for r in load_records():
        if r.err or (r.get("build") and r.get("build") != build):
            continue
        if any(isinstance(x, int) and rng[0] <= x < rng[1] for x in (r.get("addresses") or [])):
            print("  %s %s" % (r.id, r.get("title")))
            n += 1
    if not n:
        print("  なし")
    ip = state_dir() / "issues.json"
    if ip.exists():
        try:
            issues = json.loads(ip.read_text(encoding="utf-8"))
        except ValueError:
            issues = []
        pat = re.compile(r"(?<![0-9A-Za-z])0x0*%X(?![0-9A-Fa-f])" % addr, re.I)
        print("Issue:")
        m = 0
        for it in issues:
            if it.get("state") == "open" and pat.search(str(it.get("body") or "")):
                print("  #%s %s" % (it.get("number"), it.get("title")))
                m += 1
        if not m:
            print("  なし")
    return 0


# ---------- lint ----------
def cmd_lint(a) -> int:
    recs = load_records()
    builds = load_toml("builds.toml").get("builds", {})
    cats = load_toml("categories.toml")
    tags = load_toml("tags.toml").get("tags", {})
    models = load_toml("models.toml")
    targets = None
    if a.paths:
        targets = {Path(p).resolve() for p in a.paths}
    errors: list[str] = []
    warns: list[str] = []
    ids: dict[str, str] = {}
    for r in recs:
        if r.err:
            continue
        for x in [r.id, *(r.get("aliases") or [])]:
            if x in ids and ids[x] != r.rel:
                errors.append("%s: ID の重複 %s（%s と）" % (r.rel, x, ids[x]))
            ids.setdefault(x, r.rel)
    allids = {r.id for r in recs if not r.err}
    for r in recs:
        if targets is not None and r.path.resolve() not in targets:
            continue

        def err(msg, r=r):
            errors.append("%s: %s" % (r.rel, msg))

        if r.err:
            err(r.err)
            continue
        m = r.meta
        bad = False
        for k, t in REQUIRED.items():
            if k not in m:
                err("必須項目が無い: " + k)
                bad = True
            elif m[k] is None and t is str:
                err("%s が空（null）。\"\" と書く" % k)
                bad = True
            elif m[k] is not None and not isinstance(m[k], t):
                err("%s の型が違う" % k)
                bad = True
        if bad:
            continue
        mm = ID_RE.match(r.id)
        if not mm:
            err("ID の形式が違う: " + r.id)
        else:
            if r.path.stem != r.id:
                err("ID とファイル名が一致しない")
            if PREFIX.get(r.scope) != mm.group(1):
                err("ID の接頭辞とスコープが一致しない")
            if r.path.parent.name != folder_for(int(mm.group(2))):
                err("フォルダが番号と合わない（%s）" % folder_for(int(mm.group(2))))
        allowed = set(cats.get("scopes", {}).get(r.scope, {}).get("categories", [])) | set(
            cats.get("special", {}).get("categories", []))
        if m["category"] not in allowed:
            err("category が台帳に無い: %s" % m["category"])
        if m["build"] not in builds:
            err("build が台帳に無い: %s" % m["build"])
        for t in m["tags"]:
            if t not in tags:
                err("tag が台帳に無い: %s" % t)
        if m["confidence"] not in ("LOW", "MEDIUM", "HIGH") and not (m["confidence"] == "" and "source" in m):
            err("confidence の値が不正: %r" % m["confidence"])
        for x in m["addresses"]:
            if not isinstance(x, int) or isinstance(x, bool):
                err("addresses に整数でない値: %r" % (x,))
        if m["state"] not in STATES:
            err("state の値が不正: %s" % m["state"])
        else:
            need = {"superseded": "superseded_by", "consolidated": "consolidated_into", "duplicate": "duplicate_of"}
            if m["state"] in need and not m[need[m["state"]]]:
                err("state %s なのに %s が空" % (m["state"], need[m["state"]]))
        for x in m["supersedes"]:
            if x not in allids:
                err("supersedes の参照先が無い: %s" % x)
        for k in ("superseded_by", "duplicate_of"):
            if m[k] and m[k] not in allids:
                err("%s の参照先が無い: %s" % (k, m[k]))
        destination = m["consolidated_into"]
        if destination.startswith("topics/"):
            if (not re.fullmatch(r"topics/[^/]+/[^/]+\.md", destination)
                    or ".." in destination.split("/") or not (root() / destination).is_file()):
                err("consolidated_into の参照先が無い: %s" % destination)
        elif destination and destination not in allids:
            err("consolidated_into の参照先が無い: %s" % destination)
        corrected = m.get("corrected_by", [])
        if not isinstance(corrected, list):
            err("corrected_by の型が違う")
        else:
            for x in corrected:
                if not isinstance(x, str) or x not in allids:
                    err("corrected_by の参照先が無い: %s" % x)
                if x == r.id:
                    err("corrected_by は自分自身を指せない: %s" % x)
        if m["by"] != "auto" and canonical_model(m["by"], models) is None:
            err("by が models.toml に無い: %s" % m["by"])
    exp = build_index(recs)
    stale = []
    for rel, text in exp.items():
        p = root() / rel
        if not p.exists() or p.read_text(encoding="utf-8") != text:
            stale.append(rel)
    stale += sorted(generated_existing() - set(exp))
    for rel in stale:
        (errors if a.strict else warns).append("%s: 生成物が古い（kb.py index）" % rel)
    for e in errors:
        print("エラー: " + e)
    if not a.quiet:
        for w in warns:
            print("警告: " + w)
        if not errors:
            print("lint: %d 件の記録、エラーなし" % len(recs))
    return 1 if errors else 0


# ---------- stamp ----------
def cmd_stamp(a) -> int:
    models = load_toml("models.toml")
    m = os.environ.get("AC3DS_MODEL", "") if a.self_ else (a.model or "")
    if not m:
        print("モデル名が無い（--model か --self と AC3DS_MODEL）", file=sys.stderr)
        return 2
    canon = canonical_model(m, models)
    if not canon:
        print("models.toml に無いモデル: " + m, file=sys.stderr)
        return 2
    paths: list[Path] = []
    if a.files:
        paths = [Path(f).resolve() for f in a.files]
    else:
        names: set[str] = set()
        for args in (["diff", "--name-only", "--diff-filter=A", "%s...HEAD" % a.base],
                     ["diff", "--cached", "--name-only", "--diff-filter=A"],
                     ["ls-files", "--others", "--exclude-standard", "--", "findings"]):
            try:
                names |= {x for x in run_git(args).splitlines() if x}
            except RuntimeError:
                pass
        for n in sorted(names):
            p = root() / n
            if re.match(r"findings/[^/]+/\d+-\d+/[^/]+\.md$", n) and p.exists():
                paths.append(p.resolve())
    for p in paths:
        text = p.read_text(encoding="utf-8")
        r = Rec(p, p.parent.parent.name)
        if r.err:
            print("警告: %s: %s" % (p, r.err), file=sys.stderr)
            continue
        if "source" in r.meta:
            print("stamp: %s 旧記録のため飛ばした（by は %s のまま）" % (p.name, r.get("by")))
            continue
        for k, (lit, val) in MANAGED_DEFAULTS.items():
            if r.meta.get(k, val) != val:
                print("警告: %s: 管理項目 %s を既定値に戻した" % (p.name, k), file=sys.stderr)
                text = set_field(text, k, lit)
        text = set_field(text, "by", canon)
        write_text(p, text)
        print("stamp: %s by=%s" % (p.name, canon))
    return 0


# ---------- tags / 未実装 ----------
def cmd_tags(a) -> int:
    tags = load_toml("tags.toml").get("tags", {})
    use: dict[str, int] = {}
    for r in load_records():
        if not r.err:
            for t in r.get("tags") or []:
                use[t] = use.get(t, 0) + 1
    for t, v in tags.items():
        print("%-14s %3d  %s  [%s]" % (t, use.pop(t, 0), v.get("description", ""), ", ".join(v.get("synonyms", []))))
    for t, n in sorted(use.items()):
        print("%-14s %3d  (台帳に無い)" % (t, n))
    return 0


def cmd_todo(a) -> int:
    print("段階1b で実装")
    return 0


def main(argv=None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    p = argparse.ArgumentParser(prog="kb.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("new")
    s.add_argument("--scope", required=True, choices=list(PREFIX))
    s.add_argument("--category", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--build")
    s.add_argument("--tool", default="IDA")
    s.set_defaults(f=cmd_new)
    s = sub.add_parser("index")
    s.set_defaults(f=cmd_index)
    s = sub.add_parser("search")
    s.add_argument("query", nargs="+")
    s.add_argument("--scope")
    s.add_argument("--category")
    s.add_argument("--tag")
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(f=cmd_search)
    s = sub.add_parser("show")
    s.add_argument("id")
    s.set_defaults(f=cmd_show)
    s = sub.add_parser("relate")
    s.add_argument("--file", required=True)
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(f=cmd_relate)
    s = sub.add_parser("addr")
    s.add_argument("addr")
    s.add_argument("--build")
    s.set_defaults(f=cmd_addr)
    s = sub.add_parser("lint")
    s.add_argument("--quiet", action="store_true")
    s.add_argument("--strict", action="store_true")
    s.add_argument("paths", nargs="*")
    s.set_defaults(f=cmd_lint)
    s = sub.add_parser("stamp")
    s.add_argument("--model")
    s.add_argument("--self", dest="self_", action="store_true")
    s.add_argument("--base", default="main")
    s.add_argument("files", nargs="*")
    s.set_defaults(f=cmd_stamp)
    s = sub.add_parser("tags")
    s.set_defaults(f=cmd_tags)
    for n in ("impact", "cat", "history"):
        s = sub.add_parser(n)
        s.add_argument("args", nargs="*")
        s.set_defaults(f=cmd_todo)
    a = p.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
