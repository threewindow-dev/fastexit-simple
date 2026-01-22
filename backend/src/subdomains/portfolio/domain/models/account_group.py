from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from subdomains.portfolio.domain.errors import InvalidStateError


@dataclass
class AccountGroup:
    account_group_id: int | None
    name: str
    account_ids: list[int]
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.name:
            raise InvalidStateError("account_group", "name is required")
        if not self.account_ids:
            raise InvalidStateError("account_group", "at least one account is required")

    @classmethod
    def create(cls, name: str, account_ids: list[int]) -> "AccountGroup":
        return cls(
            account_group_id=None,
            name=name,
            account_ids=account_ids,
            created_at=datetime.utcnow(),
        )

    def to_dict(self) -> dict:
        return {
            "account_group_id": self.account_group_id,
            "name": self.name,
            "account_ids": self.account_ids,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
