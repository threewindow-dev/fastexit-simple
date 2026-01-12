"""
User Application DTOs (Commands & Queries)

애플리케이션 계층: Use Case 입/출력 인터페이스
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domains.user.domain.models.user import User


# ============================================================================
# Commands (쓰기 작업 - Create, Update, Delete)
# ============================================================================

@dataclass
class RegisterUserCommand:
    """사용자 등록 명령"""
    username: str
    email: str
    full_name: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "RegisterUserCommand":
        return cls(
            username=data["username"],
            email=data["email"],
            full_name=data.get("full_name"),
        )


@dataclass
class UpdateUserCommand:
    """사용자 수정 명령"""
    user_id: int
    full_name: Optional[str] = None


@dataclass
class DeleteUserCommand:
    """사용자 삭제 명령"""
    user_id: int


@dataclass
class UserPagedListQuery:
    """사용자 페이징 목록 조회 쿼리"""
    skip: int = 0
    limit: int = 100

    @classmethod
    def from_dict(cls, data: dict) -> "UserPagedListQuery":
        return cls(skip=data.get("skip", 0), limit=data.get("limit", 100))


@dataclass
class RegisterUserCommandResult:
    """사용자 결과 DTO"""
    id: Optional[int]
    username: str
    email: str
    full_name: Optional[str]
    created_at: datetime

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def from_domain(cls, user: "User") -> "RegisterUserCommandResult":
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at,
        )


@dataclass
class UserPagedListQueryResult:
    """사용자 페이징 목록 조회 결과 DTO"""
    items: list[RegisterUserCommandResult]
    total_count: int
    skip: int
    limit: int

    def to_dict(self) -> dict:
        return {
            "items": [item.to_dict() for item in self.items],
            "total_count": self.total_count,
            "skip": self.skip,
            "limit": self.limit,
        }
