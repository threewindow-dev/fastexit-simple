from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from subdomains.portfolio.domain.errors import InvalidStateError


@dataclass
class WeeklySnapshot:
    weekly_snapshot_id: int
    user_id: int
    reference_date: date
    source_snapshot_id: int
    status: str
    editable_until: datetime | None
    created_at: datetime

    def __post_init__(self) -> None:
        if self.status not in {"in_progress", "locked"}:
            raise InvalidStateError("weekly_snapshot", "invalid status")
