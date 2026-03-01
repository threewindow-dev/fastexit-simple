"""Portfolio API 요청/응답 스키마."""

from __future__ import annotations

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, Field

from shared.schemas import ApiResponse

# ---------------------------------------------------------------------------
# Institutions
# ---------------------------------------------------------------------------


class CreateInstitutionRequest(BaseModel):
    name: str = Field(..., description="기관명", examples=["KB증권", "국민은행"])
    type: str = Field(..., description="유형", examples=["증권사", "은행", "기타기관"])
    display_order: int = Field(0, description="표시 순서", examples=[0])


class UpdateInstitutionRequest(BaseModel):
    name: str = Field(..., description="기관명", examples=["KB증권", "국민은행"])
    type: str = Field(..., description="유형", examples=["증권사", "은행", "기타기관"])
    display_order: int = Field(0, description="표시 순서", examples=[0])


class InstitutionResponseData(BaseModel):
    institution_id: int | None = Field(None, description="기관 ID", examples=[1])
    name: str = Field(..., description="기관명", examples=["KB증권"])
    type: str = Field(..., description="유형", examples=["증권사", "은행", "기타기관"])
    display_order: int = Field(0, description="표시 순서", examples=[0])
    created_at: str = Field(
        ..., description="생성 시각", examples=["2025-01-01T00:00:00"]
    )


class InstitutionResponse(ApiResponse[InstitutionResponseData]):
    pass


class InstitutionsResponseData(BaseModel):
    items: list[InstitutionResponseData] = Field(..., description="기관 목록")
    max_display_order: int = Field(0, description="최대 표시 순서", examples=[10])


class InstitutionsResponse(ApiResponse[InstitutionsResponseData]):
    pass


class InstitutionDisplayOrderItem(BaseModel):
    institution_id: int = Field(..., description="기관 ID", examples=[1])
    display_order: int = Field(..., description="표시 순서", examples=[1])


class UpdateInstitutionDisplayOrderRequest(BaseModel):
    items: list[InstitutionDisplayOrderItem] = Field(
        ..., description="표시 순서 변경 항목"
    )


class DisplayOrderUpdateResponseData(BaseModel):
    updated_count: int = Field(..., description="갱신된 건수", examples=[3])


class DisplayOrderUpdateResponse(ApiResponse[DisplayOrderUpdateResponseData]):
    pass


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------


class CreateProductRequest(BaseModel):
    product_name: str = Field(..., description="상품명", examples=["KOSPI ETF"])
    asset_class: str = Field(..., description="자산군", examples=["주식"])
    region: str = Field(..., description="지역", examples=["대한민국"])
    currency: str = Field(..., description="통화", examples=["KRW", "USD"])
    investment_type: str = Field(..., description="투자유형", examples=["ETF", "직접"])
    characteristics: list[str] | None = Field(None, description="특성 태그")
    risk_level: str = Field(..., description="위험도", examples=["안전", "위험"])
    display_order: int = Field(0, description="표시 순서", examples=[0])


class UpdateProductRequest(BaseModel):
    product_name: str = Field(..., description="상품명", examples=["KOSPI ETF"])
    asset_class: str = Field(..., description="자산군", examples=["주식"])
    region: str = Field(..., description="지역", examples=["대한민국"])
    currency: str = Field(..., description="통화", examples=["KRW", "USD"])
    investment_type: str = Field(..., description="투자유형", examples=["ETF", "직접"])
    characteristics: list[str] | None = Field(None, description="특성 태그")
    risk_level: str = Field(..., description="위험도", examples=["안전", "위험"])


class ProductResponseData(BaseModel):
    product_id: int | None = Field(None, description="상품 ID", examples=[10])
    product_name: str = Field(..., description="상품명")
    asset_class: str = Field(..., description="자산군")
    region: str = Field(..., description="지역")
    currency: str = Field(..., description="통화")
    investment_type: str = Field(..., description="투자유형")
    characteristics: list[str] | None = Field(None, description="특성 태그")
    risk_level: str = Field(..., description="위험도")
    display_order: int = Field(0, description="표시 순서")
    created_at: str = Field(..., description="생성 시각")


class ProductResponse(ApiResponse[ProductResponseData]):
    pass


class ProductDisplayOrderItem(BaseModel):
    product_id: int = Field(..., description="상품 ID", examples=[10])
    display_order: int = Field(..., description="표시 순서", examples=[1])


class UpdateProductDisplayOrderRequest(BaseModel):
    items: list[ProductDisplayOrderItem] = Field(..., description="표시 순서 변경 항목")


# ---------------------------------------------------------------------------
# Accounts
# ---------------------------------------------------------------------------


class CreateAccountRequest(BaseModel):
    institution_id: int = Field(..., description="기관 ID", examples=[1])
    name: str = Field(..., description="계좌명", examples=["위탁계좌-1"])
    type: str = Field(
        ...,
        description="계좌유형",
        examples=[
            "위탁계좌",
            "연금계좌",
            "ISA계좌",
            "예금계좌",
            "금현물계좌",
            "CMA",
            "기타계좌",
        ],
    )
    display_order: int = Field(0, description="표시 순서", examples=[0])


class UpdateAccountRequest(BaseModel):
    name: str = Field(..., description="계좌명", examples=["위탁계좌-1"])
    type: str = Field(
        ...,
        description="계좌유형",
        examples=[
            "위탁계좌",
            "연금계좌",
            "ISA계좌",
            "예금계좌",
            "금현물계좌",
            "CMA",
            "기타계좌",
        ],
    )
    display_order: int = Field(0, description="표시 순서", examples=[0])


class AccountResponseData(BaseModel):
    account_id: int | None = Field(None, description="계좌 ID", examples=[3])
    institution_id: int = Field(..., description="기관 ID", examples=[1])
    name: str = Field(..., description="계좌명")
    type: str = Field(..., description="계좌유형")
    display_order: int = Field(0, description="표시 순서", examples=[0])
    created_at: str = Field(..., description="생성 시각")


class AccountResponse(ApiResponse[AccountResponseData]):
    pass


class AccountDisplayOrderItem(BaseModel):
    account_id: int = Field(..., description="계좌 ID", examples=[3])
    display_order: int = Field(..., description="표시 순서", examples=[1])


class UpdateAccountDisplayOrderRequest(BaseModel):
    items: list[AccountDisplayOrderItem] = Field(..., description="표시 순서 변경 항목")


class AccountGroupDisplayOrderItem(BaseModel):
    account_group_id: int = Field(..., description="계좌 그룹 ID")
    display_order: int = Field(..., description="표시 순서")


class UpdateAccountGroupDisplayOrderRequest(BaseModel):
    items: list[AccountGroupDisplayOrderItem] = Field(
        ..., description="표시 순서 변경 항목"
    )


# ---------------------------------------------------------------------------
# Account Groups
# ---------------------------------------------------------------------------


class CreateAccountGroupRequest(BaseModel):
    name: str = Field(..., description="계좌 그룹명", examples=["국내증권"])
    account_ids: list[int] = Field(
        ..., description="그룹에 포함할 계좌 ID 목록", examples=[[1, 2, 3]]
    )
    include_in_weekly_report: bool = Field(
        False, description="주간 보고서에 포함", examples=[True]
    )


class UpdateAccountGroupRequest(BaseModel):
    name: str = Field(..., description="계좌 그룹명", examples=["미국 투자 계좌"])
    account_ids: list[int] = Field(
        ..., description="그룹에 포함할 계좌 ID 목록", examples=[[1, 4, 7]]
    )
    include_in_weekly_report: bool = Field(
        False, description="주간 보고서에 포함", examples=[False]
    )


class AccountGroupResponseData(BaseModel):
    account_group_id: int | None = Field(None, description="계좌 그룹 ID", examples=[5])
    name: str = Field(..., description="그룹명")
    account_ids: list[int] = Field(..., description="포함된 계좌 ID 목록")
    include_in_weekly_report: bool = Field(..., description="주간 보고서에 포함")
    display_order: int = Field(..., description="표시 순서")
    created_at: str = Field(..., description="생성 시각")


class AccountGroupResponse(ApiResponse[AccountGroupResponseData]):
    pass


class DeleteAccountGroupResponse(ApiResponse[dict[str, Any] | None]):
    pass


# ---------------------------------------------------------------------------
# Holdings
# ---------------------------------------------------------------------------


class CreateHoldingRequest(BaseModel):
    account_id: int = Field(..., description="계좌 ID", examples=[1])
    product_id: int = Field(..., description="상품 ID", examples=[10])


class HoldingResponseData(BaseModel):
    holding_id: int | None = Field(None, description="보유자산 ID", examples=[7])
    account_id: int = Field(..., description="계좌 ID")
    product_id: int = Field(..., description="상품 ID")
    is_visible: bool = Field(..., description="노출 여부")
    deletion_reason: str | None = Field(None, description="숨김/삭제 사유")
    deleted_at: str | None = Field(None, description="숨김/삭제 시각")
    created_at: str = Field(..., description="생성 시각")


class HoldingResponse(ApiResponse[HoldingResponseData]):
    pass


class DeleteHoldingRequest(BaseModel):
    action: Literal["hide", "hard_delete"] = Field(
        ..., description="삭제 동작", examples=["hide", "hard_delete"]
    )
    reason: str | None = Field(None, description="숨김 사유", examples=["중복"])


class DeleteHoldingResponse(ApiResponse[HoldingResponseData | None]):
    pass


# ---------------------------------------------------------------------------
# Snapshots
# ---------------------------------------------------------------------------


class CreateSnapshotRequest(BaseModel):
    user_id: int = Field(..., description="사용자 ID", examples=[1])
    reference_date: date = Field(..., description="기준 일자", examples=["2025-01-03"])


class SnapshotHoldingResponseData(BaseModel):
    snapshot_holding_id: int | None = Field(None, description="스냅샷 보유자산 ID")
    snapshot_id: int | None = Field(None, description="스냅샷 ID")
    holding_id: int = Field(..., description="보유자산 ID")
    valuation_amount: float = Field(..., description="평가 금액")
    data_source: str = Field(
        ..., description="데이터 출처", examples=["auto", "manual"]
    )
    created_at: str | None = Field(None, description="생성 시각")


class SnapshotResponseData(BaseModel):
    snapshot_id: int | None = Field(None, description="스냅샷 ID")
    user_id: int = Field(..., description="사용자 ID")
    reference_date: date = Field(..., description="기준 일자")
    status: str = Field(..., description="상태", examples=["in_progress", "locked"])
    locked_at: str | None = Field(None, description="잠금 시각")
    editable_until: str | None = Field(None, description="편집 가능 시각")
    created_at: str = Field(..., description="생성 시각")
    holdings: list[SnapshotHoldingResponseData] = Field(
        default_factory=list, description="스냅샷 보유자산"
    )


class SnapshotResponse(ApiResponse[SnapshotResponseData]):
    pass


class UpsertSnapshotHoldingRequest(BaseModel):
    valuation_amount: float = Field(..., description="평가 금액")
    data_source: str = Field(..., description="데이터 출처", examples=["auto"])


class SnapshotHoldingResponse(ApiResponse[SnapshotHoldingResponseData]):
    pass


class LockSnapshotResponse(ApiResponse[dict[str, Any] | None]):
    pass


class UnlockSnapshotResponse(ApiResponse[dict[str, Any] | None]):
    pass


class CreateWeeklySnapshotRequest(BaseModel):
    user_id: int = Field(..., description="사용자 ID", examples=[1])
    reference_date: date = Field(
        ..., description="주간 기준일", examples=["2025-01-10"]
    )
    source_snapshot_id: int = Field(..., description="소스 스냅샷 ID", examples=[11])


class WeeklySnapshotResponseData(BaseModel):
    weekly_snapshot_id: int = Field(..., description="주간 스냅샷 ID")


class WeeklySnapshotResponse(ApiResponse[WeeklySnapshotResponseData]):
    pass


class WeeklySnapshotListItem(BaseModel):
    weekly_snapshot_id: int = Field(..., description="주간 스냅샷 ID")
    user_id: int = Field(..., description="사용자 ID")
    reference_date: date = Field(..., description="주간 기준일")
    source_snapshot_id: int = Field(..., description="소스 스냅샷 ID")
    status: str = Field(..., description="상태", examples=["in_progress", "locked"])
    editable_until: str | None = Field(None, description="편집 가능 시각")
    created_at: str = Field(..., description="생성 시각")


class CreateAnnualSnapshotRequest(BaseModel):
    user_id: int = Field(..., description="사용자 ID", examples=[1])
    reference_date: date = Field(
        ..., description="연간 기준일", examples=["2025-12-31"]
    )
    source_snapshot_id: int = Field(..., description="소스 스냅샷 ID", examples=[11])


class AnnualSnapshotResponseData(BaseModel):
    annual_snapshot_id: int = Field(..., description="연간 스냅샷 ID")


class AnnualSnapshotResponse(ApiResponse[AnnualSnapshotResponseData]):
    pass


class AnnualSnapshotListItem(BaseModel):
    annual_snapshot_id: int = Field(..., description="연간 스냅샷 ID")
    user_id: int = Field(..., description="사용자 ID")
    reference_date: date = Field(..., description="연간 기준일")
    source_snapshot_id: int = Field(..., description="소스 스냅샷 ID")
    status: str = Field(..., description="상태", examples=["locked"])
    editable_until: str | None = Field(None, description="편집 가능 시각")
    created_at: str = Field(..., description="생성 시각")


class AnnualSnapshotHoldingListItem(BaseModel):
    annual_snapshot_holding_id: int = Field(..., description="연간 스냅샷 보유자산 ID")
    annual_snapshot_id: int = Field(..., description="연간 스냅샷 ID")
    holding_id: int = Field(..., description="보유자산 ID")
    valuation_amount: float = Field(..., description="평가 금액")
    data_source: str = Field(..., description="데이터 출처", examples=["manual"])
    created_at: str | None = Field(None, description="생성 시각")
    institution_id: int = Field(..., description="기관 ID")
    institution_name: str = Field(..., description="기관명")
    institution_display_order: int = Field(..., description="기관 표시순서")
    account_id: int = Field(..., description="계좌 ID")
    account_name: str = Field(..., description="계좌명")
    account_display_order: int = Field(..., description="계좌 표시순서")
    product_id: int = Field(..., description="상품 ID")
    product_name: str = Field(..., description="상품명")
    product_display_order: int = Field(..., description="상품 표시순서")


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


class WeeklyAccountReportItem(BaseModel):
    reference_date: date
    institution_name: str
    account_id: int
    account_name: str
    total_valuation: float


class WeeklyAccountReportData(BaseModel):
    items: list[WeeklyAccountReportItem]
    total_amount: float | None = None


class WeeklyAccountReportResponse(ApiResponse[WeeklyAccountReportData]):
    pass


class AnnualAccountReportItem(BaseModel):
    year: int
    reference_date: date
    institution_name: str
    institution_display_order: int
    account_id: int
    account_name: str
    account_display_order: int
    total_valuation: float


class AnnualAccountReportData(BaseModel):
    items: list[AnnualAccountReportItem]
    total_amount: float | None = None


class AnnualAccountReportResponse(ApiResponse[AnnualAccountReportData]):
    pass


class WeeklyAccountGroupReportItem(BaseModel):
    reference_date: date
    account_group_name: str
    account_id: int
    account_name: str
    valuation: float
    group_total: float


class WeeklyAccountGroupReportData(BaseModel):
    items: list[WeeklyAccountGroupReportItem]
    total_amount: float | None = None


class WeeklyAccountGroupReportResponse(ApiResponse[WeeklyAccountGroupReportData]):
    pass


class AnnualAccountGroupReportItem(BaseModel):
    year: int
    reference_date: date
    account_group_name: str
    account_id: int
    account_name: str
    valuation: float
    group_total: float


class AnnualAccountGroupReportData(BaseModel):
    items: list[AnnualAccountGroupReportItem]
    total_amount: float | None = None


class AnnualAccountGroupReportResponse(ApiResponse[AnnualAccountGroupReportData]):
    pass


class AssetClassReportItem(BaseModel):
    asset_class: str
    product_name: str
    valuation_amount: float
    subtotal: float


class AssetClassReportData(BaseModel):
    items: list[AssetClassReportItem]
    total_amount: float | None = None


class AssetClassReportResponse(ApiResponse[AssetClassReportData]):
    pass


# Weekly Pivot Report
class WeeklyPivotWeekInfo(BaseModel):
    weekly_snapshot_id: int
    reference_date: date
    week_number: int


class WeeklyPivotAccountValuation(BaseModel):
    weekly_snapshot_id: int
    amount: float


class WeeklyPivotAccountRow(BaseModel):
    account_id: int
    account_name: str
    institution_name: str
    valuations: list[WeeklyPivotAccountValuation]


class WeeklyPivotAccountGroupRow(BaseModel):
    account_group_id: int
    account_group_name: str
    display_order: int
    valuations: list[WeeklyPivotAccountValuation]


class WeeklyPivotReportData(BaseModel):
    year: int
    weeks: list[WeeklyPivotWeekInfo]
    account_groups: list[WeeklyPivotAccountGroupRow]
    accounts: list[WeeklyPivotAccountRow]


class WeeklyPivotReportResponse(ApiResponse[WeeklyPivotReportData]):
    pass
