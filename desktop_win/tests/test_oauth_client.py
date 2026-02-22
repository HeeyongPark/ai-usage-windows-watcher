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


def test_open_auth_page_default_mode_uses_webbrowser(monkeypatch) -> None:
    monkeypatch.setenv("AUIW_OAUTH_BROWSER", "default")
    monkeypatch.setattr(oauth_client.webbrowser, "open", lambda _: True)
    monkeypatch.setattr(oauth_client, "_open_auth_page_in_chrome", lambda _: False)
    _open_auth_page("https://example.com/oauth")


def test_open_auth_page_chrome_mode_prefers_chrome(monkeypatch) -> None:
    monkeypatch.setenv("AUIW_OAUTH_BROWSER", "chrome")
    state = {"web_open_called": False}

    monkeypatch.setattr(oauth_client, "_open_auth_page_in_chrome", lambda _: True)

    def _web_open(_: str) -> bool:
        state["web_open_called"] = True
        return True

    monkeypatch.setattr(oauth_client.webbrowser, "open", _web_open)
    _open_auth_page("https://example.com/oauth")
    assert state["web_open_called"] is False


def test_open_auth_page_chrome_mode_falls_back_to_webbrowser(monkeypatch) -> None:
    monkeypatch.setenv("AUIW_OAUTH_BROWSER", "chrome")
    monkeypatch.setattr(oauth_client, "_open_auth_page_in_chrome", lambda _: False)
    monkeypatch.setattr(oauth_client.webbrowser, "open", lambda _: True)
    _open_auth_page("https://example.com/oauth")


def test_open_auth_page_chrome_only_raises_when_chrome_not_opened(monkeypatch) -> None:
    monkeypatch.setenv("AUIW_OAUTH_BROWSER", "chrome_only")
    monkeypatch.setattr(oauth_client, "_open_auth_page_in_chrome", lambda _: False)
    with pytest.raises(RuntimeError):
        _open_auth_page("https://example.com/oauth")


def test_open_auth_page_raises_when_browser_not_opened(monkeypatch) -> None:
    monkeypatch.setenv("AUIW_OAUTH_BROWSER", "default")
    monkeypatch.setattr(oauth_client.webbrowser, "open", lambda _: False)
    url = "https://example.com/oauth"
    with pytest.raises(RuntimeError) as exc:
        _open_auth_page(url)
    assert url in str(exc.value)


def test_open_auth_page_invalid_browser_mode_raises(monkeypatch) -> None:
    monkeypatch.setenv("AUIW_OAUTH_BROWSER", "safari")
    with pytest.raises(ValueError):
        _open_auth_page("https://example.com/oauth")
