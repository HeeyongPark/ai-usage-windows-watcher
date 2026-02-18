from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESKTOP_SRC = ROOT / "desktop_win" / "src"
if str(DESKTOP_SRC) not in sys.path:
    sys.path.insert(0, str(DESKTOP_SRC))

from oauth_client import load_token, save_token  # noqa: E402


def test_save_and_load_token(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("APPDATA", str(tmp_path))
    payload = {"access_token": "abc123", "token_type": "bearer"}
    saved_path = save_token(payload)
    assert saved_path.exists()
    loaded = load_token()
    assert loaded == payload

