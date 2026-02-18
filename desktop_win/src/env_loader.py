from __future__ import annotations

import os
from pathlib import Path


def load_env_file(env_path: Path | None = None, override: bool = False) -> Path:
    if env_path is None:
        env_path = Path(__file__).resolve().parents[1] / ".env"

    if not env_path.exists():
        return env_path

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if override or key not in os.environ:
            os.environ[key] = value

    return env_path

