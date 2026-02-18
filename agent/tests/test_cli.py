from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from collector import UsageCollector, UsageEvent, now_utc  # noqa: E402
import storage  # noqa: E402


def test_daily_summary_has_expected_counts(tmp_path: Path) -> None:
    db_path = tmp_path / "usage.db"
    session_id = "session-test-1"
    start_at = now_utc() - timedelta(hours=1)
    end_at = now_utc()

    events = [
        UsageEvent(
            event_id="event-1",
            session_id=session_id,
            tool_name="codex",
            event_type="session_start",
            occurred_at=start_at,
        ),
        UsageEvent(
            event_id="event-2",
            session_id=session_id,
            tool_name="codex",
            event_type="request",
            occurred_at=start_at + timedelta(minutes=5),
        ),
        UsageEvent(
            event_id="event-3",
            session_id=session_id,
            tool_name="codex",
            event_type="token_estimate",
            occurred_at=end_at - timedelta(minutes=1),
            payload_json="500",
        ),
        UsageEvent(
            event_id="event-4",
            session_id=session_id,
            tool_name="codex",
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
        rows = storage.list_daily_summary(connection)

    assert len(rows) == 1
    assert rows[0]["tool_name"] == "codex"
    assert rows[0]["sessions"] == 1
    assert rows[0]["requests"] == 1
    assert rows[0]["tokens"] == 500
