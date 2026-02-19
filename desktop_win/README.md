# Windows UI (OAuth + Codex Usage)

Tkinter-based Windows desktop MVP.

## What this does now
- OAuth login button (Authorization Code + PKCE).
- Codex daily/weekly usage tabs from local SQLite.
- Quick sample insertion for demo.
- Default fullscreen startup for small displays (5-inch monitor friendly).
- Auto refresh every 1 hour by default.
- Budget alert rule panel (daily/weekly token threshold).
- Windows no-install `onedir` bundle build and launcher flow.

## Run (no-install onedir bundle, recommended for users)
PowerShell (Windows build machine):
```powershell
cd C:\path\to\ai-usage-windows-watcher\desktop_win\
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows_bundle.ps1
```

Bundle output:
- `desktop_win\dist\AIUsageWatcher\`
- main app: `AIUsageWatcher.exe`
- launcher: `run_ai_usage_watcher.bat`
- evidence helper: `collect_windows_smoke_evidence.bat`
- evidence scripts: `prepare_windows_smoke_evidence.ps1`, `windows_runtime_probe.ps1`
- evidence templates: `smoke_evidence\templates\*.md`
- config template: `.env.example`
- build script pins bundle layout to `_internal` and validates `collector.py` path

End-user launch:
- Double-click `run_ai_usage_watcher.bat`
- For smoke evidence, double-click `collect_windows_smoke_evidence.bat`
- Fill `.env` OAuth values before first login

## Run (development)
```bash
cd /Users/mirador/Documents/ai-usage-windows-watcher/agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd /Users/mirador/Documents/ai-usage-windows-watcher/desktop_win
python src/app.py
```

## Windows quick start
- See `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/WINDOWS_USAGE.md`

## Windows runtime smoke artifacts
- One-click evidence collector (bundle root):
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/collect_windows_smoke_evidence.bat`
- Evidence pack helper script:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/prepare_windows_smoke_evidence.ps1`
- Runtime probe script:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/windows_runtime_probe.ps1`
- Bundle build script:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/build_windows_bundle.ps1`
- Launcher script:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/scripts/run_ai_usage_watcher.bat`
- Manual checklist:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-smoke-checklist.md`
- Evidence template:
  - `/Users/mirador/Documents/ai-usage-windows-watcher/desktop_win/tests/manual/windows-runtime-evidence-template.md`

Quick start (Windows evidence pack):
1) from onedir bundle root:
```bat
collect_windows_smoke_evidence.bat
```

2) from repository (build/dev machine):
```powershell
cd C:\path\to\ai-usage-windows-watcher\desktop_win\
powershell -ExecutionPolicy Bypass -File .\scripts\prepare_windows_smoke_evidence.ps1 -BundleRoot .\dist\AIUsageWatcher
```

## OAuth config
Create `.env` from `.env.example` before launching.
`.env` loading behavior:
- development mode: auto-load `desktop_win/.env`
- bundled (`frozen`) mode: resolve in this order
  - `sys._MEIPASS/.env`
  - `AIUsageWatcher.exe` directory `.env`
  - `AIUsageWatcher.exe` directory `_internal/.env`

Required:
- `AUIW_OAUTH_AUTH_URL`
- `AUIW_OAUTH_TOKEN_URL`
- `AUIW_OAUTH_CLIENT_ID`

The app stores OAuth tokens at:
- Windows: `%APPDATA%\\AIUsageWatcher\\oauth_token.json`
- Others: `~/.ai-usage-watcher/oauth_token.json`

## Fullscreen controls
- `F11`: toggle fullscreen
- `Esc`: exit fullscreen

## Refresh interval
- default: `1 hour` (`AUIW_REFRESH_INTERVAL_SEC=3600`)
- manual immediate refresh: `새로고침` button

## Budget alert rule
- `AUIW_DAILY_TOKEN_BUDGET` (default `20000`)
- `AUIW_WEEKLY_TOKEN_BUDGET` (default `100000`)
- `AUIW_ALERT_THRESHOLD_PCT` (default `80`)
- 상태 기준:
  - normal: 임계치 미만
  - warning: 임계치 비율 이상
  - critical: 예산 초과
