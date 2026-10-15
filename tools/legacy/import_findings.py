#!/usr/bin/env python3
"""旧 FINDINGS の ## 節を、原文を保って一節一記録へ取り込む。

順序は v1、IDA/ACNL、IDA/HHD、Ghidra とし、各ファイルは行順。
既存 source は再採番しない。原本は git show または読み取りだけで取得する。
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import audit  # noqa: E402
import kb  # noqa: E402

HEADING = re.compile(r"(?m)^## [^\n]+(?:\n|$)")
OLD_ID = re.compile(r"(?<![\w-])F-(\d{1,4})(?!\d)")
FULL_ID = re.compile(r"(?:IDA|Ghidra|TreeSitter)-[A-Za-z0-9.\-]+-[FT]\d+(?:-HW)?")
DATE = re.compile(r"20\d{2}-\d{2}-\d{2}")
ADDRESS = re.compile(r"0x[0-9A-Fa-f]+\b")
PRODUCT = re.compile(r"(?i)gohan|plugin/|3gx|チート|cheat|実装|製品|ビルド|frontend|launcher")
CATEGORIES = {
    "chat": "text", "チャット": "text", "swkbd": "text", "キーボード": "text",
    "font": "text", "フォント": "text", "文字": "text", "メッセージ": "text",
    "pocket": "item", "inventory": "item", "item": "item", "持ち物": "item",
    "収納": "item", "家具": "item", "catalog": "item", "カタログ": "item",
    "マップ": "field", "地面": "field", "建物": "field", "公共事業": "field",
    "プレイヤー": "actor", "住民": "actor", "actor": "actor", "電車": "actor",
    "セーブ": "save", "save": "save", "通信": "network", "packet": "network",
    "音": "sound", "時計": "time", "天気": "time", "イベント": "time",
    "描画": "render", "モデル": "render", "texture": "render", "カメラ": "render",
    "メニュー": "ui", "画面": "ui", "レイアウト": "ui", "layout": "ui",
    "入力": "input", "タッチ": "input", "button": "input", "ボタン": "input",
    "heap": "system", "ヒープ": "system", "スレッド": "system", "起動": "system",
}


def git_show(repo: Path, spec: str) -> bytes:
    cp = subprocess.run([kb.git_cmd(), "-C", str(repo), "show", spec], capture_output=True)
    if cp.returncode:
        raise RuntimeError(cp.stderr.decode("utf-8", "replace"))
    return cp.stdout


def sources(v1: Path, v2: Path):
    return [
        ("v1:RE/FINDINGS.md", "acnl", "IDA", v1.read_bytes()),
        ("IDA:work/FINDINGS.md", "acnl", "IDA", git_show(v2, "IDA:work/FINDINGS.md")),
        ("IDA:work/hhd/FINDINGS.md", "hhd", "IDA", git_show(v2, "IDA:work/hhd/FINDINGS.md")),
        ("Ghidra:work/FINDINGS.md", "acnl", "Ghidra", git_show(v2, "Ghidra:work/FINDINGS.md")),
    ]


def sections(data: bytes):
    text = data.decode("utf-8-sig").replace("\r\n", "\n")
    matches = list(HEADING.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        # ## 見出しから次の ## の直前まで。末尾の改行も本文の一部。
        yield text[m.start():end], text.count("\n", 0, m.start()) + 1, text.count("\n", 0, end) + (0 if text[:end].endswith("\n") else 1)


def category(title: str, body: str) -> str:
    low = title.lower()
    if PRODUCT.search(title + "\n" + body[:500]):
        return "_product"
    hits = {v for k, v in CATEGORIES.items() if k.lower() in low}
    return hits.pop() if len(hits) == 1 else "_triage"


def by_from_id(old: str, tool: str) -> str:
    if old.startswith(("IDA-gpt-6-", "TreeSitter-gpt-6-")):
        return "gpt-6"
    if old.startswith("IDA-gpt-6.1-sol-"):
        return "gpt-6.1-sol"
    if old.startswith("IDA-gpt-6-astra-"):
        return "gpt-6-astra"
    if old.startswith("IDA-gpt-6-sol-"):
        return "gpt-6-sol"
    if old.startswith("IDA-opus-5.5-"):
        return "opus-5.5"
    if old.startswith("Ghidra-gpt-sol-5.6-"):
        return "gpt-sol-5.6"
    return "unknown"


def redacted(text: str, rel: str, rid: str):
    changes = []
    # audit の判定をそのまま用いる。値は sources.toml に書かない。
    for _ in range(5):
        problems = audit.scan_text(rel, text, [])
        if not problems:
            break
        lines = text.split("\n")
        for p in problems:
            replacement = "<USER>" if "ユーザーのパス" in p.reason else "<REDACTED>"
            lines[p.line - 1] = lines[p.line - 1].replace(p.match, replacement)
            changes.append((rid, p.line, p.reason))
        text = "\n".join(lines)
    if audit.scan_text(rel, text, []):
        raise RuntimeError("伏せられない情報: " + rel)
    return text, sorted(set(changes))


def existing_sources():
    found = {}
    for rec in kb.load_records():
        source = rec.get("source")
        if source:
            found[source] = rec
    return found


def make_record(source, scope, tool, body, start, end, prior_date, mapping, builds, tag_defs):
    heading = body.split("\n", 1)[0][3:].strip()
    full = FULL_ID.search(heading)
    old = full.group(0) if full else ""
    aliases = [old] if old else []
    if old:
        aliases += sorted(k for k, v in mapping.get(tool, {}).items() if v == old and k not in aliases)
    # v1 の F 番号は、重複見出しがあるので呼出側で衝突を解決する。
    if source.startswith("v1:"):
        f = OLD_ID.search(heading)
        if f:
            aliases.append("F-" + f.group(1))
    elif not old:
        short = re.match(r"(?:F|T)-?\d+", heading)
        if short:
            aliases.append(short.group(0))
    title = heading
    if full:
        title = heading[len(old):].lstrip(": ")
    date = (DATE.search(heading) or DATE.search(body))
    date_str = date.group(0) if date else prior_date
    if not date_str:
        date_str = "2026-09-19" if not source.startswith("v1:") else "2026-09-12"
    confidence = re.search(r"\b(?:HIGH|MEDIUM|LOW)\b", body)
    confidence_str = confidence.group(0) if confidence else ""
    summary_line = next((x.strip(" -\t") for x in body.splitlines()[1:] if x.strip() and not x.startswith("#")), "")
    summary = summary_line[:240] if summary_line else title
    build = "acnl_jpn_v15" if scope == "acnl" else "hhd_jpn_v11"
    ranges = [(int(a, 16), int(b, 16)) for a, b in builds[build]["segments"].values()]
    addresses = []
    for m in ADDRESS.finditer(body):
        addr = int(m.group(0), 16)
        if any(a <= addr < b for a, b in ranges) and addr not in addresses:
            addresses.append(addr)
        if len(addresses) == 20:
            break
    tags = [name for name, info in tag_defs.items()
            if any(re.search(r"(?<![A-Za-z])" + re.escape(word) + r"(?![A-Za-z])", heading, re.I)
                   for word in [name, *info.get("synonyms", [])] if len(word) >= 3)]
    meta = {
        "aliases": list(dict.fromkeys(aliases)), "title": title, "summary": summary,
        "date": date_str, "category": category(title, body), "build": build,
        "confidence": confidence_str, "tool": tool, "addresses": addresses,
        "tags": tags, "supersedes": [], "source": f"{source}:{start}-{end}",
        "by": by_from_id(old, tool), "original_by": "", "reviewed_by": [],
        "state": "active", "consolidated_into": "", "duplicate_of": "", "superseded_by": "",
    }
    return meta, body, date_str


def write_sources(path: Path, hashes, changes):
    lines = ["# 原本の SHA256 と公開のための伏せ字。伏せた値は記載しない。"]
    for name, digest in hashes.items():
        lines += ["", "[[sources]]", f"name = {json.dumps(name, ensure_ascii=False)}", f"sha256 = {json.dumps(digest)}"]
    for rid, line, kind in sorted(set(changes)):
        lines += ["", "[[redactions]]", f"id = {json.dumps(rid)}", f"line = {line}", f"kind = {json.dumps(kind, ensure_ascii=False)}"]
    kb.write_text(path, "\n".join(lines) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--v1", type=Path, default=Path(r"A:\Disassemble\acnl\RE\FINDINGS.md"))
    ap.add_argument("--v2", type=Path, default=Path(r"A:\Disassemble\acnl\project_v2"))
    args = ap.parse_args(argv)
    mapping = {tool: json.loads(git_show(args.v2, f"{tool}:work/record_ids.{tool}.json"))["aliases"]
               for tool in ("IDA", "Ghidra")}
    builds = kb.load_toml("builds.toml")["builds"]
    tag_defs = kb.load_toml("tags.toml")["tags"]
    records_at_start = kb.load_records()
    current = {rec.get("source"): rec for rec in records_at_start if rec.get("source")}
    aliases_used = {alias for rec in records_at_start for alias in rec.get("aliases", [])}
    # reserve_number は台帳をロックして増やす。既存ファイルの最大番号は
    # 開始時に一度だけ読めばよく、以降の採番は台帳が単調増加を保証する。
    kb.load_records = lambda: records_at_start
    hashes, changes = {}, []
    counts = collections.Counter()
    skipped = []
    for source, scope, tool, data in sources(args.v1, args.v2):
        hashes[source] = hashlib.sha256(data).hexdigest()
        date = ""
        for body, start, end in sections(data):
            meta, body, date = make_record(source, scope, tool, body, start, end, date, mapping, builds, tag_defs)
            key = meta["source"]
            old_rec = current.get(key)
            if old_rec:
                aliases_used.difference_update(old_rec.get("aliases", []))
            # 旧番号が複数節に現れる場合は最初の節のみ単独 alias とし、
            # 後続は出所行付き alias で一意にする。
            fixed = []
            for alias in meta["aliases"]:
                unique = alias if alias not in aliases_used else f"{alias}@{source}:{start}"
                if unique in aliases_used:
                    skipped.append((key, "alias collision: " + unique))
                    break
                fixed.append(unique)
            else:
                meta["aliases"] = fixed
                n = int(old_rec.id.split("-F")[-1]) if old_rec else kb.reserve_number(scope)
                rid = old_rec.id if old_rec else f"{kb.PREFIX[scope]}-F{n:04d}"
                meta = {"id": rid, **meta}
                path = ROOT / "findings" / scope / kb.folder_for(n) / (rid + ".md")
                rel = path.relative_to(ROOT).as_posix()
                fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000)
                full_text, redactions = redacted("---\n" + fm + "---\n" + body, rel, rid)
                kb.write_text(path, full_text)
                changes.extend(redactions)
                aliases_used.update(fixed)
                counts[(source, "refreshed" if old_rec else "created")] += 1
                continue
            # 採番前の失敗は一覧で報告し、別の節の処理を続ける。
    write_sources(ROOT / "archive" / "legacy-findings" / "sources.toml", hashes, changes)
    for key, value in sorted(counts.items()):
        print(*key, value)
    for item in skipped:
        print("UNIMPORTED", *item)
    return 1 if skipped else 0


if __name__ == "__main__":
    raise SystemExit(main())
