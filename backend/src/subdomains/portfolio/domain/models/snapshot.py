from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime

from subdomains.portfolio.domain.errors import InvalidStateError, SnapshotLockedError


@dataclass
class SnapshotHolding:
    holding_id: int
    valuation_amount: float
    data_source: str

    def __post_init__(self) -> None:
        if self.data_source not in {"auto", "manual", "missing"}:
            raise InvalidStateError("snapshot_holding", "invalid data_source")
        if self.valuation_amount is None:
            raise InvalidStateError("snapshot_holding", "valuation_amount required")


@dataclass
class Snapshot:
    snapshot_id: int | None
    user_id: int
    reference_date: date
    status: str
    locked_at: datetime | None
    editable_until: datetime | None
    created_at: datetime
    holdings: list[SnapshotHolding] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.status not in {"in_progress", "locked"}:
            raise InvalidStateError("snapshot", "invalid status")

    @classmethod
    def create(cls, user_id: int, reference_date: date) -> "Snapshot":
        return cls(
            snapshot_id=None,
            user_id=user_id,
            reference_date=reference_date,
            status="in_progress",
            locked_at=None,
            editable_until=None,
            created_at=datetime.utcnow(),
            holdings=[],
        )

    def lock(self) -> None:
        if self.status == "locked":
            raise SnapshotLockedError(self.snapshot_id or 0)
        self.status = "locked"
        self.locked_at = datetime.utcnow()

    def upsert_holding(
        self, holding_id: int, valuation_amount: float, data_source: str
    ) -> None:
        if self.status == "locked":
            raise SnapshotLockedError(self.snapshot_id or 0)
        found = None
        for h in self.holdings:
            if h.holding_id == holding_id:
                found = h
                break
        if found:
            found.valuation_amount = valuation_amount
            found.data_source = data_source
        else:
            self.holdings.append(
                SnapshotHolding(
                    holding_id=holding_id,
                    valuation_amount=valuation_amount,
                    data_source=data_source,
                )
            )
