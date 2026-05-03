"""Portfolio API Router."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, Path, Query, status

from core.common_responses import common_responses
from dependencies import get_portfolio_app_service
from shared.schemas import ApiResponse
from subdomains.portfolio.application.dtos import (
    CreateInstitutionCommand,
    UpdateInstitutionCommand,
    DeleteInstitutionCommand,
    UpdateInstitutionDisplayOrdersCommand,
    InstitutionDisplayOrderItem,
    CreateProductCommand,
    UpdateProductCommand,
    DeleteProductCommand,
    UpdateProductDisplayOrdersCommand,
    ProductDisplayOrderItem,
    CreateAccountCommand,
    UpdateAccountCommand,
    DeleteAccountCommand,
    UpdateAccountDisplayOrdersCommand,
    AccountDisplayOrderItem,
    CreateAccountGroupCommand,
    UpdateAccountGroupCommand,
    DeleteAccountGroupCommand,
    UpdateAccountGroupDisplayOrdersCommand,
    AccountGroupDisplayOrderItem,
    CreateHoldingCommand,
    DeleteHoldingCommand,
    CreateSnapshotCommand,
    UpsertSnapshotHoldingCommand,
    LockSnapshotCommand,
    UnlockSnapshotCommand,
    CreateWeeklySnapshotCommand,
    CreateAnnualSnapshotCommand,
    WeeklyAccountReportQuery,
    AnnualAccountReportQuery,
    WeeklyAccountGroupReportQuery,
    AnnualAccountGroupReportQuery,
    AssetClassReportQuery,
    WeeklyPivotReportQuery,
    AnnualPivotReportQuery,
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
    DeleteInstitutionResponse,
    DisplayOrderUpdateResponse,
    DisplayOrderUpdateResponseData,
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
    ProductResponseData,
    ProductBetaCollectItem,
    ProductBetaCollectResponse,
    ProductBetaCollectResponseData,
    ProductTickerResolveResponse,
    ProductTickerResolveResponseData,
    DeleteProductResponse,
    UpdateProductDisplayOrderRequest,
    CreateAccountRequest,
    AccountResponse,
    AccountResponseData,
    DeleteAccountResponse,
    UpdateAccountRequest,
    UpdateAccountDisplayOrderRequest,
    CreateAccountGroupRequest,
    UpdateAccountGroupRequest,
    UpdateAccountGroupDisplayOrderRequest,
    AccountGroupResponse,
    AccountGroupResponseData,
    DeleteAccountGroupResponse,
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
    UnlockSnapshotResponse,
    CreateWeeklySnapshotRequest,
    WeeklySnapshotResponse,
    WeeklySnapshotResponseData,
    WeeklySnapshotListItem,
    CreateAnnualSnapshotRequest,
    AnnualSnapshotResponse,
    AnnualSnapshotResponseData,
    AnnualSnapshotListItem,
    AnnualSnapshotHoldingListItem,
    WeeklyAccountReportResponse,
    WeeklyAccountReportData,
    WeeklyAccountReportItem,
    AnnualAccountReportResponse,
    AnnualAccountReportData,
    AnnualAccountReportItem,
    WeeklyAccountGroupReportResponse,
    WeeklyAccountGroupReportData,
    WeeklyAccountGroupReportItem,
    AnnualAccountGroupReportResponse,
    AnnualAccountGroupReportData,
    AnnualAccountGroupReportItem,
    AssetClassReportResponse,
    AssetClassReportData,
    AssetClassReportItem,
    WeeklyPivotReportResponse,
    WeeklyPivotReportData,
    WeeklyPivotWeekInfo,
    WeeklyPivotAccountValuation,
    WeeklyPivotAccountRow,
    WeeklyPivotAccountGroupRow,
    AnnualMddItem as AnnualMddItemSchema,
    CreateTargetAllocationRequest,
    TargetAllocationSchema,
    TargetAllocationListResponse,
    TargetAllocationResponse,
    DeleteTargetAllocationResponse,
    CreateTargetAllocationAccountRequest,
    TargetAllocationAccountSchema,
    TargetAllocationAccountListResponse,
    TargetAllocationAccountResponse,
    CreateTargetAllocationTotalRequest,
    TargetAllocationTotalSchema,
    TargetAllocationTotalResponse,
    CreateTargetAllocationAssetClassRequest,
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


@router.delete(
    "/institutions/{institution_id}",
    response_model=DeleteInstitutionResponse,
    status_code=status.HTTP_200_OK,
    summary="기관 삭제",
    responses={**common_responses},
)
async def delete_institution(
    institution_id: int = Path(..., description="기관 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DeleteInstitutionResponse:
    cmd = DeleteInstitutionCommand(institution_id=institution_id)
    await service.delete_institution(cmd)
    return DeleteInstitutionResponse(code=0, message="success", data=None)


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
            allow_snapshot_input=r.allow_snapshot_input,
            ticker=r.ticker,
            domestic_beta=r.domestic_beta,
            global_beta=r.global_beta,
            beta_collected_at=_iso(r.beta_collected_at),
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
        allow_snapshot_input=request.allow_snapshot_input,
        ticker=request.ticker,
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
        allow_snapshot_input=result.allow_snapshot_input,
        ticker=result.ticker,
        domestic_beta=result.domestic_beta,
        global_beta=result.global_beta,
        beta_collected_at=_iso(result.beta_collected_at),
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
        allow_snapshot_input=request.allow_snapshot_input,
        ticker=request.ticker,
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
        allow_snapshot_input=result.allow_snapshot_input,
        ticker=result.ticker,
        domestic_beta=result.domestic_beta,
        global_beta=result.global_beta,
        beta_collected_at=_iso(result.beta_collected_at),
        display_order=result.display_order,
        created_at=_iso(result.created_at),
    )
    return ProductResponse(code=0, message="success", data=data)


@router.post(
    "/products/{product_id}/beta:collect",
    response_model=ProductBetaCollectResponse,
    status_code=status.HTTP_200_OK,
    summary="단일 상품 베타 수집",
    responses={**common_responses},
)
async def collect_product_beta(
    product_id: int = Path(..., description="상품 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> ProductBetaCollectResponse:
    result = await service.collect_product_beta(product_id)
    data = ProductBetaCollectResponseData(
        updated_count=1 if result.updated else 0,
        items=[
            ProductBetaCollectItem(
                product_id=result.product_id,
                product_name=result.product_name,
                domestic_beta=result.domestic_beta,
                global_beta=result.global_beta,
                beta_collected_at=_iso(result.beta_collected_at),
                message=result.message,
                updated=result.updated,
            )
        ],
    )
    return ProductBetaCollectResponse(code=0, message="success", data=data)


@router.post(
    "/products/beta:collect",
    response_model=ProductBetaCollectResponse,
    status_code=status.HTTP_200_OK,
    summary="전체 상품 베타 일괄 수집",
    responses={**common_responses},
)
async def collect_all_product_betas(
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> ProductBetaCollectResponse:
    result = await service.collect_all_product_betas()
    data = ProductBetaCollectResponseData(
        updated_count=result.updated_count,
        items=[
            ProductBetaCollectItem(
                product_id=item.product_id,
                product_name=item.product_name,
                domestic_beta=item.domestic_beta,
                global_beta=item.global_beta,
                beta_collected_at=_iso(item.beta_collected_at),
                message=item.message,
                updated=item.updated,
            )
            for item in result.items
        ],
    )
    return ProductBetaCollectResponse(code=0, message="success", data=data)


@router.post(
    "/products/{product_id}/ticker:resolve",
    response_model=ProductTickerResolveResponse,
    status_code=status.HTTP_200_OK,
    summary="단일 상품 티커 정정",
    responses={**common_responses},
)
async def resolve_product_ticker(
    product_id: int = Path(..., description="상품 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> ProductTickerResolveResponse:
    result = await service.resolve_product_ticker(product_id)
    data = ProductTickerResolveResponseData(
        product_id=result.product_id,
        old_ticker=result.old_ticker,
        new_ticker=result.new_ticker,
        message=result.message,
        updated=result.updated,
    )
    return ProductTickerResolveResponse(code=0, message="success", data=data)


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


@router.delete(
    "/products/{product_id}",
    response_model=DeleteProductResponse,
    status_code=status.HTTP_200_OK,
    summary="상품 삭제",
    responses={**common_responses},
)
async def delete_product(
    product_id: int = Path(..., description="상품 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DeleteProductResponse:
    cmd = DeleteProductCommand(product_id=product_id)
    await service.delete_product(cmd)
    return DeleteProductResponse(code=0, message="success", data=None)


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
            allow_snapshot_input=r.allow_snapshot_input,
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
        allow_snapshot_input=request.allow_snapshot_input,
        display_order=request.display_order,
    )
    result = await service.create_account(cmd)
    data = AccountResponseData(
        account_id=result.account_id,
        institution_id=result.institution_id,
        name=result.name,
        type=result.type,
        allow_snapshot_input=result.allow_snapshot_input,
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
        allow_snapshot_input=request.allow_snapshot_input,
        display_order=request.display_order,
    )
    result = await service.update_account(cmd)
    data = AccountResponseData(
        account_id=result.account_id,
        institution_id=result.institution_id,
        name=result.name,
        type=result.type,
        allow_snapshot_input=result.allow_snapshot_input,
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


@router.delete(
    "/accounts/{account_id}",
    response_model=DeleteAccountResponse,
    status_code=status.HTTP_200_OK,
    summary="계좌 삭제",
    responses={**common_responses},
)
async def delete_account(
    account_id: int = Path(..., description="계좌 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DeleteAccountResponse:
    cmd = DeleteAccountCommand(account_id=account_id)
    await service.delete_account(cmd)
    return DeleteAccountResponse(code=0, message="success", data=None)


# ---------------------------------------------------------------------------
# Account Groups
# ---------------------------------------------------------------------------


@router.get(
    "/account-groups",
    response_model=list[AccountGroupResponseData],
    summary="계좌 그룹 목록 조회",
    responses={**common_responses},
)
async def list_account_groups(
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> list[AccountGroupResponseData]:
    results = await service.list_account_groups()
    return [
        AccountGroupResponseData(
            account_group_id=result.account_group_id,
            name=result.name,
            account_ids=result.account_ids,
            include_in_report=result.include_in_report,
            display_order=result.display_order,
            created_at=_iso(result.created_at),
        )
        for result in results
    ]


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
    cmd = CreateAccountGroupCommand(
        name=request.name,
        account_ids=request.account_ids,
        include_in_report=request.include_in_report,
    )
    result = await service.create_account_group(cmd)
    data = AccountGroupResponseData(
        account_group_id=result.account_group_id,
        name=result.name,
        account_ids=result.account_ids,
        include_in_report=result.include_in_report,
        display_order=result.display_order,
        created_at=_iso(result.created_at),
    )
    return AccountGroupResponse(code=0, message="success", data=data)


@router.put(
    "/account-groups/{account_group_id}",
    response_model=AccountGroupResponse,
    summary="계좌 그룹 수정",
    responses={**common_responses},
)
async def update_account_group(
    request: UpdateAccountGroupRequest,
    account_group_id: int = Path(..., description="계좌 그룹 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> AccountGroupResponse:
    cmd = UpdateAccountGroupCommand(
        account_group_id=account_group_id,
        name=request.name,
        account_ids=request.account_ids,
        include_in_report=request.include_in_report,
    )
    result = await service.update_account_group(cmd)
    data = AccountGroupResponseData(
        account_group_id=result.account_group_id,
        name=result.name,
        account_ids=result.account_ids,
        include_in_report=result.include_in_report,
        display_order=result.display_order,
        created_at=_iso(result.created_at),
    )
    return AccountGroupResponse(code=0, message="success", data=data)


@router.delete(
    "/account-groups/{account_group_id}",
    response_model=DeleteAccountGroupResponse,
    summary="계좌 그룹 삭제",
    responses={**common_responses},
)
async def delete_account_group(
    account_group_id: int = Path(..., description="계좌 그룹 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DeleteAccountGroupResponse:
    cmd = DeleteAccountGroupCommand(account_group_id=account_group_id)
    await service.delete_account_group(cmd)
    return DeleteAccountGroupResponse(code=0, message="success", data=None)


@router.put(
    "/account-groups:reorder",
    response_model=DisplayOrderUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="계좌 그룹 표시순서 일괄 변경",
    responses={**common_responses},
)
async def update_account_group_display_order(
    request: UpdateAccountGroupDisplayOrderRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DisplayOrderUpdateResponse:
    cmd = UpdateAccountGroupDisplayOrdersCommand(
        items=[
            AccountGroupDisplayOrderItem(
                account_group_id=item.account_group_id,
                display_order=item.display_order,
            )
            for item in request.items
        ]
    )
    updated_count = await service.update_account_group_display_orders(cmd)
    data = DisplayOrderUpdateResponseData(updated_count=updated_count)
    return DisplayOrderUpdateResponse(code=0, message="success", data=data)


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


@router.post(
    "/snapshots/{snapshot_id}/unlock",
    response_model=UnlockSnapshotResponse,
    status_code=status.HTTP_200_OK,
    summary="스냅샷 잠금 해제",
    responses={**common_responses},
)
async def unlock_snapshot(
    snapshot_id: int = Path(..., description="스냅샷 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> UnlockSnapshotResponse:
    cmd = UnlockSnapshotCommand(snapshot_id=snapshot_id)
    await service.unlock_snapshot(cmd)
    return UnlockSnapshotResponse(code=0, message="unlocked", data=None)


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


@router.get(
    "/weekly-snapshots",
    response_model=list[WeeklySnapshotListItem],
    summary="주간 스냅샷 목록 조회",
    responses={**common_responses},
)
async def list_weekly_snapshots(
    user_id: int = 1,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> list[WeeklySnapshotListItem]:
    """사용자의 주간 스냅샷 목록 조회"""
    results = await service.list_weekly_snapshots(user_id)
    return [
        WeeklySnapshotListItem(
            weekly_snapshot_id=item.weekly_snapshot_id,
            user_id=item.user_id,
            reference_date=item.reference_date,
            source_snapshot_id=item.source_snapshot_id,
            status=item.status,
            editable_until=_iso(item.editable_until),
            created_at=_iso(item.created_at),
        )
        for item in results
    ]


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


@router.get(
    "/annual-snapshots",
    response_model=list[AnnualSnapshotListItem],
    summary="연간 스냅샷 목록 조회",
    responses={**common_responses},
)
async def list_annual_snapshots(
    user_id: int = 1,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> list[AnnualSnapshotListItem]:
    """사용자의 연간 스냅샷 목록 조회"""
    results = await service.list_annual_snapshots(user_id)
    return [
        AnnualSnapshotListItem(
            annual_snapshot_id=item.annual_snapshot_id,
            user_id=item.user_id,
            reference_date=item.reference_date,
            source_snapshot_id=item.source_snapshot_id,
            status=item.status,
            editable_until=_iso(item.editable_until),
            created_at=_iso(item.created_at),
        )
        for item in results
    ]


@router.get(
    "/annual-snapshot-holdings",
    response_model=list[AnnualSnapshotHoldingListItem],
    summary="연간 스냅샷 보유자산 목록 조회",
    responses={**common_responses},
)
async def list_annual_snapshot_holdings(
    annual_snapshot_id: int = Query(..., description="연간 스냅샷 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> list[AnnualSnapshotHoldingListItem]:
    """특정 연간 스냅샷의 보유자산 목록 조회"""
    result = await service.annual_snapshot_holdings_report(annual_snapshot_id)
    return [
        AnnualSnapshotHoldingListItem(
            annual_snapshot_holding_id=item.data.get("annual_snapshot_holding_id"),
            annual_snapshot_id=item.data.get("annual_snapshot_id"),
            holding_id=item.data.get("holding_id"),
            valuation_amount=float(item.data.get("valuation_amount", 0) or 0),
            data_source=item.data.get("data_source"),
            created_at=_iso(item.data.get("created_at")),
            institution_id=item.data.get("institution_id"),
            institution_name=item.data.get("institution_name"),
            institution_display_order=item.data.get("institution_display_order"),
            account_id=item.data.get("account_id"),
            account_name=item.data.get("account_name"),
            account_display_order=item.data.get("account_display_order"),
            product_id=item.data.get("product_id"),
            product_name=item.data.get("product_name"),
            product_display_order=item.data.get("product_display_order"),
        )
        for item in result.items
    ]


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
            institution_display_order=item.data.get("institution_display_order", 0),
            account_id=item.data.get("account_id"),
            account_name=item.data.get("account_name"),
            account_display_order=item.data.get("account_display_order", 0),
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
    "/reports/annual/account-groups",
    response_model=AnnualAccountGroupReportResponse,
    summary="연간 계좌그룹 리포트",
    responses={**common_responses},
)
async def annual_account_group_report(
    user_id: int = Query(..., description="사용자 ID"),
    year: int | None = Query(None, description="연도 (옵션)"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> AnnualAccountGroupReportResponse:
    query = AnnualAccountGroupReportQuery(user_id=user_id, year=year)
    result = await service.annual_account_group_report(query)
    items = [
        AnnualAccountGroupReportItem(
            year=(
                int(item.data.get("year"))
                if item.data.get("year") is not None
                else year or 0
            ),
            reference_date=item.data.get("reference_date"),
            account_group_name=item.data.get("account_group_name"),
            account_id=item.data.get("account_id"),
            account_name=item.data.get("account_name"),
            valuation=float(item.data.get("valuation", 0) or 0),
            group_total=float(item.data.get("group_total", 0) or 0),
        )
        for item in result.items
    ]
    data = AnnualAccountGroupReportData(items=items, total_amount=result.total_amount)
    return AnnualAccountGroupReportResponse(code=0, message="success", data=data)


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


@router.get(
    "/reports/weekly/pivot",
    response_model=WeeklyPivotReportResponse,
    summary="주간 Pivot 보고서 (연도별 계좌 평가액 비교)",
    responses={**common_responses},
)
async def weekly_pivot_report(
    user_id: int = Query(..., description="사용자 ID"),
    year: int = Query(..., description="연도"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> WeeklyPivotReportResponse:
    """연도별 주간 스냅샷을 열로, 계좌를 행으로 하는 Pivot 보고서"""
    query = WeeklyPivotReportQuery(user_id=user_id, year=year)
    result = await service.weekly_pivot_report(query)

    weeks = [
        WeeklyPivotWeekInfo(
            weekly_snapshot_id=w.weekly_snapshot_id,
            reference_date=w.reference_date,
            week_number=w.week_number,
        )
        for w in result.weeks
    ]

    account_groups = [
        WeeklyPivotAccountGroupRow(
            account_group_id=grp.account_group_id,
            account_group_name=grp.account_group_name,
            display_order=grp.display_order,
            valuations=[
                WeeklyPivotAccountValuation(
                    weekly_snapshot_id=val.weekly_snapshot_id, amount=val.amount
                )
                for val in grp.valuations
            ],
        )
        for grp in result.account_groups
    ]

    accounts = [
        WeeklyPivotAccountRow(
            account_id=acc.account_id,
            account_name=acc.account_name,
            institution_name=acc.institution_name,
            valuations=[
                WeeklyPivotAccountValuation(
                    weekly_snapshot_id=val.weekly_snapshot_id, amount=val.amount
                )
                for val in acc.valuations
            ],
        )
        for acc in result.accounts
    ]

    data = WeeklyPivotReportData(
        year=result.year, weeks=weeks, account_groups=account_groups, accounts=accounts
    )
    return WeeklyPivotReportResponse(code=0, message="success", data=data)


@router.get(
    "/reports/annual/pivot",
    response_model=WeeklyPivotReportResponse,
    summary="연간 Pivot 보고서 (모든 연간 스냅샷을 열로)",
    responses={**common_responses},
)
async def annual_pivot_report(
    user_id: int = Query(..., description="사용자 ID"),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> WeeklyPivotReportResponse:
    """모든 연간 스냅샷을 열로, 계좌를 행으로 하는 Pivot 보고서"""
    query = AnnualPivotReportQuery(user_id=user_id)
    result = await service.annual_pivot_report(query)

    weeks = [
        WeeklyPivotWeekInfo(
            weekly_snapshot_id=w.weekly_snapshot_id,
            reference_date=w.reference_date,
            week_number=w.week_number,
        )
        for w in result.weeks
    ]

    account_groups = [
        WeeklyPivotAccountGroupRow(
            account_group_id=grp.account_group_id,
            account_group_name=grp.account_group_name,
            display_order=grp.display_order,
            valuations=[
                WeeklyPivotAccountValuation(
                    weekly_snapshot_id=val.weekly_snapshot_id, amount=val.amount
                )
                for val in grp.valuations
            ],
        )
        for grp in result.account_groups
    ]

    accounts = [
        WeeklyPivotAccountRow(
            account_id=acc.account_id,
            account_name=acc.account_name,
            institution_name=acc.institution_name,
            valuations=[
                WeeklyPivotAccountValuation(
                    weekly_snapshot_id=val.weekly_snapshot_id, amount=val.amount
                )
                for val in acc.valuations
            ],
        )
        for acc in result.accounts
    ]

    data = WeeklyPivotReportData(
        year=result.year, weeks=weeks, account_groups=account_groups, accounts=accounts,
        mdd_by_year=[
            AnnualMddItemSchema(
                data_year=m.data_year,
                annual_snapshot_id=m.annual_snapshot_id,
                peak_amount=m.peak_amount,
                trough_amount=m.trough_amount,
                mdd_percentage=m.mdd_percentage,
                weekly_snapshot_count=m.weekly_snapshot_count,
            )
            for m in result.mdd_by_year
        ],
    )
    return WeeklyPivotReportResponse(code=0, message="success", data=data)


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


# ---------------------------------------------------------------------------
# Target Allocations - Account-Level
# ---------------------------------------------------------------------------


@router.post(
    "/target-allocations/account",
    response_model=TargetAllocationAccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="계좌 단위 목표 평가금액 설정",
    responses={**common_responses},
)
async def create_or_update_account_target_allocation(
    request: CreateTargetAllocationAccountRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> TargetAllocationAccountResponse:
    """계좌 단위 목표 평가금액을 설정하거나 업데이트합니다."""
    account_target = (
        await service.target_allocation_service.create_or_update_account_target(
            year=request.year,
            account_id=request.account_id,
            target_amount=request.target_amount,
        )
    )
    return TargetAllocationAccountResponse(
        code=0,
        message="success",
        data=TargetAllocationAccountSchema(
            target_allocation_account_id=account_target.target_allocation_account_id,
            year=account_target.year,
            account_id=account_target.account_id,
            target_amount=account_target.target_amount,
        ),
    )


@router.get(
    "/target-allocations/account",
    response_model=TargetAllocationAccountListResponse,
    summary="연도별 계좌 단위 목표 평가금액 조회",
    responses={**common_responses},
)
async def get_account_target_allocations_by_year(
    year: int = Query(..., description="연도", ge=2020, le=2100),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> TargetAllocationAccountListResponse:
    """특정 연도의 모든 계좌 단위 목표 평가금액을 조회합니다."""
    account_targets = (
        await service.target_allocation_service.get_account_targets_by_year(year=year)
    )
    return TargetAllocationAccountListResponse(
        year=year,
        account_targets=[
            TargetAllocationAccountSchema(
                target_allocation_account_id=t.target_allocation_account_id,
                year=t.year,
                account_id=t.account_id,
                target_amount=t.target_amount,
            )
            for t in account_targets
        ],
    )


@router.get(
    "/target-allocations/account/{year}/{account_id}",
    response_model=TargetAllocationAccountResponse,
    summary="특정 계좌의 목표 평가금액 조회",
    responses={**common_responses},
)
async def get_account_target_allocation(
    year: int = Path(..., description="연도", ge=2020, le=2100),
    account_id: int = Path(..., description="계좌 ID", gt=0),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> TargetAllocationAccountResponse:
    """특정 연도와 계좌의 목표 평가금액을 조회합니다."""
    account_target = await service.target_allocation_service.get_account_target(
        year=year, account_id=account_id
    )
    return TargetAllocationAccountResponse(
        code=0,
        message="success",
        data=(
            TargetAllocationAccountSchema(
                target_allocation_account_id=account_target.target_allocation_account_id,
                year=account_target.year,
                account_id=account_target.account_id,
                target_amount=account_target.target_amount,
            )
            if account_target
            else None
        ),
    )


@router.delete(
    "/target-allocations/account/{target_allocation_account_id}",
    response_model=DeleteTargetAllocationResponse,
    summary="계좌 단위 목표 평가금액 삭제",
    responses={**common_responses},
)
async def delete_account_target_allocation(
    target_allocation_account_id: int = Path(
        ..., description="계좌 단위 목표 ID", gt=0
    ),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DeleteTargetAllocationResponse:
    """계좌 단위 목표 평가금액을 삭제합니다."""
    await service.target_allocation_service.delete_account_target(
        target_allocation_account_id=target_allocation_account_id
    )
    return DeleteTargetAllocationResponse(code=0, message="success", data=None)


# ---------------------------------------------------------------------------
# Target Allocations
# ---------------------------------------------------------------------------


@router.post(
    "/target-allocations/total",
    response_model=TargetAllocationTotalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="연간 총 목표 평가금액 설정",
    responses={**common_responses},
)
async def create_or_update_total_target_allocation(
    request: CreateTargetAllocationTotalRequest,
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> TargetAllocationTotalResponse:
    """연간 총 목표 평가금액을 설정하거나 업데이트합니다."""
    total = await service.target_allocation_service.create_or_update_total_target(
        year=request.year,
        target_amount=request.target_amount,
    )
    return TargetAllocationTotalResponse(
        code=0,
        message="success",
        data=TargetAllocationTotalSchema(
            target_allocation_total_id=total.target_allocation_total_id,
            year=total.year,
            target_amount=total.target_amount,
        ),
    )


@router.get(
    "/target-allocations/total",
    response_model=TargetAllocationTotalResponse,
    summary="연간 총 목표 평가금액 조회",
    responses={**common_responses},
)
async def get_total_target_allocation(
    year: int = Query(..., description="연도", ge=2020, le=2100),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> TargetAllocationTotalResponse:
    """연간 총 목표 평가금액을 조회합니다."""
    total = await service.target_allocation_service.get_total_target_by_year(year=year)
    return TargetAllocationTotalResponse(
        code=0,
        message="success",
        data=(
            TargetAllocationTotalSchema(
                target_allocation_total_id=total.target_allocation_total_id,
                year=total.year,
                target_amount=total.target_amount,
            )
            if total
            else None
        ),
    )


@router.delete(
    "/target-allocations/total",
    response_model=DeleteTargetAllocationResponse,
    summary="연간 총 목표 평가금액 삭제",
    responses={**common_responses},
)
async def delete_total_target_allocation(
    year: int = Query(..., description="연도", ge=2020, le=2100),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DeleteTargetAllocationResponse:
    """연간 총 목표 평가금액을 삭제합니다."""
    await service.target_allocation_service.delete_total_target_by_year(year=year)
    return DeleteTargetAllocationResponse(code=0, message="success", data=None)


# @router.post(
#     "/target-allocations",
#     response_model=TargetAllocationResponse,
#     status_code=status.HTTP_201_CREATED,
#     summary="목표 자산배분 설정",
#     responses={**common_responses},
# )
# async def create_or_update_target_allocation(
#     request: CreateTargetAllocationRequest,
#     service: PortfolioAppService = Depends(get_portfolio_app_service),
# ) -> TargetAllocationResponse:
#     """목표 자산배분을 설정하거나 업데이트합니다."""
#     target = await service.target_allocation_service.create_or_update_target(
#         year=request.year,
#         account_group_id=request.account_group_id,
#         target_amount=request.target_amount,
#     )
#     return TargetAllocationResponse(
#         code=0,
#         message="success",
#         data=TargetAllocationSchema(
#             target_allocation_id=target.target_allocation_id,
#             year=target.year,
#             account_group_id=target.account_group_id,
#             target_amount=target.target_amount,
#         ),
#     )


# @router.get(
#     "/target-allocations",
#     response_model=TargetAllocationListResponse,
#     summary="연도별 목표 자산배분 조회",
#     responses={**common_responses},
# )
# async def get_target_allocations_by_year(
#     year: int = Query(..., description="연도", ge=2020, le=2100),
#     service: PortfolioAppService = Depends(get_portfolio_app_service),
# ) -> TargetAllocationListResponse:
#     """특정 연도의 모든 목표 자산배분을 조회합니다."""
#     targets = await service.target_allocation_service.get_targets_by_year(year=year)
#     return TargetAllocationListResponse(
#         year=year,
#         targets=[
#             TargetAllocationSchema(
#                 target_allocation_id=t.target_allocation_id,
#                 year=t.year,
#                 account_group_id=t.account_group_id,
#                 target_amount=t.target_amount,
#             )
#             for t in targets
#         ],
#     )


@router.get(
    "/target-allocations/{year}/{account_group_id}",
    response_model=TargetAllocationResponse,
    summary="특정 목표 자산배분 조회",
    responses={**common_responses},
)
async def get_target_allocation(
    year: int = Path(..., description="연도", ge=2020, le=2100),
    account_group_id: int = Path(..., description="계좌그룹 ID", gt=0),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> TargetAllocationResponse:
    """특정 연도와 계좌그룹의 목표 자산배분을 조회합니다."""
    target = await service.target_allocation_service.get_target(
        year=year, account_group_id=account_group_id
    )
    if not target:
        raise ValueError(
            f"Target allocation for year {year} and account_group {account_group_id} not found"
        )
    return TargetAllocationResponse(
        code=0,
        message="success",
        data=TargetAllocationSchema(
            target_allocation_id=target.target_allocation_id,
            year=target.year,
            account_group_id=target.account_group_id,
            target_amount=target.target_amount,
        ),
    )


@router.delete(
    "/target-allocations/{target_allocation_id}",
    response_model=DeleteTargetAllocationResponse,
    summary="목표 자산배분 삭제",
    responses={**common_responses},
)
async def delete_target_allocation(
    target_allocation_id: int = Path(..., description="목표 자산배분 ID", gt=0),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> DeleteTargetAllocationResponse:
    """목표 자산배분을 삭제합니다."""
    await service.target_allocation_service.delete_target(
        target_allocation_id=target_allocation_id
    )
    return DeleteTargetAllocationResponse(code=0, message="success", data=None)


# ========== Asset Class Target Allocation Endpoints ==========


@router.post(
    "/target-allocations/asset-classes",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="자산클래스별 목표 비율 일괄 저장",
    responses={**common_responses},
)
async def batch_create_or_update_asset_class_targets(
    request: list[CreateTargetAllocationAssetClassRequest],
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> ApiResponse:
    """자산클래스별 목표 비율을 일괄 저장합니다."""
    from subdomains.portfolio.interface.schemas.target_allocation_schema import (
        TargetAllocationAssetClassSchema,
    )

    results = []
    for item in request:
        result = (
            await service.target_allocation_service.create_or_update_asset_class_target(
                year=item.year,
                asset_class=item.asset_class,
                target_percentage=item.target_percentage,
            )
        )
        results.append(
            TargetAllocationAssetClassSchema(
                target_allocation_asset_class_id=result[
                    "target_allocation_asset_class_id"
                ],
                year=result["year"],
                asset_class=result["asset_class"],
                target_percentage=result["target_percentage"],
            )
        )

    return ApiResponse(code=0, message="success", data={"targets": results})


@router.get(
    "/target-allocations/asset-classes/year/{year}",
    response_model=ApiResponse,
    summary="연도별 자산클래스 목표 비율 조회",
    responses={**common_responses},
)
async def get_asset_class_targets_by_year(
    year: int = Path(..., description="조회할 연도", ge=2020, le=2100),
    service: PortfolioAppService = Depends(get_portfolio_app_service),
) -> ApiResponse:
    """특정 연도의 모든 자산클래스 목표 비율을 조회합니다."""
    from subdomains.portfolio.interface.schemas.target_allocation_schema import (
        TargetAllocationAssetClassSchema,
    )

    results = await service.target_allocation_service.get_asset_class_targets_by_year(
        year=year
    )

    targets = [
        TargetAllocationAssetClassSchema(
            target_allocation_asset_class_id=r["target_allocation_asset_class_id"],
            year=r["year"],
            asset_class=r["asset_class"],
            target_percentage=r["target_percentage"],
        )
        for r in results
    ]

    return ApiResponse(
        code=0,
        message="success",
        data={"year": year, "targets": targets},
    )
