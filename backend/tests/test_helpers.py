"""Test helper utilities for transaction mocking."""

from unittest.mock import AsyncMock, MagicMock
from shared.protocols.transaction import TransactionManager, TransactionProtocol


class MockTransaction(TransactionProtocol):
    """Mock transaction for testing."""

    def __init__(self, mock_connection=None):
        self.mode = "writable"
        self._connection = mock_connection or AsyncMock()
        self._entered = False

    @property
    def connection(self):
        return self._connection

    async def commit(self) -> None:
        return None

    async def rollback(self) -> None:
        return None

    async def __aenter__(self):
        self._entered = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()


class MockTransactionManager(TransactionManager):
    """Mock transaction manager for testing."""

    def __init__(self):
        self.mock_connection = AsyncMock()
        self._readonly_tx = MockTransaction(self.mock_connection)
        self._writable_tx = MockTransaction(self.mock_connection)
        self._readonly_tx.mode = "readonly"
        self._writable_tx.mode = "writable"

    async def create_readonly_transaction(self) -> TransactionProtocol:
        return self._readonly_tx

    async def create_writable_transaction(self) -> TransactionProtocol:
        return self._writable_tx
