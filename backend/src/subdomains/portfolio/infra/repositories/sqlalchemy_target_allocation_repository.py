"""SQLAlchemy implementation of target allocation repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.decorators import use_transaction
from subdomains.portfolio.domain.models import (
    TargetAllocation,
    TargetAllocationAccount,
    TargetAllocationTotal,
)
from subdomains.portfolio.domain.protocols.target_allocation_repository import (
    TargetAllocationRepository,
)
from subdomains.portfolio.infra.entities import (
    TargetAllocationEntity,
    TargetAllocationAccountEntity,
    TargetAllocationTotalEntity,
)


class SqlAlchemyTargetAllocationRepository(TargetAllocationRepository):
    """SQLAlchemy implementation of target allocation repository."""

    # ========== Account-Level Target Allocations ==========

    @use_transaction()
    async def save_account(
        self, conn: AsyncSession, target_allocation_account: TargetAllocationAccount
    ) -> TargetAllocationAccount:
        """Save or update an account-level target allocation."""
        session: AsyncSession = conn

        if target_allocation_account.target_allocation_account_id is None:
            # Insert new record
            entity = TargetAllocationAccountEntity(
                year=target_allocation_account.year,
                account_id=target_allocation_account.account_id,
                target_amount=target_allocation_account.target_amount,
                created_at=target_allocation_account.created_at,
                updated_at=target_allocation_account.updated_at,
            )
            session.add(entity)
            await session.flush()
            await session.refresh(
                entity,
                ["target_allocation_account_id", "created_at", "updated_at"],
            )
            return self._account_entity_to_model(entity)
        else:
            # Update existing record
            stmt = select(TargetAllocationAccountEntity).where(
                TargetAllocationAccountEntity.target_allocation_account_id
                == target_allocation_account.target_allocation_account_id
            )
            result = await session.execute(stmt)
            entity = result.scalars().first()
            if entity:
                entity.year = target_allocation_account.year
                entity.account_id = target_allocation_account.account_id
                entity.target_amount = target_allocation_account.target_amount
                entity.updated_at = target_allocation_account.updated_at
                await session.flush()
                await session.refresh(entity)
                return self._account_entity_to_model(entity)
            else:
                raise ValueError(
                    f"Target allocation account with ID {target_allocation_account.target_allocation_account_id} not found"
                )

    @use_transaction()
    async def get_account_by_year_and_account(
        self, conn: AsyncSession, year: int, account_id: int
    ) -> TargetAllocationAccount | None:
        """Get an account-level target allocation by year and account ID."""
        stmt = select(TargetAllocationAccountEntity).where(
            (TargetAllocationAccountEntity.year == year)
            & (TargetAllocationAccountEntity.account_id == account_id)
        )
        result = await conn.execute(stmt)
        entity = result.scalars().first()
        return self._account_entity_to_model(entity) if entity else None

    @use_transaction()
    async def get_accounts_by_year(
        self, conn: AsyncSession, year: int
    ) -> list[TargetAllocationAccount]:
        """Get all account-level target allocations for a specific year."""
        stmt = select(TargetAllocationAccountEntity).where(
            TargetAllocationAccountEntity.year == year
        )
        result = await conn.execute(stmt)
        entities = result.scalars().all()
        return [self._account_entity_to_model(entity) for entity in entities]

    @use_transaction()
    async def get_accounts_by_year_and_account_group(
        self, conn: AsyncSession, year: int, account_group_id: int
    ) -> list[TargetAllocationAccount]:
        """Get account-level target allocations for a year and account group."""
        from subdomains.portfolio.infra.entities import (
            AccountGroupAccountEntity,
        )

        stmt = select(TargetAllocationAccountEntity).where(
            TargetAllocationAccountEntity.year == year
        )
        result = await conn.execute(stmt)
        all_targets = result.scalars().all()

        # Filter by account_group_id
        stmt_group = select(AccountGroupAccountEntity.account_id).where(
            AccountGroupAccountEntity.account_group_id == account_group_id
        )
        result_group = await conn.execute(stmt_group)
        account_ids_in_group = {row[0] for row in result_group.fetchall()}

        return [
            self._account_entity_to_model(entity)
            for entity in all_targets
            if entity.account_id in account_ids_in_group
        ]

    @use_transaction()
    async def delete_account(
        self, conn: AsyncSession, target_allocation_account_id: int
    ) -> None:
        """Delete an account-level target allocation."""
        stmt = select(TargetAllocationAccountEntity).where(
            TargetAllocationAccountEntity.target_allocation_account_id
            == target_allocation_account_id
        )
        result = await conn.execute(stmt)
        entity = result.scalars().first()
        if entity:
            await conn.delete(entity)
            await conn.flush()
        else:
            raise ValueError(
                f"Target allocation account with ID {target_allocation_account_id} not found"
            )

    async def save(
        self, conn: AsyncSession, target_allocation: TargetAllocation
    ) -> TargetAllocation:
        """Save or update a target allocation."""
        session: AsyncSession = conn

        if target_allocation.target_allocation_id is None:
            # Insert new record
            entity = TargetAllocationEntity(
                year=target_allocation.year,
                account_group_id=target_allocation.account_group_id,
                target_amount=target_allocation.target_amount,
                created_at=target_allocation.created_at,
                updated_at=target_allocation.updated_at,
            )
            session.add(entity)
            await session.flush()
            await session.refresh(
                entity, ["target_allocation_id", "created_at", "updated_at"]
            )
            return self._entity_to_model(entity)
        else:
            # Update existing record
            stmt = select(TargetAllocationEntity).where(
                TargetAllocationEntity.target_allocation_id
                == target_allocation.target_allocation_id
            )
            result = await session.execute(stmt)
            entity = result.scalars().first()
            if entity:
                entity.year = target_allocation.year
                entity.account_group_id = target_allocation.account_group_id
                entity.target_amount = target_allocation.target_amount
                entity.updated_at = target_allocation.updated_at
                await session.flush()
                await session.refresh(entity)
                return self._entity_to_model(entity)
            else:
                raise ValueError(
                    f"Target allocation with ID {target_allocation.target_allocation_id} not found"
                )

    @use_transaction()
    async def get_by_year_and_account_group(
        self, conn: AsyncSession, year: int, account_group_id: int
    ) -> TargetAllocation | None:
        """Get a target allocation by year and account group ID."""
        stmt = select(TargetAllocationEntity).where(
            (TargetAllocationEntity.year == year)
            & (TargetAllocationEntity.account_group_id == account_group_id)
        )
        result = await conn.execute(stmt)
        entity = result.scalars().first()
        return self._entity_to_model(entity) if entity else None

    @use_transaction()
    async def get_by_year(
        self, conn: AsyncSession, year: int
    ) -> list[TargetAllocation]:
        """Get all target allocations for a specific year."""
        stmt = select(TargetAllocationEntity).where(TargetAllocationEntity.year == year)
        result = await conn.execute(stmt)
        entities = result.scalars().all()
        return [self._entity_to_model(entity) for entity in entities]

    @use_transaction()
    async def delete(self, conn: AsyncSession, target_allocation_id: int) -> None:
        """Delete a target allocation."""
        stmt = select(TargetAllocationEntity).where(
            TargetAllocationEntity.target_allocation_id == target_allocation_id
        )
        result = await conn.execute(stmt)
        entity = result.scalars().first()
        if entity:
            await conn.delete(entity)
            await conn.flush()
        else:
            raise ValueError(
                f"Target allocation with ID {target_allocation_id} not found"
            )

    @use_transaction()
    async def save_total(
        self, conn: AsyncSession, target_allocation_total: TargetAllocationTotal
    ) -> TargetAllocationTotal:
        """Save or update annual total target allocation."""
        session: AsyncSession = conn

        if target_allocation_total.target_allocation_total_id is None:
            entity = TargetAllocationTotalEntity(
                year=target_allocation_total.year,
                target_amount=target_allocation_total.target_amount,
                created_at=target_allocation_total.created_at,
                updated_at=target_allocation_total.updated_at,
            )
            session.add(entity)
            await session.flush()
            await session.refresh(
                entity,
                ["target_allocation_total_id", "created_at", "updated_at"],
            )
            return self._total_entity_to_model(entity)

        stmt = select(TargetAllocationTotalEntity).where(
            TargetAllocationTotalEntity.target_allocation_total_id
            == target_allocation_total.target_allocation_total_id
        )
        result = await session.execute(stmt)
        entity = result.scalars().first()
        if not entity:
            raise ValueError(
                "Target allocation total with ID "
                f"{target_allocation_total.target_allocation_total_id} not found"
            )
        entity.year = target_allocation_total.year
        entity.target_amount = target_allocation_total.target_amount
        entity.updated_at = target_allocation_total.updated_at
        await session.flush()
        await session.refresh(entity)
        return self._total_entity_to_model(entity)

    @use_transaction()
    async def get_total_by_year(
        self, conn: AsyncSession, year: int
    ) -> TargetAllocationTotal | None:
        """Get annual total target allocation by year."""
        stmt = select(TargetAllocationTotalEntity).where(
            TargetAllocationTotalEntity.year == year
        )
        result = await conn.execute(stmt)
        entity = result.scalars().first()
        return self._total_entity_to_model(entity) if entity else None

    @use_transaction()
    async def delete_total_by_year(self, conn: AsyncSession, year: int) -> None:
        """Delete annual total target allocation by year."""
        stmt = select(TargetAllocationTotalEntity).where(
            TargetAllocationTotalEntity.year == year
        )
        result = await conn.execute(stmt)
        entity = result.scalars().first()
        if not entity:
            raise ValueError(f"Target allocation total for year {year} not found")
        await conn.delete(entity)
        await conn.flush()

    @staticmethod
    def _account_entity_to_model(
        entity: TargetAllocationAccountEntity,
    ) -> TargetAllocationAccount:
        """Convert account entity to domain model."""
        return TargetAllocationAccount(
            target_allocation_account_id=entity.target_allocation_account_id,
            year=entity.year,
            account_id=entity.account_id,
            target_amount=entity.target_amount,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def _entity_to_model(entity: TargetAllocationEntity) -> TargetAllocation:
        """Convert entity to domain model."""
        return TargetAllocation(
            target_allocation_id=entity.target_allocation_id,
            year=entity.year,
            account_group_id=entity.account_group_id,
            target_amount=entity.target_amount,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def _total_entity_to_model(
        entity: TargetAllocationTotalEntity,
    ) -> TargetAllocationTotal:
        """Convert total entity to domain model."""
        return TargetAllocationTotal(
            target_allocation_total_id=entity.target_allocation_total_id,
            year=entity.year,
            target_amount=entity.target_amount,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    # ========== Asset Class Target Allocations ==========

    @use_transaction()
    async def save_asset_class(
        self, conn: AsyncSession, year: int, asset_class: str, target_percentage: float
    ) -> dict:
        """Save or update an asset class target allocation."""
        from decimal import Decimal
        from datetime import datetime
        from subdomains.portfolio.infra.entities.target_allocation_asset_class_entity import (
            TargetAllocationAssetClassEntity,
        )

        session: AsyncSession = conn

        # Check if exists
        stmt = select(TargetAllocationAssetClassEntity).where(
            (TargetAllocationAssetClassEntity.year == year)
            & (TargetAllocationAssetClassEntity.asset_class == asset_class)
        )
        result = await session.execute(stmt)
        entity = result.scalars().first()

        if entity:
            # Update
            entity.target_percentage = Decimal(str(target_percentage))
            entity.updated_at = datetime.utcnow()
        else:
            # Insert
            entity = TargetAllocationAssetClassEntity(
                year=year,
                asset_class=asset_class,
                target_percentage=Decimal(str(target_percentage)),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(entity)

        await session.flush()
        await session.refresh(entity)
        return {
            "target_allocation_asset_class_id": entity.target_allocation_asset_class_id,
            "year": entity.year,
            "asset_class": entity.asset_class,
            "target_percentage": float(entity.target_percentage),
            "created_at": entity.created_at.isoformat(),
            "updated_at": entity.updated_at.isoformat(),
        }

    @use_transaction()
    async def get_asset_class_by_year_and_class(
        self, conn: AsyncSession, year: int, asset_class: str
    ) -> dict | None:
        """Get an asset class target allocation by year and asset class."""
        from subdomains.portfolio.infra.entities.target_allocation_asset_class_entity import (
            TargetAllocationAssetClassEntity,
        )

        stmt = select(TargetAllocationAssetClassEntity).where(
            (TargetAllocationAssetClassEntity.year == year)
            & (TargetAllocationAssetClassEntity.asset_class == asset_class)
        )
        result = await conn.execute(stmt)
        entity = result.scalars().first()
        if not entity:
            return None
        return {
            "target_allocation_asset_class_id": entity.target_allocation_asset_class_id,
            "year": entity.year,
            "asset_class": entity.asset_class,
            "target_percentage": float(entity.target_percentage),
            "created_at": entity.created_at.isoformat(),
            "updated_at": entity.updated_at.isoformat(),
        }

    @use_transaction()
    async def get_asset_classes_by_year(
        self, conn: AsyncSession, year: int
    ) -> list[dict]:
        """Get all asset class target allocations for a specific year."""
        from subdomains.portfolio.infra.entities.target_allocation_asset_class_entity import (
            TargetAllocationAssetClassEntity,
        )

        stmt = select(TargetAllocationAssetClassEntity).where(
            TargetAllocationAssetClassEntity.year == year
        )
        result = await conn.execute(stmt)
        entities = result.scalars().all()
        return [
            {
                "target_allocation_asset_class_id": entity.target_allocation_asset_class_id,
                "year": entity.year,
                "asset_class": entity.asset_class,
                "target_percentage": float(entity.target_percentage),
                "created_at": entity.created_at.isoformat(),
                "updated_at": entity.updated_at.isoformat(),
            }
            for entity in entities
        ]

    @use_transaction()
    async def delete_asset_class(
        self, conn: AsyncSession, target_allocation_asset_class_id: int
    ) -> None:
        """Delete an asset class target allocation."""
        from subdomains.portfolio.infra.entities.target_allocation_asset_class_entity import (
            TargetAllocationAssetClassEntity,
        )

        stmt = select(TargetAllocationAssetClassEntity).where(
            TargetAllocationAssetClassEntity.target_allocation_asset_class_id
            == target_allocation_asset_class_id
        )
        result = await conn.execute(stmt)
        entity = result.scalars().first()
        if entity:
            await conn.delete(entity)
            await conn.flush()
