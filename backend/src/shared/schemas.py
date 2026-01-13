"""
공통 응답 래퍼 및 기본 Schema 정의

interface/schemas 계층에서 사용할 수 있는 기본 응답 구조
"""
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """공통 API 응답 래퍼
    
    모든 API 응답은 이 구조를 따릅니다:
    - code: 비즈니스 코드 (SUCCESS, CREATED, USER_EMAIL_DUPLICATED 등)
    - message: 사람이 읽을 수 있는 메시지
    - data: 성공 시 리소스/결과, 실패 시 에러 상세 정보
    """

    code: str | int = Field(..., description="응답 코드")
    message: str = Field(..., description="응답 메시지")
    data: T | None = Field(..., description="응답 데이터")
