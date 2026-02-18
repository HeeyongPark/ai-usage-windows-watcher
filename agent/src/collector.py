from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable


@dataclass(frozen=True)
class UsageEvent:
    event_id: str
    session_id: str
    tool_name: str
    event_type: str
    occurred_at: datetime
    payload_json: str = ""


@dataclass(frozen=True)
class UsageSession:
    session_id: str
    tool_name: str
    session_start: datetime
    session_end: datetime
    request_count: int
    token_estimate: int


class UsageCollector:
    """Builds session-level records from event streams."""

    def build_session_from_events(self, events: Iterable[UsageEvent]) -> UsageSession:
        sorted_events = sorted(events, key=lambda item: item.occurred_at)
        if not sorted_events:
            raise ValueError("events must not be empty")

        first = sorted_events[0]
        last = sorted_events[-1]
        request_count = sum(1 for item in sorted_events if item.event_type == "request")
        token_estimate = sum(
            int(item.payload_json or "0")
            for item in sorted_events
            if item.event_type == "token_estimate"
        )

        return UsageSession(
            session_id=first.session_id,
            tool_name=first.tool_name,
            session_start=first.occurred_at.astimezone(timezone.utc),
            session_end=last.occurred_at.astimezone(timezone.utc),
            request_count=request_count,
            token_estimate=token_estimate,
        )


def now_utc() -> datetime:
    return datetime.now(tz=timezone.utc)

