"""Psycopg implementation of target allocation repository."""

from datetime import datetime
from decimal import Decimal

from shared.decorators import use_transaction
from subdomains.portfolio.domain.models import (
    TargetAllocation,
    TargetAllocationAccount,
    TargetAllocationTotal,
)
from subdomains.portfolio.domain.protocols.target_allocation_repository import (
    TargetAllocationRepository,
)


class PsycopgTargetAllocationRepository(TargetAllocationRepository):
    """Psycopg implementation of target allocation repository."""

    # ========== Account-Level Target Allocations ==========

    @use_transaction()
    async def save_account(
        self, conn, target_allocation_account: TargetAllocationAccount
    ) -> TargetAllocationAccount:
        """Save or update an account-level target allocation."""
        if target_allocation_account.target_allocation_account_id is None:
            async with conn.cursor() as cur:
                current_time = datetime.utcnow()
                await cur.execute(
                    """
                    INSERT INTO target_allocation_accounts (year, account_id, target_amount, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING target_allocation_account_id, created_at, updated_at
                    """,
                    (
                        target_allocation_account.year,
                        target_allocation_account.account_id,
                        target_allocation_account.target_amount,
                        current_time,
                        current_time,
                    ),
                )
                row = await cur.fetchone()
                if not row:
                    raise ValueError("Failed to insert account target allocation")
                return TargetAllocationAccount(
                    target_allocation_account_id=row[0],
                    year=target_allocation_account.year,
                    account_id=target_allocation_account.account_id,
                    target_amount=target_allocation_account.target_amount,
                    created_at=row[1],
                    updated_at=row[2],
                )

        async with conn.cursor() as cur:
            current_time = datetime.utcnow()
            await cur.execute(
                """
                UPDATE target_allocation_accounts
                SET year = %s, account_id = %s, target_amount = %s, updated_at = %s
                WHERE target_allocation_account_id = %s
                RETURNING created_at, updated_at
                """,
                (
                    target_allocation_account.year,
                    target_allocation_account.account_id,
                    target_allocation_account.target_amount,
                    current_time,
                    target_allocation_account.target_allocation_account_id,
                ),
            )
            row = await cur.fetchone()
            if not row:
                raise ValueError(
                    f"Account target allocation with ID {target_allocation_account.target_allocation_account_id} not found"
                )
            return TargetAllocationAccount(
                target_allocation_account_id=target_allocation_account.target_allocation_account_id,
                year=target_allocation_account.year,
                account_id=target_allocation_account.account_id,
                target_amount=target_allocation_account.target_amount,
                created_at=row[0],
                updated_at=row[1],
            )

    @use_transaction()
    async def get_account_by_year_and_account(
        self, conn, year: int, account_id: int
    ) -> TargetAllocationAccount | None:
        """Get an account-level target allocation by year and account ID."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT target_allocation_account_id, year, account_id, target_amount, created_at, updated_at
                FROM target_allocation_accounts
                WHERE year = %s AND account_id = %s
                """,
                (year, account_id),
            )
            row = await cur.fetchone()
            if not row:
                return None
            return TargetAllocationAccount(
                target_allocation_account_id=row[0],
                year=row[1],
                account_id=row[2],
                target_amount=Decimal(str(row[3])),
                created_at=row[4],
                updated_at=row[5],
            )

    @use_transaction()
    async def get_accounts_by_year(
        self, conn, year: int
    ) -> list[TargetAllocationAccount]:
        """Get all account-level target allocations for a specific year."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT target_allocation_account_id, year, account_id, target_amount, created_at, updated_at
                FROM target_allocation_accounts
                WHERE year = %s
                ORDER BY account_id
                """,
                (year,),
            )
            rows = await cur.fetchall()
            return [
                TargetAllocationAccount(
                    target_allocation_account_id=row[0],
                    year=row[1],
                    account_id=row[2],
                    target_amount=Decimal(str(row[3])),
                    created_at=row[4],
                    updated_at=row[5],
                )
                for row in rows
            ]

    @use_transaction()
    async def get_accounts_by_year_and_account_group(
        self, conn, year: int, account_group_id: int
    ) -> list[TargetAllocationAccount]:
        """Get account-level targets for a year and account group."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT taa.target_allocation_account_id, taa.year, taa.account_id, taa.target_amount, taa.created_at, taa.updated_at
                FROM target_allocation_accounts taa
                INNER JOIN account_group_accounts aga ON taa.account_id = aga.account_id
                WHERE taa.year = %s AND aga.account_group_id = %s
                ORDER BY taa.account_id
                """,
                (year, account_group_id),
            )
            rows = await cur.fetchall()
            return [
                TargetAllocationAccount(
                    target_allocation_account_id=row[0],
                    year=row[1],
                    account_id=row[2],
                    target_amount=Decimal(str(row[3])),
                    created_at=row[4],
                    updated_at=row[5],
                )
                for row in rows
            ]

    @use_transaction()
    async def delete_account(self, conn, target_allocation_account_id: int) -> None:
        """Delete an account-level target allocation."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM target_allocation_accounts
                WHERE target_allocation_account_id = %s
                """,
                (target_allocation_account_id,),
            )
            if cur.rowcount == 0:
                raise ValueError(
                    f"Account target allocation with ID {target_allocation_account_id} not found"
                )

    async def save(self, conn, target_allocation: TargetAllocation) -> TargetAllocation:
        """Save or update a target allocation."""
        if target_allocation.target_allocation_id is None:
            async with conn.cursor() as cur:
                current_time = datetime.utcnow()
                await cur.execute(
                    """
                    INSERT INTO target_allocations (year, account_group_id, target_amount, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING target_allocation_id, created_at, updated_at
                    """,
                    (
                        target_allocation.year,
                        target_allocation.account_group_id,
                        target_allocation.target_amount,
                        current_time,
                        current_time,
                    ),
                )
                row = await cur.fetchone()
                if not row:
                    raise ValueError("Failed to insert target allocation")
                return TargetAllocation(
                    target_allocation_id=row[0],
                    year=target_allocation.year,
                    account_group_id=target_allocation.account_group_id,
                    target_amount=target_allocation.target_amount,
                    created_at=row[1],
                    updated_at=row[2],
                )

        async with conn.cursor() as cur:
            current_time = datetime.utcnow()
            await cur.execute(
                """
                UPDATE target_allocations
                SET year = %s, account_group_id = %s, target_amount = %s, updated_at = %s
                WHERE target_allocation_id = %s
                RETURNING created_at, updated_at
                """,
                (
                    target_allocation.year,
                    target_allocation.account_group_id,
                    target_allocation.target_amount,
                    current_time,
                    target_allocation.target_allocation_id,
                ),
            )
            row = await cur.fetchone()
            if not row:
                raise ValueError(
                    f"Target allocation with ID {target_allocation.target_allocation_id} not found"
                )
            return TargetAllocation(
                target_allocation_id=target_allocation.target_allocation_id,
                year=target_allocation.year,
                account_group_id=target_allocation.account_group_id,
                target_amount=target_allocation.target_amount,
                created_at=row[0],
                updated_at=row[1],
            )

    @use_transaction()
    async def get_by_year_and_account_group(
        self, conn, year: int, account_group_id: int
    ) -> TargetAllocation | None:
        """Get a target allocation by year and account group ID."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT target_allocation_id, year, account_group_id, target_amount, created_at, updated_at
                FROM target_allocations
                WHERE year = %s AND account_group_id = %s
                """,
                (year, account_group_id),
            )
            row = await cur.fetchone()
            if not row:
                return None
            return TargetAllocation(
                target_allocation_id=row[0],
                year=row[1],
                account_group_id=row[2],
                target_amount=Decimal(str(row[3])),
                created_at=row[4],
                updated_at=row[5],
            )

    @use_transaction()
    async def get_by_year(self, conn, year: int) -> list[TargetAllocation]:
        """Get all target allocations for a specific year."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT target_allocation_id, year, account_group_id, target_amount, created_at, updated_at
                FROM target_allocations
                WHERE year = %s
                ORDER BY account_group_id
                """,
                (year,),
            )
            rows = await cur.fetchall()
            return [
                TargetAllocation(
                    target_allocation_id=row[0],
                    year=row[1],
                    account_group_id=row[2],
                    target_amount=Decimal(str(row[3])),
                    created_at=row[4],
                    updated_at=row[5],
                )
                for row in rows
            ]

    @use_transaction()
    async def delete(self, conn, target_allocation_id: int) -> None:
        """Delete a target allocation."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM target_allocations
                WHERE target_allocation_id = %s
                """,
                (target_allocation_id,),
            )
            if cur.rowcount == 0:
                raise ValueError(
                    f"Target allocation with ID {target_allocation_id} not found"
                )

    @use_transaction()
    async def save_total(
        self, conn, target_allocation_total: TargetAllocationTotal
    ) -> TargetAllocationTotal:
        """Save or update annual total target allocation."""
        if target_allocation_total.target_allocation_total_id is None:
            async with conn.cursor() as cur:
                current_time = datetime.utcnow()
                await cur.execute(
                    """
                    INSERT INTO target_allocation_totals (year, target_amount, created_at, updated_at)
                    VALUES (%s, %s, %s, %s)
                    RETURNING target_allocation_total_id, created_at, updated_at
                    """,
                    (
                        target_allocation_total.year,
                        target_allocation_total.target_amount,
                        current_time,
                        current_time,
                    ),
                )
                row = await cur.fetchone()
                if not row:
                    raise ValueError("Failed to insert target allocation total")
                return TargetAllocationTotal(
                    target_allocation_total_id=row[0],
                    year=target_allocation_total.year,
                    target_amount=target_allocation_total.target_amount,
                    created_at=row[1],
                    updated_at=row[2],
                )

        async with conn.cursor() as cur:
            current_time = datetime.utcnow()
            await cur.execute(
                """
                UPDATE target_allocation_totals
                SET year = %s, target_amount = %s, updated_at = %s
                WHERE target_allocation_total_id = %s
                RETURNING created_at, updated_at
                """,
                (
                    target_allocation_total.year,
                    target_allocation_total.target_amount,
                    current_time,
                    target_allocation_total.target_allocation_total_id,
                ),
            )
            row = await cur.fetchone()
            if not row:
                raise ValueError(
                    "Target allocation total with ID "
                    f"{target_allocation_total.target_allocation_total_id} not found"
                )
            return TargetAllocationTotal(
                target_allocation_total_id=target_allocation_total.target_allocation_total_id,
                year=target_allocation_total.year,
                target_amount=target_allocation_total.target_amount,
                created_at=row[0],
                updated_at=row[1],
            )

    @use_transaction()
    async def get_total_by_year(self, conn, year: int) -> TargetAllocationTotal | None:
        """Get annual total target allocation by year."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT target_allocation_total_id, year, target_amount, created_at, updated_at
                FROM target_allocation_totals
                WHERE year = %s
                """,
                (year,),
            )
            row = await cur.fetchone()
            if not row:
                return None
            return TargetAllocationTotal(
                target_allocation_total_id=row[0],
                year=row[1],
                target_amount=Decimal(str(row[2])),
                created_at=row[3],
                updated_at=row[4],
            )

    @use_transaction()
    async def delete_total_by_year(self, conn, year: int) -> None:
        """Delete annual total target allocation by year."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM target_allocation_totals
                WHERE year = %s
                """,
                (year,),
            )
            if cur.rowcount == 0:
                raise ValueError(f"Target allocation total for year {year} not found")

    # ========== Asset Class Target Allocations ==========

    @use_transaction()
    async def save_asset_class(
        self, conn, year: int, asset_class: str, target_percentage: float
    ) -> dict:
        """Save or update an asset class target allocation."""
        current_time = datetime.utcnow()
        async with conn.cursor() as cur:
            # Check if exists
            await cur.execute(
                """
                SELECT target_allocation_asset_class_id, created_at
                FROM target_allocation_asset_classes
                WHERE year = %s AND asset_class = %s
                """,
                (year, asset_class),
            )
            row = await cur.fetchone()

            if row:
                # Update
                await cur.execute(
                    """
                    UPDATE target_allocation_asset_classes
                    SET target_percentage = %s, updated_at = %s
                    WHERE target_allocation_asset_class_id = %s
                    RETURNING target_allocation_asset_class_id, year, asset_class, 
                              target_percentage, created_at, updated_at
                    """,
                    (Decimal(str(target_percentage)), current_time, row[0]),
                )
            else:
                # Insert
                await cur.execute(
                    """
                    INSERT INTO target_allocation_asset_classes 
                    (year, asset_class, target_percentage, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING target_allocation_asset_class_id, year, asset_class, 
                              target_percentage, created_at, updated_at
                    """,
                    (
                        year,
                        asset_class,
                        Decimal(str(target_percentage)),
                        current_time,
                        current_time,
                    ),
                )

            result_row = await cur.fetchone()
            if not result_row:
                raise ValueError("Failed to save asset class target allocation")

            return {
                "target_allocation_asset_class_id": result_row[0],
                "year": result_row[1],
                "asset_class": result_row[2],
                "target_percentage": float(result_row[3]),
                "created_at": result_row[4].isoformat(),
                "updated_at": result_row[5].isoformat(),
            }

    @use_transaction()
    async def get_asset_class_by_year_and_class(
        self, conn, year: int, asset_class: str
    ) -> dict | None:
        """Get an asset class target allocation by year and asset class."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT target_allocation_asset_class_id, year, asset_class, 
                       target_percentage, created_at, updated_at
                FROM target_allocation_asset_classes
                WHERE year = %s AND asset_class = %s
                """,
                (year, asset_class),
            )
            row = await cur.fetchone()
            if not row:
                return None
            return {
                "target_allocation_asset_class_id": row[0],
                "year": row[1],
                "asset_class": row[2],
                "target_percentage": float(row[3]),
                "created_at": row[4].isoformat(),
                "updated_at": row[5].isoformat(),
            }

    @use_transaction()
    async def get_asset_classes_by_year(self, conn, year: int) -> list[dict]:
        """Get all asset class target allocations for a specific year."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT target_allocation_asset_class_id, year, asset_class, 
                       target_percentage, created_at, updated_at
                FROM target_allocation_asset_classes
                WHERE year = %s
                ORDER BY asset_class
                """,
                (year,),
            )
            rows = await cur.fetchall()
            return [
                {
                    "target_allocation_asset_class_id": row[0],
                    "year": row[1],
                    "asset_class": row[2],
                    "target_percentage": float(row[3]),
                    "created_at": row[4].isoformat(),
                    "updated_at": row[5].isoformat(),
                }
                for row in rows
            ]

    @use_transaction()
    async def delete_asset_class(
        self, conn, target_allocation_asset_class_id: int
    ) -> None:
        """Delete an asset class target allocation."""
        async with conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM target_allocation_asset_classes
                WHERE target_allocation_asset_class_id = %s
                """,
                (target_allocation_asset_class_id,),
            )
            if cur.rowcount == 0:
                raise ValueError(
                    f"Asset class target allocation with ID {target_allocation_asset_class_id} not found"
                )
