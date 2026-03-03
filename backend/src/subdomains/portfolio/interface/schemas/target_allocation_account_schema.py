"""Schemas for account-level target allocation API."""

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class TargetAllocationAccountSchema(BaseModel):
    """Schema for account-level target allocation response."""

    target_allocation_account_id: int = Field(
        ..., description="Account target allocation ID"
    )
    year: int = Field(..., description="Target year")
    account_id: int = Field(..., description="Account ID")
    target_amount: Decimal = Field(..., description="Target asset amount for account")

    class Config:
        """Pydantic config."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "target_allocation_account_id": 1,
                "year": 2026,
                "account_id": 1,
                "target_amount": "5000000.00",
            }
        }


class CreateTargetAllocationAccountRequest(BaseModel):
    """Request schema for creating/updating account-level target allocation."""

    year: int = Field(..., description="Target year", ge=2020, le=2100)
    account_id: int = Field(..., description="Account ID", gt=0)
    target_amount: Decimal = Field(
        ..., description="Target asset amount for account", ge=0
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "year": 2026,
                "account_id": 1,
                "target_amount": "5000000.00",
            }
        }


class TargetAllocationAccountListResponse(BaseModel):
    """Response schema for list of account-level target allocations."""

    year: int = Field(..., description="Target year")
    account_targets: list[TargetAllocationAccountSchema] = Field(
        ..., description="List of account-level target allocations"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "year": 2026,
                "account_targets": [
                    {
                        "target_allocation_account_id": 1,
                        "year": 2026,
                        "account_id": 1,
                        "target_amount": "5000000.00",
                    },
                    {
                        "target_allocation_account_id": 2,
                        "year": 2026,
                        "account_id": 2,
                        "target_amount": "3000000.00",
                    },
                ],
            }
        }
