import shutil
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parent.parent
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS))


@pytest.fixture
def repo(tmp_path, monkeypatch):
    r = tmp_path / "repo"
    r.mkdir()
    shutil.copytree(REPO / "meta", r / "meta")
    monkeypatch.setenv("AC3DS_REPO", str(r))
    monkeypatch.setenv("AC3DS_STATE", str(tmp_path / "state"))
    return r
