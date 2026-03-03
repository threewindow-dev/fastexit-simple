"""Response schemas for target allocation API."""

from typing import Optional

from pydantic import BaseModel, Field

from subdomains.portfolio.interface.schemas.target_allocation_schema import (
    TargetAllocationSchema,
    TargetAllocationListResponse,
)
from subdomains.portfolio.interface.schemas.target_allocation_account_schema import (
    TargetAllocationAccountSchema,
)


class TargetAllocationResponse(BaseModel):
    """API response for single target allocation."""

    code: int = Field(..., description="응답 코드")
    message: str = Field(..., description="응답 메시지")
    data: Optional[TargetAllocationSchema] = Field(
        None, description="목표 자산배분 데이터"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "code": 0,
                "message": "success",
                "data": {
                    "target_allocation_id": 1,
                    "year": 2024,
                    "account_group_id": 1,
                    "target_amount": "10000000.00",
                },
            }
        }


class TargetAllocationAccountResponse(BaseModel):
    """API response for account-level target allocation."""

    code: int = Field(..., description="응답 코드")
    message: str = Field(..., description="응답 메시지")
    data: Optional[TargetAllocationAccountSchema] = Field(
        None, description="계좌 단위 목표 자산배분 데이터"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "code": 0,
                "message": "success",
                "data": {
                    "target_allocation_account_id": 1,
                    "year": 2026,
                    "account_id": 1,
                    "target_amount": "5000000.00",
                },
            }
        }


class DeleteTargetAllocationResponse(BaseModel):
    """API response for delete target allocation."""

    code: int = Field(..., description="응답 코드")
    message: str = Field(..., description="응답 메시지")
    data: Optional[dict] = Field(None, description="응답 데이터")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "code": 0,
                "message": "success",
                "data": None,
            }
        }
