"""
Transaction protocol definition.

기준: .dev-standards/python/TRANSACTION_MANAGEMENT.md
"""

from abc import ABC, abstractmethod


class TransactionProtocol(ABC):
    """Transaction abstraction for boundary management.
    
    Async context manager로 사용:
    ```python
    async with transaction:
        await repository.save(obj)
        # 블록을 벗어나면서 자동 commit/rollback
    ```
    
    예외 발생 시 자동 rollback.
    정상 완료 시 자동 commit.
    """
    
    async def __aenter__(self) -> "TransactionProtocol":
        """Enter async context manager."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager with auto commit/rollback."""
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
    
    @abstractmethod
    async def commit(self) -> None:
        """트랜잭션 커밋."""
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """트랜잭션 롤백."""
        pass
