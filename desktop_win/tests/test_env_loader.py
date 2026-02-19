from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESKTOP_SRC = ROOT / "desktop_win" / "src"
if str(DESKTOP_SRC) not in sys.path:
    sys.path.insert(0, str(DESKTOP_SRC))

import env_loader  # noqa: E402
from env_loader import load_env_file  # noqa: E402


def test_load_env_file_sets_variables(tmp_path: Path, monkeypatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "# comment",
                "AUIW_OAUTH_CLIENT_ID=test-client",
                "AUIW_OAUTH_SCOPE=openid profile",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.delenv("AUIW_OAUTH_CLIENT_ID", raising=False)
    monkeypatch.delenv("AUIW_OAUTH_SCOPE", raising=False)

    load_env_file(env_file)

    assert os.getenv("AUIW_OAUTH_CLIENT_ID") == "test-client"
    assert os.getenv("AUIW_OAUTH_SCOPE") == "openid profile"


def test_default_env_path_prefers_meipass_env_when_frozen(
    tmp_path: Path, monkeypatch
) -> None:
    fake_executable = tmp_path / "dist" / "AIUsageWatcher" / "AIUsageWatcher.exe"
    fake_meipass = tmp_path / "dist" / "AIUsageWatcher" / "_internal"
    fake_executable.parent.mkdir(parents=True)
    fake_meipass.mkdir(parents=True)
    fake_executable.write_text("stub", encoding="utf-8")
    meipass_env = fake_meipass / ".env"
    meipass_env.write_text("AUIW_TEST=1\n", encoding="utf-8")
    (fake_executable.parent / ".env").write_text("AUIW_TEST=2\n", encoding="utf-8")

    monkeypatch.setattr(env_loader.sys, "frozen", True, raising=False)
    monkeypatch.setattr(env_loader.sys, "executable", str(fake_executable))
    monkeypatch.setattr(env_loader.sys, "_MEIPASS", str(fake_meipass), raising=False)

    assert env_loader.default_env_path() == meipass_env


def test_default_env_path_falls_back_to_executable_then_internal(
    tmp_path: Path, monkeypatch
) -> None:
    fake_executable = tmp_path / "dist" / "AIUsageWatcher" / "AIUsageWatcher.exe"
    fake_meipass = tmp_path / "dist" / "AIUsageWatcher" / "_internal"
    fake_executable.parent.mkdir(parents=True)
    fake_meipass.mkdir(parents=True)
    fake_executable.write_text("stub", encoding="utf-8")

    monkeypatch.setattr(env_loader.sys, "frozen", True, raising=False)
    monkeypatch.setattr(env_loader.sys, "executable", str(fake_executable))
    monkeypatch.setattr(env_loader.sys, "_MEIPASS", str(fake_meipass), raising=False)

    exe_env = fake_executable.parent / ".env"
    exe_env.write_text("AUIW_TEST=2\n", encoding="utf-8")
    assert env_loader.default_env_path() == exe_env

    exe_env.unlink()
    internal_env = fake_executable.parent / "_internal" / ".env"
    internal_env.write_text("AUIW_TEST=3\n", encoding="utf-8")
    assert env_loader.default_env_path() == internal_env
