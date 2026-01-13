"""
Pytest configuration and fixtures for User domain tests
"""
import pytest
from unittest.mock import AsyncMock
from datetime import datetime

from subdomains.user.domain.models import User
from subdomains.user.domain.protocols import UserRepository
from tests.test_helpers import MockTransactionManager


# ============================================================================
# Domain Model Fixtures
# ============================================================================

@pytest.fixture
def sample_user() -> User:
    """Sample valid user for testing"""
    return User(
        id=1,
        username="john_doe",
        email="john@example.com",
        full_name="John Doe",
        created_at=datetime(2025, 1, 11, 10, 30, 0),
    )


@pytest.fixture
def sample_user_no_id() -> User:
    """Sample user without ID (before saving)"""
    return User(
        id=None,
        username="alice",
        email="alice@example.com",
        full_name="Alice Park",
        created_at=datetime(2025, 1, 11, 11, 0, 0),
    )


@pytest.fixture
def sample_users() -> list[User]:
    """List of sample users for pagination tests"""
    return [
        User(
            id=i,
            username=f"user_{i}",
            email=f"user{i}@example.com",
            full_name=f"User {i}",
            created_at=datetime(2025, 1, 11, 10 + i, 0, 0),
        )
        for i in range(1, 11)
    ]


# ============================================================================
# Mock Repository Fixtures
# ============================================================================

@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """Mock UserRepository for unit tests"""
    mock_repo = AsyncMock(spec=UserRepository)
    
    # Configure default behaviors
    mock_repo.exists_by_username = AsyncMock(return_value=False)
    mock_repo.exists_by_email = AsyncMock(return_value=False)
    mock_repo.find_by_id = AsyncMock(return_value=None)
    mock_repo.find_all = AsyncMock(return_value=([], 0))
    mock_repo.add = AsyncMock()
    mock_repo.update = AsyncMock()
    mock_repo.remove = AsyncMock()
    
    return mock_repo


@pytest.fixture
def mock_transaction_manager() -> MockTransactionManager:
    """Mock TransactionManager for unit tests."""
    return MockTransactionManager()
