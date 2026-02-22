from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESKTOP_SRC = ROOT / "desktop_win" / "src"
if str(DESKTOP_SRC) not in sys.path:
    sys.path.insert(0, str(DESKTOP_SRC))

from app import _font_option_value, resolve_refresh_interval_ms  # noqa: E402


def test_refresh_interval_default(monkeypatch) -> None:
    monkeypatch.delenv("AUIW_REFRESH_INTERVAL_SEC", raising=False)
    assert resolve_refresh_interval_ms() == 3_600_000


def test_refresh_interval_has_minimum(monkeypatch) -> None:
    monkeypatch.setenv("AUIW_REFRESH_INTERVAL_SEC", "1")
    assert resolve_refresh_interval_ms() == 60_000


def test_font_option_value_escapes_family_with_space() -> None:
    assert _font_option_value(11) == "{Segoe UI} 11"
