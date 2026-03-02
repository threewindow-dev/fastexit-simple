from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from subdomains.portfolio.domain.errors import InvalidStateError


@dataclass
class TargetAllocationTotal:
    target_allocation_total_id: int | None
    year: int
    target_amount: Decimal
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        if self.year < 2020 or self.year > 2100:
            raise InvalidStateError(
                "target_allocation_total", "year must be between 2020 and 2100"
            )
        if self.target_amount < 0:
            raise InvalidStateError(
                "target_allocation_total", "target_amount cannot be negative"
            )

    @classmethod
    def create(
        cls,
        year: int,
        target_amount: Decimal,
    ) -> "TargetAllocationTotal":
        return cls(
            target_allocation_total_id=None,
            year=year,
            target_amount=target_amount,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
