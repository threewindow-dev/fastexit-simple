from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from subdomains.portfolio.domain.errors import InvalidStateError, DeletionConflictError


@dataclass
class Holding:
    holding_id: int | None
    account_id: int
    product_id: int
    is_visible: bool
    deleted_at: datetime | None
    deletion_reason: str | None
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.account_id or not self.product_id:
            raise InvalidStateError("holding", "account_id and product_id are required")

    @classmethod
    def create(cls, account_id: int, product_id: int) -> "Holding":
        return cls(
            holding_id=None,
            account_id=account_id,
            product_id=product_id,
            is_visible=True,
            deleted_at=None,
            deletion_reason=None,
            created_at=datetime.utcnow(),
        )

    def hide(self, reason: str | None = None) -> None:
        if not self.is_visible:
            raise DeletionConflictError("holding", "already hidden")
        self.is_visible = False
        self.deletion_reason = reason
        self.deleted_at = datetime.utcnow()

    def hard_delete_allowed(self) -> bool:
        return True  # business rule placeholder
