"""Target allocation application service."""

from datetime import datetime
from decimal import Decimal

from shared.decorators import transactional
from shared.protocols.transaction import TransactionManager
from subdomains.portfolio.domain.models import (
    TargetAllocation,
    TargetAllocationAccount,
    TargetAllocationTotal,
)
from subdomains.portfolio.domain.protocols.target_allocation_repository import (
    TargetAllocationRepository,
)


class TargetAllocationAppService:
    """Application service for target allocation operations."""

    def __init__(
        self,
        repository: TargetAllocationRepository,
        transaction_manager: TransactionManager,
    ):
        """Initialize with repository and transaction manager."""
        self.repository = repository
        self._txm = transaction_manager

    # ========== Account-Level Target Allocations ==========

    @transactional(mode="writable")
    async def create_or_update_account_target(
        self, year: int, account_id: int, target_amount: Decimal
    ) -> TargetAllocationAccount:
        """Create or update an account-level target allocation."""
        existing = await self.repository.get_account_by_year_and_account(
            year, account_id
        )

        if existing:
            # Update
            updated = TargetAllocationAccount(
                target_allocation_account_id=existing.target_allocation_account_id,
                year=year,
                account_id=account_id,
                target_amount=target_amount,
                created_at=existing.created_at,
                updated_at=datetime.utcnow(),
            )
            return await self.repository.save_account(updated)
        else:
            # Create
            new_allocation = TargetAllocationAccount.create(
                year, account_id, target_amount
            )
            return await self.repository.save_account(new_allocation)

    @transactional(mode="readonly")
    async def get_account_targets_by_year(
        self, year: int
    ) -> list[TargetAllocationAccount]:
        """Get all account-level target allocations for a specific year."""
        return await self.repository.get_accounts_by_year(year)

    @transactional(mode="readonly")
    async def get_account_targets_by_year_and_group(
        self, year: int, account_group_id: int
    ) -> list[TargetAllocationAccount]:
        """Get account-level targets for a year and account group."""
        return await self.repository.get_accounts_by_year_and_account_group(
            year, account_group_id
        )

    @transactional(mode="readonly")
    async def get_account_target(
        self, year: int, account_id: int
    ) -> TargetAllocationAccount | None:
        """Get a specific account-level target allocation."""
        return await self.repository.get_account_by_year_and_account(year, account_id)

    @transactional(mode="writable")
    async def delete_account_target(self, target_allocation_account_id: int) -> None:
        """Delete an account-level target allocation."""
        await self.repository.delete_account(target_allocation_account_id)

    # ========== Account-Group-Level Target (Aggregated from Accounts) ==========

    @transactional(mode="readonly")
    async def get_account_group_target_by_year(
        self, year: int, account_group_id: int
    ) -> Decimal:
        """Get aggregated target amount for account group (sum of all accounts in group)."""
        account_targets = await self.repository.get_accounts_by_year_and_account_group(
            year, account_group_id
        )
        return sum(
            (target.target_amount for target in account_targets),
            Decimal("0"),
        )

    @transactional(mode="readonly")
    async def get_all_account_groups_targets_by_year(
        self, year: int, account_group_ids: list[int]
    ) -> dict[int, Decimal]:
        """Get aggregated target amounts for multiple account groups."""
        result = {}
        for account_group_id in account_group_ids:
            result[account_group_id] = await self.get_account_group_target_by_year(
                year, account_group_id
            )
        return result

    # ========== Annual Total Target (Aggregated from All Accounts) ==========

    @transactional(mode="readonly")
    async def get_total_account_target_by_year(self, year: int) -> Decimal:
        """Get aggregated total target amount for year (sum of all accounts)."""
        account_targets = await self.repository.get_accounts_by_year(year)
        return sum(
            (target.target_amount for target in account_targets),
            Decimal("0"),
        )

    # ========== Legacy Account-Group-Level Methods (Deprecated) ==========

    @transactional(mode="writable")
    async def create_or_update_target(
        self, year: int, account_group_id: int, target_amount: Decimal
    ) -> TargetAllocation:
        """Create or update a target allocation for a year and account group."""
        # Check if already exists
        existing = await self.repository.get_by_year_and_account_group(
            year, account_group_id
        )

        if existing:
            # Update
            updated = TargetAllocation(
                target_allocation_id=existing.target_allocation_id,
                year=year,
                account_group_id=account_group_id,
                target_amount=target_amount,
                created_at=existing.created_at,
                updated_at=datetime.utcnow(),
            )
            return await self.repository.save(updated)
        else:
            # Create
            new_allocation = TargetAllocation.create(
                year, account_group_id, target_amount
            )
            return await self.repository.save(new_allocation)

    @transactional(mode="readonly")
    async def get_targets_by_year(self, year: int) -> list[TargetAllocation]:
        """Get all target allocations for a specific year."""
        return await self.repository.get_by_year(year)

    @transactional(mode="readonly")
    async def get_target(
        self, year: int, account_group_id: int
    ) -> TargetAllocation | None:
        """Get a specific target allocation."""
        return await self.repository.get_by_year_and_account_group(
            year, account_group_id
        )

    @transactional(mode="writable")
    async def delete_target(self, target_allocation_id: int) -> None:
        """Delete a target allocation."""
        await self.repository.delete(target_allocation_id)

    # ========== Annual Total Target (Legacy, manually set) ==========

    @transactional(mode="writable")
    async def create_or_update_total_target(
        self, year: int, target_amount: Decimal
    ) -> TargetAllocationTotal:
        """Create or update annual total target allocation."""
        existing = await self.repository.get_total_by_year(year)

        if existing:
            updated = TargetAllocationTotal(
                target_allocation_total_id=existing.target_allocation_total_id,
                year=year,
                target_amount=target_amount,
                created_at=existing.created_at,
                updated_at=datetime.utcnow(),
            )
            return await self.repository.save_total(updated)

        new_total = TargetAllocationTotal.create(year=year, target_amount=target_amount)
        return await self.repository.save_total(new_total)

    @transactional(mode="readonly")
    async def get_total_target_by_year(self, year: int) -> TargetAllocationTotal | None:
        """Get annual total target allocation by year."""
        return await self.repository.get_total_by_year(year)

    @transactional(mode="writable")
    async def delete_total_target_by_year(self, year: int) -> None:
        """Delete annual total target allocation by year."""
        await self.repository.delete_total_by_year(year)

    # ========== Asset Class Target Allocations ==========

    @transactional(mode="writable")
    async def create_or_update_asset_class_target(
        self, year: int, asset_class: str, target_percentage: Decimal
    ) -> dict:
        """Create or update an asset class target allocation."""
        return await self.repository.save_asset_class(
            year, asset_class, float(target_percentage)
        )

    @transactional(mode="readonly")
    async def get_asset_class_targets_by_year(self, year: int) -> list[dict]:
        """Get all asset class target allocations for a specific year."""
        return await self.repository.get_asset_classes_by_year(year)

    @transactional(mode="readonly")
    async def get_asset_class_target(self, year: int, asset_class: str) -> dict | None:
        """Get a specific asset class target allocation."""
        return await self.repository.get_asset_class_by_year_and_class(
            year, asset_class
        )

    @transactional(mode="writable")
    async def delete_asset_class_target(
        self, target_allocation_asset_class_id: int
    ) -> None:
        """Delete an asset class target allocation."""
        await self.repository.delete_asset_class(target_allocation_asset_class_id)
