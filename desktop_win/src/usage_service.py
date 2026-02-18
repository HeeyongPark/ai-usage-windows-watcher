from __future__ import annotations

import sys
import uuid
from datetime import timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
AGENT_SRC = ROOT / "agent" / "src"
if str(AGENT_SRC) not in sys.path:
    sys.path.insert(0, str(AGENT_SRC))

from collector import UsageCollector, UsageEvent, now_utc  # noqa: E402
from config import ensure_db_parent, load_settings  # noqa: E402
import storage  # noqa: E402


def codex_daily_summary() -> list[dict[str, Any]]:
    settings = load_settings()
    ensure_db_parent(settings.db_path)
    with storage.connect(settings.db_path) as connection:
        storage.init_db(connection)
        rows = storage.list_daily_summary(connection)

    codex_rows = []
    for row in rows:
        if row["tool_name"].lower() != "codex":
            continue
        codex_rows.append(
            {
                "day": row["day"],
                "tool_name": row["tool_name"],
                "sessions": int(row["sessions"]),
                "requests": int(row["requests"]),
                "tokens": int(row["tokens"]),
            }
        )
    return codex_rows


def insert_codex_sample_session(request_count: int = 5, token_estimate: int = 2500) -> str:
    settings = load_settings()
    ensure_db_parent(settings.db_path)

    session_id = str(uuid.uuid4())
    started_at = now_utc() - timedelta(minutes=15)
    ended_at = now_utc()

    events = [
        UsageEvent(
            event_id=str(uuid.uuid4()),
            session_id=session_id,
            tool_name="codex",
            event_type="session_start",
            occurred_at=started_at,
        ),
        UsageEvent(
            event_id=str(uuid.uuid4()),
            session_id=session_id,
            tool_name="codex",
            event_type="request",
            occurred_at=started_at + timedelta(minutes=3),
        ),
        UsageEvent(
            event_id=str(uuid.uuid4()),
            session_id=session_id,
            tool_name="codex",
            event_type="token_estimate",
            occurred_at=ended_at - timedelta(minutes=1),
            payload_json=str(token_estimate),
        ),
        UsageEvent(
            event_id=str(uuid.uuid4()),
            session_id=session_id,
            tool_name="codex",
            event_type="session_end",
            occurred_at=ended_at,
        ),
    ]

    collector = UsageCollector()
    session = collector.build_session_from_events(events)
    session = session.__class__(
        session_id=session.session_id,
        tool_name=session.tool_name,
        session_start=session.session_start,
        session_end=session.session_end,
        request_count=request_count,
        token_estimate=session.token_estimate,
    )

    with storage.connect(settings.db_path) as connection:
        storage.init_db(connection)
        storage.upsert_session(connection, session)
        for event in events:
            storage.append_event(connection, event)

    return session_id

