"""code.bin から独立解析を作り、別コピーへ symbols を取り込む。README.md 参照。"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import tomllib

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import symlib
# このディレクトリの ghidra が Java パッケージを隠さないよう、起動前に外す。
sys.path.remove(str(HERE.parent))
from common import LANGUAGE, COMPILER, plan_segments, compare_starts, ida_starts, discover_workspace, discover_ghidra


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def write_comparison(project, base, info, backend):
    index = base / "export/index.txt"
    ida = ida_starts(index, info["code_sha256"])
    import pyghidra
    with pyghidra.program_context(project, "/independent") as program:
        starts = {int(f.getEntryPoint().getOffset()) for f in program.getFunctionManager().getFunctions(True)}
    diff = compare_starts(ida, starts)
    diff.update(backend.compare_boundaries(project, ida))
    diff["ida_index"] = str(index)
    diff["ida_index_header"] = index.read_text(encoding="utf-8").splitlines()[:5]
    write_json(base / "ghidra/starts.json", diff)
    return {key: value for key, value in diff.items() if key not in ("ida_only", "ghidra_only")}


def main(argv=None):
    start = time.monotonic()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["create", "import", "dump", "compare"])
    ap.add_argument("--build", required=True)
    ap.add_argument("--workspace", type=Path, default=os.environ.get("AC3DS_WORKSPACE"))
    ap.add_argument("--ghidra", type=Path, default=os.environ.get("GHIDRA_INSTALL_DIR"))
    ap.add_argument("--target", help="番地または symbols の関数名")
    ap.add_argument("--view", choices=["independent", "symbols"], default="independent")
    ap.add_argument("--out", type=Path, help="dump の出力テキスト")
    ap.add_argument("--create", action="store_true", dest="create_requested", help="dump: 一時コピーで指定番地から関数を作成")
    ap.add_argument("--mode", choices=["arm", "thumb"], help="dump --create の命令セット（省略時は symbols の下位ビット、無ければ ARM）")
    a = ap.parse_args(argv)
    if (a.create_requested or a.mode) and (a.action != "dump" or a.view != "independent"):
        ap.error("--create / --mode は独立ビューの dump で使う")
    if a.mode and not a.create_requested:
        ap.error("--mode には --create が必要")
    a.workspace = discover_workspace(REPO, a.workspace)
    a.ghidra = discover_ghidra(a.workspace, a.ghidra)
    if a.action == "dump":
        if not a.target:
            ap.error("dump には --target が必要")
        if a.out is None:
            a.out = a.workspace / "_local/builds" / a.build / "ghidra/dump.txt"
    with (REPO / "meta/builds.toml").open("rb") as f:
        info = tomllib.load(f)["builds"][a.build]
    base = a.workspace / "_local/builds" / a.build
    project_dir = base / "ghidra"
    symbols = REPO / "symbols" / a.build
    # JVM を起動する前に入力を検証する。
    if a.action == "import":
        with (symbols / "meta.toml").open("rb") as f:
            meta = tomllib.load(f)
        if meta["build"] != a.build or meta["code_sha256"] != info["code_sha256"]:
            raise ValueError("symbols のビルド・ハッシュが builds.toml と違う")
    if a.action == "dump" and a.out is not None:
        if not a.out.resolve().is_relative_to((a.workspace / "_local").resolve()):
            raise ValueError("逆コンパイルの出力先は作業場の _local の中に指定する")
    if a.action == "create":
        code = next((p for p in (base / "extracted/update/exefs/code.bin", base / "extracted/exefs/code.bin") if p.exists()), None)
        if code is None:
            raise FileNotFoundError("code.bin がない")
        data = code.read_bytes()
        segments = plan_segments(info, data)
        if (project_dir / "create.json").exists():
            raise FileExistsError("プロジェクトは既存（上書きしない）")
    import pyghidra
    pyghidra.start(install_dir=a.ghidra)
    import backend
    project_dir.mkdir(parents=True, exist_ok=True)
    project = pyghidra.open_project(project_dir, "ac3ds", create=a.action == "create")
    try:
        if a.action == "create":
            if project.getProjectData().getFile("/independent") is not None:
                raise FileExistsError("independent は既存（上書きしない）")
            result = backend.create(project, data, segments)
            result.update(build=a.build, code_sha256=info["code_sha256"], language=LANGUAGE, compiler=COMPILER,
                          segments=segments, seconds=time.monotonic() - start)
            write_json(project_dir / "create.json", result)
        else:
            manifest = json.loads((project_dir / "create.json").read_text(encoding="utf-8"))
            if manifest["code_sha256"] != info["code_sha256"] or manifest["build"] != a.build:
                raise ValueError("プロジェクトの由来が builds.toml と違う")
            if a.action == "import":
                result = backend.import_symbols(project, symlib.read_all(symbols), symbols / "types")
                result["seconds"] = time.monotonic() - start
                result["symbols_sha256"] = {p.relative_to(symbols).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                                             for p in sorted(symbols.rglob("*")) if p.is_file()}
                write_json(project_dir / "import.json", result)
            elif a.action == "compare":
                result = write_comparison(project, base, info, backend)
            else:
                if not a.target or not a.out:
                    ap.error("dump には --target と --out が必要")
                backend.dump(project, a.view, a.target, symlib.read_all(symbols)["functions"], a.out, manifest,
                             create_requested=a.create_requested, mode=a.mode, scratch=project_dir)
                result = {"out": str(a.out), "view": a.view}
        if a.action == "create" and (base / "export/index.txt").exists():
            write_comparison(project, base, info, backend)
        print(json.dumps({k: v for k, v in result.items() if k != "starts"}, ensure_ascii=False, default=str))
    finally:
        project.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

