from __future__ import annotations

import os
import sys
from pathlib import Path


def _dedupe_paths(paths: list[Path]) -> list[Path]:
    unique: list[Path] = []
    for path in paths:
        if path not in unique:
            unique.append(path)
    return unique


def _runtime_roots() -> list[Path]:
    if getattr(sys, "frozen", False):
        candidates: list[Path] = []
        meipass = getattr(sys, "_MEIPASS", "")
        if meipass:
            candidates.append(Path(meipass).resolve())
        executable_dir = Path(sys.executable).resolve().parent
        candidates.append(executable_dir)
        candidates.append(executable_dir / "_internal")
        return _dedupe_paths(candidates)
    return [Path(__file__).resolve().parents[1]]


def default_env_path() -> Path:
    roots = _runtime_roots()
    for root in roots:
        env_path = root / ".env"
        if env_path.exists():
            return env_path
    return roots[0] / ".env"


def load_env_file(env_path: Path | None = None, override: bool = False) -> Path:
    if env_path is None:
        env_path = default_env_path()

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
