"""
User Domain Model (DDD Entity)

도메인 계층: 비즈니스 로직 및 불변성 보호
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from shared.errors import DomainError


@dataclass
class User:
    """
    User Entity

    DDD 원칙:
    - Value Objects (username, email)을 통한 도메인 언어 표현
    - 비즈니스 규칙 (이메일 형식 검증) 포함
    - id는 Aggregate Root의 식별자
    """

    id: int | None
    username: str
    email: str
    full_name: str | None
    created_at: datetime

    def __post_init__(self) -> None:
        """엔티티 생성 후 기본 정합성만 확인

        주의: 테스트 및 유연한 생성(예: ORM 로드)을 위해
        강제 검증은 `create()` 팩토리에서 수행한다.
        """
        if self.username is None or self.email is None:
            raise DomainError(
                code="USER_INVALID_STATE",
                message="Username and email must not be None",
            )

    @classmethod
    def create(
        cls,
        username: str,
        email: str,
        full_name: str | None = None,
    ) -> User:
        """
        팩토리 메서드: 새로운 User 생성

        비즈니스 규칙:
        - 사용자명은 3글자 이상이어야 함
        - 이메일은 유효한 형식이어야 함
        - 생성 시간은 현재 시간

        Args:
            username: 사용자명 (고유)
            email: 이메일 주소 (고유)
            full_name: 전체 이름 (선택)

        Returns:
            생성된 User 엔티티
        """
        # 입력값 검증 (팩토리에서 강제 수행)
        # 사용자명: 3글자 이상
        if not username or len(username) < 3:
            raise DomainError(
                code="USER_INVALID_USERNAME",
                message="Username must be at least 3 characters",
            )
        # 이메일: local@domain, local/domain 공백 금지, domain에 '.' 포함
        if "@" not in email:
            raise DomainError(code="USER_INVALID_EMAIL", message="Invalid email format")
        local, _, domain = email.partition("@")
        if (
            not local
            or not domain
            or "." not in domain
            or domain.startswith(".")
            or domain.endswith(".")
        ):
            raise DomainError(code="USER_INVALID_EMAIL", message="Invalid email format")

        return cls(
            id=None,
            username=username,
            email=email,
            full_name=full_name,
            created_at=datetime.now(),
        )

    def _validate_username(self) -> None:
        """사용자명 검증 (도메인 규칙)"""
        if not self.username or len(self.username) < 3:
            raise DomainError(
                code="USER_INVALID_USERNAME",
                message="Username must be at least 3 characters",
            )

    def _validate_email(self) -> None:
        """이메일 검증 (도메인 규칙)"""
        # 간단한 이메일 형식 검증: local@domain, domain에 '.' 포함
        if "@" not in self.email:
            raise DomainError(
                code="USER_INVALID_EMAIL",
                message="Invalid email format",
            )
        local, _, domain = self.email.partition("@")
        if (
            not local
            or not domain
            or "." not in domain
            or domain.startswith(".")
            or domain.endswith(".")
        ):
            raise DomainError(
                code="USER_INVALID_EMAIL",
                message="Invalid email format",
            )

    def change_full_name(self, new_full_name: str) -> None:
        """이름 변경 (도메인 로직)"""
        if not new_full_name:
            raise DomainError(
                code="USER_INVALID_FULL_NAME",
                message="Full name cannot be empty",
            )
        self.full_name = new_full_name

    def is_valid(self) -> bool:
        """엔티티 유효성 확인"""
        try:
            self._validate_username()
            self._validate_email()
            return True
        except Exception:
            return False

    def to_dict(self) -> dict:
        """도메인 모델을 딕셔너리로 변환 (응답 생성용)"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
