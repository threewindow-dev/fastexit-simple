"""Unit tests for PortfolioAppService."""

from datetime import date
from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from subdomains.portfolio.application.dtos import (
    CreateInstitutionCommand,
    UpdateInstitutionCommand,
    UpsertSnapshotHoldingCommand,
)
from subdomains.portfolio.application.services import PortfolioAppService
from subdomains.portfolio.domain.errors import (
    DuplicateEntityError,
    InvalidStateError,
    NotFoundError,
)
from subdomains.portfolio.domain.models import (
    Holding,
    Institution,
    Product,
    Snapshot,
    SnapshotHolding,
)


class TestPortfolioInstitutionService:
    @pytest.mark.asyncio
    async def test_create_institution_success(
        self, mock_institution_repository, mock_transaction_manager
    ):
        command = CreateInstitutionCommand(
            name="KB증권",
            type="증권사",
            display_order=1,
        )
        created = Institution(
            institution_id=1,
            name="KB증권",
            type="증권사",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        mock_institution_repository.exists_by_name.return_value = False
        mock_institution_repository.add.return_value = created

        service = PortfolioAppService(
            mock_institution_repository,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        result = await service.create_institution(command)

        assert result.institution_id == 1
        assert result.name == "KB증권"
        mock_institution_repository.exists_by_name.assert_awaited_once_with("KB증권")
        mock_institution_repository.add.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_institution_duplicate_name(
        self, mock_institution_repository, mock_transaction_manager
    ):
        command = CreateInstitutionCommand(
            name="KB증권", type="증권사", display_order=1
        )
        mock_institution_repository.exists_by_name.return_value = True

        service = PortfolioAppService(
            mock_institution_repository,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        with pytest.raises(DuplicateEntityError):
            await service.create_institution(command)

    @pytest.mark.asyncio
    async def test_update_institution_not_found(
        self, mock_institution_repository, mock_transaction_manager
    ):
        command = UpdateInstitutionCommand(
            institution_id=999,
            name="KB증권",
            type="증권사",
            display_order=1,
        )
        mock_institution_repository.find_by_id.return_value = None

        service = PortfolioAppService(
            mock_institution_repository,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        with pytest.raises(NotFoundError):
            await service.update_institution(command)

    @pytest.mark.asyncio
    async def test_update_institution_success(
        self, mock_institution_repository, mock_transaction_manager
    ):
        command = UpdateInstitutionCommand(
            institution_id=1,
            name="KB증권",
            type="증권사",
            display_order=2,
        )
        existing = Institution(
            institution_id=1,
            name="KB증권",
            type="증권사",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        updated = Institution(
            institution_id=1,
            name="KB증권",
            type="증권사",
            display_order=2,
            created_at=existing.created_at,
        )
        mock_institution_repository.find_by_id.return_value = existing
        mock_institution_repository.exists_by_name.return_value = False
        mock_institution_repository.update.return_value = updated

        service = PortfolioAppService(
            mock_institution_repository,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        result = await service.update_institution(command)

        assert result.display_order == 2
        mock_institution_repository.update.assert_awaited_once()


class TestPortfolioSnapshotHoldingService:
    @pytest.mark.asyncio
    async def test_upsert_snapshot_holding_rejects_disallowed_product(
        self, mock_transaction_manager
    ):
        mock_institution_repo = AsyncMock()
        mock_product_repo = AsyncMock()
        mock_account_repo = AsyncMock()
        mock_account_group_repo = AsyncMock()
        mock_holding_repo = AsyncMock()
        mock_snapshot_repo = AsyncMock()
        mock_report_repo = AsyncMock()

        snapshot = Snapshot.create(user_id=1, reference_date=date(2025, 1, 22))
        snapshot.snapshot_id = 10
        holding = Holding.create(account_id=1, product_id=2)
        holding.holding_id = 100
        product = Product.create(
            product_name="평가금액 보정",
            asset_class="기타자산",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=["보정"],
            risk_level="안전",
            allow_snapshot_input=False,
        )
        product.product_id = 2

        mock_snapshot_repo.find_by_id.return_value = snapshot
        mock_holding_repo.find_by_id.return_value = holding
        mock_product_repo.find_by_id.return_value = product

        service = PortfolioAppService(
            mock_institution_repo,
            mock_product_repo,
            mock_account_repo,
            mock_account_group_repo,
            mock_holding_repo,
            mock_snapshot_repo,
            mock_report_repo,
            mock_transaction_manager,
        )

        command = UpsertSnapshotHoldingCommand(
            snapshot_id=10,
            holding_id=100,
            valuation_amount=12345.0,
            data_source="manual",
        )

        with pytest.raises(InvalidStateError):
            await service.upsert_snapshot_holding(command)

        mock_snapshot_repo.save_holding.assert_not_called()

    @pytest.mark.asyncio
    async def test_upsert_snapshot_holding_success_when_allowed(
        self, mock_transaction_manager
    ):
        mock_institution_repo = AsyncMock()
        mock_product_repo = AsyncMock()
        mock_account_repo = AsyncMock()
        mock_account_group_repo = AsyncMock()
        mock_holding_repo = AsyncMock()
        mock_snapshot_repo = AsyncMock()
        mock_report_repo = AsyncMock()

        snapshot = Snapshot.create(user_id=1, reference_date=date(2025, 1, 22))
        snapshot.snapshot_id = 10
        holding = Holding.create(account_id=1, product_id=2)
        holding.holding_id = 100
        product = Product.create(
            product_name="삼성전자",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=None,
            risk_level="위험",
        )
        product.product_id = 2
        saved = SnapshotHolding(
            holding_id=100,
            valuation_amount=12345.0,
            data_source="manual",
        )

        mock_snapshot_repo.find_by_id.return_value = snapshot
        mock_holding_repo.find_by_id.return_value = holding
        mock_product_repo.find_by_id.return_value = product
        mock_snapshot_repo.save_holding.return_value = saved

        service = PortfolioAppService(
            mock_institution_repo,
            mock_product_repo,
            mock_account_repo,
            mock_account_group_repo,
            mock_holding_repo,
            mock_snapshot_repo,
            mock_report_repo,
            mock_transaction_manager,
        )

        command = UpsertSnapshotHoldingCommand(
            snapshot_id=10,
            holding_id=100,
            valuation_amount=12345.0,
            data_source="manual",
        )

        result = await service.upsert_snapshot_holding(command)

        assert result.holding_id == 100
        assert result.valuation_amount == 12345.0
        mock_snapshot_repo.save_holding.assert_awaited_once()
