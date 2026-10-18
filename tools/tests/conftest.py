import os
import shutil
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS))

# 試験で作るリポジトリごとに git fsmonitor の常駐の処理が残らないように
_n = int(os.environ.get("GIT_CONFIG_COUNT") or 0)
os.environ.update({"GIT_CONFIG_COUNT": str(_n + 1), "GIT_CONFIG_KEY_%d" % _n: "core.fsmonitor",
                   "GIT_CONFIG_VALUE_%d" % _n: "false"})


@pytest.fixture
def repo(tmp_path, monkeypatch):
    r = tmp_path / "repo"
    r.mkdir()
    shutil.copytree(REPO / "meta", r / "meta")
    monkeypatch.setenv("AC3DS_REPO", str(r))
    monkeypatch.setenv("AC3DS_STATE", str(tmp_path / "state"))
    return r
