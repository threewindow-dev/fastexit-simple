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


class TargetAllocationAssetClassSchema(BaseModel):
    """Schema for asset class target allocation response."""

    target_allocation_asset_class_id: int = Field(
        ..., description="Target allocation asset class ID"
    )
    year: int = Field(..., description="Target year")
    asset_class: str = Field(..., description="Asset class name")
    target_percentage: Decimal = Field(..., description="Target percentage")

    class Config:
        """Pydantic config."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "target_allocation_asset_class_id": 1,
                "year": 2024,
                "asset_class": "국내주식",
                "target_percentage": "30.00",
            }
        }


class CreateTargetAllocationAssetClassRequest(BaseModel):
    """Request schema for creating/updating asset class target allocation."""

    year: int = Field(..., description="Target year", ge=2020, le=2100)
    asset_class: str = Field(
        ..., description="Asset class name", min_length=1, max_length=100
    )
    target_percentage: Decimal = Field(
        ..., description="Target percentage (0-100)", ge=0, le=100
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "year": 2024,
                "asset_class": "국내주식",
                "target_percentage": "30.00",
            }
        }


class TargetAllocationAssetClassListResponse(BaseModel):
    """Response schema for list of asset class target allocations."""

    year: int = Field(..., description="Target year")
    targets: list[TargetAllocationAssetClassSchema] = Field(
        ..., description="List of asset class target allocations"
    )

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "year": 2024,
                "targets": [
                    {
                        "target_allocation_asset_class_id": 1,
                        "year": 2024,
                        "asset_class": "국내주식",
                        "target_percentage": "30.00",
                    },
                    {
                        "target_allocation_asset_class_id": 2,
                        "year": 2024,
                        "asset_class": "해외주식",
                        "target_percentage": "25.00",
                    },
                ],
            }
        }
