"""Unit tests for PortfolioAppService."""

from datetime import date
from datetime import datetime
from unittest.mock import AsyncMock
from urllib.error import HTTPError

import pytest

from subdomains.portfolio.application.dtos import (
    DeleteAccountGroupCommand,
    CreateInstitutionCommand,
    DeleteAccountCommand,
    DeleteInstitutionCommand,
    DeleteProductCommand,
    DeleteHoldingCommand,
    UpdateInstitutionCommand,
    UpsertSnapshotHoldingCommand,
)
from subdomains.portfolio.application.services import PortfolioAppService
from subdomains.portfolio.domain.errors import (
    DuplicateEntityError,
    DeletionConflictError,
    InvalidStateError,
    NotFoundError,
)
from subdomains.portfolio.domain.models import (
    AccountGroup,
    Account,
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
        account = Account.create(
            institution_id=1,
            name="테스트계좌",
            type="위탁계좌",
        )
        account.account_id = 1
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
        mock_account_repo.find_by_id.return_value = account
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
        account = Account.create(
            institution_id=1,
            name="테스트계좌",
            type="위탁계좌",
        )
        account.account_id = 1
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
        mock_account_repo.find_by_id.return_value = account
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

    @pytest.mark.asyncio
    async def test_upsert_snapshot_holding_rejects_disallowed_account(
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
        account = Account.create(
            institution_id=1,
            name="사용중단계좌",
            type="예금계좌",
            allow_snapshot_input=False,
        )
        account.account_id = 1
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

        mock_snapshot_repo.find_by_id.return_value = snapshot
        mock_holding_repo.find_by_id.return_value = holding
        mock_account_repo.find_by_id.return_value = account
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


class TestPortfolioProductBetaService:
    @pytest.mark.asyncio
    async def test_fetch_close_series_with_fallback_uses_free_on_yahoo_429(
        self, mock_transaction_manager
    ):
        service = PortfolioAppService(
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        service._fetch_yahoo_close_series_with_retry = AsyncMock(
            side_effect=HTTPError(
                url="https://query1.finance.yahoo.com",
                code=429,
                msg="Too Many Requests",
                hdrs=None,
                fp=None,
            )
        )
        service._fetch_free_close_series = lambda _symbol: {
            "2026-03-10": 100.0,
            "2026-03-11": 101.0,
        }

        series, provider = await service._fetch_close_series_with_fallback("FNGU")

        assert provider == "free"
        assert len(series) == 2

    @pytest.mark.asyncio
    async def test_resolve_product_ticker_success_krx_code(
        self, mock_transaction_manager
    ):
        mock_product_repo = AsyncMock()
        product = Product(
            product_id=11,
            product_name="삼성전자",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=None,
            risk_level="위험",
            allow_snapshot_input=True,
            ticker="A005930",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        mock_product_repo.find_by_id.return_value = product
        mock_product_repo.update.return_value = product

        service = PortfolioAppService(
            AsyncMock(),
            mock_product_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        service._get_krx_market_suffix_for_code = AsyncMock(return_value=".KS")

        result = await service.resolve_product_ticker(11)

        assert result.updated is True
        assert result.old_ticker == "A005930"
        assert result.new_ticker == "005930.KS"
        assert result.message == "ticker_resolved"
        assert product.ticker == "005930.KS"
        mock_product_repo.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_resolve_product_ticker_not_krx_code(self, mock_transaction_manager):
        mock_product_repo = AsyncMock()
        product = Product(
            product_id=12,
            product_name="FNGU",
            asset_class="주식",
            region="미국",
            currency="USD",
            investment_type="ETF",
            characteristics=None,
            risk_level="위험",
            allow_snapshot_input=True,
            ticker="FNGU",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        mock_product_repo.find_by_id.return_value = product

        service = PortfolioAppService(
            AsyncMock(),
            mock_product_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        result = await service.resolve_product_ticker(12)

        assert result.updated is False
        assert result.message == "ticker_not_krx_code"
        mock_product_repo.update.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_resolve_product_ticker_fallback_default_ks(
        self, mock_transaction_manager
    ):
        mock_product_repo = AsyncMock()
        product = Product(
            product_id=13,
            product_name="TIGER 미국테크TOP10 INDXX",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="ETF",
            characteristics=None,
            risk_level="위험",
            allow_snapshot_input=True,
            ticker="A381170",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        mock_product_repo.find_by_id.return_value = product
        mock_product_repo.update.return_value = product

        service = PortfolioAppService(
            AsyncMock(),
            mock_product_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )
        service._get_krx_market_suffix_for_code = AsyncMock(return_value=None)

        result = await service.resolve_product_ticker(13)

        assert result.updated is True
        assert result.old_ticker == "A381170"
        assert result.new_ticker == "381170.KS"
        assert result.message == "ticker_resolved_default_ks"
        assert product.ticker == "381170.KS"
        mock_product_repo.update.assert_awaited_once()

    def test_resolve_ticker_normalizes_krx_code_with_a_prefix(self):
        product = Product(
            product_id=1,
            product_name="삼성전자",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=None,
            risk_level="위험",
            allow_snapshot_input=True,
            ticker="A005930",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )

        assert PortfolioAppService._resolve_ticker(product) == "A005930"

    def test_resolve_ticker_normalizes_krx_code_without_prefix(self):
        product = Product(
            product_id=1,
            product_name="삼성전자",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=None,
            risk_level="위험",
            allow_snapshot_input=True,
            ticker="005930",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )

        assert PortfolioAppService._resolve_ticker(product) == "005930"

    @pytest.mark.asyncio
    async def test_collect_product_beta_ticker_missing_defaults_zero(
        self, mock_transaction_manager
    ):
        mock_product_repo = AsyncMock()
        product = Product(
            product_id=9,
            product_name="현금성자산",
            asset_class="통화",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=None,
            risk_level="안전",
            allow_snapshot_input=True,
            ticker=None,
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        mock_product_repo.find_by_id.return_value = product
        mock_product_repo.update.return_value = product

        service = PortfolioAppService(
            AsyncMock(),
            mock_product_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        result = await service.collect_product_beta(9)

        assert result.product_id == 9
        assert result.updated is True
        assert result.domestic_beta == 0.0
        assert result.global_beta == 0.0
        assert result.message == "ticker_missing_defaulted_zero"
        assert result.beta_collected_at is not None
        mock_product_repo.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_collect_product_beta_ticker_blank_defaults_zero(
        self, mock_transaction_manager
    ):
        mock_product_repo = AsyncMock()
        product = Product(
            product_id=10,
            product_name="달러예수금",
            asset_class="통화",
            region="미국",
            currency="USD",
            investment_type="직접",
            characteristics=None,
            risk_level="안전",
            allow_snapshot_input=True,
            ticker=None,
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        # 기존 데이터에 공백 ticker가 남아있는 경우를 가정
        product.ticker = "   "
        mock_product_repo.find_by_id.return_value = product
        mock_product_repo.update.return_value = product

        service = PortfolioAppService(
            AsyncMock(),
            mock_product_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        result = await service.collect_product_beta(10)

        assert result.product_id == 10
        assert result.updated is True
        assert result.domestic_beta == 0.0
        assert result.global_beta == 0.0
        assert result.message == "ticker_missing_defaulted_zero"
        assert result.beta_collected_at is not None
        mock_product_repo.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_collect_product_beta_success(self, mock_transaction_manager):
        mock_product_repo = AsyncMock()
        product = Product(
            product_id=7,
            product_name="KODEX 200",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="ETF",
            characteristics=["인덱스"],
            risk_level="위험",
            allow_snapshot_input=True,
            ticker="KODEX200.KS",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        mock_product_repo.find_by_id.return_value = product
        mock_product_repo.update.return_value = product

        service = PortfolioAppService(
            AsyncMock(),
            mock_product_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )
        service._collect_product_beta_values = AsyncMock(
            return_value=(1.2345, 2.3456, "collected")
        )

        result = await service.collect_product_beta(7)

        assert result.product_id == 7
        assert result.domestic_beta is not None
        assert result.global_beta is not None
        assert result.beta_collected_at is not None
        mock_product_repo.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_collect_all_product_betas_success(self, mock_transaction_manager):
        mock_product_repo = AsyncMock()
        products = [
            Product(
                product_id=1,
                product_name="삼성전자",
                asset_class="주식",
                region="대한민국",
                currency="KRW",
                investment_type="직접",
                characteristics=None,
                risk_level="위험",
                allow_snapshot_input=True,
                ticker="005930.KS",
                display_order=1,
                created_at=datetime(2025, 1, 1, 0, 0, 0),
            ),
            Product(
                product_id=2,
                product_name="GOOGL",
                asset_class="주식",
                region="미국",
                currency="USD",
                investment_type="직접",
                characteristics=None,
                risk_level="위험",
                allow_snapshot_input=True,
                ticker="GOOGL",
                display_order=2,
                created_at=datetime(2025, 1, 1, 0, 0, 0),
            ),
        ]
        mock_product_repo.get_all.return_value = products
        mock_product_repo.update.side_effect = products

        service = PortfolioAppService(
            AsyncMock(),
            mock_product_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )
        service._collect_product_beta_values = AsyncMock(
            side_effect=[
                (0.9876, 1.8765, "collected"),
                (0.1234, 2.4321, "collected"),
            ]
        )

        result = await service.collect_all_product_betas()

        assert result.updated_count == 2
        assert len(result.items) == 2
        assert all(item.beta_collected_at is not None for item in result.items)
        assert mock_product_repo.update.await_count == 2


class TestPortfolioDeleteService:
    @pytest.mark.asyncio
    async def test_delete_institution_raises_conflict_when_account_exists(
        self, mock_transaction_manager
    ):
        mock_institution_repo = AsyncMock()
        mock_institution_repo.find_by_id.return_value = Institution(
            institution_id=10,
            name="테스트기관",
            type="증권사",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        mock_institution_repo.count_referencing_accounts.return_value = 1

        service = PortfolioAppService(
            mock_institution_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        with pytest.raises(DeletionConflictError):
            await service.delete_institution(
                DeleteInstitutionCommand(institution_id=10)
            )

        mock_institution_repo.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_product_raises_conflict_when_holding_exists(
        self, mock_transaction_manager
    ):
        mock_product_repo = AsyncMock()
        mock_product_repo.find_by_id.return_value = Product(
            product_id=7,
            product_name="테스트상품",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=None,
            risk_level="위험",
            allow_snapshot_input=True,
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        mock_product_repo.count_referencing_holdings.return_value = 2

        service = PortfolioAppService(
            AsyncMock(),
            mock_product_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        with pytest.raises(DeletionConflictError):
            await service.delete_product(DeleteProductCommand(product_id=7))

        mock_product_repo.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_account_raises_conflict_when_holding_exists(
        self, mock_transaction_manager
    ):
        mock_account_repo = AsyncMock()
        mock_account_repo.find_by_id.return_value = Account(
            account_id=3,
            institution_id=1,
            name="테스트계좌",
            type="위탁계좌",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        mock_account_repo.count_referencing_holdings.return_value = 1

        service = PortfolioAppService(
            AsyncMock(),
            AsyncMock(),
            mock_account_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        with pytest.raises(DeletionConflictError):
            await service.delete_account(DeleteAccountCommand(account_id=3))

        mock_account_repo.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_account_success_calls_repository_delete(
        self, mock_transaction_manager
    ):
        mock_account_repo = AsyncMock()
        mock_account_repo.find_by_id.return_value = Account(
            account_id=3,
            institution_id=1,
            name="테스트계좌",
            type="위탁계좌",
            display_order=1,
            created_at=datetime(2025, 1, 1, 0, 0, 0),
        )
        mock_account_repo.count_referencing_holdings.return_value = 0

        service = PortfolioAppService(
            AsyncMock(),
            AsyncMock(),
            mock_account_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        await service.delete_account(DeleteAccountCommand(account_id=3))

        mock_account_repo.delete.assert_awaited_once_with(3)

    @pytest.mark.asyncio
    async def test_delete_holding_hard_delete_raises_conflict_when_snapshot_holding_exists(
        self, mock_transaction_manager
    ):
        mock_holding_repo = AsyncMock()
        holding = Holding.create(account_id=1, product_id=2)
        holding.holding_id = 22
        mock_holding_repo.find_by_id.return_value = holding
        mock_holding_repo.count_referencing_snapshot_holdings.return_value = 3

        service = PortfolioAppService(
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_holding_repo,
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        with pytest.raises(DeletionConflictError):
            await service.delete_holding(
                DeleteHoldingCommand(holding_id=22, action="hard_delete")
            )

        mock_holding_repo.hard_delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_account_group_allows_empty_group(
        self, mock_transaction_manager
    ):
        mock_account_group_repo = AsyncMock()
        mock_account_group_repo.find_by_id.side_effect = InvalidStateError(
            "account_group", "at least one account is required"
        )

        service = PortfolioAppService(
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_account_group_repo,
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            mock_transaction_manager,
        )

        await service.delete_account_group(
            DeleteAccountGroupCommand(account_group_id=11)
        )

        mock_account_group_repo.delete.assert_awaited_once_with(11)
