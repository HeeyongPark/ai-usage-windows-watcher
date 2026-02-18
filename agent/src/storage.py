from __future__ import annotations

import sqlite3
from pathlib import Path

from collector import UsageEvent, UsageSession

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"


def connect(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON;")
    return connection


def init_db(connection: sqlite3.Connection, schema_path: Path = SCHEMA_PATH) -> None:
    sql = schema_path.read_text(encoding="utf-8")
    connection.executescript(sql)
    connection.commit()


def append_event(connection: sqlite3.Connection, event: UsageEvent) -> None:
    connection.execute(
        """
        INSERT OR REPLACE INTO usage_events (
            event_id, session_id, tool_name, event_type, occurred_at, payload_json
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            event.event_id,
            event.session_id,
            event.tool_name,
            event.event_type,
            event.occurred_at.isoformat(),
            event.payload_json,
        ),
    )
    connection.commit()


def upsert_session(connection: sqlite3.Connection, session: UsageSession) -> None:
    connection.execute(
        """
        INSERT INTO usage_sessions (
            session_id, tool_name, session_start, session_end, request_count, token_estimate
        ) VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(session_id) DO UPDATE SET
            tool_name=excluded.tool_name,
            session_start=excluded.session_start,
            session_end=excluded.session_end,
            request_count=excluded.request_count,
            token_estimate=excluded.token_estimate,
            updated_at=datetime('now')
        """,
        (
            session.session_id,
            session.tool_name,
            session.session_start.isoformat(),
            session.session_end.isoformat(),
            session.request_count,
            session.token_estimate,
        ),
    )
    connection.commit()


def list_daily_summary(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    cursor = connection.execute(
        """
        SELECT
            DATE(session_start) AS day,
            tool_name,
            COUNT(*) AS sessions,
            SUM(request_count) AS requests,
            SUM(token_estimate) AS tokens
        FROM usage_sessions
        GROUP BY DATE(session_start), tool_name
        ORDER BY day DESC, tool_name ASC
        """
    )
    return list(cursor.fetchall())


def list_weekly_summary(connection: sqlite3.Connection) -> list[sqlite3.Row]:
    cursor = connection.execute(
        """
        SELECT
            strftime('%Y-W%W', session_start) AS week,
            tool_name,
            COUNT(*) AS sessions,
            SUM(request_count) AS requests,
            SUM(token_estimate) AS tokens
        FROM usage_sessions
        GROUP BY strftime('%Y-W%W', session_start), tool_name
        ORDER BY week DESC, tool_name ASC
        """
    )
    return list(cursor.fetchall())
