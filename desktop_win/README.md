# Windows UI (OAuth + Codex Usage)

Tkinter-based Windows desktop MVP.

## What this does now
- OAuth login button (Authorization Code + PKCE).
- Codex daily usage table from local SQLite.
- Quick sample insertion for demo.
- Default fullscreen startup for small displays (5-inch monitor friendly).
- Auto refresh every 1 hour by default.

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
