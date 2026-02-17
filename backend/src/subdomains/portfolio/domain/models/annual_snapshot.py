from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from subdomains.portfolio.domain.errors import InvalidStateError


@dataclass
class AnnualSnapshot:
    annual_snapshot_id: int
    user_id: int
    reference_date: date
    source_snapshot_id: int
    status: str
    editable_until: datetime | None
    created_at: datetime

    def __post_init__(self) -> None:
        if self.status not in {"locked"}:
            raise InvalidStateError("annual_snapshot", "invalid status")
