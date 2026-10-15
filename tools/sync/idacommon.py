"""IDA（idalib）を使う道具の共通部分。idalib の python（workspace.local.toml の idalib_python）で動かす。"""
from __future__ import annotations

import hashlib
import os
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent  # ac3ds-re
WORKSPACE = Path(os.environ.get("AC3DS_WORKSPACE") or REPO.parent)

sys.path.insert(0, str(HERE))


def local_config() -> dict:
    p = WORKSPACE / "workspace.local.toml"
    if p.exists():
        with open(p, "rb") as f:
            return tomllib.load(f)
    return {}


def data_dir() -> Path:
    p = WORKSPACE / "workspace.toml"
    name = "_local"
    if p.exists():
        with open(p, "rb") as f:
            name = tomllib.load(f).get("data", "_local")
    return WORKSPACE / name


def load_builds() -> dict:
    with open(REPO / "meta" / "builds.toml", "rb") as f:
        return tomllib.load(f)["builds"]


def build_info(build: str) -> dict:
    b = load_builds()
    if build not in b or "segments" not in b[build]:
        raise SystemExit("解析の対象ではないビルド: %s" % build)
    return b[build]


def build_dir(build: str) -> Path:
    return data_dir() / "builds" / build


def code_bin_path(build: str) -> Path:
    base = build_dir(build) / "extracted"
    for rel in ("update/exefs/code.bin", "exefs/code.bin"):
        if (base / rel).exists():
            return base / rel
    raise SystemExit("code.bin が見つからない: %s" % base)


def exheader_path(build: str) -> Path:
    return code_bin_path(build).parent.parent / "exheader.bin"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def seg_ranges(info: dict) -> dict[str, tuple[int, int]]:
    return {k: (int(v[0], 16), int(v[1], 16)) for k, v in info["segments"].items()}


def init_ida(console: bool = False):
    """idapro を読み込む。環境変数は import の前に決める。"""
    cfg = local_config()
    os.environ.setdefault("IDADIR", cfg.get("ida_dir", "C:/Program Files/IDA Professional 9.3"))
    usr = data_dir() / "ida-user"
    usr.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("IDAUSR", str(usr))  # プラグインを入れない空の設定
    import idapro  # noqa: WPS433

    idapro.enable_console_messages(console)
    return idapro


class OpenDb:
    """with OpenDb(path, save=True) as _: ... で IDB を開いて閉じる。"""

    def __init__(self, path, save: bool = False, auto: bool = False, args: str | None = None, console: bool = False):
        self.path = str(path)
        self.save = save
        self.auto = auto
        self.args = args
        self.console = console

    def __enter__(self):
        self.idapro = init_ida(self.console)
        rc = self.idapro.open_database(self.path, self.auto, args=self.args) if self.args else \
            self.idapro.open_database(self.path, self.auto)
        if rc != 0:
            raise SystemExit("IDB を開けない (rc=%s): %s" % (rc, self.path))
        return self

    def __exit__(self, et, ev, tb):
        self.idapro.close_database(bool(self.save and et is None))
        return False


def ida_version() -> str:
    import ida_kernwin

    return ida_kernwin.get_kernel_version()


def processor_info() -> dict:
    """プロセッサ・コンパイラ・セグメントの設定を、比較できる形で返す。"""
    import ida_ida
    import ida_nalt
    import ida_segment
    import ida_typeinf

    d: dict = {}
    for n in sorted(dir(ida_ida)):
        if n.startswith("inf_get_") and n not in (
            "inf_get_min_ea", "inf_get_max_ea", "inf_get_main", "inf_get_start_ea", "inf_get_start_ip",
            "inf_get_start_cs", "inf_get_start_ss", "inf_get_start_sp", "inf_get_privrange_start_ea",
            "inf_get_privrange_end_ea", "inf_get_omin_ea", "inf_get_omax_ea", "inf_get_lowoff", "inf_get_highoff",
            "inf_get_database_change_count", "inf_get_ctime", "inf_get_elapsed", "inf_get_nopens",
            "inf_get_idb_ctime", "inf_get_idb_version", "inf_get_genflags", "inf_get_main", "inf_get_start_ip",
        ):
            try:
                v = getattr(ida_ida, n)()
            except Exception:  # noqa: BLE001
                continue
            if isinstance(v, (int, str, bool, bytes)):
                d[n[8:]] = v
    d["compiler"] = ida_typeinf.get_compiler_name(ida_ida.inf_get_cc_id())
    d["imagebase"] = ida_nalt.get_imagebase()
    segs = []
    for i in range(ida_segment.get_segm_qty()):
        s = ida_segment.getnseg(i)
        segs.append({"name": ida_segment.get_segm_name(s), "start": s.start_ea, "end": s.end_ea, "perm": s.perm,
                     "class": ida_segment.get_segm_class(s), "bitness": s.bitness, "align": s.align,
                     "comb": s.comb})
    d["segments"] = segs
    return d
