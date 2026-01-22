from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from subdomains.portfolio.domain.errors import InvalidStateError


@dataclass
class Account:
    account_id: int | None
    institution_id: int
    name: str
    type: str
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.name:
            raise InvalidStateError("account", "name is required")
        if not self.type:
            raise InvalidStateError("account", "type is required")

    @classmethod
    def create(cls, institution_id: int, name: str, type: str) -> "Account":
        return cls(
            account_id=None,
            institution_id=institution_id,
            name=name,
            type=type,
            created_at=datetime.utcnow(),
        )

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "institution_id": self.institution_id,
            "name": self.name,
            "type": self.type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
