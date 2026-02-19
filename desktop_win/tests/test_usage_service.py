from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESKTOP_SRC = ROOT / "desktop_win" / "src"
AGENT_SRC = ROOT / "agent" / "src"

for path in (str(DESKTOP_SRC), str(AGENT_SRC)):
    if path not in sys.path:
        sys.path.insert(0, path)

from collector import UsageCollector, UsageEvent, now_utc  # noqa: E402
import storage  # noqa: E402
import usage_service  # noqa: E402
from usage_service import codex_daily_summary, codex_weekly_summary  # noqa: E402


def _insert_session(
    db_path: Path, tool_name: str, session_id: str, start_offset_days: int = 0
) -> None:
    start_at = now_utc() - timedelta(minutes=30, days=start_offset_days)
    end_at = now_utc()
    events = [
        UsageEvent(
            event_id=f"{session_id}-start",
            session_id=session_id,
            tool_name=tool_name,
            event_type="session_start",
            occurred_at=start_at,
        ),
        UsageEvent(
            event_id=f"{session_id}-request",
            session_id=session_id,
            tool_name=tool_name,
            event_type="request",
            occurred_at=start_at + timedelta(minutes=10),
        ),
        UsageEvent(
            event_id=f"{session_id}-token",
            session_id=session_id,
            tool_name=tool_name,
            event_type="token_estimate",
            occurred_at=end_at - timedelta(minutes=1),
            payload_json="321",
        ),
        UsageEvent(
            event_id=f"{session_id}-end",
            session_id=session_id,
            tool_name=tool_name,
            event_type="session_end",
            occurred_at=end_at,
        ),
    ]

    collector = UsageCollector()
    session = collector.build_session_from_events(events)
    with storage.connect(db_path) as connection:
        storage.init_db(connection)
        storage.upsert_session(connection, session)
        for event in events:
            storage.append_event(connection, event)


def test_codex_daily_summary_only_returns_codex(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "usage.db"
    monkeypatch.setenv("AUIW_DB_PATH", str(db_path))

    _insert_session(db_path, "codex", "session-codex")
    _insert_session(db_path, "chatgpt", "session-chatgpt")

    rows = codex_daily_summary()
    assert len(rows) == 1
    assert rows[0]["tool_name"] == "codex"


def test_codex_weekly_summary_aggregates_codex_sessions(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "usage.db"
    monkeypatch.setenv("AUIW_DB_PATH", str(db_path))

    _insert_session(db_path, "codex", "session-codex-a")
    _insert_session(db_path, "codex", "session-codex-b", start_offset_days=8)
    _insert_session(db_path, "chatgpt", "session-chatgpt")

    rows = codex_weekly_summary()
    assert len(rows) >= 1
    assert all(row["tool_name"] == "codex" for row in rows)


def test_runtime_root_uses_meipass_first_when_frozen(monkeypatch, tmp_path: Path) -> None:
    fake_executable = tmp_path / "dist" / "AIUsageWatcher" / "AIUsageWatcher.exe"
    fake_meipass = tmp_path / "dist" / "AIUsageWatcher" / "_internal"
    fake_executable.parent.mkdir(parents=True)
    fake_meipass.mkdir(parents=True)
    fake_executable.write_text("stub", encoding="utf-8")

    monkeypatch.setattr(usage_service.sys, "frozen", True, raising=False)
    monkeypatch.setattr(usage_service.sys, "executable", str(fake_executable))
    monkeypatch.setattr(usage_service.sys, "_MEIPASS", str(fake_meipass), raising=False)

    assert usage_service._runtime_root() == fake_meipass


def test_runtime_root_falls_back_to_executable_when_meipass_missing(
    monkeypatch, tmp_path: Path
) -> None:
    fake_executable = tmp_path / "dist" / "AIUsageWatcher" / "AIUsageWatcher.exe"
    fake_executable.parent.mkdir(parents=True)
    fake_executable.write_text("stub", encoding="utf-8")

    monkeypatch.setattr(usage_service.sys, "frozen", True, raising=False)
    monkeypatch.setattr(usage_service.sys, "executable", str(fake_executable))
    monkeypatch.delattr(usage_service.sys, "_MEIPASS", raising=False)

    assert usage_service._runtime_root() == fake_executable.parent


def test_agent_src_path_from_runtime_root(tmp_path: Path) -> None:
    runtime_root = tmp_path / "AIUsageWatcher"
    expected = runtime_root / "agent" / "src"
    assert usage_service._agent_src_path(runtime_root) == expected


def test_resolve_agent_src_path_supports_internal_layout(
    monkeypatch, tmp_path: Path
) -> None:
    fake_executable = tmp_path / "dist" / "AIUsageWatcher" / "AIUsageWatcher.exe"
    fake_executable.parent.mkdir(parents=True)
    fake_executable.write_text("stub", encoding="utf-8")
    internal_agent_src = fake_executable.parent / "_internal" / "agent" / "src"
    internal_agent_src.mkdir(parents=True)
    (internal_agent_src / "collector.py").write_text("# stub", encoding="utf-8")

    monkeypatch.setattr(usage_service.sys, "frozen", True, raising=False)
    monkeypatch.setattr(usage_service.sys, "executable", str(fake_executable))
    monkeypatch.delattr(usage_service.sys, "_MEIPASS", raising=False)

    assert usage_service._resolve_agent_src_path() == internal_agent_src
