"""SQLAlchemy repository implementations for portfolio domain."""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Iterable

from sqlalchemy import select, insert, update, text, bindparam, Date, Integer
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
            display_order=account.display_order,
        )
        session.add(entity)
        await session.flush()
        return Account(
            account_id=entity.account_id,
            institution_id=entity.institution_id,
            name=entity.name,
            type=entity.type,
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
                display_order=e.display_order,
                created_at=e.created_at,
            )
            for e in entities
        ]

    @use_transaction()
    async def get_all(self, conn: Connection) -> list[Account]:
        session = self._require_session(conn)
        result = await session.execute(select(AccountEntity))
        entities = result.scalars().all()
        return [
            Account(
                account_id=e.account_id,
                institution_id=e.institution_id,
                name=e.name,
                type=e.type,
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
        for account_id, display_order in orders:
            await session.execute(
                update(AccountEntity)
                .where(AccountEntity.account_id == account_id)
                .values(display_order=display_order)
            )
            updated += 1
        return updated


# ---------------------------------------------------------------------------
# Account Group
# ---------------------------------------------------------------------------


class SQLAlchemyAccountGroupRepository(_BaseRepo, AccountGroupRepository):
    @use_transaction()
    async def add(self, conn: Connection, group: AccountGroup) -> AccountGroup:
        session = self._require_session(conn)
        entity = AccountGroupEntity(name=group.name)
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
    async def clone_weekly(
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
            INSERT INTO weekly_snapshots (user_id, reference_date, source_snapshot_id, status, created_at)
            VALUES (:user_id, :reference_date, :source_snapshot_id, 'locked', :created_at)
            RETURNING weekly_snapshot_id
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
            GROUP BY ws.reference_date, i.name, a.account_id, a.name
            ORDER BY ws.reference_date DESC, i.name, a.account_id
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
                   a.account_id,
                   a.name AS account_name,
                   SUM(ash.valuation_amount) AS total_valuation
            FROM annual_snapshots asnap
            JOIN annual_snapshot_holdings ash ON asnap.annual_snapshot_id = ash.annual_snapshot_id
            JOIN holdings h ON ash.holding_id = h.holding_id
            JOIN accounts a ON h.account_id = a.account_id
            JOIN institutions i ON a.institution_id = i.institution_id
            WHERE asnap.user_id = :user_id
              AND (:year IS NULL OR EXTRACT(YEAR FROM asnap.reference_date) = :year)
            GROUP BY year, asnap.reference_date, i.name, a.account_id, a.name
            ORDER BY year DESC, i.name, a.account_id
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


__all__ = [
    "SQLAlchemyInstitutionRepository",
    "SQLAlchemyProductRepository",
    "SQLAlchemyAccountRepository",
    "SQLAlchemyAccountGroupRepository",
    "SQLAlchemyHoldingRepository",
    "SQLAlchemySnapshotRepository",
    "SQLAlchemyReportQueryRepository",
]
