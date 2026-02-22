from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DESKTOP_SRC = ROOT / "desktop_win" / "src"
if str(DESKTOP_SRC) not in sys.path:
    sys.path.insert(0, str(DESKTOP_SRC))

import oauth_client  # noqa: E402
from oauth_client import _open_auth_page, load_token, save_token  # noqa: E402


def test_save_and_load_token(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("APPDATA", str(tmp_path))
    payload = {"access_token": "abc123", "token_type": "bearer"}
    saved_path = save_token(payload)
    assert saved_path.exists()
    loaded = load_token()
    assert loaded == payload


def test_open_auth_page_raises_when_browser_not_opened(monkeypatch) -> None:
    monkeypatch.setattr(oauth_client.webbrowser, "open", lambda _: False)
    url = "https://example.com/oauth"
    with pytest.raises(RuntimeError) as exc:
        _open_auth_page(url)
    assert url in str(exc.value)


def test_open_auth_page_succeeds_when_browser_opened(monkeypatch) -> None:
    monkeypatch.setattr(oauth_client.webbrowser, "open", lambda _: True)
    _open_auth_page("https://example.com/oauth")
