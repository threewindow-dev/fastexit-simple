from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from subdomains.portfolio.domain.errors import InvalidStateError


@dataclass
class TargetAllocation:
    target_allocation_id: int | None
    year: int
    account_group_id: int
    target_amount: Decimal
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        if self.year < 2020 or self.year > 2100:
            raise InvalidStateError(
                "target_allocation", "year must be between 2020 and 2100"
            )
        if self.account_group_id <= 0:
            raise InvalidStateError(
                "target_allocation", "account_group_id must be positive"
            )
        if self.target_amount < 0:
            raise InvalidStateError(
                "target_allocation", "target_amount cannot be negative"
            )

    @classmethod
    def create(
        cls,
        year: int,
        account_group_id: int,
        target_amount: Decimal,
    ) -> TargetAllocation:
        return cls(
            target_allocation_id=None,
            year=year,
            account_group_id=account_group_id,
            target_amount=target_amount,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
