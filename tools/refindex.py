#!/usr/bin/env python3
"""参考資料の番地候補を索引化する。本文・値・ID 一覧は出力しない。"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import tomllib
from pathlib import Path

FIELDS = ("address", "build", "key", "file", "line")
UNKNOWN = "unknown"
MIN_ADDRESS = 0x00100000
MAX_ADDRESS = 0x40000000  # 上端は含まない。
PAIR = re.compile(r"^\s*([0-9a-fA-F]{8})\s+([0-9a-fA-F]{8})\s*$")
HEX = re.compile(r"(?<![\w])0x([0-9a-fA-F]{1,8})(?:[uUlL]{1,3})?(?![0-9a-zA-Z_])")
TEXT_EXTENSIONS = {".txt", ".md", ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".inl", ".inc"}


def local_dir(repo: Path) -> Path:
    """通常の配置と _local/worktrees 内の作業ツリーに対応する。"""
    if workspace := os.environ.get("AC3DS_WORKSPACE"):
        return Path(workspace) / "_local"
    for parent in (repo, *repo.parents):
        if parent.name == "_local":
            return parent
        if (parent / "_local").is_dir():
            return parent / "_local"
    return repo / "_local"


def index_dir(repo: Path) -> Path:
    return local_dir(repo) / "refs" / "index"


def read_text(path: Path) -> str | None:
    data = path.read_bytes()
    if b"\0" in data:
        return None
    for encoding in ("utf-8-sig", "cp932"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            pass
    return None


def addresses(text: str, gateway: bool = False):
    """(仮想番地, 1 始まりの行番号)。Gateway のデータ列は飛ばす。"""
    payload = 0
    for number, line in enumerate(text.splitlines(), 1):
        if not gateway:
            for address in sorted({int(m[1], 16) for m in HEX.finditer(line)}):
                if MIN_ADDRESS <= address < MAX_ADDRESS:
                    yield address, number
            continue
        pair = PAIR.fullmatch(line)
        if not pair:
            continue
        if payload:
            payload -= 1
            continue
        code, value = (int(part, 16) for part in pair.groups())
        kind = code >> 28
        if kind in (0, 1, 2):
            # 上位ニブルは書き込み幅の指定（32/16/8 bit）。
            address = code & 0x0FFFFFFF
            if MIN_ADDRESS <= address < MAX_ADDRESS:
                yield address, number
        elif kind == 0xE:
            payload = (value + 7) // 8


def build_for(ref: dict, relative: Path, builds: set[str]) -> str:
    # 地域名だけ、既定ビルド、同じ番地という理由では版を推定しない。
    explicit = ref.get("build")
    if explicit:
        if explicit not in builds and explicit != UNKNOWN:
            raise ValueError("台帳の未知の build: " + str(explicit))
        return explicit
    matches = builds.intersection(relative.parts)
    return next(iter(matches)) if len(matches) == 1 else UNKNOWN


def generate(repo: Path, refs_root: Path, output: Path) -> int:
    with (repo / "meta/references.toml").open("rb") as stream:
        refs = tomllib.load(stream).get("refs", {})
    with (repo / "meta/builds.toml").open("rb") as stream:
        builds = set(tomllib.load(stream).get("builds", {}))
    rows = set()
    for key, ref in sorted(refs.items()):
        if key not in {"CHEATS", "CTRPF_PROJECTS", "TEXTS", "IDS"}:
            continue
        source = (refs_root / ref["path"]).resolve()
        source.relative_to(refs_root.resolve())
        if not source.exists():
            raise ValueError("資料が見つからない: " + str(source))
        for path in sorted(source.rglob("*") if source.is_dir() else [source]):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            # IDS は ID の表であって番地の資料ではない。数値を索引に複写しない。
            if key == "IDS" or (key == "CHEATS" and path.name.lower() == "index.md"):
                continue
            relative = path.resolve().relative_to(refs_root.resolve())
            text = read_text(path)
            if text is None:
                continue
            build = build_for(ref, relative, builds)
            for address, line in addresses(text, key == "CHEATS" and path.suffix.lower() == ".txt"):
                rows.add((address, build, key, relative.as_posix(), line))
    output.mkdir(parents=True, exist_ok=True)
    path = output / "addresses.tsv"
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(FIELDS)
        for address, *rest in sorted(rows):
            writer.writerow(["0x%08X" % address, *rest])
    return len(rows)


def lookup(directory: Path, address: int, build: str):
    """索引が無い環境でも空の結果を返す。別ビルドは混ぜない。"""
    for path in sorted(directory.glob("*.tsv")):
        with path.open(encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream, delimiter="\t"):
                if int(row["address"], 0) == address and row["build"] in (build, UNKNOWN):
                    yield row


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    repo = Path(os.environ.get("AC3DS_REPO") or Path(__file__).resolve().parent.parent)
    parser.add_argument("--refs-root", type=Path, default=local_dir(repo) / "refs",
                        help="台帳の path の基準（既定: _local/refs）")
    parser.add_argument("--output-dir", type=Path, default=index_dir(repo),
                        help="索引の出力先（既定: _local/refs/index）")
    args = parser.parse_args(argv)
    try:
        count = generate(repo, args.refs_root, args.output_dir)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print("%s: %d 件" % (args.output_dir / "addresses.tsv", count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
