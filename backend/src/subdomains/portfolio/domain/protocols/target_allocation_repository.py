"""Protocol for target allocation repository."""

from abc import ABC, abstractmethod
from decimal import Decimal

from subdomains.portfolio.domain.models import (
    TargetAllocation,
    TargetAllocationAccount,
    TargetAllocationTotal,
)


class TargetAllocationRepository(ABC):
    """Protocol for target allocation repository operations."""

    # ========== Account-Level Target Allocations ==========

    @abstractmethod
    async def save_account(
        self, target_allocation_account: TargetAllocationAccount
    ) -> TargetAllocationAccount:
        """Save or update an account-level target allocation."""
        pass

    @abstractmethod
    async def get_account_by_year_and_account(
        self, year: int, account_id: int
    ) -> TargetAllocationAccount | None:
        """Get an account-level target allocation by year and account ID."""
        pass

    @abstractmethod
    async def get_accounts_by_year(self, year: int) -> list[TargetAllocationAccount]:
        """Get all account-level target allocations for a specific year."""
        pass

    @abstractmethod
    async def get_accounts_by_year_and_account_group(
        self, year: int, account_group_id: int
    ) -> list[TargetAllocationAccount]:
        """Get account-level target allocations for a year and account group."""
        pass

    @abstractmethod
    async def delete_account(self, target_allocation_account_id: int) -> None:
        """Delete an account-level target allocation."""
        pass

    # ========== Account-Group-Level Target Allocations (Legacy, kept for backward compatibility) ==========

    @abstractmethod
    async def save(self, target_allocation: TargetAllocation) -> TargetAllocation:
        """Save or update a target allocation."""
        pass

    @abstractmethod
    async def get_by_year_and_account_group(
        self, year: int, account_group_id: int
    ) -> TargetAllocation | None:
        """Get a target allocation by year and account group ID."""
        pass

    @abstractmethod
    async def get_by_year(self, year: int) -> list[TargetAllocation]:
        """Get all target allocations for a specific year."""
        pass

    @abstractmethod
    async def delete(self, target_allocation_id: int) -> None:
        """Delete a target allocation."""
        pass

    # ========== Annual Total Target Allocations ==========

    @abstractmethod
    async def save_total(
        self, target_allocation_total: TargetAllocationTotal
    ) -> TargetAllocationTotal:
        """Save or update annual total target allocation."""
        pass

    @abstractmethod
    async def get_total_by_year(self, year: int) -> TargetAllocationTotal | None:
        """Get annual total target allocation by year."""
        pass

    @abstractmethod
    async def delete_total_by_year(self, year: int) -> None:
        """Delete annual total target allocation by year."""
        pass

    # ========== Asset Class Target Allocations ==========

    @abstractmethod
    async def save_asset_class(
        self, year: int, asset_class: str, target_percentage: Decimal
    ) -> dict:
        """Save or update an asset class target allocation."""
        pass

    @abstractmethod
    async def get_asset_class_by_year_and_class(
        self, year: int, asset_class: str
    ) -> dict | None:
        """Get an asset class target allocation by year and asset class."""
        pass

    @abstractmethod
    async def get_asset_classes_by_year(self, year: int) -> list[dict]:
        """Get all asset class target allocations for a specific year."""
        pass

    @abstractmethod
    async def delete_asset_class(self, target_allocation_asset_class_id: int) -> None:
        """Delete an asset class target allocation."""
        pass
