"""Domain model for account-level target allocation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from subdomains.portfolio.domain.errors import InvalidStateError


@dataclass
class TargetAllocationAccount:
    """Domain model for account-level target allocation."""

    target_allocation_account_id: int | None
    year: int
    account_id: int
    target_amount: Decimal
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        if self.year < 2020 or self.year > 2100:
            raise InvalidStateError(
                "target_allocation_account", "year must be between 2020 and 2100"
            )
        if self.account_id <= 0:
            raise InvalidStateError(
                "target_allocation_account", "account_id must be positive"
            )
        if self.target_amount < 0:
            raise InvalidStateError(
                "target_allocation_account", "target_amount cannot be negative"
            )

    @classmethod
    def create(
        cls,
        year: int,
        account_id: int,
        target_amount: Decimal,
    ) -> TargetAllocationAccount:
        """Create a new target allocation account."""
        current_time = datetime.utcnow()
        return cls(
            target_allocation_account_id=None,
            year=year,
            account_id=account_id,
            target_amount=target_amount,
            created_at=current_time,
            updated_at=current_time,
        )
