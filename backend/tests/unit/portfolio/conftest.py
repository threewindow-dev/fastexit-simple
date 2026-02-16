"""Portfolio unit test fixtures."""

from unittest.mock import AsyncMock

import pytest

from subdomains.portfolio.domain.protocols import InstitutionRepository
from tests.test_helpers import MockTransactionManager


@pytest.fixture
def mock_institution_repository() -> AsyncMock:
    """Mock InstitutionRepository for unit tests."""
    mock_repo = AsyncMock(spec=InstitutionRepository)
    mock_repo.exists_by_name = AsyncMock(return_value=False)
    mock_repo.find_by_id = AsyncMock(return_value=None)
    mock_repo.add = AsyncMock()
    mock_repo.update = AsyncMock()
    mock_repo.get_all = AsyncMock(return_value=[])
    mock_repo.update_display_orders = AsyncMock(return_value=0)
    return mock_repo


@pytest.fixture
def mock_transaction_manager() -> MockTransactionManager:
    """Mock TransactionManager for unit tests."""
    return MockTransactionManager()
