"""Target allocation application service."""

from datetime import datetime
from decimal import Decimal

from shared.decorators import transactional
from shared.protocols.transaction import TransactionManager
from subdomains.portfolio.domain.models import TargetAllocation, TargetAllocationTotal
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
