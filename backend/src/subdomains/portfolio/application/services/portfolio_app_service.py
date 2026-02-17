"""Portfolio application service implementing admin/report use cases."""

from datetime import date, datetime, time, timedelta

from subdomains.portfolio.application.dtos import (
    CreateInstitutionCommand,
    UpdateInstitutionCommand,
    UpdateInstitutionDisplayOrdersCommand,
    CreateProductCommand,
    UpdateProductCommand,
    UpdateProductDisplayOrdersCommand,
    CreateAccountCommand,
    UpdateAccountCommand,
    UpdateAccountDisplayOrdersCommand,
    CreateHoldingCommand,
    DeleteHoldingCommand,
    CreateSnapshotCommand,
    UpsertSnapshotHoldingCommand,
    LockSnapshotCommand,
    CreateWeeklySnapshotCommand,
    CreateAnnualSnapshotCommand,
    CreateAccountGroupCommand,
    WeeklyAccountReportQuery,
    AnnualAccountReportQuery,
    WeeklyAccountGroupReportQuery,
    AssetClassReportQuery,
    InstitutionResult,
    ProductResult,
    AccountResult,
    AccountGroupResult,
    HoldingResult,
    SnapshotHoldingResult,
    SnapshotResult,
    WeeklySnapshotResult,
    AnnualSnapshotResult,
    ReportItem,
    ReportResult,
)
from subdomains.portfolio.domain import (
    Institution,
    Product,
    Account,
    AccountGroup,
    Holding,
    Snapshot,
    SnapshotHolding,
    DuplicateEntityError,
    NotFoundError,
    SnapshotLockedError,
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
from shared.decorators import transactional
from shared.protocols.transaction import TransactionManager


class PortfolioAppService:
    """Application service for portfolio domain."""

    def __init__(
        self,
        institution_repo: InstitutionRepository,
        product_repo: ProductRepository,
        account_repo: AccountRepository,
        account_group_repo: AccountGroupRepository,
        holding_repo: HoldingRepository,
        snapshot_repo: SnapshotRepository,
        report_repo: ReportQueryRepository,
        transaction_manager: TransactionManager,
    ):
        self._institution_repo = institution_repo
        self._product_repo = product_repo
        self._account_repo = account_repo
        self._account_group_repo = account_group_repo
        self._holding_repo = holding_repo
        self._snapshot_repo = snapshot_repo
        self._report_repo = report_repo
        self._txm = transaction_manager

    # ------------------------------------------------------------------
    # Institutions
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_institution(
        self, command: CreateInstitutionCommand
    ) -> InstitutionResult:
        if await self._institution_repo.exists_by_name(command.name):
            raise DuplicateEntityError("institution", command.name)
        model = Institution.create(
            name=command.name,
            type=command.type,
            display_order=command.display_order,
        )
        saved = await self._institution_repo.add(model)
        return InstitutionResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_institution(
        self, command: UpdateInstitutionCommand
    ) -> InstitutionResult:
        existing = await self._institution_repo.find_by_id(command.institution_id)
        if not existing:
            raise NotFoundError("institution", command.institution_id)
        if (
            existing.name != command.name
            and await self._institution_repo.exists_by_name(command.name)
        ):
            raise DuplicateEntityError("institution", command.name)
        updated = Institution(
            institution_id=command.institution_id,
            name=command.name,
            type=command.type,
            display_order=command.display_order,
            created_at=existing.created_at,
        )
        saved = await self._institution_repo.update(updated)
        return InstitutionResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_institution_display_orders(
        self, command: UpdateInstitutionDisplayOrdersCommand
    ) -> int:
        orders = [(item.institution_id, item.display_order) for item in command.items]
        return await self._institution_repo.update_display_orders(orders)

    # ------------------------------------------------------------------
    # Products
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_product(self, command: CreateProductCommand) -> ProductResult:
        if await self._product_repo.exists_identity(
            product_name=command.product_name,
            asset_class=command.asset_class,
            region=command.region,
            currency=command.currency,
            investment_type=command.investment_type,
        ):
            raise DuplicateEntityError("product", command.product_name)
        model = Product.create(
            product_name=command.product_name,
            asset_class=command.asset_class,
            region=command.region,
            currency=command.currency,
            investment_type=command.investment_type,
            characteristics=command.characteristics,
            risk_level=command.risk_level,
            display_order=command.display_order,
        )
        saved = await self._product_repo.add(model)
        return ProductResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_product_display_orders(
        self, command: UpdateProductDisplayOrdersCommand
    ) -> int:
        orders = [(item.product_id, item.display_order) for item in command.items]
        return await self._product_repo.update_display_orders(orders)

    @transactional(mode="writable")
    async def update_product(self, command: UpdateProductCommand) -> ProductResult:
        product = await self._product_repo.find_by_id(command.product_id)
        if product is None:
            raise NotFoundError("product", command.product_id)
        identity_changed = (
            product.product_name != command.product_name
            or product.asset_class != command.asset_class
            or product.region != command.region
            or product.currency != command.currency
            or product.investment_type != command.investment_type
        )
        if identity_changed and await self._product_repo.exists_identity(
            product_name=command.product_name,
            asset_class=command.asset_class,
            region=command.region,
            currency=command.currency,
            investment_type=command.investment_type,
        ):
            raise DuplicateEntityError("product", command.product_name)
        product.update(
            product_name=command.product_name,
            asset_class=command.asset_class,
            region=command.region,
            currency=command.currency,
            investment_type=command.investment_type,
            characteristics=command.characteristics,
            risk_level=command.risk_level,
        )
        saved = await self._product_repo.update(product)
        return ProductResult.from_domain(saved)

    # ------------------------------------------------------------------
    # Accounts
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_account(self, command: CreateAccountCommand) -> AccountResult:
        institution = await self._institution_repo.find_by_id(command.institution_id)
        if institution is None:
            raise NotFoundError("institution", command.institution_id)
        if await self._account_repo.exists_by_name(
            command.institution_id, command.name
        ):
            raise DuplicateEntityError("account", command.name)
        model = Account.create(
            institution_id=command.institution_id,
            name=command.name,
            type=command.type,
            display_order=command.display_order,
        )
        saved = await self._account_repo.add(model)
        return AccountResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_account(self, command: UpdateAccountCommand) -> AccountResult:
        account = await self._account_repo.find_by_id(command.account_id)
        if account is None:
            raise NotFoundError("account", command.account_id)
        if account.name != command.name and await self._account_repo.exists_by_name(
            account.institution_id, command.name
        ):
            raise DuplicateEntityError("account", command.name)
        account.update(
            name=command.name,
            type=command.type,
            display_order=command.display_order,
        )
        saved = await self._account_repo.update(account)
        return AccountResult.from_domain(saved)

    @transactional(mode="writable")
    async def update_account_display_orders(
        self, command: UpdateAccountDisplayOrdersCommand
    ) -> int:
        orders = [(item.account_id, item.display_order) for item in command.items]
        return await self._account_repo.update_display_orders(orders)

    # ------------------------------------------------------------------
    # Account Groups
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_account_group(
        self, command: CreateAccountGroupCommand
    ) -> AccountGroupResult:
        if await self._account_group_repo.exists_by_name(command.name):
            raise DuplicateEntityError("account_group", command.name)
        accounts = await self._account_repo.find_many(command.account_ids)
        if len(accounts) != len(command.account_ids):
            raise NotFoundError("account", "one or more missing")
        model = AccountGroup.create(name=command.name, account_ids=command.account_ids)
        saved = await self._account_group_repo.add(model)
        return AccountGroupResult.from_domain(saved)

    # ------------------------------------------------------------------
    # Holdings
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_holding(self, command: CreateHoldingCommand) -> HoldingResult:
        account = await self._account_repo.find_by_id(command.account_id)
        if account is None:
            raise NotFoundError("account", command.account_id)
        product = await self._product_repo.find_by_id(command.product_id)
        if product is None:
            raise NotFoundError("product", command.product_id)
        if await self._holding_repo.exists_by_account_product(
            command.account_id, command.product_id
        ):
            raise DuplicateEntityError(
                "holding", f"{command.account_id}-{command.product_id}"
            )
        model = Holding.create(
            account_id=command.account_id, product_id=command.product_id
        )
        saved = await self._holding_repo.add(model)
        return HoldingResult.from_domain(saved)

    @transactional(mode="writable")
    async def delete_holding(
        self, command: DeleteHoldingCommand
    ) -> HoldingResult | None:
        holding = await self._holding_repo.find_by_id(command.holding_id)
        if holding is None:
            raise NotFoundError("holding", command.holding_id)
        action = command.action
        if action == "hide":
            holding.hide(command.reason)
            saved = await self._holding_repo.hide(holding, command.reason)
            return HoldingResult.from_domain(saved)
        if action == "hard_delete":
            await self._holding_repo.hard_delete(command.holding_id)
            return None
        raise ValueError("Unsupported action for delete_holding")

    # ------------------------------------------------------------------
    # Snapshots
    # ------------------------------------------------------------------

    @transactional(mode="writable")
    async def create_snapshot(self, command: CreateSnapshotCommand) -> SnapshotResult:
        existing = await self._snapshot_repo.find_by_reference(
            command.user_id, command.reference_date
        )
        if existing:
            raise DuplicateEntityError("snapshot", str(command.reference_date))
        model = Snapshot.create(
            user_id=command.user_id, reference_date=command.reference_date
        )
        saved = await self._snapshot_repo.add(model)
        return SnapshotResult.from_domain(saved)

    @transactional(mode="writable")
    async def upsert_snapshot_holding(
        self, command: UpsertSnapshotHoldingCommand
    ) -> SnapshotHoldingResult:
        snapshot = await self._snapshot_repo.find_by_id(command.snapshot_id)
        if snapshot is None:
            raise NotFoundError("snapshot", command.snapshot_id)
        snapshot.upsert_holding(
            holding_id=command.holding_id,
            valuation_amount=command.valuation_amount,
            data_source=command.data_source,
        )
        sh = SnapshotHolding(
            holding_id=command.holding_id,
            valuation_amount=command.valuation_amount,
            data_source=command.data_source,
        )
        saved = await self._snapshot_repo.save_holding(command.snapshot_id, sh)
        return SnapshotHoldingResult.from_domain(saved)

    @transactional(mode="writable")
    async def lock_snapshot(self, command: LockSnapshotCommand) -> None:
        snapshot = await self._snapshot_repo.find_by_id(command.snapshot_id)
        if snapshot is None:
            raise NotFoundError("snapshot", command.snapshot_id)
        snapshot.lock()
        await self._snapshot_repo.lock(command.snapshot_id)

    @transactional(mode="writable")
    async def create_weekly_snapshot(self, command: CreateWeeklySnapshotCommand) -> int:
        source = await self._snapshot_repo.find_by_id(command.source_snapshot_id)
        if source is None:
            raise NotFoundError("snapshot", command.source_snapshot_id)
        if source.status != "locked":
            raise SnapshotLockedError(source.snapshot_id or 0)
        editable_until = datetime.combine(command.reference_date, time.min) + timedelta(
            days=7
        )
        return await self._snapshot_repo.clone_weekly(
            source_snapshot_id=command.source_snapshot_id,
            user_id=command.user_id,
            reference_date=command.reference_date,
            status="in_progress",
            editable_until=editable_until,
        )

    @transactional(mode="writable")
    async def create_annual_snapshot(self, command: CreateAnnualSnapshotCommand) -> int:
        source = await self._snapshot_repo.find_by_id(command.source_snapshot_id)
        if source is None:
            raise NotFoundError("snapshot", command.source_snapshot_id)
        if source.status != "locked":
            raise SnapshotLockedError(source.snapshot_id or 0)
        return await self._snapshot_repo.clone_annual(
            source_snapshot_id=command.source_snapshot_id,
            user_id=command.user_id,
            reference_date=command.reference_date,
        )

    # ------------------------------------------------------------------
    # Reports (쿼리 시점 실시간 집계)
    # ------------------------------------------------------------------

    @transactional(mode="readonly")
    async def weekly_account_report(
        self, query: WeeklyAccountReportQuery
    ) -> ReportResult:
        rows = await self._report_repo.weekly_account_report(
            query.user_id, query.start_date, query.end_date
        )
        items = [ReportItem(row) for row in rows]
        total = sum(r.get("total_valuation", 0) or 0 for r in rows)
        return ReportResult(items=items, total_amount=total)

    @transactional(mode="readonly")
    async def annual_account_report(
        self, query: AnnualAccountReportQuery
    ) -> ReportResult:
        rows = await self._report_repo.annual_account_report(query.user_id, query.year)
        items = [ReportItem(row) for row in rows]
        total = sum(r.get("total_valuation", 0) or 0 for r in rows)
        return ReportResult(items=items, total_amount=total)

    @transactional(mode="readonly")
    async def weekly_account_group_report(
        self, query: WeeklyAccountGroupReportQuery
    ) -> ReportResult:
        rows = await self._report_repo.weekly_account_group_report(
            query.user_id, query.start_date, query.end_date
        )
        items = [ReportItem(row) for row in rows]
        total = sum(r.get("group_total", 0) or 0 for r in rows)
        return ReportResult(items=items, total_amount=total)

    @transactional(mode="readonly")
    async def asset_class_report(self, query: AssetClassReportQuery) -> ReportResult:
        rows = await self._report_repo.asset_class_report(
            query.user_id, query.snapshot_date
        )
        items = [ReportItem(row) for row in rows]
        total = sum(r.get("subtotal", 0) or 0 for r in rows)
        return ReportResult(items=items, total_amount=total)

    # ------------------------------------------------------------------
    # List/Read Operations
    # ------------------------------------------------------------------

    @transactional(mode="readonly")
    async def list_institutions(self) -> list[InstitutionResult]:
        """조회: 모든 금융기관 목록"""
        institutions = await self._institution_repo.get_all()
        return [
            InstitutionResult(
                institution_id=inst.institution_id,
                name=inst.name,
                type=inst.type,
                display_order=inst.display_order,
                created_at=inst.created_at,
            )
            for inst in institutions
        ]

    @transactional(mode="readonly")
    async def list_products(self) -> list[ProductResult]:
        """조회: 모든 상품 목록"""
        products = await self._product_repo.get_all()
        return [
            ProductResult(
                product_id=prod.product_id,
                product_name=prod.product_name,
                asset_class=prod.asset_class,
                region=prod.region,
                currency=prod.currency,
                investment_type=prod.investment_type,
                characteristics=prod.characteristics,
                risk_level=prod.risk_level,
                display_order=prod.display_order,
                created_at=prod.created_at,
            )
            for prod in products
        ]

    @transactional(mode="readonly")
    async def list_accounts(self) -> list[AccountResult]:
        """조회: 모든 계좌 목록"""
        accounts = await self._account_repo.get_all()
        return [
            AccountResult(
                account_id=acc.account_id,
                institution_id=acc.institution_id,
                name=acc.name,
                type=acc.type,
                display_order=acc.display_order,
                created_at=acc.created_at,
            )
            for acc in accounts
        ]

    @transactional(mode="readonly")
    async def list_snapshots(self, user_id: int) -> list[SnapshotResult]:
        """조회: 사용자의 모든 스냅샷"""
        snapshots = await self._snapshot_repo.get_all()
        # 사용자 필터링
        user_snapshots = [s for s in snapshots if s.user_id == user_id]
        return [
            SnapshotResult(
                snapshot_id=snap.snapshot_id,
                user_id=snap.user_id,
                reference_date=snap.reference_date,
                status=snap.status,
                locked_at=snap.locked_at,
                editable_until=snap.editable_until,
                created_at=snap.created_at,
                holdings=[],
            )
            for snap in user_snapshots
        ]

    @transactional(mode="readonly")
    async def list_weekly_snapshots(self, user_id: int) -> list[WeeklySnapshotResult]:
        """조회: 사용자의 모든 주간 스냅샷"""
        snapshots = await self._snapshot_repo.get_weekly_by_user(user_id)
        return [WeeklySnapshotResult.from_domain(snap) for snap in snapshots]

    @transactional(mode="readonly")
    async def list_annual_snapshots(self, user_id: int) -> list[AnnualSnapshotResult]:
        """조회: 사용자의 모든 연간 스냅샷"""
        snapshots = await self._snapshot_repo.get_annual_by_user(user_id)
        return [AnnualSnapshotResult.from_domain(snap) for snap in snapshots]

    @transactional(mode="readonly")
    async def list_holdings(self) -> list[HoldingResult]:
        """조회: 모든 보유자산 목록"""
        holdings = await self._holding_repo.get_all()
        return [
            HoldingResult(
                holding_id=h.holding_id,
                account_id=h.account_id,
                product_id=h.product_id,
                is_visible=h.is_visible,
                deleted_at=h.deleted_at,
                deletion_reason=h.deletion_reason,
                created_at=h.created_at,
            )
            for h in holdings
        ]

    @transactional(mode="readonly")
    async def list_snapshot_holdings(self) -> list[SnapshotHoldingResult]:
        """조회: 모든 스냅샷 보유자산"""
        snapshots = await self._snapshot_repo.get_all()
        result = []
        for snapshot in snapshots:
            for holding in snapshot.holdings:
                result.append(
                    SnapshotHoldingResult(
                        snapshot_id=snapshot.snapshot_id,
                        holding_id=holding.holding_id,
                        valuation_amount=holding.valuation_amount,
                        data_source=holding.data_source,
                    )
                )
        return result
