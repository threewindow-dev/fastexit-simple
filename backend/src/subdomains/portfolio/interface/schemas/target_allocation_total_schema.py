"""Schemas for annual total target allocation API."""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class TargetAllocationTotalSchema(BaseModel):
    """Schema for annual total target allocation response."""

    target_allocation_total_id: int
    year: int
    target_amount: Decimal

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "target_allocation_total_id": 1,
                "year": 2026,
                "target_amount": "50000000.00",
            }
        }


class CreateTargetAllocationTotalRequest(BaseModel):
    """Request schema for creating/updating annual total target allocation."""

    year: int = Field(..., description="Target year", ge=2020, le=2100)
    target_amount: Decimal = Field(..., description="Total target asset amount", ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "year": 2026,
                "target_amount": "50000000.00",
            }
        }


class TargetAllocationTotalResponse(BaseModel):
    """API response for annual total target allocation."""

    code: int
    message: str
    data: Optional[TargetAllocationTotalSchema]

    class Config:
        json_schema_extra = {
            "example": {
                "code": 0,
                "message": "success",
                "data": {
                    "target_allocation_total_id": 1,
                    "year": 2026,
                    "target_amount": "50000000.00",
                },
            }
        }
