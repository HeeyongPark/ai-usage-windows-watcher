# Integration Test

## Subject
- ai-usage-windows-watcher

## Latest Run
- pre_deploy:
  - pass
- post_deploy:
  - pending

## Pre-Deploy Run (2026-02-18 22:37 KST)
- mode:
  - pre_deploy
- test_profile:
  - ui_optional
- scope:
  - phase1-win-agent-usage-collector
  - phase1-desktop-dashboard
  - phase1-budget-alert-rule

### Planning AC -> 테스트 케이스 -> 코드 구현 매트릭스
- phase1-win-agent-usage-collector
  - AC: 로컬 수집/저장/조회 흐름 재현
  - 테스트: `agent/tests/test_cli.py`, `desktop_win/tests/test_usage_service.py`
  - 구현: `/Users/mirador/Documents/ai-usage-windows-watcher/agent/src/collector.py`, `/Users/mirador/Documents/ai-usage-windows-watcher/agent/src/storage.py`, `/Users/mirador/Documents/ai-usage-windows-watcher/agent/src/cli.py`
- phase1-desktop-dashboard
  - AC: Codex 일/주 집계 대시보드 제공
  - 테스트: `desktop_win/tests/test_usage_service.py`, `desktop_win/tests/test_refresh_interval.py`
  - 구현: `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py`, `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/usage_service.py`
- phase1-budget-alert-rule
  - AC: 예산 임계치 규칙과 UI 상태 표시
  - 테스트: `desktop_win/tests/test_budget_rules.py`
  - 구현: `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/budget_rules.py`, `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/app.py`

### 실행 증적
- command:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/agent/.venv/bin/python -m pytest -q`
  - `python3 -m py_compile /Users/mirador/Documents/ai-usage-windows-watcher/agent/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/src/*.py /Users/mirador/Documents/ai-usage-windows-watcher/agent/tests/*.py /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/*.py`
- result:
  - `9 passed in 0.09s`
  - py_compile 오류 없음

### Gate 판정
- overall:
  - pass
- git_release 진행 가능:
  - yes
- blockers:
  - 없음
