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
    display_order: int
    created_at: datetime
    allow_snapshot_input: bool = True

    def __post_init__(self) -> None:
        if not self.name:
            raise InvalidStateError("account", "name is required")
        if not self.type:
            raise InvalidStateError("account", "type is required")
        if self.display_order < 0:
            raise InvalidStateError("account", "display_order must be >= 0")

    @classmethod
    def create(
        cls,
        institution_id: int,
        name: str,
        type: str,
        display_order: int = 0,
        allow_snapshot_input: bool = True,
    ) -> "Account":
        return cls(
            account_id=None,
            institution_id=institution_id,
            name=name,
            type=type,
            display_order=display_order,
            created_at=datetime.utcnow(),
            allow_snapshot_input=allow_snapshot_input,
        )

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "institution_id": self.institution_id,
            "name": self.name,
            "type": self.type,
            "display_order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "allow_snapshot_input": self.allow_snapshot_input,
        }

    def update(
        self,
        name: str,
        type: str,
        display_order: int,
        allow_snapshot_input: bool,
    ) -> None:
        if not name:
            raise InvalidStateError("account", "name is required")
        if not type:
            raise InvalidStateError("account", "type is required")
        if display_order < 0:
            raise InvalidStateError("account", "display_order must be >= 0")
        self.name = name
        self.type = type
        self.display_order = display_order
        self.allow_snapshot_input = allow_snapshot_input
