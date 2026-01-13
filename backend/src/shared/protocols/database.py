"""
Database pool abstraction protocol.

기준: .dev-standards/python/DATABASE_STANDARDS.md
"""

from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from shared.protocols.transaction import TransactionMode, Connection


class DatabasePool(ABC):
    """데이터베이스 연결 풀 추상화.
    
    SQLAlchemy와 Psycopg 구현체가 이 인터페이스를 구현한다.
    Application 계층은 이 추상화에만 의존한다.
    """
    
    @abstractmethod
    async def initialize(self) -> None:
        """연결 풀 초기화."""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """연결 풀 종료 및 리소스 해제."""
        pass
    
    @abstractmethod
    async def get_connection(self, mode: TransactionMode = "writable") -> Connection:
        """DB 연결 획득 (SQLAlchemy: AsyncSession, Psycopg: AsyncConnection)."""
        pass
    
    @abstractmethod
    @asynccontextmanager
    async def connection(self, mode: TransactionMode = "writable") -> AsyncGenerator[Connection, None]:
        """DB 연결 컨텍스트 매니저."""
        pass
