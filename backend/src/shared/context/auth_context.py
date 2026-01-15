"""
Authentication context management using ContextVar.

ContextVar를 사용한 인증 컨텍스트 관리.
비동기 요청별로 격리된 인증 사용자 정보를 유지합니다.
"""

from contextvars import ContextVar
from dataclasses import dataclass


@dataclass
class AuthenticatedUser:
    """
    인증된 사용자 정보
    
    Attributes:
        user_id: 사용자 고유 ID (필수)
        role: 사용자의 역할 (선택적, 프로젝트별로 다를 수 있음)
        metadata: 추가 정보 저장 (선택적)
    """
    user_id: str
    role: str | None = None
    metadata: dict | None = None


# ContextVar: 비동기 컨텍스트별로 격리된 인증 사용자 저장
authenticated_user_context: ContextVar[AuthenticatedUser | None] = ContextVar(
    "authenticated_user", default=None
)


def get_authenticated_user() -> AuthenticatedUser | None:
    """현재 요청의 인증된 사용자 정보를 반환합니다.
    
    Returns:
        AuthenticatedUser | None: 인증된 사용자, 없으면 None
    """
    return authenticated_user_context.get()


def set_authenticated_user(user: AuthenticatedUser) -> None:
    """현재 요청의 인증된 사용자 정보를 설정합니다.
    
    Args:
        user: 설정할 인증된 사용자
    """
    authenticated_user_context.set(user)


def clear_authenticated_user() -> None:
    """현재 요청의 인증된 사용자 정보를 제거합니다."""
    authenticated_user_context.set(None)
