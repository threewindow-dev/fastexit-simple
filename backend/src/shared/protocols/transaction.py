"""
Transaction protocol definition.

기준: .dev-standards/python/TRANSACTION_MANAGEMENT.md
"""

from abc import ABC, abstractmethod
from typing import Literal, Protocol


TransactionMode = Literal["readonly", "writable"]


class Connection(Protocol):
    """Database connection abstraction.
    
    실제로는 SQLAlchemy AsyncSession 또는 psycopg AsyncConnection.
    Repository는 이 인터페이스를 통해 DB에 접근.
    """
    pass


class TransactionProtocol(ABC):
    """Transaction abstraction for boundary management.
    
    Async context manager로 사용:
    ```python
    async with transaction:
        await repository.save(transaction.connection, obj)
        # 블록을 벗어나면서 자동 commit/rollback
    ```
    
    예외 발생 시 자동 rollback.
    정상 완료 시 자동 commit.
    """
    
    mode: TransactionMode = "writable"
    
    @property
    @abstractmethod
    def connection(self) -> Connection:
        """트랜잭션이 관리하는 DB 연결."""
        pass

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


class TransactionManager(ABC):
    """트랜잭션 매니저: readonly/writable 트랜잭션 생성 팩토리."""
    
    @abstractmethod
    async def create_readonly_transaction(self) -> TransactionProtocol:
        """읽기 전용 트랜잭션 생성."""
        pass
    
    @abstractmethod
    async def create_writable_transaction(self) -> TransactionProtocol:
        """쓰기 트랜잭션 생성."""
        pass
