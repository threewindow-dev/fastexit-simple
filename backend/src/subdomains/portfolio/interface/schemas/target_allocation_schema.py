"""Schemas for target allocation API."""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class TargetAllocationSchema(BaseModel):
    """Schema for target allocation response."""

    target_allocation_id: int = Field(..., description="Target allocation ID")
    year: int = Field(..., description="Target year")
    account_group_id: int = Field(..., description="Account group ID")
    target_amount: Decimal = Field(..., description="Target asset amount")

    class Config:
        """Pydantic config."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "target_allocation_id": 1,
                "year": 2024,
                "account_group_id": 1,
                "target_amount": "10000000.00",
            }
        }


class CreateTargetAllocationRequest(BaseModel):
    """Request schema for creating/updating target allocation."""

    year: int = Field(..., description="Target year", ge=2020, le=2100)
    account_group_id: int = Field(..., description="Account group ID", gt=0)
    target_amount: Decimal = Field(..., description="Target asset amount", ge=0)

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "year": 2024,
                "account_group_id": 1,
                "target_amount": "10000000.00",
            }
        }


class TargetAllocationListResponse(BaseModel):
    """Response schema for list of target allocations."""

    year: int = Field(..., description="Target year")
    targets: list[TargetAllocationSchema] = Field(
        ..., description="List of target allocations"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "year": 2024,
                "targets": [
                    {
                        "target_allocation_id": 1,
                        "year": 2024,
                        "account_group_id": 1,
                        "target_amount": "10000000.00",
                    },
                    {
                        "target_allocation_id": 2,
                        "year": 2024,
                        "account_group_id": 2,
                        "target_amount": "5000000.00",
                    },
                ],
            }
        }
