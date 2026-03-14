"""SQLAlchemy repository implementations for portfolio domain."""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Iterable

from sqlalchemy import (
    select,
    insert,
    update,
    delete,
    text,
    bindparam,
    Date,
    Integer,
    func,
)
from sqlalchemy.ext.asyncio import AsyncSession

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
from subdomains.portfolio.infra.entities import (
    InstitutionEntity,
    ProductEntity,
    AccountEntity,
    AccountGroupEntity,
    AccountGroupAccountEntity,
    HoldingEntity,
    SnapshotEntity,
    SnapshotHoldingEntity,
    WeeklySnapshotEntity,
    WeeklySnapshotHoldingEntity,
    AnnualSnapshotEntity,
    AnnualSnapshotHoldingEntity,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class _BaseRepo:
    @staticmethod
    def _require_session(conn: Connection) -> AsyncSession:
        if not isinstance(conn, AsyncSession):
            raise InfraError("Connection is not an AsyncSession")
        return conn


# ---------------------------------------------------------------------------
# Institution
# ---------------------------------------------------------------------------


class SQLAlchemyInstitutionRepository(_BaseRepo, InstitutionRepository):
    @use_transaction()
    async def add(self, conn: Connection, institution: Institution) -> Institution:
        session = self._require_session(conn)
        entity = InstitutionEntity(
            name=institution.name,
            type=institution.type,
            display_order=institution.display_order,
        )
        session.add(entity)
        await session.flush()
        return Institution(
            institution_id=entity.institution_id,
            name=entity.name,
            type=entity.type,
            display_order=entity.display_order,
            created_at=entity.created_at,
        )

    @use_transaction()
    async def find_by_id(
        self, conn: Connection, institution_id: int
    ) -> Institution | None:
        session = self._require_session(conn)
        result = await session.execute(
            select(InstitutionEntity).where(
                InstitutionEntity.institution_id == institution_id
            )
        )
        entity = result.scalar_one_or_none()
        if not entity:
            return None
        return Institution(
            institution_id=entity.institution_id,
            name=entity.name,
            type=entity.type,
            display_order=entity.display_order,
            created_at=entity.created_at,
        )

    @use_transaction()
    async def exists_by_name(self, conn: Connection, name: str) -> bool:
        session = self._require_session(conn)
        result = await session.execute(
            select(InstitutionEntity.institution_id).where(
                InstitutionEntity.name == name
            )
        )
        return result.scalar_one_or_none() is not None

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Institution]:
        session = self._require_session(conn)
        result = await session.execute(select(InstitutionEntity))
        entities = result.scalars().all()
        return [
            Institution(
                institution_id=e.institution_id,
                name=e.name,
                type=e.type,
                display_order=e.display_order,
                created_at=e.created_at,
            )
            for e in entities
        ]

    @use_transaction()
    async def update(self, conn: Connection, institution: Institution) -> Institution:
        session = self._require_session(conn)
        await session.execute(
            update(InstitutionEntity)
            .where(InstitutionEntity.institution_id == institution.institution_id)
            .values(
                name=institution.name,
                type=institution.type,
                display_order=institution.display_order,
            )
        )
        result = await session.execute(
            select(InstitutionEntity).where(
                InstitutionEntity.institution_id == institution.institution_id
            )
        )
        entity = result.scalar_one()
        return Institution(
            institution_id=entity.institution_id,
            name=entity.name,
            type=entity.type,
            display_order=entity.display_order,
            created_at=entity.created_at,
        )

    @use_transaction()
    async def update_display_orders(
        self, conn: Connection, orders: Iterable[tuple[int, int]]
    ) -> int:
        session = self._require_session(conn)
        updated = 0
        for institution_id, display_order in orders:
            await session.execute(
                update(InstitutionEntity)
                .where(InstitutionEntity.institution_id == institution_id)
                .values(display_order=display_order)
            )
            updated += 1
        return updated

    @use_transaction()
    async def delete(self, conn: Connection, institution_id: int) -> None:
        session = self._require_session(conn)
        await session.execute(
            delete(InstitutionEntity).where(
                InstitutionEntity.institution_id == institution_id
            )
        )

    @use_transaction()
    async def count_referencing_accounts(
        self, conn: Connection, institution_id: int
    ) -> int:
        session = self._require_session(conn)
        result = await session.execute(
            select(func.count(AccountEntity.account_id)).where(
                AccountEntity.institution_id == institution_id
            )
        )
        return int(result.scalar_one() or 0)


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------


class SQLAlchemyProductRepository(_BaseRepo, ProductRepository):
    @use_transaction()
    async def add(self, conn: Connection, product: Product) -> Product:
        session = self._require_session(conn)
        entity = ProductEntity(
            product_name=product.product_name,
            asset_class=product.asset_class,
            region=product.region,
            currency=product.currency,
            investment_type=product.investment_type,
            characteristics=product.characteristics,
            risk_level=product.risk_level,
            allow_snapshot_input=product.allow_snapshot_input,
            display_order=product.display_order,
        )
        session.add(entity)
        await session.flush()
        return Product(
            product_id=entity.product_id,
            product_name=entity.product_name,
            asset_class=entity.asset_class,
            region=entity.region,
            currency=entity.currency,
            investment_type=entity.investment_type,
            characteristics=entity.characteristics,
            risk_level=entity.risk_level,
            allow_snapshot_input=entity.allow_snapshot_input,
            display_order=entity.display_order,
            created_at=entity.created_at,
        )

    @use_transaction()
    async def find_by_id(self, conn: Connection, product_id: int) -> Product | None:
        session = self._require_session(conn)
        result = await session.execute(
            select(ProductEntity).where(ProductEntity.product_id == product_id)
        )
        entity = result.scalar_one_or_none()
        if not entity:
            return None
        return Product(
            product_id=entity.product_id,
            product_name=entity.product_name,
            asset_class=entity.asset_class,
            region=entity.region,
            currency=entity.currency,
            investment_type=entity.investment_type,
            characteristics=entity.characteristics,
            risk_level=entity.risk_level,
            allow_snapshot_input=entity.allow_snapshot_input,
            display_order=entity.display_order,
            created_at=entity.created_at,
        )

    @use_transaction()
    async def update(self, conn: Connection, product: Product) -> Product:
        session = self._require_session(conn)
        await session.execute(
            update(ProductEntity)
            .where(ProductEntity.product_id == product.product_id)
            .values(
                product_name=product.product_name,
                asset_class=product.asset_class,
                region=product.region,
                currency=product.currency,
                investment_type=product.investment_type,
                characteristics=product.characteristics,
                risk_level=product.risk_level,
                allow_snapshot_input=product.allow_snapshot_input,
                display_order=product.display_order,
            )
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
        session = self._require_session(conn)
        result = await session.execute(
            select(ProductEntity.product_id).where(
                ProductEntity.product_name == product_name,
                ProductEntity.asset_class == asset_class,
                ProductEntity.region == region,
                ProductEntity.currency == currency,
                ProductEntity.investment_type == investment_type,
            )
        )
        return result.scalar_one_or_none() is not None

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Product]:
        session = self._require_session(conn)
        result = await session.execute(
            select(ProductEntity).order_by(
                ProductEntity.display_order, ProductEntity.product_id
            )
        )
        entities = result.scalars().all()
        return [
            Product(
                product_id=e.product_id,
                product_name=e.product_name,
                asset_class=e.asset_class,
                region=e.region,
                currency=e.currency,
                investment_type=e.investment_type,
                characteristics=e.characteristics,
                risk_level=e.risk_level,
                allow_snapshot_input=e.allow_snapshot_input,
                display_order=e.display_order,
                created_at=e.created_at,
            )
            for e in entities
        ]

    @use_transaction()
    async def update_display_orders(
        self, conn: Connection, orders: Iterable[tuple[int, int]]
    ) -> int:
        session = self._require_session(conn)
        updated = 0
        for product_id, display_order in orders:
            await session.execute(
                update(ProductEntity)
                .where(ProductEntity.product_id == product_id)
                .values(display_order=display_order)
            )
            updated += 1
        return updated

    @use_transaction()
    async def delete(self, conn: Connection, product_id: int) -> None:
        session = self._require_session(conn)
        await session.execute(
            delete(ProductEntity).where(ProductEntity.product_id == product_id)
        )

    @use_transaction()
    async def count_referencing_holdings(
        self, conn: Connection, product_id: int
    ) -> int:
        session = self._require_session(conn)
        result = await session.execute(
            select(func.count(HoldingEntity.holding_id)).where(
                HoldingEntity.product_id == product_id
            )
        )
        return int(result.scalar_one() or 0)


# ---------------------------------------------------------------------------
# Account
# ---------------------------------------------------------------------------


class SQLAlchemyAccountRepository(_BaseRepo, AccountRepository):
    @use_transaction()
    async def add(self, conn: Connection, account: Account) -> Account:
        session = self._require_session(conn)
        entity = AccountEntity(
            institution_id=account.institution_id,
            name=account.name,
            type=account.type,
            allow_snapshot_input=account.allow_snapshot_input,
            display_order=account.display_order,
        )
        session.add(entity)
        await session.flush()
        return Account(
            account_id=entity.account_id,
            institution_id=entity.institution_id,
            name=entity.name,
            type=entity.type,
            allow_snapshot_input=entity.allow_snapshot_input,
            display_order=entity.display_order,
            created_at=entity.created_at,
        )

    @use_transaction()
    async def find_by_id(self, conn: Connection, account_id: int) -> Account | None:
        session = self._require_session(conn)
        result = await session.execute(
            select(AccountEntity).where(AccountEntity.account_id == account_id)
        )
        entity = result.scalar_one_or_none()
        if not entity:
            return None
        return Account(
            account_id=entity.account_id,
            institution_id=entity.institution_id,
            name=entity.name,
            type=entity.type,
            allow_snapshot_input=entity.allow_snapshot_input,
            display_order=entity.display_order,
            created_at=entity.created_at,
        )

    @use_transaction()
    async def exists_by_name(
        self, conn: Connection, institution_id: int, name: str
    ) -> bool:
        session = self._require_session(conn)
        result = await session.execute(
            select(AccountEntity.account_id).where(
                AccountEntity.institution_id == institution_id,
                AccountEntity.name == name,
            )
        )
        return result.scalar_one_or_none() is not None

    @use_transaction()
    async def update(self, conn: Connection, account: Account) -> Account:
        session = self._require_session(conn)
        await session.execute(
            update(AccountEntity)
            .where(AccountEntity.account_id == account.account_id)
            .values(
                name=account.name,
                type=account.type,
                allow_snapshot_input=account.allow_snapshot_input,
                display_order=account.display_order,
            )
        )
        return account

    @use_transaction()
    async def find_many(
        self, conn: Connection, account_ids: Iterable[int]
    ) -> list[Account]:
        session = self._require_session(conn)
        if not account_ids:
            return []
        result = await session.execute(
            select(AccountEntity).where(AccountEntity.account_id.in_(list(account_ids)))
        )
        entities = result.scalars().all()
        return [
            Account(
                account_id=e.account_id,
                institution_id=e.institution_id,
                name=e.name,
                type=e.type,
                allow_snapshot_input=e.allow_snapshot_input,
                display_order=e.display_order,
                created_at=e.created_at,
            )
            for e in entities
        ]

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Account]:
        session = self._require_session(conn)
        stmt = text(
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
        result = await session.execute(stmt)
        rows = result.mappings().all()
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
        session = self._require_session(conn)
        updated = 0
        for account_id, display_order in orders:
            await session.execute(
                update(AccountEntity)
                .where(AccountEntity.account_id == account_id)
                .values(display_order=display_order)
            )
            updated += 1
        return updated

    @use_transaction()
    async def delete(self, conn: Connection, account_id: int) -> None:
        session = self._require_session(conn)
        impacted_group_rows = await session.execute(
            select(AccountGroupAccountEntity.account_group_id).where(
                AccountGroupAccountEntity.account_id == account_id
            )
        )
        impacted_group_ids = {
            int(row[0]) for row in impacted_group_rows.all() if row[0] is not None
        }

        await session.execute(
            delete(AccountEntity).where(AccountEntity.account_id == account_id)
        )

        # Delete only groups that were linked to this account and became empty.
        for account_group_id in impacted_group_ids:
            mapped_count_result = await session.execute(
                select(func.count(AccountGroupAccountEntity.account_id)).where(
                    AccountGroupAccountEntity.account_group_id == account_group_id
                )
            )
            mapped_count = int(mapped_count_result.scalar_one() or 0)
            if mapped_count == 0:
                await session.execute(
                    delete(AccountGroupEntity).where(
                        AccountGroupEntity.account_group_id == account_group_id
                    )
                )

    @use_transaction()
    async def count_referencing_holdings(
        self, conn: Connection, account_id: int
    ) -> int:
        session = self._require_session(conn)
        result = await session.execute(
            select(func.count(HoldingEntity.holding_id)).where(
                HoldingEntity.account_id == account_id
            )
        )
        return int(result.scalar_one() or 0)


# ---------------------------------------------------------------------------
# Account Group
# ---------------------------------------------------------------------------


class SQLAlchemyAccountGroupRepository(_BaseRepo, AccountGroupRepository):
    @use_transaction()
    async def add(self, conn: Connection, group: AccountGroup) -> AccountGroup:
        session = self._require_session(conn)
        entity = AccountGroupEntity(
            name=group.name,
            include_in_report=group.include_in_report,
            display_order=group.display_order,
        )
        session.add(entity)
        await session.flush()
        # insert mappings
        if group.account_ids:
            await session.execute(
                insert(AccountGroupAccountEntity),
                [
                    {
                        "account_group_id": entity.account_group_id,
                        "account_id": aid,
                        "created_at": _utc_now_naive(),
                    }
                    for aid in group.account_ids
                ],
            )
        return AccountGroup(
            account_group_id=entity.account_group_id,
            name=entity.name,
            account_ids=list(group.account_ids),
            include_in_report=entity.include_in_report,
            display_order=entity.display_order,
            created_at=entity.created_at,
        )

    @use_transaction()
    async def exists_by_name(self, conn: Connection, name: str) -> bool:
        session = self._require_session(conn)
        result = await session.execute(
            select(AccountGroupEntity.account_group_id).where(
                AccountGroupEntity.name == name
            )
        )
        return result.scalar_one_or_none() is not None

    @use_transaction()
    async def find_by_id(
        self, conn: Connection, account_group_id: int
    ) -> AccountGroup | None:
        session = self._require_session(conn)
        group_result = await session.execute(
            select(AccountGroupEntity).where(
                AccountGroupEntity.account_group_id == account_group_id
            )
        )
        group_entity = group_result.scalar_one_or_none()
        if group_entity is None:
            return None

        mapping_result = await session.execute(
            select(AccountGroupAccountEntity.account_id)
            .where(AccountGroupAccountEntity.account_group_id == account_group_id)
            .order_by(AccountGroupAccountEntity.account_id.asc())
        )
        account_ids = [row[0] for row in mapping_result.all()]

        return AccountGroup(
            account_group_id=group_entity.account_group_id,
            name=group_entity.name,
            account_ids=account_ids,
            include_in_report=group_entity.include_in_report,
            display_order=group_entity.display_order,
            created_at=group_entity.created_at,
        )

    @use_transaction()
    async def update(self, conn: Connection, group: AccountGroup) -> AccountGroup:
        session = self._require_session(conn)
        await session.execute(
            update(AccountGroupEntity)
            .where(AccountGroupEntity.account_group_id == group.account_group_id)
            .values(
                name=group.name,
                include_in_report=group.include_in_report,
                display_order=group.display_order,
            )
        )
        await session.execute(
            delete(AccountGroupAccountEntity).where(
                AccountGroupAccountEntity.account_group_id == group.account_group_id
            )
        )
        if group.account_ids:
            await session.execute(
                insert(AccountGroupAccountEntity),
                [
                    {
                        "account_group_id": group.account_group_id,
                        "account_id": aid,
                        "created_at": _utc_now_naive(),
                    }
                    for aid in group.account_ids
                ],
            )
        return group

    @use_transaction()
    async def delete(self, conn: Connection, account_group_id: int) -> None:
        session = self._require_session(conn)
        await session.execute(
            delete(AccountGroupEntity).where(
                AccountGroupEntity.account_group_id == account_group_id
            )
        )

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[AccountGroup]:
        session = self._require_session(conn)
        groups_result = await session.execute(
            select(AccountGroupEntity).order_by(
                AccountGroupEntity.account_group_id.desc()
            )
        )
        group_entities = list(groups_result.scalars().all())
        if not group_entities:
            return []

        group_ids = [group.account_group_id for group in group_entities]
        mappings_result = await session.execute(
            select(
                AccountGroupAccountEntity.account_group_id,
                AccountGroupAccountEntity.account_id,
            )
            .where(AccountGroupAccountEntity.account_group_id.in_(group_ids))
            .order_by(
                AccountGroupAccountEntity.account_group_id.asc(),
                AccountGroupAccountEntity.account_id.asc(),
            )
        )

        account_ids_by_group: dict[int, list[int]] = {
            group_id: [] for group_id in group_ids
        }
        for group_id, account_id in mappings_result.all():
            account_ids_by_group[group_id].append(account_id)

        return [
            AccountGroup(
                account_group_id=entity.account_group_id,
                name=entity.name,
                account_ids=account_ids_by_group.get(entity.account_group_id, []),
                include_in_report=entity.include_in_report,
                display_order=entity.display_order,
                created_at=entity.created_at,
            )
            for entity in group_entities
        ]

    @use_transaction()
    async def update_display_orders(
        self, conn: Connection, orders: Iterable[tuple[int, int]]
    ) -> int:
        session = self._require_session(conn)
        updated = 0
        for account_group_id, display_order in orders:
            await session.execute(
                update(AccountGroupEntity)
                .where(AccountGroupEntity.account_group_id == account_group_id)
                .values(display_order=display_order)
            )
            updated += 1
        return updated


# ---------------------------------------------------------------------------
# Holding
# ---------------------------------------------------------------------------


class SQLAlchemyHoldingRepository(_BaseRepo, HoldingRepository):
    @use_transaction()
    async def add(self, conn: Connection, holding: Holding) -> Holding:
        session = self._require_session(conn)
        entity = HoldingEntity(
            account_id=holding.account_id,
            product_id=holding.product_id,
            is_visible=holding.is_visible,
            deletion_reason=holding.deletion_reason,
            deleted_at=holding.deleted_at,
        )
        session.add(entity)
        await session.flush()
        return Holding(
            holding_id=entity.holding_id,
            account_id=entity.account_id,
            product_id=entity.product_id,
            is_visible=entity.is_visible,
            deleted_at=entity.deleted_at,
            deletion_reason=entity.deletion_reason,
            created_at=entity.created_at,
        )

    @use_transaction()
    async def find_by_id(self, conn: Connection, holding_id: int) -> Holding | None:
        session = self._require_session(conn)
        result = await session.execute(
            select(HoldingEntity).where(HoldingEntity.holding_id == holding_id)
        )
        entity = result.scalar_one_or_none()
        if not entity:
            return None
        return Holding(
            holding_id=entity.holding_id,
            account_id=entity.account_id,
            product_id=entity.product_id,
            is_visible=entity.is_visible,
            deleted_at=entity.deleted_at,
            deletion_reason=entity.deletion_reason,
            created_at=entity.created_at,
        )

    @use_transaction()
    async def exists_by_account_product(
        self, conn: Connection, account_id: int, product_id: int
    ) -> bool:
        session = self._require_session(conn)
        result = await session.execute(
            select(HoldingEntity.holding_id).where(
                HoldingEntity.account_id == account_id,
                HoldingEntity.product_id == product_id,
            )
        )
        return result.scalar_one_or_none() is not None

    @use_transaction()
    async def hide(
        self, conn: Connection, holding: Holding, reason: str | None = None
    ) -> Holding:
        session = self._require_session(conn)
        await session.execute(
            update(HoldingEntity)
            .where(HoldingEntity.holding_id == holding.holding_id)
            .values(
                is_visible=False,
                deletion_reason=reason,
                deleted_at=_utc_now_naive(),
            )
        )
        return holding

    @use_transaction()
    async def hard_delete(self, conn: Connection, holding_id: int) -> None:
        session = self._require_session(conn)
        entity = await session.get(HoldingEntity, holding_id)
        if entity:
            await session.delete(entity)

    @use_transaction()
    async def count_referencing_snapshot_holdings(
        self, conn: Connection, holding_id: int
    ) -> int:
        session = self._require_session(conn)
        result = await session.execute(
            select(func.count(SnapshotHoldingEntity.snapshot_holding_id)).where(
                SnapshotHoldingEntity.holding_id == holding_id
            )
        )
        return int(result.scalar_one() or 0)

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Holding]:
        session = self._require_session(conn)
        result = await session.execute(select(HoldingEntity))
        entities = result.scalars().all()
        return [
            Holding(
                holding_id=e.holding_id,
                account_id=e.account_id,
                product_id=e.product_id,
                is_visible=e.is_visible,
                deleted_at=e.deleted_at,
                deletion_reason=e.deletion_reason,
                created_at=e.created_at,
            )
            for e in entities
        ]


# ---------------------------------------------------------------------------
# Snapshot
# ---------------------------------------------------------------------------


class SQLAlchemySnapshotRepository(_BaseRepo, SnapshotRepository):
    async def _load_snapshot(
        self, session: AsyncSession, snapshot_id: int
    ) -> Snapshot | None:
        result = await session.execute(
            select(SnapshotEntity).where(SnapshotEntity.snapshot_id == snapshot_id)
        )
        snap = result.scalar_one_or_none()
        if not snap:
            return None
        holdings_res = await session.execute(
            select(SnapshotHoldingEntity).where(
                SnapshotHoldingEntity.snapshot_id == snapshot_id
            )
        )
        holdings_entities = holdings_res.scalars().all()
        holdings = [
            SnapshotHolding(
                holding_id=he.holding_id,
                valuation_amount=float(he.valuation_amount),
                data_source=he.data_source,
            )
            for he in holdings_entities
        ]
        return Snapshot(
            snapshot_id=snap.snapshot_id,
            user_id=snap.user_id,
            reference_date=snap.reference_date,
            status=snap.status,
            locked_at=snap.locked_at,
            editable_until=snap.editable_until,
            created_at=snap.created_at,
            holdings=holdings,
        )

    @use_transaction()
    async def add(self, conn: Connection, snapshot: Snapshot) -> Snapshot:
        session = self._require_session(conn)
        entity = SnapshotEntity(
            user_id=snapshot.user_id,
            reference_date=snapshot.reference_date,
            status=snapshot.status,
            locked_at=snapshot.locked_at,
            editable_until=snapshot.editable_until,
        )
        session.add(entity)
        await session.flush()
        return Snapshot(
            snapshot_id=entity.snapshot_id,
            user_id=entity.user_id,
            reference_date=entity.reference_date,
            status=entity.status,
            locked_at=entity.locked_at,
            editable_until=entity.editable_until,
            created_at=entity.created_at,
            holdings=[],
        )

    @use_transaction()
    async def find_by_id(self, conn: Connection, snapshot_id: int) -> Snapshot | None:
        session = self._require_session(conn)
        return await self._load_snapshot(session, snapshot_id)

    @use_transaction()
    async def find_by_reference(
        self, conn: Connection, user_id: int, reference_date: date
    ) -> Snapshot | None:
        session = self._require_session(conn)
        result = await session.execute(
            select(SnapshotEntity.snapshot_id).where(
                SnapshotEntity.user_id == user_id,
                SnapshotEntity.reference_date == reference_date,
            )
        )
        sid = result.scalar_one_or_none()
        if sid is None:
            return None
        return await self._load_snapshot(session, sid)

    @use_transaction()
    async def save_holding(
        self, conn: Connection, snapshot_id: int, snapshot_holding: SnapshotHolding
    ) -> SnapshotHolding:
        session = self._require_session(conn)
        # upsert
        stmt = text(
            """
            INSERT INTO snapshot_holdings (snapshot_id, holding_id, valuation_amount, data_source, created_at)
            VALUES (:snapshot_id, :holding_id, :valuation_amount, :data_source, :created_at)
            ON CONFLICT (snapshot_id, holding_id)
            DO UPDATE SET valuation_amount = EXCLUDED.valuation_amount,
                          data_source = EXCLUDED.data_source,
                          created_at = EXCLUDED.created_at
            RETURNING holding_id, valuation_amount, data_source
            """
        )
        result = await session.execute(
            stmt,
            {
                "snapshot_id": snapshot_id,
                "holding_id": snapshot_holding.holding_id,
                "valuation_amount": snapshot_holding.valuation_amount,
                "data_source": snapshot_holding.data_source,
                "created_at": _utc_now_naive(),
            },
        )
        row = result.fetchone()
        return SnapshotHolding(
            holding_id=row[0], valuation_amount=float(row[1]), data_source=row[2]
        )

    @use_transaction()
    async def lock(self, conn: Connection, snapshot_id: int) -> None:
        session = self._require_session(conn)
        await session.execute(
            update(SnapshotEntity)
            .where(SnapshotEntity.snapshot_id == snapshot_id)
            .values(status="locked", locked_at=_utc_now_naive())
        )

    @use_transaction()
    async def unlock(self, conn: Connection, snapshot_id: int) -> None:
        session = self._require_session(conn)
        await session.execute(
            update(SnapshotEntity)
            .where(SnapshotEntity.snapshot_id == snapshot_id)
            .values(status="in_progress", locked_at=None)
        )

    @use_transaction()
    async def has_later_locked_snapshots(
        self, conn: Connection, user_id: int, reference_date: date
    ) -> bool:
        session = self._require_session(conn)
        result = await session.execute(
            select(SnapshotEntity)
            .where(
                SnapshotEntity.user_id == user_id,
                SnapshotEntity.reference_date > reference_date,
                SnapshotEntity.status == "locked",
            )
            .limit(1)
        )
        return result.scalar_one_or_none() is not None

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
        session = self._require_session(conn)
        insert_snap = text(
            """
            INSERT INTO weekly_snapshots (
                user_id,
                reference_date,
                source_snapshot_id,
                status,
                editable_until,
                created_at
            )
            VALUES (:user_id, :reference_date, :source_snapshot_id, :status, :editable_until, :created_at)
            RETURNING weekly_snapshot_id
            """
        )
        snap_res = await session.execute(
            insert_snap,
            {
                "user_id": user_id,
                "reference_date": reference_date,
                "source_snapshot_id": source_snapshot_id,
                "status": status,
                "editable_until": editable_until,
                "created_at": _utc_now_naive(),
            },
        )
        weekly_id = snap_res.scalar_one()
        insert_holdings = text(
            """
            INSERT INTO weekly_snapshot_holdings (weekly_snapshot_id, holding_id, valuation_amount, data_source, created_at)
            SELECT :weekly_id, holding_id, valuation_amount, data_source, :created_at
            FROM snapshot_holdings WHERE snapshot_id = :source_snapshot_id
            ON CONFLICT (weekly_snapshot_id, holding_id) DO NOTHING
            """
        )
        await session.execute(
            insert_holdings,
            {
                "weekly_id": weekly_id,
                "source_snapshot_id": source_snapshot_id,
                "created_at": _utc_now_naive(),
            },
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
        session = self._require_session(conn)
        insert_snap = text(
            """
            INSERT INTO annual_snapshots (user_id, reference_date, source_snapshot_id, status, created_at)
            VALUES (:user_id, :reference_date, :source_snapshot_id, 'locked', :created_at)
            RETURNING annual_snapshot_id
            """
        )
        snap_res = await session.execute(
            insert_snap,
            {
                "user_id": user_id,
                "reference_date": reference_date,
                "source_snapshot_id": source_snapshot_id,
                "created_at": _utc_now_naive(),
            },
        )
        annual_id = snap_res.scalar_one()
        insert_holdings = text(
            """
            INSERT INTO annual_snapshot_holdings (annual_snapshot_id, holding_id, valuation_amount, data_source, created_at)
            SELECT :annual_id, holding_id, valuation_amount, data_source, :created_at
            FROM snapshot_holdings WHERE snapshot_id = :source_snapshot_id
            ON CONFLICT (annual_snapshot_id, holding_id) DO NOTHING
            """
        )
        await session.execute(
            insert_holdings,
            {
                "annual_id": annual_id,
                "source_snapshot_id": source_snapshot_id,
                "created_at": _utc_now_naive(),
            },
        )
        return int(annual_id)

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Snapshot]:
        session = self._require_session(conn)
        result = await session.execute(select(SnapshotEntity))
        entities = result.scalars().all()
        snapshots = []
        for entity in entities:
            loaded = await self._load_snapshot(session, entity.snapshot_id)
            if loaded:
                snapshots.append(loaded)
        return snapshots

    @use_transaction()
    async def get_weekly_by_user(
        self, conn: Connection, user_id: int
    ) -> list[WeeklySnapshot]:
        session = self._require_session(conn)
        result = await session.execute(
            select(WeeklySnapshotEntity)
            .where(WeeklySnapshotEntity.user_id == user_id)
            .order_by(
                WeeklySnapshotEntity.reference_date.desc(),
                WeeklySnapshotEntity.weekly_snapshot_id.desc(),
            )
        )
        entities = result.scalars().all()
        return [
            WeeklySnapshot(
                weekly_snapshot_id=entity.weekly_snapshot_id,
                user_id=entity.user_id,
                reference_date=entity.reference_date,
                source_snapshot_id=entity.source_snapshot_id,
                status=entity.status,
                editable_until=entity.editable_until,
                created_at=entity.created_at,
            )
            for entity in entities
        ]

    @use_transaction()
    async def get_annual_by_user(
        self, conn: Connection, user_id: int
    ) -> list[AnnualSnapshot]:
        session = self._require_session(conn)
        result = await session.execute(
            select(AnnualSnapshotEntity)
            .where(AnnualSnapshotEntity.user_id == user_id)
            .order_by(
                AnnualSnapshotEntity.reference_date.desc(),
                AnnualSnapshotEntity.annual_snapshot_id.desc(),
            )
        )
        entities = result.scalars().all()
        return [
            AnnualSnapshot(
                annual_snapshot_id=entity.annual_snapshot_id,
                user_id=entity.user_id,
                reference_date=entity.reference_date,
                source_snapshot_id=entity.source_snapshot_id,
                status=entity.status,
                editable_until=entity.editable_until,
                created_at=entity.created_at,
            )
            for entity in entities
        ]


# ---------------------------------------------------------------------------
# Reports (쿼리 시점 집계)
# ---------------------------------------------------------------------------


class SQLAlchemyReportQueryRepository(_BaseRepo, ReportQueryRepository):
    @use_transaction()
    async def weekly_account_report(
        self,
        conn: Connection,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ) -> list[dict]:
        session = self._require_session(conn)
        stmt = text(
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
            WHERE ws.user_id = :user_id
              AND (:start_date IS NULL OR ws.reference_date >= :start_date)
              AND (:end_date IS NULL OR ws.reference_date <= :end_date)
            GROUP BY ws.reference_date, i.name, a.account_id, a.name, i.display_order, a.display_order
            ORDER BY ws.reference_date DESC, i.display_order, a.display_order
            """
        ).bindparams(
            bindparam("user_id", type_=Integer),
            bindparam("start_date", type_=Date),
            bindparam("end_date", type_=Date),
        )
        result = await session.execute(
            stmt,
            {"user_id": user_id, "start_date": start_date, "end_date": end_date},
        )
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    @use_transaction()
    async def annual_account_report(
        self, conn: Connection, user_id: int, year: int | None
    ) -> list[dict]:
        session = self._require_session(conn)
        stmt = text(
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
            WHERE asnap.user_id = :user_id
              AND (:year IS NULL OR EXTRACT(YEAR FROM asnap.reference_date) = :year)
            GROUP BY year, asnap.reference_date, i.name, i.display_order, a.account_id, a.name, a.display_order
            ORDER BY year DESC, i.display_order, a.display_order
            """
        ).bindparams(
            bindparam("user_id", type_=Integer),
            bindparam("year", type_=Integer),
        )
        result = await session.execute(stmt, {"user_id": user_id, "year": year})
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    @use_transaction()
    async def weekly_account_group_report(
        self,
        conn: Connection,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ) -> list[dict]:
        session = self._require_session(conn)
        stmt = text(
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
            WHERE ws.user_id = :user_id
              AND (:start_date IS NULL OR ws.reference_date >= :start_date)
              AND (:end_date IS NULL OR ws.reference_date <= :end_date)
            GROUP BY ws.reference_date, ag.account_group_id, ag.name, a.account_id, a.name
            ORDER BY ws.reference_date DESC, ag.name, a.account_id
            """
        ).bindparams(
            bindparam("user_id", type_=Integer),
            bindparam("start_date", type_=Date),
            bindparam("end_date", type_=Date),
        )
        result = await session.execute(
            stmt,
            {"user_id": user_id, "start_date": start_date, "end_date": end_date},
        )
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    @use_transaction()
    async def annual_account_group_report(
        self, conn: Connection, user_id: int, year: int | None
    ) -> list[dict]:
        session = self._require_session(conn)
        stmt = text(
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
            WHERE asnap.user_id = :user_id
              AND (:year IS NULL OR EXTRACT(YEAR FROM asnap.reference_date) = :year)
            GROUP BY year, asnap.reference_date, ag.account_group_id, ag.name, a.account_id, a.name
            ORDER BY year DESC, ag.name, a.account_id
            """
        ).bindparams(
            bindparam("user_id", type_=Integer),
            bindparam("year", type_=Integer),
        )
        result = await session.execute(stmt, {"user_id": user_id, "year": year})
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    @use_transaction()
    async def asset_class_report(
        self, conn: Connection, user_id: int, snapshot_date: date
    ) -> list[dict]:
        session = self._require_session(conn)
        stmt = text(
            """
            SELECT p.asset_class,
                   p.product_name,
                   SUM(sh.valuation_amount) AS valuation_amount,
                   SUM(SUM(sh.valuation_amount)) OVER (PARTITION BY p.asset_class) AS subtotal
            FROM snapshots s
            JOIN snapshot_holdings sh ON s.snapshot_id = sh.snapshot_id
            JOIN holdings h ON sh.holding_id = h.holding_id
            JOIN products p ON h.product_id = p.product_id
            WHERE s.user_id = :user_id
              AND s.reference_date = :snapshot_date
              AND s.status = 'locked'
            GROUP BY p.asset_class, p.product_name
            ORDER BY p.asset_class, p.product_name
            """
        )
        result = await session.execute(
            stmt, {"user_id": user_id, "snapshot_date": snapshot_date}
        )
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    @use_transaction()
    async def get_weekly_snapshot_holdings(
        self, conn: Connection, weekly_snapshot_ids: list[int]
    ) -> list[dict]:
        """주간 스냅샷들의 보유자산 데이터 조회"""
        if not weekly_snapshot_ids:
            return []

        session = self._require_session(conn)
        stmt = text(
            """
            SELECT wsh.weekly_snapshot_id,
                   wsh.holding_id,
                   wsh.valuation_amount,
                   h.account_id,
                   a.institution_id,
                   a.name AS account_name,
                   a.display_order,
                   i.name AS institution_name
            FROM weekly_snapshot_holdings wsh
            JOIN holdings h ON wsh.holding_id = h.holding_id
            JOIN accounts a ON h.account_id = a.account_id
            JOIN institutions i ON a.institution_id = i.institution_id
            WHERE wsh.weekly_snapshot_id = ANY(:snapshot_ids)
            ORDER BY i.display_order, a.display_order
            """
        )
        result = await session.execute(stmt, {"snapshot_ids": weekly_snapshot_ids})
        rows = result.mappings().all()
        return [dict(row) for row in rows]

    @use_transaction()
    async def get_annual_snapshot_holdings(
        self, conn: Connection, annual_snapshot_id: int
    ) -> list[dict]:
        session = self._require_session(conn)
        stmt = text(
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
                   p.display_order AS product_display_order
            FROM annual_snapshot_holdings ash
            JOIN holdings h ON ash.holding_id = h.holding_id
            JOIN accounts a ON h.account_id = a.account_id
            JOIN institutions i ON a.institution_id = i.institution_id
            JOIN products p ON h.product_id = p.product_id
            WHERE ash.annual_snapshot_id = :annual_snapshot_id
            ORDER BY i.display_order, a.display_order, p.display_order, p.product_id
            """
        ).bindparams(bindparam("annual_snapshot_id", type_=Integer))
        result = await session.execute(stmt, {"annual_snapshot_id": annual_snapshot_id})
        rows = result.mappings().all()
        return [dict(row) for row in rows]


__all__ = [
    "SQLAlchemyInstitutionRepository",
    "SQLAlchemyProductRepository",
    "SQLAlchemyAccountRepository",
    "SQLAlchemyAccountGroupRepository",
    "SQLAlchemyHoldingRepository",
    "SQLAlchemySnapshotRepository",
    "SQLAlchemyReportQueryRepository",
]
