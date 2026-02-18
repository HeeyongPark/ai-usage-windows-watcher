from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / ".ai-usage-watcher" / "usage.db"
DEFAULT_PROCESS_PATTERNS = ["codex", "chatgpt", "claude", "cursor"]


def _parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    db_path: Path = DEFAULT_DB_PATH
    process_patterns: list[str] = field(
        default_factory=lambda: DEFAULT_PROCESS_PATTERNS.copy()
    )


def load_settings() -> Settings:
    db_path = Path(os.getenv("AUIW_DB_PATH", str(DEFAULT_DB_PATH))).expanduser()
    patterns_raw = os.getenv("AUIW_PROCESS_PATTERNS", "")
    process_patterns = _parse_csv(patterns_raw) or DEFAULT_PROCESS_PATTERNS.copy()
    return Settings(db_path=db_path, process_patterns=process_patterns)


def ensure_db_parent(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)

