from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

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

# ============================================================================
# Commands / Queries
# ============================================================================


@dataclass
class CreateInstitutionCommand:
    name: str
    type: str
    display_order: int = 0


@dataclass
class UpdateInstitutionCommand:
    institution_id: int
    name: str
    type: str
    display_order: int = 0


@dataclass
class InstitutionDisplayOrderItem:
    institution_id: int
    display_order: int


@dataclass
class CreateProductCommand:
    product_name: str
    asset_class: str
    region: str
    currency: str
    investment_type: str
    characteristics: list[str] | None
    risk_level: str
    display_order: int = 0


@dataclass
class UpdateProductCommand:
    product_id: int
    product_name: str
    asset_class: str
    region: str
    currency: str
    investment_type: str
    characteristics: list[str] | None
    risk_level: str


@dataclass
class ProductDisplayOrderItem:
    product_id: int
    display_order: int


@dataclass
class CreateAccountCommand:
    institution_id: int
    name: str
    type: str
    display_order: int = 0


@dataclass
class AccountDisplayOrderItem:
    account_id: int
    display_order: int


@dataclass
class UpdateAccountCommand:
    account_id: int
    name: str
    type: str
    display_order: int = 0


@dataclass
class UpdateInstitutionDisplayOrdersCommand:
    items: list[InstitutionDisplayOrderItem]


@dataclass
class UpdateAccountDisplayOrdersCommand:
    items: list[AccountDisplayOrderItem]


@dataclass
class UpdateProductDisplayOrdersCommand:
    items: list[ProductDisplayOrderItem]


@dataclass
class CreateHoldingCommand:
    account_id: int
    product_id: int


@dataclass
class DeleteHoldingCommand:
    holding_id: int
    action: str  # hide | hard_delete
    reason: str | None = None


@dataclass
class CreateSnapshotCommand:
    user_id: int
    reference_date: date


@dataclass
class UpsertSnapshotHoldingCommand:
    snapshot_id: int
    holding_id: int
    valuation_amount: float
    data_source: str  # auto | manual | missing


@dataclass
class LockSnapshotCommand:
    snapshot_id: int


@dataclass
class CreateWeeklySnapshotCommand:
    user_id: int
    reference_date: date
    source_snapshot_id: int


@dataclass
class CreateAnnualSnapshotCommand:
    user_id: int
    reference_date: date
    source_snapshot_id: int


@dataclass
class CreateAccountGroupCommand:
    name: str
    account_ids: list[int]


@dataclass
class WeeklyAccountReportQuery:
    user_id: int
    start_date: date | None = None
    end_date: date | None = None


@dataclass
class AnnualAccountReportQuery:
    user_id: int
    year: int | None = None


@dataclass
class WeeklyAccountGroupReportQuery:
    user_id: int
    start_date: date | None = None
    end_date: date | None = None


@dataclass
class AssetClassReportQuery:
    user_id: int
    snapshot_date: date


@dataclass
class WeeklyPivotReportQuery:
    user_id: int
    year: int


# ============================================================================
# Results
# ============================================================================


@dataclass
class InstitutionResult:
    institution_id: int | None
    name: str
    type: str
    display_order: int
    created_at: datetime

    @classmethod
    def from_domain(cls, model: Institution) -> "InstitutionResult":
        return cls(
            institution_id=model.institution_id,
            name=model.name,
            type=model.type,
            display_order=model.display_order,
            created_at=model.created_at,
        )


@dataclass
class ProductResult:
    product_id: int | None
    product_name: str
    asset_class: str
    region: str
    currency: str
    investment_type: str
    characteristics: list[str] | None
    risk_level: str
    display_order: int
    created_at: datetime

    @classmethod
    def from_domain(cls, model: Product) -> "ProductResult":
        return cls(
            product_id=model.product_id,
            product_name=model.product_name,
            asset_class=model.asset_class,
            region=model.region,
            currency=model.currency,
            investment_type=model.investment_type,
            characteristics=model.characteristics,
            risk_level=model.risk_level,
            display_order=model.display_order,
            created_at=model.created_at,
        )


@dataclass
class AccountResult:
    account_id: int | None
    institution_id: int
    name: str
    type: str
    display_order: int
    created_at: datetime

    @classmethod
    def from_domain(cls, model: Account) -> "AccountResult":
        return cls(
            account_id=model.account_id,
            institution_id=model.institution_id,
            name=model.name,
            type=model.type,
            display_order=model.display_order,
            created_at=model.created_at,
        )


@dataclass
class AccountGroupResult:
    account_group_id: int | None
    name: str
    account_ids: list[int]
    created_at: datetime

    @classmethod
    def from_domain(cls, model: AccountGroup) -> "AccountGroupResult":
        return cls(
            account_group_id=model.account_group_id,
            name=model.name,
            account_ids=model.account_ids,
            created_at=model.created_at,
        )


@dataclass
class HoldingResult:
    holding_id: int | None
    account_id: int
    product_id: int
    is_visible: bool
    deletion_reason: str | None
    deleted_at: datetime | None
    created_at: datetime

    @classmethod
    def from_domain(cls, model: Holding) -> "HoldingResult":
        return cls(
            holding_id=model.holding_id,
            account_id=model.account_id,
            product_id=model.product_id,
            is_visible=model.is_visible,
            deletion_reason=model.deletion_reason,
            deleted_at=model.deleted_at,
            created_at=model.created_at,
        )


@dataclass
class SnapshotHoldingResult:
    holding_id: int
    valuation_amount: float
    data_source: str
    snapshot_id: int | None = None
    snapshot_holding_id: int | None = None
    created_at: datetime | None = None

    @classmethod
    def from_domain(cls, model: SnapshotHolding) -> "SnapshotHoldingResult":
        return cls(
            holding_id=model.holding_id,
            valuation_amount=model.valuation_amount,
            data_source=model.data_source,
        )


@dataclass
class SnapshotResult:
    snapshot_id: int | None
    user_id: int
    reference_date: date
    status: str
    locked_at: datetime | None
    editable_until: datetime | None
    created_at: datetime
    holdings: list[SnapshotHoldingResult]

    @classmethod
    def from_domain(cls, model: Snapshot) -> "SnapshotResult":
        return cls(
            snapshot_id=model.snapshot_id,
            user_id=model.user_id,
            reference_date=model.reference_date,
            status=model.status,
            locked_at=model.locked_at,
            editable_until=model.editable_until,
            created_at=model.created_at,
            holdings=[SnapshotHoldingResult.from_domain(h) for h in model.holdings],
        )


@dataclass
class WeeklySnapshotResult:
    weekly_snapshot_id: int
    user_id: int
    reference_date: date
    source_snapshot_id: int
    status: str
    editable_until: datetime | None
    created_at: datetime

    @classmethod
    def from_domain(cls, model: WeeklySnapshot) -> "WeeklySnapshotResult":
        return cls(
            weekly_snapshot_id=model.weekly_snapshot_id,
            user_id=model.user_id,
            reference_date=model.reference_date,
            source_snapshot_id=model.source_snapshot_id,
            status=model.status,
            editable_until=model.editable_until,
            created_at=model.created_at,
        )


@dataclass
class AnnualSnapshotResult:
    annual_snapshot_id: int
    user_id: int
    reference_date: date
    source_snapshot_id: int
    status: str
    editable_until: datetime | None
    created_at: datetime

    @classmethod
    def from_domain(cls, model: AnnualSnapshot) -> "AnnualSnapshotResult":
        return cls(
            annual_snapshot_id=model.annual_snapshot_id,
            user_id=model.user_id,
            reference_date=model.reference_date,
            source_snapshot_id=model.source_snapshot_id,
            status=model.status,
            editable_until=model.editable_until,
            created_at=model.created_at,
        )


@dataclass
class ReportItem:
    data: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return self.data


@dataclass
class ReportResult:
    items: list[ReportItem]
    total_amount: float | None = None

    def to_dict(self) -> dict:
        return {
            "items": [item.to_dict() for item in self.items],
            "total_amount": self.total_amount,
        }


@dataclass
class WeeklyPivotWeekInfo:
    """주간 스냅샷 정보"""
    weekly_snapshot_id: int
    reference_date: date
    week_number: int  # ISO week number


@dataclass
class WeeklyPivotAccountValuation:
    """특정 주의 계좌 평가액"""
    weekly_snapshot_id: int
    amount: float


@dataclass
class WeeklyPivotAccountRow:
    """계좌별 행 데이터"""
    account_id: int
    account_name: str
    institution_name: str
    valuations: list[WeeklyPivotAccountValuation]  # 주차별 평가액


@dataclass
class WeeklyPivotReportResult:
    """주간 Pivot 보고서 결과"""
    year: int
    weeks: list[WeeklyPivotWeekInfo]
    accounts: list[WeeklyPivotAccountRow]
