from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from subdomains.portfolio.domain.errors import InvalidStateError


@dataclass
class Institution:
    institution_id: int | None
    name: str
    type: str
    display_order: int
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.name:
            raise InvalidStateError("institution", "name is required")
        if self.type not in {"증권사", "은행", "기타"}:
            raise InvalidStateError("institution", "invalid type")
        if self.display_order < 0:
            raise InvalidStateError("institution", "display_order must be >= 0")

    @classmethod
    def create(cls, name: str, type: str, display_order: int = 0) -> "Institution":
        return cls(
            institution_id=None,
            name=name,
            type=type,
            display_order=display_order,
            created_at=datetime.utcnow(),
        )

    def to_dict(self) -> dict:
        return {
            "institution_id": self.institution_id,
            "name": self.name,
            "type": self.type,
            "display_order": self.display_order,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
