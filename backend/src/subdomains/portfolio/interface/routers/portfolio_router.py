"""Portfolio API Router."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Path, Query, status

from core.common_responses import common_responses
from dependencies import get_portfolio_app_service
from subdomains.portfolio.application.dtos import (
    CreateInstitutionCommand,
    UpdateInstitutionCommand,
    UpdateInstitutionDisplayOrdersCommand,
    InstitutionDisplayOrderItem,
    CreateProductCommand,
    UpdateProductCommand,
    UpdateProductDisplayOrdersCommand,
    ProductDisplayOrderItem,
    CreateAccountCommand,
    UpdateAccountCommand,
    UpdateAccountDisplayOrdersCommand,
    AccountDisplayOrderItem,
    CreateAccountGroupCommand,
    CreateHoldingCommand,
    DeleteHoldingCommand,
    CreateSnapshotCommand,
    UpsertSnapshotHoldingCommand,
    LockSnapshotCommand,
    CreateWeeklySnapshotCommand,
    CreateAnnualSnapshotCommand,
    WeeklyAccountReportQuery,
    AnnualAccountReportQuery,
    WeeklyAccountGroupReportQuery,
    AssetClassReportQuery,
)
from subdomains.portfolio.application.services import PortfolioAppService
from subdomains.portfolio.interface.schemas import (
    CreateInstitutionRequest,
    UpdateInstitutionRequest,
    UpdateInstitutionDisplayOrderRequest,
    InstitutionResponse,
    InstitutionResponseData,
    InstitutionsResponse,
    InstitutionsResponseData,
    DisplayOrderUpdateResponse,
    DisplayOrderUpdateResponseData,
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
    ProductResponseData,
    UpdateProductDisplayOrderRequest,
    CreateAccountRequest,
    AccountResponse,
    AccountResponseData,
    UpdateAccountRequest,
    UpdateAccountDisplayOrderRequest,
    CreateAccountGroupRequest,
    AccountGroupResponse,
    AccountGroupResponseData,
    CreateHoldingRequest,
    HoldingResponse,
    HoldingResponseData,
    DeleteHoldingRequest,
    DeleteHoldingResponse,
    CreateSnapshotRequest,
    SnapshotResponse,
    SnapshotResponseData,
    SnapshotHoldingResponse,
    SnapshotHoldingResponseData,
    UpsertSnapshotHoldingRequest,
    LockSnapshotResponse,
    CreateWeeklySnapshotRequest,
    WeeklySnapshotResponse,
    WeeklySnapshotResponseData,
    CreateAnnualSnapshotRequest,
    AnnualSnapshotResponse,
    AnnualSnapshotResponseData,
    WeeklyAccountReportResponse,
    WeeklyAccountReportData,
    WeeklyAccountReportItem,
    AnnualAccountReportResponse,
    AnnualAccountReportData,
    AnnualAccountReportItem,
    WeeklyAccountGroupReportResponse,
    WeeklyAccountGroupReportData,
    WeeklyAccountGroupReportItem,
    AssetClassReportResponse,
    AssetClassReportData,
    AssetClassReportItem,
)

router = APIRouter(
    tags=["portfolio"],
    responses={
        400: {"description": "Bad request"},
        500: {"description": "Server error"},
    },
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _iso(dt) -> str | None:
    if dt is None:
        return None
    if hasattr(dt, "isoformat"):
        return dt.isoformat()
    return str(dt)


# ---------------------------------------------------------------------------
# Institutions
# ---------------------------------------------------------------------------


@router.get(
    "/institutions",
    response_model=InstitutionsResponse,
    summary="기관 목록 조회",
    responses={**common_responses},
)
async def list_institutions(
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> InstitutionsResponse:
    """모든 금융기관 목록 조회"""
    results = await service.list_institutions()
    items = [
        InstitutionResponseData(
            institution_id=r.institution_id,
            name=r.name,
            type=r.type,
            display_order=r.display_order,
            created_at=_iso(r.created_at),
        )
        for r in results
    ]
    max_display_order = max(
        (r.display_order or 0 for r in results),
        default=0,
    )
    data = InstitutionsResponseData(
        items=items,
        max_display_order=max_display_order,
    )
    return InstitutionsResponse(code=0, message="success", data=data)


@router.post(
    "/institutions",
    response_model=InstitutionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="기관 생성",
    responses={**common_responses},
)
async def create_institution(
    request: CreateInstitutionRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> InstitutionResponse:
    cmd = CreateInstitutionCommand(
        name=request.name,
        type=request.type,
        display_order=request.display_order,
    )
    result = await service.create_institution(cmd)
    data = InstitutionResponseData(
        institution_id=result.institution_id,
        name=result.name,
        type=result.type,
        display_order=result.display_order,
        created_at=_iso(result.created_at),
    )
    return InstitutionResponse(code=0, message="success", data=data)


@router.put(
    "/institutions/{institution_id}",
    response_model=InstitutionResponse,
    status_code=status.HTTP_200_OK,
    summary="기관 수정",
    responses={**common_responses},
)
async def update_institution(
    request: UpdateInstitutionRequest,
    institution_id: int = Path(..., description="기관 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> InstitutionResponse:
    cmd = UpdateInstitutionCommand(
        institution_id=institution_id,
        name=request.name,
        type=request.type,
        display_order=request.display_order,
    )
    result = await service.update_institution(cmd)
    data = InstitutionResponseData(
        institution_id=result.institution_id,
        name=result.name,
        type=result.type,
        display_order=result.display_order,
        created_at=_iso(result.created_at),
    )
    return InstitutionResponse(code=0, message="success", data=data)


@router.post(
    "/institutions:reorder",
    response_model=DisplayOrderUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="기관 표시순서 일괄 변경",
    responses={**common_responses},
)
async def update_institution_display_order(
    request: UpdateInstitutionDisplayOrderRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DisplayOrderUpdateResponse:
    cmd = UpdateInstitutionDisplayOrdersCommand(
        items=[
            InstitutionDisplayOrderItem(
                institution_id=item.institution_id,
                display_order=item.display_order,
            )
            for item in request.items
        ]
    )
    updated_count = await service.update_institution_display_orders(cmd)
    data = DisplayOrderUpdateResponseData(updated_count=updated_count)
    return DisplayOrderUpdateResponse(code=0, message="success", data=data)


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------


@router.get(
    "/products",
    response_model=list[ProductResponseData],
    summary="상품 목록 조회",
    responses={**common_responses},
)
async def list_products(
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> list[ProductResponseData]:
    """모든 상품 목록 조회"""
    results = await service.list_products()
    return [
        ProductResponseData(
            product_id=r.product_id,
            product_name=r.product_name,
            asset_class=r.asset_class,
            region=r.region,
            currency=r.currency,
            investment_type=r.investment_type,
            risk_level=r.risk_level,
            characteristics=r.characteristics,
            display_order=r.display_order,
            created_at=_iso(r.created_at),
        )
        for r in results
    ]


@router.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="상품 생성",
    responses={**common_responses},
)
async def create_product(
    request: CreateProductRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> ProductResponse:
    cmd = CreateProductCommand(
        product_name=request.product_name,
        asset_class=request.asset_class,
        region=request.region,
        currency=request.currency,
        investment_type=request.investment_type,
        characteristics=request.characteristics,
        risk_level=request.risk_level,
        display_order=request.display_order,
    )
    result = await service.create_product(cmd)
    data = ProductResponseData(
        product_id=result.product_id,
        product_name=result.product_name,
        asset_class=result.asset_class,
        region=result.region,
        currency=result.currency,
        investment_type=result.investment_type,
        characteristics=result.characteristics,
        risk_level=result.risk_level,
        display_order=result.display_order,
        created_at=_iso(result.created_at),
    )
    return ProductResponse(code=0, message="success", data=data)


@router.put(
    "/products/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="상품 수정",
    responses={**common_responses},
)
async def update_product(
    request: UpdateProductRequest,
    product_id: int = Path(..., description="상품 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> ProductResponse:
    cmd = UpdateProductCommand(
        product_id=product_id,
        product_name=request.product_name,
        asset_class=request.asset_class,
        region=request.region,
        currency=request.currency,
        investment_type=request.investment_type,
        characteristics=request.characteristics,
        risk_level=request.risk_level,
    )
    result = await service.update_product(cmd)
    data = ProductResponseData(
        product_id=result.product_id,
        product_name=result.product_name,
        asset_class=result.asset_class,
        region=result.region,
        currency=result.currency,
        investment_type=result.investment_type,
        characteristics=result.characteristics,
        risk_level=result.risk_level,
        display_order=result.display_order,
        created_at=_iso(result.created_at),
    )
    return ProductResponse(code=0, message="success", data=data)


@router.post(
    "/products:reorder",
    response_model=DisplayOrderUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="상품 표시순서 일괄 변경",
    responses={**common_responses},
)
async def update_product_display_order(
    request: UpdateProductDisplayOrderRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DisplayOrderUpdateResponse:
    cmd = UpdateProductDisplayOrdersCommand(
        items=[
            ProductDisplayOrderItem(
                product_id=item.product_id,
                display_order=item.display_order,
            )
            for item in request.items
        ]
    )
    updated_count = await service.update_product_display_orders(cmd)
    data = DisplayOrderUpdateResponseData(updated_count=updated_count)
    return DisplayOrderUpdateResponse(code=0, message="success", data=data)


# ---------------------------------------------------------------------------
# Accounts
# ---------------------------------------------------------------------------


@router.get(
    "/accounts",
    response_model=list[AccountResponseData],
    summary="계좌 목록 조회",
    responses={**common_responses},
)
async def list_accounts(
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> list[AccountResponseData]:
    """모든 계좌 목록 조회"""
    results = await service.list_accounts()
    return [
        AccountResponseData(
            account_id=r.account_id,
            institution_id=r.institution_id,
            name=r.name,
            type=r.type,
            display_order=r.display_order,
            created_at=_iso(r.created_at),
        )
        for r in results
    ]


@router.post(
    "/accounts",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="계좌 생성",
    responses={**common_responses},
)
async def create_account(
    request: CreateAccountRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> AccountResponse:
    cmd = CreateAccountCommand(
        institution_id=request.institution_id,
        name=request.name,
        type=request.type,
        display_order=request.display_order,
    )
    result = await service.create_account(cmd)
    data = AccountResponseData(
        account_id=result.account_id,
        institution_id=result.institution_id,
        name=result.name,
        type=result.type,
        display_order=result.display_order,
        created_at=_iso(result.created_at),
    )
    return AccountResponse(code=0, message="success", data=data)


@router.put(
    "/accounts/{account_id}",
    response_model=AccountResponse,
    status_code=status.HTTP_200_OK,
    summary="계좌 수정",
    responses={**common_responses},
)
async def update_account(
    request: UpdateAccountRequest,
    account_id: int = Path(..., description="계좌 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> AccountResponse:
    cmd = UpdateAccountCommand(
        account_id=account_id,
        name=request.name,
        type=request.type,
        display_order=request.display_order,
    )
    result = await service.update_account(cmd)
    data = AccountResponseData(
        account_id=result.account_id,
        institution_id=result.institution_id,
        name=result.name,
        type=result.type,
        display_order=result.display_order,
        created_at=_iso(result.created_at),
    )
    return AccountResponse(code=0, message="success", data=data)


@router.post(
    "/accounts:reorder",
    response_model=DisplayOrderUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="계좌 표시순서 일괄 변경",
    responses={**common_responses},
)
async def update_account_display_order(
    request: UpdateAccountDisplayOrderRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DisplayOrderUpdateResponse:
    cmd = UpdateAccountDisplayOrdersCommand(
        items=[
            AccountDisplayOrderItem(
                account_id=item.account_id,
                display_order=item.display_order,
            )
            for item in request.items
        ]
    )
    updated_count = await service.update_account_display_orders(cmd)
    data = DisplayOrderUpdateResponseData(updated_count=updated_count)
    return DisplayOrderUpdateResponse(code=0, message="success", data=data)


# ---------------------------------------------------------------------------
# Account Groups
# ---------------------------------------------------------------------------


@router.post(
    "/account-groups",
    response_model=AccountGroupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="계좌 그룹 생성",
    responses={**common_responses},
)
async def create_account_group(
    request: CreateAccountGroupRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> AccountGroupResponse:
    cmd = CreateAccountGroupCommand(name=request.name, account_ids=request.account_ids)
    result = await service.create_account_group(cmd)
    data = AccountGroupResponseData(
        account_group_id=result.account_group_id,
        name=result.name,
        account_ids=result.account_ids,
        created_at=_iso(result.created_at),
    )
    return AccountGroupResponse(code=0, message="success", data=data)


# ---------------------------------------------------------------------------
# Holdings
# ---------------------------------------------------------------------------


@router.get(
    "/holdings",
    response_model=list[HoldingResponseData],
    summary="보유자산 목록 조회",
    responses={**common_responses},
)
async def list_holdings(
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> list[HoldingResponseData]:
    """모든 보유자산 목록 조회"""
    results = await service.list_holdings()
    return [
        HoldingResponseData(
            holding_id=r.holding_id,
            account_id=r.account_id,
            product_id=r.product_id,
            is_visible=r.is_visible,
            deletion_reason=r.deletion_reason,
            deleted_at=_iso(r.deleted_at),
            created_at=_iso(r.created_at),
        )
        for r in results
    ]


@router.post(
    "/holdings",
    response_model=HoldingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="보유자산 생성",
    responses={**common_responses},
)
async def create_holding(
    request: CreateHoldingRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> HoldingResponse:
    cmd = CreateHoldingCommand(
        account_id=request.account_id,
        product_id=request.product_id,
    )
    result = await service.create_holding(cmd)
    data = HoldingResponseData(
        holding_id=result.holding_id,
        account_id=result.account_id,
        product_id=result.product_id,
        is_visible=result.is_visible,
        deletion_reason=result.deletion_reason,
        deleted_at=_iso(result.deleted_at),
        created_at=_iso(result.created_at),
    )
    return HoldingResponse(code=0, message="success", data=data)


@router.delete(
    "/holdings/{holding_id}",
    response_model=DeleteHoldingResponse,
    status_code=status.HTTP_200_OK,
    summary="보유자산 삭제/숨김",
    responses={**common_responses},
)
async def delete_holding(
    request: DeleteHoldingRequest,
    holding_id: int = Path(..., description="보유자산 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DeleteHoldingResponse:
    cmd = DeleteHoldingCommand(
        holding_id=holding_id, action=request.action, reason=request.reason
    )
    result = await service.delete_holding(cmd)
    if result is None:
        return DeleteHoldingResponse(code=0, message="Holding hard deleted", data=None)
    data = HoldingResponseData(
        holding_id=result.holding_id,
        account_id=result.account_id,
        product_id=result.product_id,
        is_visible=result.is_visible,
        deletion_reason=result.deletion_reason,
        deleted_at=_iso(result.deleted_at),
        created_at=_iso(result.created_at),
    )
    return DeleteHoldingResponse(code=0, message="Holding hidden", data=data)


# ---------------------------------------------------------------------------
# Snapshots
# ---------------------------------------------------------------------------


@router.get(
    "/snapshots",
    response_model=list[SnapshotResponseData],
    summary="스냅샷 목록 조회",
    responses={**common_responses},
)
async def list_snapshots(
    user_id: int = 1,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> list[SnapshotResponseData]:
    """사용자의 스냅샷 목록 조회"""
    results = await service.list_snapshots(user_id)
    return [
        SnapshotResponseData(
            snapshot_id=r.snapshot_id,
            user_id=r.user_id,
            reference_date=r.reference_date.isoformat() if r.reference_date else None,
            status=r.status,
            locked_at=_iso(r.locked_at),
            editable_until=_iso(r.editable_until),
            created_at=_iso(r.created_at),
        )
        for r in results
    ]


@router.post(
    "/snapshots",
    response_model=SnapshotResponse,
    status_code=status.HTTP_201_CREATED,
    summary="스냅샷 생성",
    responses={**common_responses},
)
async def create_snapshot(
    request: CreateSnapshotRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> SnapshotResponse:
    cmd = CreateSnapshotCommand(
        user_id=request.user_id, reference_date=request.reference_date
    )
    result = await service.create_snapshot(cmd)
    data = SnapshotResponseData(
        snapshot_id=result.snapshot_id,
        user_id=result.user_id,
        reference_date=result.reference_date,
        status=result.status,
        locked_at=_iso(result.locked_at),
        editable_until=_iso(result.editable_until),
        created_at=_iso(result.created_at),
        holdings=[
            SnapshotHoldingResponseData(
                holding_id=h.holding_id,
                valuation_amount=h.valuation_amount,
                data_source=h.data_source,
            )
            for h in result.holdings
        ],
    )
    return SnapshotResponse(code=0, message="success", data=data)


@router.post(
    "/snapshots/{snapshot_id}/holdings/{holding_id}",
    response_model=SnapshotHoldingResponse,
    status_code=status.HTTP_200_OK,
    summary="스냅샷 보유자산 업서트",
    responses={**common_responses},
)
async def upsert_snapshot_holding(
    request: UpsertSnapshotHoldingRequest,
    snapshot_id: int = Path(..., description="스냅샷 ID"),
    holding_id: int = Path(..., description="보유자산 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> SnapshotHoldingResponse:
    cmd = UpsertSnapshotHoldingCommand(
        snapshot_id=snapshot_id,
        holding_id=holding_id,
        valuation_amount=request.valuation_amount,
        data_source=request.data_source,
    )
    result = await service.upsert_snapshot_holding(cmd)
    data = SnapshotHoldingResponseData(
        holding_id=result.holding_id,
        valuation_amount=result.valuation_amount,
        data_source=result.data_source,
    )
    return SnapshotHoldingResponse(code=0, message="success", data=data)


@router.post(
    "/snapshots/{snapshot_id}/lock",
    response_model=LockSnapshotResponse,
    status_code=status.HTTP_200_OK,
    summary="스냅샷 잠금",
    responses={**common_responses},
)
async def lock_snapshot(
    snapshot_id: int = Path(..., description="스냅샷 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> LockSnapshotResponse:
    cmd = LockSnapshotCommand(snapshot_id=snapshot_id)
    await service.lock_snapshot(cmd)
    return LockSnapshotResponse(code=0, message="locked", data=None)


# ---------------------------------------------------------------------------
# Weekly / Annual Snapshots
# ---------------------------------------------------------------------------


@router.post(
    "/weekly-snapshots",
    response_model=WeeklySnapshotResponse,
    status_code=status.HTTP_201_CREATED,
    summary="주간 스냅샷 생성",
    responses={**common_responses},
)
async def create_weekly_snapshot(
    request: CreateWeeklySnapshotRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> WeeklySnapshotResponse:
    cmd = CreateWeeklySnapshotCommand(
        user_id=request.user_id,
        reference_date=request.reference_date,
        source_snapshot_id=request.source_snapshot_id,
    )
    weekly_id = await service.create_weekly_snapshot(cmd)
    data = WeeklySnapshotResponseData(weekly_snapshot_id=weekly_id)
    return WeeklySnapshotResponse(code=0, message="success", data=data)


@router.post(
    "/annual-snapshots",
    response_model=AnnualSnapshotResponse,
    status_code=status.HTTP_201_CREATED,
    summary="연간 스냅샷 생성",
    responses={**common_responses},
)
async def create_annual_snapshot(
    request: CreateAnnualSnapshotRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> AnnualSnapshotResponse:
    cmd = CreateAnnualSnapshotCommand(
        user_id=request.user_id,
        reference_date=request.reference_date,
        source_snapshot_id=request.source_snapshot_id,
    )
    annual_id = await service.create_annual_snapshot(cmd)
    data = AnnualSnapshotResponseData(annual_snapshot_id=annual_id)
    return AnnualSnapshotResponse(code=0, message="success", data=data)


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------


@router.get(
    "/reports/weekly/accounts",
    response_model=WeeklyAccountReportResponse,
    summary="주간 계좌별 리포트",
    responses={**common_responses},
)
async def weekly_account_report(
    user_id: int = Query(..., description="사용자 ID"),
    start_date: date | None = Query(None, description="시작일"),
    end_date: date | None = Query(None, description="종료일"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> WeeklyAccountReportResponse:
    query = WeeklyAccountReportQuery(
        user_id=user_id, start_date=start_date, end_date=end_date
    )
    result = await service.weekly_account_report(query)
    items = [
        WeeklyAccountReportItem(
            reference_date=item.data.get("reference_date"),
            institution_name=item.data.get("institution_name"),
            account_id=item.data.get("account_id"),
            account_name=item.data.get("account_name"),
            total_valuation=float(item.data.get("total_valuation", 0) or 0),
        )
        for item in result.items
    ]
    data = WeeklyAccountReportData(items=items, total_amount=result.total_amount)
    return WeeklyAccountReportResponse(code=0, message="success", data=data)


@router.get(
    "/reports/annual/accounts",
    response_model=AnnualAccountReportResponse,
    summary="연간 계좌별 리포트",
    responses={**common_responses},
)
async def annual_account_report(
    user_id: int = Query(..., description="사용자 ID"),
    year: int | None = Query(None, description="연도 (옵션)"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> AnnualAccountReportResponse:
    query = AnnualAccountReportQuery(user_id=user_id, year=year)
    result = await service.annual_account_report(query)
    items = [
        AnnualAccountReportItem(
            year=(
                int(item.data.get("year"))
                if item.data.get("year") is not None
                else year or 0
            ),
            reference_date=item.data.get("reference_date"),
            institution_name=item.data.get("institution_name"),
            account_id=item.data.get("account_id"),
            account_name=item.data.get("account_name"),
            total_valuation=float(item.data.get("total_valuation", 0) or 0),
        )
        for item in result.items
    ]
    data = AnnualAccountReportData(items=items, total_amount=result.total_amount)
    return AnnualAccountReportResponse(code=0, message="success", data=data)


@router.get(
    "/reports/weekly/account-groups",
    response_model=WeeklyAccountGroupReportResponse,
    summary="주간 계좌그룹 리포트",
    responses={**common_responses},
)
async def weekly_account_group_report(
    user_id: int = Query(..., description="사용자 ID"),
    start_date: date | None = Query(None, description="시작일"),
    end_date: date | None = Query(None, description="종료일"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> WeeklyAccountGroupReportResponse:
    query = WeeklyAccountGroupReportQuery(
        user_id=user_id, start_date=start_date, end_date=end_date
    )
    result = await service.weekly_account_group_report(query)
    items = [
        WeeklyAccountGroupReportItem(
            reference_date=item.data.get("reference_date"),
            account_group_name=item.data.get("account_group_name"),
            account_id=item.data.get("account_id"),
            account_name=item.data.get("account_name"),
            valuation=float(item.data.get("valuation", 0) or 0),
            group_total=float(item.data.get("group_total", 0) or 0),
        )
        for item in result.items
    ]
    data = WeeklyAccountGroupReportData(items=items, total_amount=result.total_amount)
    return WeeklyAccountGroupReportResponse(code=0, message="success", data=data)


@router.get(
    "/reports/asset-class",
    response_model=AssetClassReportResponse,
    summary="자산군 리포트",
    responses={**common_responses},
)
async def asset_class_report(
    user_id: int = Query(..., description="사용자 ID"),
    snapshot_date: date = Query(..., description="스냅샷 기준일"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> AssetClassReportResponse:
    query = AssetClassReportQuery(user_id=user_id, snapshot_date=snapshot_date)
    result = await service.asset_class_report(query)
    items = [
        AssetClassReportItem(
            asset_class=item.data.get("asset_class"),
            product_name=item.data.get("product_name"),
            valuation_amount=float(item.data.get("valuation_amount", 0) or 0),
            subtotal=float(item.data.get("subtotal", 0) or 0),
        )
        for item in result.items
    ]
    data = AssetClassReportData(items=items, total_amount=result.total_amount)
    return AssetClassReportResponse(code=0, message="success", data=data)


# ---------------------------------------------------------------------------
# Snapshot Holdings
# ---------------------------------------------------------------------------


@router.get(
    "/snapshot-holdings",
    response_model=list[SnapshotHoldingResponseData],
    summary="스냅샷 보유자산 목록 조회",
    responses={**common_responses},
)
async def list_snapshot_holdings(
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> list[SnapshotHoldingResponseData]:
    """모든 스냅샷 보유자산 목록 조회"""
    results = await service.list_snapshot_holdings()
    return [
        SnapshotHoldingResponseData(
            snapshot_holding_id=r.snapshot_holding_id,
            snapshot_id=r.snapshot_id,
            holding_id=r.holding_id,
            valuation_amount=float(r.valuation_amount),
            data_source=r.data_source,
            created_at=_iso(r.created_at),
        )
        for r in results
    ]
