"""
User domain-specific errors.

User 서브도메인의 Application/Domain 에러 정의.
"""

from shared.errors import ApplicationError


class DuplicateUserError(ApplicationError):
    """사용자 중복 에러 (username 또는 email)."""

    code = "USER_CREATE_DUPLICATED"

    def __init__(self, identifier: str, origin_exc: Exception | None = None):
        super().__init__(f"User already exists: {identifier}", origin_exc)


class UserNotFoundError(ApplicationError):
    """사용자 미존재 에러."""

    code = "USER_GET_NOT_FOUND"

    def __init__(self, user_id: int, origin_exc: Exception | None = None):
        super().__init__(f"User not found: {user_id}", origin_exc)
