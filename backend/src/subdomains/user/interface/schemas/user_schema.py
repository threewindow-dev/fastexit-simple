"""
User Pydantic Schemas (API 요청/응답)

인터페이스 계층: HTTP 요청/응답 모델
"""
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


# ============================================================================
# POST /api/users - 사용자 생성
# ============================================================================

class PostUserRequest(BaseModel):
    """사용자 생성 요청"""

    username: str = Field(
        ...,
        # 도메인 규칙으로 검증(3자 이상). 스키마는 완화하여 400 도메인 에러를 유도.
        max_length=100,
        description="사용자명",
        examples=["john_doe", "alice", "kim_minsoo"],
    )
    email: EmailStr = Field(
        ...,
        description="이메일 주소",
        examples=["john@example.com", "alice@example.com"],
    )
    full_name: Optional[str] = Field(
        None,
        max_length=255,
        description="전체 이름 (선택)",
        examples=["John Doe", "Alice Park"],
    )


# ============================================================================
# PATCH /api/users/{user_id} - 사용자 업데이트
# ============================================================================

class PatchUserRequest(BaseModel):
    """사용자 업데이트 요청"""

    full_name: Optional[str] = Field(
        ...,
        max_length=255,
        description="전체 이름",
        examples=["John Smith", "Alex Kim"],
    )


# ============================================================================
# GET /api/users/{user_id} - 사용자 단건 조회
# ============================================================================

class GetUserResponseItemInfo(BaseModel):
    """사용자 조회 응답 아이템"""

    id: int = Field(
        ...,
        description="사용자 ID",
        examples=[1, 2, 100],
    )
    username: str = Field(
        ...,
        description="사용자명",
        examples=["john_doe", "alice"],
    )
    email: str = Field(
        ...,
        description="이메일 주소",
        examples=["john@example.com"],
    )
    full_name: Optional[str] = Field(
        None,
        description="전체 이름",
        examples=["John Doe", None],
    )
    created_at: str = Field(
        ...,
        description="생성 시간 (ISO 8601)",
        examples=["2025-01-11T10:30:00", "2025-02-02T09:00:00"],
    )


class GetUserResponse(BaseModel):
    """사용자 단건 조회 응답"""

    item: GetUserResponseItemInfo


# ============================================================================
# GET /api/users - 사용자 목록 조회 (페이징)
# ============================================================================

class GetUserPagedListRequest(BaseModel):
    """사용자 목록 조회 요청"""

    skip: int = Field(
        0,
        ge=0,
        description="건너뛸 개수",
        examples=[0, 10],
    )
    limit: int = Field(
        100,
        ge=1,
        le=1000,
        description="조회할 개수 (1-1000)",
        examples=[50, 100],
    )


class GetUserPagedListItemInfo(BaseModel):
    """사용자 목록 아이템"""

    id: int = Field(..., examples=[1])
    username: str = Field(..., examples=["john_doe"])
    email: str = Field(..., examples=["john@example.com"])
    full_name: Optional[str] = Field(None, examples=["John Doe", None])
    created_at: str = Field(..., examples=["2025-01-11T10:30:00"])


class GetUserPagedListResponse(BaseModel):
    """사용자 목록 조회 응답"""

    items: list[GetUserPagedListItemInfo]
    total_count: int
    skip: int
    limit: int

    # Model-level examples are discouraged; use field-level examples.


# ============================================================================
# DELETE /api/users/{user_id} - 사용자 삭제
# ============================================================================

class DeleteUserResponse(BaseModel):
    """사용자 삭제 응답"""

    pass
