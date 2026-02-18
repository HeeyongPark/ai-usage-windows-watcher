from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESKTOP_SRC = ROOT / "desktop_win" / "src"
if str(DESKTOP_SRC) not in sys.path:
    sys.path.insert(0, str(DESKTOP_SRC))

from budget_rules import evaluate_budget_alert, load_budget_rule_settings  # noqa: E402


def test_load_budget_rule_settings_defaults(monkeypatch) -> None:
    monkeypatch.delenv("AUIW_DAILY_TOKEN_BUDGET", raising=False)
    monkeypatch.delenv("AUIW_WEEKLY_TOKEN_BUDGET", raising=False)
    monkeypatch.delenv("AUIW_ALERT_THRESHOLD_PCT", raising=False)
    settings = load_budget_rule_settings()
    assert settings.daily_token_budget == 20000
    assert settings.weekly_token_budget == 100000
    assert settings.warning_ratio == 0.8


def test_evaluate_budget_alert_warning_and_critical() -> None:
    settings = load_budget_rule_settings()

    warning = evaluate_budget_alert(
        daily_tokens=16000,
        weekly_tokens=30000,
        settings=settings,
    )
    assert warning.level == "warning"

    critical = evaluate_budget_alert(
        daily_tokens=25000,
        weekly_tokens=30000,
        settings=settings,
    )
    assert critical.level == "critical"
