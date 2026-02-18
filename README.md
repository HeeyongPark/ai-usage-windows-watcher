# AI Usage Watcher for Windows

Local-first usage tracker for AI tools on Windows.

## Goal
- Capture tool/session usage metadata.
- Store records in local SQLite.
- Show daily summary for quick budget tracking.

## Current Scope
- Phase 1 bootstrap for agent, storage schema, CLI summary, and Windows UI (OAuth + Codex daily/weekly view + budget alert rule).

## Project Layout
- `agent/README.md`: agent usage guide
- `agent/src/`: collector, storage, and CLI
- `agent/sql/`: SQLite schema
- `agent/tests/`: pytest-based smoke tests
- `desktop_win/README.md`: Windows UI guide
- `desktop_win/src/app.py`: desktop dashboard entrypoint
- `desktop_win/src/oauth_client.py`: OAuth PKCE login client
