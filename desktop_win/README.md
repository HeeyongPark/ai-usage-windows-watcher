# Windows UI (OAuth + Codex Usage)

Tkinter-based Windows desktop MVP.

## What this does now
- OAuth login button (Authorization Code + PKCE).
- Codex daily/weekly usage tabs from local SQLite.
- Quick sample insertion for demo.
- Default fullscreen startup for small displays (5-inch monitor friendly).
- Auto refresh every 1 hour by default.
- Budget alert rule panel (daily/weekly token threshold).

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

## OAuth config
Create `.env` from `.env.example` before launching.
`src/app.py` auto-loads `desktop_win/.env`.

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
