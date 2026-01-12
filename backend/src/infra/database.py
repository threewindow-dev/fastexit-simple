"""
Database connection and session management.

기준: .dev-standards/python/TRANSACTION_MANAGEMENT.md
현재: psycopg 기반 (향후 SQLAlchemy async로 확장 가능)
"""

import os
import logging
from contextlib import asynccontextmanager

import psycopg
from psycopg import AsyncConnection
from psycopg.rows import dict_row

from shared.errors import DbConnectionError, InfraError
from shared.protocols.transaction import TransactionProtocol


logger = logging.getLogger(__name__)


class PsycopgTransaction(TransactionProtocol):
    """psycopg 기반 트랜잭션 구현."""
    
    def __init__(self, conn: AsyncConnection):
        self.conn = conn
    
    async def commit(self) -> None:
        """트랜잭션 커밋."""
        try:
            await self.conn.commit()
        except Exception as exc:
            logger.error(f"Commit failed: {exc}")
            raise InfraError("Failed to commit transaction", origin_exc=exc)
    
    async def rollback(self) -> None:
        """트랜잭션 롤백."""
        try:
            await self.conn.rollback()
        except Exception as exc:
            logger.error(f"Rollback failed: {exc}")
            # 롤백 실패도 에러이지만, 이미 문제 상황이므로 조용히 처리
            raise InfraError("Failed to rollback transaction", origin_exc=exc)


class DatabasePool:
    """데이터베이스 연결 풀 관리."""
    
    def __init__(self):
        self._dsn: str | None = None
    
    async def initialize(self) -> None:
        """연결 풀 초기화."""
        dsn = self._build_connection_string()
        try:
            # 연결 문자열만 준비하여 지연 연결 방식으로 동작
            self._dsn = dsn
            logger.info("Database pool initialized (lazy)")
        except Exception as exc:
            raise DbConnectionError(os.getenv("DB_HOST", "localhost"), origin_exc=exc)
    
    async def close(self) -> None:
        """연결 풀 종료."""
        # 지연 연결 방식: 명시적으로 관리할 풀 없음
        logger.info("Database pool closed")
    
    async def get_connection(self) -> AsyncConnection:
        """풀에서 연결 획득."""
        if not self._dsn:
            raise InfraError("Database pool not initialized")
        
        try:
            conn = await psycopg.AsyncConnection.connect(self._dsn, row_factory=dict_row)
            return conn
        except Exception as exc:
            raise InfraError("Failed to get database connection", origin_exc=exc)
    
    async def put_connection(self, conn: AsyncConnection) -> None:
        """풀에 연결 반환."""
        # 지연 연결: 즉시 연결 종료
        try:
            await conn.close()
        except Exception:
            pass
    
    @asynccontextmanager
    async def connection(self):
        """연결 컨텍스트 매니저."""
        conn = await self.get_connection()
        try:
            yield conn
        finally:
            await self.put_connection(conn)
    
    @staticmethod
    def _build_connection_string() -> str:
        """환경 변수에서 DB 연결 문자열 구성."""
        db_password = os.getenv("DB_PASSWORD")
        if not db_password:
            raise ValueError("DB_PASSWORD environment variable is required")
        
        host = os.getenv("DB_HOST", "postgres")
        port = os.getenv("DB_PORT", "5432")
        dbname = os.getenv("DB_NAME", "fastexit")
        user = os.getenv("DB_USER", "postgres")
        
        return f"postgresql://{user}:{db_password}@{host}:{port}/{dbname}"


# 전역 데이터베이스 풀
db_pool = DatabasePool()


async def get_transaction() -> TransactionProtocol:
    """의존성 주입용 트랜잭션 팩토리."""
    conn = await db_pool.get_connection()
    try:
        return PsycopgTransaction(conn)
    except Exception:
        await db_pool.put_connection(conn)
        raise


async def get_db_connection() -> AsyncConnection:
    """의존성 주입용 DB 연결 팩토리."""
    return await db_pool.get_connection()
