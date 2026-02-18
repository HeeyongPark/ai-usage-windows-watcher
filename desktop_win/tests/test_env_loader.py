from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESKTOP_SRC = ROOT / "desktop_win" / "src"
if str(DESKTOP_SRC) not in sys.path:
    sys.path.insert(0, str(DESKTOP_SRC))

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

