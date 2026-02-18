# Windows Runtime Smoke Checklist

## Scope
- OS targets: Windows 10 (22H2+) and Windows 11
- App target: `desktop_win/src/app.py`
- Required evidence:
  - runtime context JSON (`windows_runtime_probe.ps1`)
  - pass/fail checklist
  - screenshot or log for every failed step

## Run Metadata
- Run date (local):
- Tester:
- Machine:
- OS version:
- Python version:
- Screen resolution:
- OAuth provider:

## Required Scenarios
1. Install and launch
- Step:
  - Create venv in `agent`, install requirements, launch `python .\src\app.py`.
- Expected:
  - App window starts without traceback and shows dashboard UI.
- Result:
  - [ ] pass
  - [ ] fail
- Evidence:

2. OAuth login
- Step:
  - Click `OAuth 로그인`, complete browser auth, return to app.
- Expected:
  - Status changes to `OAuth 완료` and no blocking error dialog.
- Result:
  - [ ] pass
  - [ ] fail
- Evidence:

3. Data visibility
- Step:
  - Click `Codex 샘플 1건 생성`, verify daily/weekly rows.
- Expected:
  - Daily and weekly tabs both show codex rows.
- Result:
  - [ ] pass
  - [ ] fail
- Evidence:

4. Refresh interval guard
- Step:
  - Set `AUIW_REFRESH_INTERVAL_SEC=10` and relaunch.
- Expected:
  - App applies minimum guard (`60s`) and remains stable.
- Result:
  - [ ] pass
  - [ ] fail
- Evidence:

5. Budget alert states
- Step:
  - Use low token budget env values and trigger sample creation.
- Expected:
  - Alert state transitions to `warning` or `critical`.
- Result:
  - [ ] pass
  - [ ] fail
- Evidence:

6. Restart durability
- Step:
  - Close app, relaunch app.
- Expected:
  - OAuth token and local usage DB remain available.
- Result:
  - [ ] pass
  - [ ] fail
- Evidence:

## Severity Rules
- P0:
  - App launch failure, OAuth login blocked, no data rendering
- P1:
  - Refresh scheduler failure, budget status mismatch
- P2:
  - Text clipping or compact-mode usability issue

## Final Decision
- Overall:
  - [ ] pass
  - [ ] fail
- Blocking issues:
- Follow-up action:
