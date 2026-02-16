"""Shared fixtures for API/integration tests."""

import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.core.waiting_utils import wait_for_logs


@pytest.fixture(scope="session")
def postgres_container():
    """Start a single PostgreSQL container for all API tests."""
    container = PostgresContainer("postgres:17-alpine")
    container.start()
    wait_for_logs(container, "database system is ready to accept connections")
    yield container
    container.stop()
