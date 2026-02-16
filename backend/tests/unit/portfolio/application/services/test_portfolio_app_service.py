"""Unit tests for PortfolioAppService (institutions)."""

from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from subdomains.portfolio.application.dtos import (
    CreateInstitutionCommand,
    UpdateInstitutionCommand,
)
from subdomains.portfolio.application.services import PortfolioAppService
from subdomains.portfolio.domain.errors import DuplicateEntityError, NotFoundError
from subdomains.portfolio.domain.models import Institution


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
