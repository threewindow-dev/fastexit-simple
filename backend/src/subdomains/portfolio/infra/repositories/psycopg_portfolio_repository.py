"""Psycopg repository implementations for portfolio domain."""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Iterable

from psycopg import AsyncConnection

from shared.decorators import use_transaction
from shared.errors import InfraError
from shared.protocols.transaction import Connection
from subdomains.portfolio.domain import (
    Institution,
    Product,
    Account,
    AccountGroup,
    Holding,
    Snapshot,
    SnapshotHolding,
    WeeklySnapshot,
    AnnualSnapshot,
)
from subdomains.portfolio.domain.protocols import (
    InstitutionRepository,
    ProductRepository,
    AccountRepository,
    AccountGroupRepository,
    HoldingRepository,
    SnapshotRepository,
    ReportQueryRepository,
)


def _utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class _BaseRepo:
    @staticmethod
    def _require_conn(conn: Connection) -> AsyncConnection:
        if not isinstance(conn, AsyncConnection):
            raise InfraError("Connection is not an AsyncConnection")
        return conn


# ---------------------------------------------------------------------------
# Institution
# ---------------------------------------------------------------------------


class PsycopgInstitutionRepository(_BaseRepo, InstitutionRepository):
    @use_transaction()
    async def add(self, conn: Connection, institution: Institution) -> Institution:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO institutions (name, type, display_order, created_at)
                VALUES (%s, %s, %s, %s)
                RETURNING institution_id, name, type, display_order, created_at
                """,
                (
                    institution.name,
                    institution.type,
                    institution.display_order,
                    _utc_now_naive(),
                ),
            )
            row = await cur.fetchone()
        return Institution(
            institution_id=row["institution_id"],
            name=row["name"],
            type=row["type"],
            display_order=row["display_order"],
            created_at=row["created_at"],
        )

    @use_transaction()
    async def find_by_id(
        self, conn: Connection, institution_id: int
    ) -> Institution | None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT institution_id, name, type, display_order, created_at FROM institutions WHERE institution_id = %s",
                (institution_id,),
            )
            row = await cur.fetchone()
        if not row:
            return None
        return Institution(
            institution_id=row["institution_id"],
            name=row["name"],
            type=row["type"],
            display_order=row["display_order"],
            created_at=row["created_at"],
        )

    @use_transaction()
    async def exists_by_name(self, conn: Connection, name: str) -> bool:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute("SELECT 1 FROM institutions WHERE name = %s", (name,))
            row = await cur.fetchone()
            return row is not None

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Institution]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT institution_id, name, type, display_order, created_at FROM institutions ORDER BY institution_id"
            )
            rows = await cur.fetchall()
        return [
            Institution(
                institution_id=row["institution_id"],
                name=row["name"],
                type=row["type"],
                display_order=row["display_order"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    @use_transaction()
    async def update(self, conn: Connection, institution: Institution) -> Institution:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                UPDATE institutions
                SET name = %s, type = %s, display_order = %s
                WHERE institution_id = %s
                RETURNING institution_id, name, type, display_order, created_at
                """,
                (
                    institution.name,
                    institution.type,
                    institution.display_order,
                    institution.institution_id,
                ),
            )
            row = await cur.fetchone()
        return Institution(
            institution_id=row["institution_id"],
            name=row["name"],
            type=row["type"],
            display_order=row["display_order"],
            created_at=row["created_at"],
        )

    @use_transaction()
    async def update_display_orders(
        self, conn: Connection, orders: Iterable[tuple[int, int]]
    ) -> int:
        connection = self._require_conn(conn)
        order_list = list(orders)
        if not order_list:
            return 0
        async with connection.cursor() as cur:
            await cur.executemany(
                "UPDATE institutions SET display_order = %s WHERE institution_id = %s",
                [
                    (display_order, institution_id)
                    for institution_id, display_order in order_list
                ],
            )
        return len(order_list)

    @use_transaction()
    async def delete(self, conn: Connection, institution_id: int) -> None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "DELETE FROM institutions WHERE institution_id = %s",
                (institution_id,),
            )

    @use_transaction()
    async def count_referencing_accounts(
        self, conn: Connection, institution_id: int
    ) -> int:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT COUNT(*) AS cnt FROM accounts WHERE institution_id = %s",
                (institution_id,),
            )
            row = await cur.fetchone()
        return int(row["cnt"] if row else 0)


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------


class PsycopgProductRepository(_BaseRepo, ProductRepository):
    @use_transaction()
    async def add(self, conn: Connection, product: Product) -> Product:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO products (
                    product_name, asset_class, region, currency,
                    investment_type, characteristics, risk_level, allow_snapshot_input,
                    ticker, domestic_beta, global_beta, beta_collected_at,
                    display_order, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING product_id, product_name, asset_class, region, currency,
                          investment_type, characteristics, risk_level,
                          allow_snapshot_input, ticker, domestic_beta, global_beta,
                          beta_collected_at, display_order, created_at
                """,
                (
                    product.product_name,
                    product.asset_class,
                    product.region,
                    product.currency,
                    product.investment_type,
                    product.characteristics,
                    product.risk_level,
                    product.allow_snapshot_input,
                    product.ticker,
                    product.domestic_beta,
                    product.global_beta,
                    product.beta_collected_at,
                    product.display_order,
                    _utc_now_naive(),
                ),
            )
            row = await cur.fetchone()
        return Product(
            product_id=row["product_id"],
            product_name=row["product_name"],
            asset_class=row["asset_class"],
            region=row["region"],
            currency=row["currency"],
            investment_type=row["investment_type"],
            characteristics=row["characteristics"],
            risk_level=row["risk_level"],
            allow_snapshot_input=row["allow_snapshot_input"],
            ticker=row.get("ticker"),
            display_order=row["display_order"],
            created_at=row["created_at"],
            domestic_beta=float(row["domestic_beta"])
            if row.get("domestic_beta") is not None
            else None,
            global_beta=float(row["global_beta"])
            if row.get("global_beta") is not None
            else None,
            beta_collected_at=row.get("beta_collected_at"),
        )

    @use_transaction()
    async def find_by_id(self, conn: Connection, product_id: int) -> Product | None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT product_id, product_name, asset_class, region, currency,
                        investment_type, characteristics, risk_level,
                    allow_snapshot_input, ticker, domestic_beta, global_beta,
                    beta_collected_at, display_order, created_at
                FROM products WHERE product_id = %s
                """,
                (product_id,),
            )
            row = await cur.fetchone()
        if not row:
            return None
        return Product(
            product_id=row["product_id"],
            product_name=row["product_name"],
            asset_class=row["asset_class"],
            region=row["region"],
            currency=row["currency"],
            investment_type=row["investment_type"],
            characteristics=row["characteristics"],
            risk_level=row["risk_level"],
            allow_snapshot_input=row["allow_snapshot_input"],
            ticker=row.get("ticker"),
            display_order=row["display_order"],
            created_at=row["created_at"],
            domestic_beta=float(row["domestic_beta"])
            if row.get("domestic_beta") is not None
            else None,
            global_beta=float(row["global_beta"])
            if row.get("global_beta") is not None
            else None,
            beta_collected_at=row.get("beta_collected_at"),
        )

    @use_transaction()
    async def update(self, conn: Connection, product: Product) -> Product:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                UPDATE products
                SET product_name = %s,
                    asset_class = %s,
                    region = %s,
                    currency = %s,
                    investment_type = %s,
                    characteristics = %s,
                    risk_level = %s,
                    allow_snapshot_input = %s,
                    ticker = %s,
                    domestic_beta = %s,
                    global_beta = %s,
                    beta_collected_at = %s,
                    display_order = %s
                WHERE product_id = %s
                """,
                (
                    product.product_name,
                    product.asset_class,
                    product.region,
                    product.currency,
                    product.investment_type,
                    product.characteristics,
                    product.risk_level,
                    product.allow_snapshot_input,
                    product.ticker,
                    product.domestic_beta,
                    product.global_beta,
                    product.beta_collected_at,
                    product.display_order,
                    product.product_id,
                ),
            )
        return product

    @use_transaction()
    async def exists_identity(
        self,
        conn: Connection,
        *,
        product_name: str,
        asset_class: str,
        region: str,
        currency: str,
        investment_type: str,
    ) -> bool:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT 1 FROM products
                WHERE product_name = %s
                  AND asset_class = %s
                  AND region = %s
                  AND currency = %s
                  AND investment_type = %s
                LIMIT 1
                """,
                (product_name, asset_class, region, currency, investment_type),
            )
            row = await cur.fetchone()
            return row is not None

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Product]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT product_id, product_name, asset_class, region, currency,
                      investment_type, characteristics, risk_level,
                    allow_snapshot_input, ticker, domestic_beta, global_beta,
                        beta_collected_at, display_order, created_at
                FROM products ORDER BY display_order, product_id
                """
            )
            rows = await cur.fetchall()
        return [
            Product(
                product_id=row["product_id"],
                product_name=row["product_name"],
                asset_class=row["asset_class"],
                region=row["region"],
                currency=row["currency"],
                investment_type=row["investment_type"],
                characteristics=row["characteristics"],
                risk_level=row["risk_level"],
                allow_snapshot_input=row["allow_snapshot_input"],
                ticker=row.get("ticker"),
                display_order=row["display_order"],
                created_at=row["created_at"],
                domestic_beta=float(row["domestic_beta"])
                if row.get("domestic_beta") is not None
                else None,
                global_beta=float(row["global_beta"])
                if row.get("global_beta") is not None
                else None,
                beta_collected_at=row.get("beta_collected_at"),
            )
            for row in rows
        ]

    @use_transaction()
    async def update_display_orders(
        self, conn: Connection, orders: Iterable[tuple[int, int]]
    ) -> int:
        connection = self._require_conn(conn)
        order_list = list(orders)
        if not order_list:
            return 0
        async with connection.cursor() as cur:
            await cur.executemany(
                "UPDATE products SET display_order = %s WHERE product_id = %s",
                [
                    (display_order, product_id)
                    for product_id, display_order in order_list
                ],
            )
        return len(order_list)

    @use_transaction()
    async def delete(self, conn: Connection, product_id: int) -> None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "DELETE FROM products WHERE product_id = %s",
                (product_id,),
            )

    @use_transaction()
    async def count_referencing_holdings(
        self, conn: Connection, product_id: int
    ) -> int:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT COUNT(*) AS cnt FROM holdings WHERE product_id = %s",
                (product_id,),
            )
            row = await cur.fetchone()
        return int(row["cnt"] if row else 0)


# ---------------------------------------------------------------------------
# Account
# ---------------------------------------------------------------------------


class PsycopgAccountRepository(_BaseRepo, AccountRepository):
    @use_transaction()
    async def add(self, conn: Connection, account: Account) -> Account:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO accounts (
                    institution_id, name, type, allow_snapshot_input, display_order, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING account_id, institution_id, name, type,
                          allow_snapshot_input, display_order, created_at
                """,
                (
                    account.institution_id,
                    account.name,
                    account.type,
                    account.allow_snapshot_input,
                    account.display_order,
                    _utc_now_naive(),
                ),
            )
            row = await cur.fetchone()
        return Account(
            account_id=row["account_id"],
            institution_id=row["institution_id"],
            name=row["name"],
            type=row["type"],
            allow_snapshot_input=row["allow_snapshot_input"],
            display_order=row["display_order"],
            created_at=row["created_at"],
        )

    @use_transaction()
    async def find_by_id(self, conn: Connection, account_id: int) -> Account | None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT account_id, institution_id, name, type,
                       allow_snapshot_input, display_order, created_at
                FROM accounts
                WHERE account_id = %s
                """,
                (account_id,),
            )
            row = await cur.fetchone()
        if not row:
            return None
        return Account(
            account_id=row["account_id"],
            institution_id=row["institution_id"],
            name=row["name"],
            type=row["type"],
            allow_snapshot_input=row["allow_snapshot_input"],
            display_order=row["display_order"],
            created_at=row["created_at"],
        )

    @use_transaction()
    async def exists_by_name(
        self, conn: Connection, institution_id: int, name: str
    ) -> bool:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT 1 FROM accounts WHERE institution_id = %s AND name = %s LIMIT 1",
                (institution_id, name),
            )
            row = await cur.fetchone()
            return row is not None

    @use_transaction()
    async def update(self, conn: Connection, account: Account) -> Account:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                UPDATE accounts
                SET name = %s,
                    type = %s,
                    allow_snapshot_input = %s,
                    display_order = %s
                WHERE account_id = %s
                """,
                (
                    account.name,
                    account.type,
                    account.allow_snapshot_input,
                    account.display_order,
                    account.account_id,
                ),
            )
        return account

    @use_transaction()
    async def find_many(
        self, conn: Connection, account_ids: Iterable[int]
    ) -> list[Account]:
        ids = list(account_ids)
        if not ids:
            return []
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT account_id, institution_id, name, type,
                       allow_snapshot_input, display_order, created_at
                FROM accounts
                WHERE account_id = ANY(%s)
                """,
                (ids,),
            )
            rows = await cur.fetchall()
        return [
            Account(
                account_id=row["account_id"],
                institution_id=row["institution_id"],
                name=row["name"],
                type=row["type"],
                allow_snapshot_input=row["allow_snapshot_input"],
                display_order=row["display_order"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Account]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT a.account_id,
                       a.institution_id,
                       a.name,
                       a.type,
                       a.allow_snapshot_input,
                       a.display_order,
                       a.created_at
                FROM accounts a
                JOIN institutions i ON a.institution_id = i.institution_id
                ORDER BY i.display_order, a.display_order
                """
            )
            rows = await cur.fetchall()
        return [
            Account(
                account_id=row["account_id"],
                institution_id=row["institution_id"],
                name=row["name"],
                type=row["type"],
                allow_snapshot_input=row["allow_snapshot_input"],
                display_order=row["display_order"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    @use_transaction()
    async def update_display_orders(
        self, conn: Connection, orders: Iterable[tuple[int, int]]
    ) -> int:
        connection = self._require_conn(conn)
        order_list = list(orders)
        if not order_list:
            return 0
        async with connection.cursor() as cur:
            await cur.executemany(
                "UPDATE accounts SET display_order = %s WHERE account_id = %s",
                [
                    (display_order, account_id)
                    for account_id, display_order in order_list
                ],
            )
        return len(order_list)

    @use_transaction()
    async def delete(self, conn: Connection, account_id: int) -> None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT account_group_id FROM account_group_accounts WHERE account_id = %s",
                (account_id,),
            )
            impacted_rows = await cur.fetchall()
            impacted_group_ids = {
                int(row["account_group_id"])
                for row in impacted_rows
                if row.get("account_group_id") is not None
            }

            await cur.execute(
                "DELETE FROM accounts WHERE account_id = %s",
                (account_id,),
            )

            for account_group_id in impacted_group_ids:
                await cur.execute(
                    "SELECT COUNT(*) AS cnt FROM account_group_accounts WHERE account_group_id = %s",
                    (account_group_id,),
                )
                count_row = await cur.fetchone()
                mapped_count = int(count_row["cnt"] if count_row else 0)
                if mapped_count == 0:
                    await cur.execute(
                        "DELETE FROM account_groups WHERE account_group_id = %s",
                        (account_group_id,),
                    )

    @use_transaction()
    async def count_referencing_holdings(
        self, conn: Connection, account_id: int
    ) -> int:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT COUNT(*) AS cnt FROM holdings WHERE account_id = %s",
                (account_id,),
            )
            row = await cur.fetchone()
        return int(row["cnt"] if row else 0)


# ---------------------------------------------------------------------------
# Account Group
# ---------------------------------------------------------------------------


class PsycopgAccountGroupRepository(_BaseRepo, AccountGroupRepository):
    @use_transaction()
    async def add(self, conn: Connection, group: AccountGroup) -> AccountGroup:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO account_groups (name, include_in_report, display_order, created_at)
                VALUES (%s, %s, %s, %s)
                RETURNING account_group_id, name, include_in_report, display_order, created_at
                """,
                (
                    group.name,
                    group.include_in_report,
                    group.display_order,
                    _utc_now_naive(),
                ),
            )
            row = await cur.fetchone()
            group_id = row["account_group_id"]
            if group.account_ids:
                await cur.executemany(
                    """
                    INSERT INTO account_group_accounts (account_group_id, account_id, created_at)
                    VALUES (%s, %s, %s)
                    """,
                    [
                        (group_id, account_id, _utc_now_naive())
                        for account_id in group.account_ids
                    ],
                )
        return AccountGroup(
            account_group_id=group_id,
            name=row["name"],
            account_ids=list(group.account_ids),
            include_in_report=row["include_in_report"],
            display_order=row["display_order"],
            created_at=row["created_at"],
        )

    @use_transaction()
    async def exists_by_name(self, conn: Connection, name: str) -> bool:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT 1 FROM account_groups WHERE name = %s LIMIT 1", (name,)
            )
            row = await cur.fetchone()
            return row is not None

    @use_transaction()
    async def find_by_id(
        self, conn: Connection, account_group_id: int
    ) -> AccountGroup | None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT g.account_group_id, g.name, g.include_in_report, g.display_order, g.created_at, m.account_id
                FROM account_groups g
                LEFT JOIN account_group_accounts m
                  ON g.account_group_id = m.account_group_id
                WHERE g.account_group_id = %s
                ORDER BY m.account_id ASC
                """,
                (account_group_id,),
            )
            rows = await cur.fetchall()

        if not rows:
            return None

        account_ids = [
            row["account_id"] for row in rows if row["account_id"] is not None
        ]
        first = rows[0]
        return AccountGroup(
            account_group_id=first["account_group_id"],
            name=first["name"],
            account_ids=account_ids,
            include_in_report=first["include_in_report"],
            display_order=first["display_order"],
            created_at=first["created_at"],
        )

    @use_transaction()
    async def update(self, conn: Connection, group: AccountGroup) -> AccountGroup:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "UPDATE account_groups SET name = %s, include_in_report = %s, display_order = %s WHERE account_group_id = %s",
                (
                    group.name,
                    group.include_in_report,
                    group.display_order,
                    group.account_group_id,
                ),
            )
            await cur.execute(
                "DELETE FROM account_group_accounts WHERE account_group_id = %s",
                (group.account_group_id,),
            )
            if group.account_ids:
                await cur.executemany(
                    """
                    INSERT INTO account_group_accounts (account_group_id, account_id, created_at)
                    VALUES (%s, %s, %s)
                    """,
                    [
                        (group.account_group_id, account_id, _utc_now_naive())
                        for account_id in group.account_ids
                    ],
                )
        return group

    @use_transaction()
    async def delete(self, conn: Connection, account_group_id: int) -> None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "DELETE FROM account_groups WHERE account_group_id = %s",
                (account_group_id,),
            )

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[AccountGroup]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT g.account_group_id, g.name, g.include_in_report, g.display_order, g.created_at, m.account_id
                FROM account_groups g
                LEFT JOIN account_group_accounts m
                  ON g.account_group_id = m.account_group_id
                ORDER BY g.account_group_id DESC, m.account_id ASC
                """
            )
            rows = await cur.fetchall()

        if not rows:
            return []

        grouped: dict[int, AccountGroup] = {}
        for row in rows:
            group_id = row["account_group_id"]
            if group_id not in grouped:
                grouped[group_id] = AccountGroup(
                    account_group_id=group_id,
                    name=row["name"],
                    account_ids=[],
                    include_in_report=row["include_in_report"],
                    display_order=row["display_order"],
                    created_at=row["created_at"],
                )
            if row["account_id"] is not None:
                grouped[group_id].account_ids.append(row["account_id"])

        return list(grouped.values())

    @use_transaction()
    async def update_display_orders(
        self, conn: Connection, orders: Iterable[tuple[int, int]]
    ) -> int:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            updated = 0
            for account_group_id, display_order in orders:
                await cur.execute(
                    "UPDATE account_groups SET display_order = %s WHERE account_group_id = %s",
                    (display_order, account_group_id),
                )
                updated += 1
            return updated


# ---------------------------------------------------------------------------
# Holding
# ---------------------------------------------------------------------------


class PsycopgHoldingRepository(_BaseRepo, HoldingRepository):
    @use_transaction()
    async def add(self, conn: Connection, holding: Holding) -> Holding:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO holdings (
                    account_id, product_id, is_visible, deletion_reason, deleted_at, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING holding_id, account_id, product_id, is_visible, deletion_reason, deleted_at, created_at
                """,
                (
                    holding.account_id,
                    holding.product_id,
                    holding.is_visible,
                    holding.deletion_reason,
                    holding.deleted_at,
                    _utc_now_naive(),
                ),
            )
            row = await cur.fetchone()
        return Holding(
            holding_id=row["holding_id"],
            account_id=row["account_id"],
            product_id=row["product_id"],
            is_visible=row["is_visible"],
            deletion_reason=row["deletion_reason"],
            deleted_at=row["deleted_at"],
            created_at=row["created_at"],
        )

    @use_transaction()
    async def find_by_id(self, conn: Connection, holding_id: int) -> Holding | None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT holding_id, account_id, product_id, is_visible, deletion_reason, deleted_at, created_at
                FROM holdings WHERE holding_id = %s
                """,
                (holding_id,),
            )
            row = await cur.fetchone()
        if not row:
            return None
        return Holding(
            holding_id=row["holding_id"],
            account_id=row["account_id"],
            product_id=row["product_id"],
            is_visible=row["is_visible"],
            deletion_reason=row["deletion_reason"],
            deleted_at=row["deleted_at"],
            created_at=row["created_at"],
        )

    @use_transaction()
    async def exists_by_account_product(
        self, conn: Connection, account_id: int, product_id: int
    ) -> bool:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT 1 FROM holdings WHERE account_id = %s AND product_id = %s LIMIT 1",
                (account_id, product_id),
            )
            row = await cur.fetchone()
            return row is not None

    @use_transaction()
    async def hide(
        self, conn: Connection, holding: Holding, reason: str | None = None
    ) -> Holding:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                UPDATE holdings
                SET is_visible = FALSE,
                    deletion_reason = %s,
                    deleted_at = %s
                WHERE holding_id = %s
                """,
                (reason, _utc_now_naive(), holding.holding_id),
            )
        return holding

    @use_transaction()
    async def hard_delete(self, conn: Connection, holding_id: int) -> None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "DELETE FROM holdings WHERE holding_id = %s", (holding_id,)
            )

    @use_transaction()
    async def count_referencing_snapshot_holdings(
        self, conn: Connection, holding_id: int
    ) -> int:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT COUNT(*) AS cnt FROM snapshot_holdings WHERE holding_id = %s",
                (holding_id,),
            )
            row = await cur.fetchone()
        return int(row["cnt"] if row else 0)

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Holding]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT holding_id, account_id, product_id, is_visible, deletion_reason, deleted_at, created_at
                FROM holdings ORDER BY holding_id
                """
            )
            rows = await cur.fetchall()
        return [
            Holding(
                holding_id=row["holding_id"],
                account_id=row["account_id"],
                product_id=row["product_id"],
                is_visible=row["is_visible"],
                deletion_reason=row["deletion_reason"],
                deleted_at=row["deleted_at"],
                created_at=row["created_at"],
            )
            for row in rows
        ]


# ---------------------------------------------------------------------------
# Snapshot
# ---------------------------------------------------------------------------


class PsycopgSnapshotRepository(_BaseRepo, SnapshotRepository):
    async def _load_snapshot(
        self, connection: AsyncConnection, snapshot_id: int
    ) -> Snapshot | None:
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT snapshot_id, user_id, reference_date, status, locked_at, editable_until, created_at
                FROM snapshots WHERE snapshot_id = %s
                """,
                (snapshot_id,),
            )
            snap = await cur.fetchone()
            if not snap:
                return None
            await cur.execute(
                """
                SELECT holding_id, valuation_amount, data_source
                FROM snapshot_holdings WHERE snapshot_id = %s
                """,
                (snapshot_id,),
            )
            holdings_rows = await cur.fetchall()
        holdings = [
            SnapshotHolding(
                holding_id=row["holding_id"],
                valuation_amount=float(row["valuation_amount"]),
                data_source=row["data_source"],
            )
            for row in holdings_rows
        ]
        return Snapshot(
            snapshot_id=snap["snapshot_id"],
            user_id=snap["user_id"],
            reference_date=snap["reference_date"],
            status=snap["status"],
            locked_at=snap["locked_at"],
            editable_until=snap["editable_until"],
            created_at=snap["created_at"],
            holdings=holdings,
        )

    @use_transaction()
    async def add(self, conn: Connection, snapshot: Snapshot) -> Snapshot:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO snapshots (user_id, reference_date, status, locked_at, editable_until, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING snapshot_id, user_id, reference_date, status, locked_at, editable_until, created_at
                """,
                (
                    snapshot.user_id,
                    snapshot.reference_date,
                    snapshot.status,
                    snapshot.locked_at,
                    snapshot.editable_until,
                    _utc_now_naive(),
                ),
            )
            row = await cur.fetchone()
        return Snapshot(
            snapshot_id=row["snapshot_id"],
            user_id=row["user_id"],
            reference_date=row["reference_date"],
            status=row["status"],
            locked_at=row["locked_at"],
            editable_until=row["editable_until"],
            created_at=row["created_at"],
            holdings=[],
        )

    @use_transaction()
    async def find_by_id(self, conn: Connection, snapshot_id: int) -> Snapshot | None:
        connection = self._require_conn(conn)
        return await self._load_snapshot(connection, snapshot_id)

    @use_transaction()
    async def find_by_reference(
        self, conn: Connection, user_id: int, reference_date: date
    ) -> Snapshot | None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "SELECT snapshot_id FROM snapshots WHERE user_id = %s AND reference_date = %s",
                (user_id, reference_date),
            )
            row = await cur.fetchone()
        if not row:
            return None
        return await self._load_snapshot(connection, row["snapshot_id"])

    @use_transaction()
    async def save_holding(
        self, conn: Connection, snapshot_id: int, snapshot_holding: SnapshotHolding
    ) -> SnapshotHolding:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO snapshot_holdings (snapshot_id, holding_id, valuation_amount, data_source, created_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (snapshot_id, holding_id)
                DO UPDATE SET valuation_amount = EXCLUDED.valuation_amount,
                              data_source = EXCLUDED.data_source,
                              created_at = EXCLUDED.created_at
                RETURNING holding_id, valuation_amount, data_source
                """,
                (
                    snapshot_id,
                    snapshot_holding.holding_id,
                    snapshot_holding.valuation_amount,
                    snapshot_holding.data_source,
                    _utc_now_naive(),
                ),
            )
            row = await cur.fetchone()
        return SnapshotHolding(
            holding_id=row["holding_id"],
            valuation_amount=float(row["valuation_amount"]),
            data_source=row["data_source"],
        )

    @use_transaction()
    async def lock(self, conn: Connection, snapshot_id: int) -> None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "UPDATE snapshots SET status = 'locked', locked_at = %s WHERE snapshot_id = %s",
                (_utc_now_naive(), snapshot_id),
            )

    @use_transaction()
    async def unlock(self, conn: Connection, snapshot_id: int) -> None:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                "UPDATE snapshots SET status = 'in_progress', locked_at = NULL WHERE snapshot_id = %s",
                (snapshot_id,),
            )

    @use_transaction()
    async def has_later_locked_snapshots(
        self, conn: Connection, user_id: int, reference_date: date
    ) -> bool:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT 1 FROM snapshots
                WHERE user_id = %s
                  AND reference_date > %s
                  AND status = 'locked'
                LIMIT 1
                """,
                (user_id, reference_date),
            )
            return await cur.fetchone() is not None

    @use_transaction()
    async def clone_weekly(
        self,
        conn: Connection,
        *,
        source_snapshot_id: int,
        user_id: int,
        reference_date: date,
        status: str,
        editable_until: datetime | None,
    ) -> int:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO weekly_snapshots (
                    user_id,
                    reference_date,
                    source_snapshot_id,
                    status,
                    editable_until,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING weekly_snapshot_id
                """,
                (
                    user_id,
                    reference_date,
                    source_snapshot_id,
                    status,
                    editable_until,
                    _utc_now_naive(),
                ),
            )
            weekly_id_row = await cur.fetchone()
            weekly_id = weekly_id_row["weekly_snapshot_id"]
            await cur.execute(
                """
                INSERT INTO weekly_snapshot_holdings (weekly_snapshot_id, holding_id, valuation_amount, data_source, created_at)
                SELECT %s, holding_id, valuation_amount, data_source, %s
                FROM snapshot_holdings WHERE snapshot_id = %s
                ON CONFLICT (weekly_snapshot_id, holding_id) DO NOTHING
                """,
                (weekly_id, _utc_now_naive(), source_snapshot_id),
            )
        return int(weekly_id)

    @use_transaction()
    async def clone_annual(
        self,
        conn: Connection,
        *,
        source_snapshot_id: int,
        user_id: int,
        reference_date: date,
    ) -> int:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO annual_snapshots (user_id, reference_date, source_snapshot_id, status, created_at)
                VALUES (%s, %s, %s, 'locked', %s)
                RETURNING annual_snapshot_id
                """,
                (user_id, reference_date, source_snapshot_id, _utc_now_naive()),
            )
            annual_row = await cur.fetchone()
            annual_id = annual_row["annual_snapshot_id"]
            await cur.execute(
                """
                INSERT INTO annual_snapshot_holdings (annual_snapshot_id, holding_id, valuation_amount, data_source, created_at)
                SELECT %s, holding_id, valuation_amount, data_source, %s
                FROM snapshot_holdings WHERE snapshot_id = %s
                ON CONFLICT (annual_snapshot_id, holding_id) DO NOTHING
                """,
                (annual_id, _utc_now_naive(), source_snapshot_id),
            )
        return int(annual_id)

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Snapshot]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT snapshot_id, user_id, reference_date, status, locked_at, editable_until, created_at
                FROM snapshots ORDER BY snapshot_id
                """
            )
            rows = await cur.fetchall()
        snapshots = []
        for row in rows:
            loaded = await self._load_snapshot(connection, row["snapshot_id"])
            if loaded:
                snapshots.append(loaded)
        return snapshots

    @use_transaction()
    async def get_weekly_by_user(
        self, conn: Connection, user_id: int
    ) -> list[WeeklySnapshot]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT weekly_snapshot_id, user_id, reference_date, source_snapshot_id, status, editable_until, created_at
                FROM weekly_snapshots
                WHERE user_id = %s
                ORDER BY reference_date DESC, weekly_snapshot_id DESC
                """,
                (user_id,),
            )
            rows = await cur.fetchall()
        return [
            WeeklySnapshot(
                weekly_snapshot_id=row["weekly_snapshot_id"],
                user_id=row["user_id"],
                reference_date=row["reference_date"],
                source_snapshot_id=row["source_snapshot_id"],
                status=row["status"],
                editable_until=row["editable_until"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    @use_transaction()
    async def get_annual_by_user(
        self, conn: Connection, user_id: int
    ) -> list[AnnualSnapshot]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT annual_snapshot_id, user_id, reference_date, source_snapshot_id,
                       status, editable_until, created_at
                FROM annual_snapshots
                WHERE user_id = %s
                ORDER BY reference_date DESC, annual_snapshot_id DESC
                """,
                (user_id,),
            )
            rows = await cur.fetchall()
        return [
            AnnualSnapshot(
                annual_snapshot_id=row["annual_snapshot_id"],
                user_id=row["user_id"],
                reference_date=row["reference_date"],
                source_snapshot_id=row["source_snapshot_id"],
                status=row["status"],
                editable_until=row["editable_until"],
                created_at=row["created_at"],
            )
            for row in rows
        ]


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


class PsycopgReportQueryRepository(_BaseRepo, ReportQueryRepository):
    @use_transaction()
    async def weekly_account_report(
        self,
        conn: Connection,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ) -> list[dict]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT ws.reference_date,
                       i.name AS institution_name,
                       a.account_id,
                       a.name AS account_name,
                       SUM(wsh.valuation_amount) AS total_valuation
                FROM weekly_snapshots ws
                JOIN weekly_snapshot_holdings wsh ON ws.weekly_snapshot_id = wsh.weekly_snapshot_id
                JOIN holdings h ON wsh.holding_id = h.holding_id
                JOIN accounts a ON h.account_id = a.account_id
                JOIN institutions i ON a.institution_id = i.institution_id
                WHERE ws.user_id = %s
                  AND (%s IS NULL OR ws.reference_date >= %s)
                  AND (%s IS NULL OR ws.reference_date <= %s)
                GROUP BY ws.reference_date, i.name, a.account_id, a.name, i.display_order, a.display_order
                ORDER BY ws.reference_date DESC, i.display_order, a.display_order
                """,
                (user_id, start_date, start_date, end_date, end_date),
            )
            rows = await cur.fetchall()
        return [dict(row) for row in rows]

    @use_transaction()
    async def annual_account_report(
        self, conn: Connection, user_id: int, year: int | None
    ) -> list[dict]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT EXTRACT(YEAR FROM asnap.reference_date) AS year,
                       asnap.reference_date,
                       i.name AS institution_name,
                       i.display_order AS institution_display_order,
                       a.account_id,
                       a.name AS account_name,
                       a.display_order AS account_display_order,
                       SUM(ash.valuation_amount) AS total_valuation
                FROM annual_snapshots asnap
                JOIN annual_snapshot_holdings ash ON asnap.annual_snapshot_id = ash.annual_snapshot_id
                JOIN holdings h ON ash.holding_id = h.holding_id
                JOIN accounts a ON h.account_id = a.account_id
                JOIN institutions i ON a.institution_id = i.institution_id
                WHERE asnap.user_id = %s
                  AND (%s IS NULL OR EXTRACT(YEAR FROM asnap.reference_date) = %s)
                GROUP BY year, asnap.reference_date, i.name, i.display_order, a.account_id, a.name, a.display_order
                ORDER BY year DESC, i.display_order, a.display_order
                """,
                (user_id, year, year),
            )
            rows = await cur.fetchall()
        return [dict(row) for row in rows]

    @use_transaction()
    async def weekly_account_group_report(
        self,
        conn: Connection,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ) -> list[dict]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT ws.reference_date,
                       ag.name AS account_group_name,
                       a.account_id,
                       a.name AS account_name,
                       SUM(wsh.valuation_amount) AS valuation,
                       SUM(SUM(wsh.valuation_amount)) OVER (PARTITION BY ag.account_group_id, ws.reference_date) AS group_total
                FROM weekly_snapshots ws
                JOIN weekly_snapshot_holdings wsh ON ws.weekly_snapshot_id = wsh.weekly_snapshot_id
                JOIN holdings h ON wsh.holding_id = h.holding_id
                JOIN accounts a ON h.account_id = a.account_id
                JOIN account_group_accounts aga ON a.account_id = aga.account_id
                JOIN account_groups ag ON aga.account_group_id = ag.account_group_id
                WHERE ws.user_id = %s
                  AND (%s IS NULL OR ws.reference_date >= %s)
                  AND (%s IS NULL OR ws.reference_date <= %s)
                GROUP BY ws.reference_date, ag.account_group_id, ag.name, a.account_id, a.name
                ORDER BY ws.reference_date DESC, ag.name, a.account_id
                """,
                (user_id, start_date, start_date, end_date, end_date),
            )
            rows = await cur.fetchall()
        return [dict(row) for row in rows]

    @use_transaction()
    async def annual_account_group_report(
        self, conn: Connection, user_id: int, year: int | None
    ) -> list[dict]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT EXTRACT(YEAR FROM asnap.reference_date) AS year,
                       asnap.reference_date,
                       ag.name AS account_group_name,
                       a.account_id,
                       a.name AS account_name,
                       SUM(ash.valuation_amount) AS valuation,
                       SUM(SUM(ash.valuation_amount)) OVER (PARTITION BY ag.account_group_id, asnap.reference_date) AS group_total
                FROM annual_snapshots asnap
                JOIN annual_snapshot_holdings ash ON asnap.annual_snapshot_id = ash.annual_snapshot_id
                JOIN holdings h ON ash.holding_id = h.holding_id
                JOIN accounts a ON h.account_id = a.account_id
                JOIN account_group_accounts aga ON a.account_id = aga.account_id
                JOIN account_groups ag ON aga.account_group_id = ag.account_group_id
                WHERE asnap.user_id = %s
                  AND (%s IS NULL OR EXTRACT(YEAR FROM asnap.reference_date) = %s)
                GROUP BY year, asnap.reference_date, ag.account_group_id, ag.name, a.account_id, a.name
                ORDER BY year DESC, ag.name, a.account_id
                """,
                (user_id, year, year),
            )
            rows = await cur.fetchall()
        return [dict(row) for row in rows]

    @use_transaction()
    async def asset_class_report(
        self, conn: Connection, user_id: int, snapshot_date: date
    ) -> list[dict]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT p.asset_class,
                       p.product_name,
                       SUM(sh.valuation_amount) AS valuation_amount,
                       SUM(SUM(sh.valuation_amount)) OVER (PARTITION BY p.asset_class) AS subtotal
                FROM snapshots s
                JOIN snapshot_holdings sh ON s.snapshot_id = sh.snapshot_id
                JOIN holdings h ON sh.holding_id = h.holding_id
                JOIN products p ON h.product_id = p.product_id
                WHERE s.user_id = %s
                  AND s.reference_date = %s
                  AND s.status = 'locked'
                GROUP BY p.asset_class, p.product_name
                ORDER BY p.asset_class, p.product_name
                """,
                (user_id, snapshot_date),
            )
            rows = await cur.fetchall()
        return [dict(row) for row in rows]

    @use_transaction()
    async def get_weekly_snapshot_holdings(
        self, conn: Connection, weekly_snapshot_ids: list[int]
    ) -> list[dict]:
        """주간 스냅샷들의 보유자산 데이터 조회"""
        if not weekly_snapshot_ids:
            return []

        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT wsh.weekly_snapshot_id,
                       wsh.holding_id,
                       wsh.valuation_amount,
                       h.account_id,
                       a.institution_id,
                       a.name AS account_name,
                       a.display_order,
                      i.name AS institution_name,
                      p.asset_class
                FROM weekly_snapshot_holdings wsh
                JOIN holdings h ON wsh.holding_id = h.holding_id
                JOIN accounts a ON h.account_id = a.account_id
                JOIN institutions i ON a.institution_id = i.institution_id
                  JOIN products p ON h.product_id = p.product_id
                WHERE wsh.weekly_snapshot_id = ANY(%s)
                ORDER BY i.display_order, a.display_order
                """,
                (weekly_snapshot_ids,),
            )
            rows = await cur.fetchall()
        return [dict(row) for row in rows]

    @use_transaction()
    async def get_annual_snapshot_holdings(
        self, conn: Connection, annual_snapshot_id: int
    ) -> list[dict]:
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                SELECT ash.annual_snapshot_holding_id,
                       ash.annual_snapshot_id,
                       ash.holding_id,
                       ash.valuation_amount,
                       ash.data_source,
                       ash.created_at,
                       h.account_id,
                       a.name AS account_name,
                       a.display_order AS account_display_order,
                       i.institution_id,
                       i.name AS institution_name,
                       i.display_order AS institution_display_order,
                       p.product_id,
                       p.product_name,
                                             p.display_order AS product_display_order,
                                             p.asset_class
                  FROM annual_snapshot_holdings ash
                JOIN holdings h ON ash.holding_id = h.holding_id
                JOIN accounts a ON h.account_id = a.account_id
                JOIN institutions i ON a.institution_id = i.institution_id
                JOIN products p ON h.product_id = p.product_id
                WHERE ash.annual_snapshot_id = %s
                ORDER BY i.display_order, a.display_order, p.display_order, p.product_id
                """,
                (annual_snapshot_id,),
            )
            rows = await cur.fetchall()
        return [dict(row) for row in rows]

    @use_transaction()
    async def institution_assets_report(
        self, conn: Connection, user_id: int
    ) -> list[dict]:
        """금융기관별 최근 주간스냅샷 기준 자산총합 조회"""
        connection = self._require_conn(conn)
        async with connection.cursor() as cur:
            await cur.execute(
                """
                WITH latest_weekly_snapshot AS (
                    SELECT weekly_snapshot_id, reference_date
                    FROM weekly_snapshots
                    WHERE user_id = %s
                    ORDER BY reference_date DESC
                    LIMIT 1
                )
                SELECT i.institution_id,
                       i.name AS institution_name,
                       i.display_order,
                       i.type,
                       SUM(wsh.valuation_amount) AS total_assets
                FROM latest_weekly_snapshot lws
                JOIN weekly_snapshot_holdings wsh ON lws.weekly_snapshot_id = wsh.weekly_snapshot_id
                JOIN holdings h ON wsh.holding_id = h.holding_id
                JOIN accounts a ON h.account_id = a.account_id
                JOIN institutions i ON a.institution_id = i.institution_id
                GROUP BY i.institution_id, i.name, i.display_order, i.type
                ORDER BY i.display_order, i.institution_id
                """,
                (user_id,),
            )
            rows = await cur.fetchall()
        return [dict(row) for row in rows]


__all__ = [
    "PsycopgInstitutionRepository",
    "PsycopgProductRepository",
    "PsycopgAccountRepository",
    "PsycopgAccountGroupRepository",
    "PsycopgHoldingRepository",
    "PsycopgSnapshotRepository",
    "PsycopgReportQueryRepository",
]
