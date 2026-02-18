from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class BudgetRuleSettings:
    daily_token_budget: int
    weekly_token_budget: int
    warning_ratio: float


@dataclass(frozen=True)
class BudgetAlert:
    level: str
    message: str
    daily_tokens: int
    weekly_tokens: int


def _parse_positive_int(value: str, default_value: int) -> int:
    try:
        parsed = int(value.strip())
    except (TypeError, ValueError):
        return default_value
    if parsed <= 0:
        return default_value
    return parsed


def _parse_warning_ratio(value: str, default_ratio: float) -> float:
    try:
        parsed = int(value.strip())
    except (TypeError, ValueError):
        return default_ratio
    parsed = min(100, max(1, parsed))
    return parsed / 100.0


def load_budget_rule_settings() -> BudgetRuleSettings:
    daily_budget = _parse_positive_int(
        os.getenv("AUIW_DAILY_TOKEN_BUDGET", "20000"), default_value=20000
    )
    weekly_budget = _parse_positive_int(
        os.getenv("AUIW_WEEKLY_TOKEN_BUDGET", "100000"), default_value=100000
    )
    warning_ratio = _parse_warning_ratio(
        os.getenv("AUIW_ALERT_THRESHOLD_PCT", "80"), default_ratio=0.8
    )
    return BudgetRuleSettings(
        daily_token_budget=daily_budget,
        weekly_token_budget=weekly_budget,
        warning_ratio=warning_ratio,
    )


def evaluate_budget_alert(
    *,
    daily_tokens: int,
    weekly_tokens: int,
    settings: BudgetRuleSettings,
) -> BudgetAlert:
    daily_ratio = daily_tokens / settings.daily_token_budget
    weekly_ratio = weekly_tokens / settings.weekly_token_budget
    max_ratio = max(daily_ratio, weekly_ratio)

    if max_ratio >= 1.0:
        return BudgetAlert(
            level="critical",
            message=(
                "예산 경고: 일/주 토큰 예산을 초과했습니다. "
                "사용량을 점검하거나 예산 기준을 조정해 주세요."
            ),
            daily_tokens=daily_tokens,
            weekly_tokens=weekly_tokens,
        )

    if max_ratio >= settings.warning_ratio:
        return BudgetAlert(
            level="warning",
            message=(
                "주의: 토큰 사용량이 예산 임계치에 근접했습니다. "
                "오늘/이번 주 사용 추세를 확인해 주세요."
            ),
            daily_tokens=daily_tokens,
            weekly_tokens=weekly_tokens,
        )

    return BudgetAlert(
        level="normal",
        message="정상: 토큰 사용량이 예산 임계치 이내입니다.",
        daily_tokens=daily_tokens,
        weekly_tokens=weekly_tokens,
    )
