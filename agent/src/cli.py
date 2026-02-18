from __future__ import annotations

import argparse
import uuid
from datetime import timedelta

from collector import UsageCollector, UsageEvent, now_utc
from config import ensure_db_parent, load_settings
import storage


def command_init_db() -> None:
    settings = load_settings()
    ensure_db_parent(settings.db_path)
    with storage.connect(settings.db_path) as connection:
        storage.init_db(connection)
    print(f"Initialized DB: {settings.db_path}")


def command_record_sample(tool_name: str, request_count: int, token_estimate: int) -> None:
    settings = load_settings()
    ensure_db_parent(settings.db_path)

    session_id = str(uuid.uuid4())
    started_at = now_utc() - timedelta(minutes=20)
    ended_at = now_utc()

    events = [
        UsageEvent(
            event_id=str(uuid.uuid4()),
            session_id=session_id,
            tool_name=tool_name,
            event_type="session_start",
            occurred_at=started_at,
        ),
        UsageEvent(
            event_id=str(uuid.uuid4()),
            session_id=session_id,
            tool_name=tool_name,
            event_type="request",
            occurred_at=started_at + timedelta(minutes=5),
        ),
        UsageEvent(
            event_id=str(uuid.uuid4()),
            session_id=session_id,
            tool_name=tool_name,
            event_type="token_estimate",
            occurred_at=ended_at - timedelta(minutes=1),
            payload_json=str(token_estimate),
        ),
        UsageEvent(
            event_id=str(uuid.uuid4()),
            session_id=session_id,
            tool_name=tool_name,
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

    print(f"Recorded sample session: {session_id}")


def command_summary_daily() -> None:
    settings = load_settings()
    ensure_db_parent(settings.db_path)
    with storage.connect(settings.db_path) as connection:
        storage.init_db(connection)
        rows = storage.list_daily_summary(connection)

    if not rows:
        print("No usage records found.")
        return

    print("day | tool | sessions | requests | tokens")
    for row in rows:
        print(
            f"{row['day']} | {row['tool_name']} | {row['sessions']} | "
            f"{row['requests']} | {row['tokens']}"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Usage Watcher CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-db", help="Initialize local DB schema")

    record_sample = subparsers.add_parser(
        "record-sample", help="Insert a sample usage session"
    )
    record_sample.add_argument("--tool", default="codex")
    record_sample.add_argument("--requests", type=int, default=1)
    record_sample.add_argument("--tokens", type=int, default=100)

    summary = subparsers.add_parser("summary", help="Show summaries")
    summary.add_argument("--daily", action="store_true")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init-db":
        command_init_db()
        return

    if args.command == "record-sample":
        command_record_sample(
            tool_name=args.tool,
            request_count=args.requests,
            token_estimate=args.tokens,
        )
        return

    if args.command == "summary":
        if not args.daily:
            parser.error("summary currently supports only --daily")
        command_summary_daily()
        return

    parser.error("unsupported command")


if __name__ == "__main__":
    main()
