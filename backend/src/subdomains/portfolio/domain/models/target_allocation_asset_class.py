"""Domain model for asset class target allocation."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class TargetAllocationAssetClass:
    """Asset class target allocation domain model."""

    target_allocation_asset_class_id: int
    year: int
    asset_class: str
    target_percentage: Decimal
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        """Validate target allocation asset class data."""
        if self.year < 2020 or self.year > 2100:
            raise ValueError(f"Invalid year: {self.year}")
        if not self.asset_class or len(self.asset_class) > 100:
            raise ValueError(f"Invalid asset_class: {self.asset_class}")
        if self.target_percentage < 0 or self.target_percentage > 100:
            raise ValueError(f"Invalid target_percentage: {self.target_percentage}")
