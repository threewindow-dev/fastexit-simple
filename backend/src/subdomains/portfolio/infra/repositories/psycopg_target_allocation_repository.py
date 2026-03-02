"""Psycopg implementation of target allocation repository."""

from datetime import datetime
from decimal import Decimal

from shared.decorators import use_transaction
from subdomains.portfolio.domain.models import TargetAllocation, TargetAllocationTotal
from subdomains.portfolio.domain.protocols.target_allocation_repository import (
    TargetAllocationRepository,
)


class PsycopgTargetAllocationRepository(TargetAllocationRepository):
    """Psycopg implementation of target allocation repository."""

    @use_transaction()
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
