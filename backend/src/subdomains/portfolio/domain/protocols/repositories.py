from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Iterable

from shared.protocols.transaction import Connection
from subdomains.portfolio.domain.models import (
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


class InstitutionRepository(ABC):
    @abstractmethod
    async def add(self, conn: Connection, institution: Institution) -> Institution: ...

    @abstractmethod
    async def find_by_id(
        self, conn: Connection, institution_id: int
    ) -> Institution | None: ...

    @abstractmethod
    async def exists_by_name(self, conn: Connection, name: str) -> bool: ...

    @abstractmethod
    async def get_all(self, conn: Connection) -> list[Institution]: ...

    @abstractmethod
    async def update(
        self, conn: Connection, institution: Institution
    ) -> Institution: ...

    @abstractmethod
    async def update_display_orders(
        self, conn: Connection, orders: Iterable[tuple[int, int]]
    ) -> int: ...

    @abstractmethod
    async def delete(self, conn: Connection, institution_id: int) -> None: ...

    @abstractmethod
    async def count_referencing_accounts(
        self, conn: Connection, institution_id: int
    ) -> int: ...


class ProductRepository(ABC):
    @abstractmethod
    async def add(self, conn: Connection, product: Product) -> Product: ...

    @abstractmethod
    async def find_by_id(self, conn: Connection, product_id: int) -> Product | None: ...

    @abstractmethod
    async def exists_identity(
        self,
        conn: Connection,
        *,
        product_name: str,
        asset_class: str,
        region: str,
        currency: str,
        investment_type: str,
    ) -> bool: ...

    @abstractmethod
    async def update(self, conn: Connection, product: Product) -> Product: ...

    @abstractmethod
    async def get_all(self, conn: Connection) -> list[Product]: ...

    @abstractmethod
    async def update_display_orders(
        self, conn: Connection, orders: Iterable[tuple[int, int]]
    ) -> int: ...

    @abstractmethod
    async def delete(self, conn: Connection, product_id: int) -> None: ...

    @abstractmethod
    async def count_referencing_holdings(
        self, conn: Connection, product_id: int
    ) -> int: ...


class AccountRepository(ABC):
    @abstractmethod
    async def add(self, conn: Connection, account: Account) -> Account: ...

    @abstractmethod
    async def find_by_id(self, conn: Connection, account_id: int) -> Account | None: ...

    @abstractmethod
    async def exists_by_name(
        self, conn: Connection, institution_id: int, name: str
    ) -> bool: ...

    @abstractmethod
    async def update(self, conn: Connection, account: Account) -> Account: ...

    @abstractmethod
    async def find_many(
        self, conn: Connection, account_ids: Iterable[int]
    ) -> list[Account]: ...

    @abstractmethod
    async def get_all(self, conn: Connection) -> list[Account]: ...

    @abstractmethod
    async def update_display_orders(
        self, conn: Connection, orders: Iterable[tuple[int, int]]
    ) -> int: ...

    @abstractmethod
    async def delete(self, conn: Connection, account_id: int) -> None: ...

    @abstractmethod
    async def count_referencing_holdings(
        self, conn: Connection, account_id: int
    ) -> int: ...


class AccountGroupRepository(ABC):
    @abstractmethod
    async def add(self, conn: Connection, group: AccountGroup) -> AccountGroup: ...

    @abstractmethod
    async def exists_by_name(self, conn: Connection, name: str) -> bool: ...

    @abstractmethod
    async def find_by_id(
        self, conn: Connection, account_group_id: int
    ) -> AccountGroup | None: ...

    @abstractmethod
    async def update(self, conn: Connection, group: AccountGroup) -> AccountGroup: ...

    @abstractmethod
    async def delete(self, conn: Connection, account_group_id: int) -> None: ...

    @abstractmethod
    async def get_all(self, conn: Connection) -> list[AccountGroup]: ...


class HoldingRepository(ABC):
    @abstractmethod
    async def add(self, conn: Connection, holding: Holding) -> Holding: ...

    @abstractmethod
    async def find_by_id(self, conn: Connection, holding_id: int) -> Holding | None: ...

    @abstractmethod
    async def exists_by_account_product(
        self, conn: Connection, account_id: int, product_id: int
    ) -> bool: ...

    @abstractmethod
    async def hide(
        self, conn: Connection, holding: Holding, reason: str | None = None
    ) -> Holding: ...

    @abstractmethod
    async def hard_delete(self, conn: Connection, holding_id: int) -> None: ...

    @abstractmethod
    async def count_referencing_snapshot_holdings(
        self, conn: Connection, holding_id: int
    ) -> int: ...

    @abstractmethod
    async def get_all(self, conn: Connection) -> list[Holding]: ...


class SnapshotRepository(ABC):
    @abstractmethod
    async def add(self, conn: Connection, snapshot: Snapshot) -> Snapshot: ...

    @abstractmethod
    async def find_by_id(
        self, conn: Connection, snapshot_id: int
    ) -> Snapshot | None: ...

    @abstractmethod
    async def find_by_reference(
        self, conn: Connection, user_id: int, reference_date: date
    ) -> Snapshot | None: ...

    @abstractmethod
    async def save_holding(
        self,
        conn: Connection,
        snapshot_id: int,
        snapshot_holding: SnapshotHolding,
    ) -> SnapshotHolding: ...

    @abstractmethod
    async def lock(self, conn: Connection, snapshot_id: int) -> None: ...

    @abstractmethod
    async def unlock(self, conn: Connection, snapshot_id: int) -> None: ...

    @abstractmethod
    async def has_later_locked_snapshots(
        self, conn: Connection, user_id: int, reference_date: date
    ) -> bool: ...

    @abstractmethod
    async def clone_weekly(
        self,
        conn: Connection,
        *,
        source_snapshot_id: int,
        user_id: int,
        reference_date: date,
        status: str,
        editable_until: datetime | None,
    ) -> int: ...

    @abstractmethod
    async def clone_annual(
        self,
        conn: Connection,
        *,
        source_snapshot_id: int,
        user_id: int,
        reference_date: date,
    ) -> int: ...

    @abstractmethod
    async def get_all(self, conn: Connection) -> list[Snapshot]: ...

    @abstractmethod
    async def get_weekly_by_user(
        self, conn: Connection, user_id: int
    ) -> list[WeeklySnapshot]: ...

    @abstractmethod
    async def get_annual_by_user(
        self, conn: Connection, user_id: int
    ) -> list[AnnualSnapshot]: ...


class ReportQueryRepository(ABC):
    @abstractmethod
    async def weekly_account_report(
        self,
        conn: Connection,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ) -> list[dict]: ...

    @abstractmethod
    async def annual_account_report(
        self, conn: Connection, user_id: int, year: int | None
    ) -> list[dict]: ...

    @abstractmethod
    async def weekly_account_group_report(
        self,
        conn: Connection,
        user_id: int,
        start_date: date | None,
        end_date: date | None,
    ) -> list[dict]: ...

    @abstractmethod
    async def annual_account_group_report(
        self, conn: Connection, user_id: int, year: int | None
    ) -> list[dict]: ...

    @abstractmethod
    async def asset_class_report(
        self, conn: Connection, user_id: int, snapshot_date: date
    ) -> list[dict]: ...

    @abstractmethod
    async def get_weekly_snapshot_holdings(
        self, weekly_snapshot_ids: list[int]
    ) -> list[dict]: ...

    @abstractmethod
    async def get_annual_snapshot_holdings(
        self, conn: Connection, annual_snapshot_id: int
    ) -> list[dict]: ...

    @abstractmethod
    async def institution_assets_report(
        self, conn: Connection, user_id: int
    ) -> list[dict]: ...
