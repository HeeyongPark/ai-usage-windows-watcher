from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESKTOP_SRC = ROOT / "desktop_win" / "src"
if str(DESKTOP_SRC) not in sys.path:
    sys.path.insert(0, str(DESKTOP_SRC))

import codex_auth  # noqa: E402


def _process(stdout: str, returncode: int = 0, stderr: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=["codex"],
        returncode=returncode,
        stdout=stdout,
        stderr=stderr,
    )


def test_codex_login_status_logged_in(monkeypatch) -> None:
    monkeypatch.setattr(
        codex_auth,
        "_run_codex",
        lambda *_args, **_kwargs: _process("Logged in using ChatGPT"),
    )
    status = codex_auth.codex_login_status()
    assert status.logged_in is True
    assert status.detail == "ChatGPT"


def test_codex_login_status_not_logged_in(monkeypatch) -> None:
    monkeypatch.setattr(
        codex_auth,
        "_run_codex",
        lambda *_args, **_kwargs: _process("Not logged in", returncode=1),
    )
    status = codex_auth.codex_login_status()
    assert status.logged_in is False
    assert status.detail == "Codex 미로그인"


def test_codex_login_status_cli_missing(monkeypatch) -> None:
    def _raise(*_args, **_kwargs):
        raise FileNotFoundError("`codex` CLI를 찾지 못했습니다.")

    monkeypatch.setattr(codex_auth, "_run_codex", _raise)
    status = codex_auth.codex_login_status()
    assert status.logged_in is False
    assert "codex" in status.detail


def test_codex_login_device_auth_success(monkeypatch) -> None:
    calls = {"count": 0}

    def _run(args, timeout_sec):  # noqa: ANN001
        calls["count"] += 1
        if args == ["login", "--device-auth"]:
            return _process("Login complete")
        if args == ["login", "status"]:
            return _process("Logged in using ChatGPT")
        raise AssertionError("unexpected args")

    monkeypatch.setattr(codex_auth, "_run_codex", _run)
    status = codex_auth.codex_login_device_auth()
    assert status.logged_in is True
    assert status.detail == "ChatGPT"
    assert calls["count"] >= 2


def test_codex_login_device_auth_timeout(monkeypatch) -> None:
    def _raise(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(cmd="codex", timeout=5)

    monkeypatch.setattr(codex_auth, "_run_codex", _raise)
    status = codex_auth.codex_login_device_auth()
    assert status.logged_in is False
    assert "시간 초과" in status.detail
