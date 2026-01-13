"""
Database connection and session management.

기준: .dev-standards/python/TRANSACTION_MANAGEMENT.md
현재: psycopg + SQLAlchemy async 모두 지원
- REPOSITORY_TYPE 환경변수로 선택: "psycopg" | "sqlalchemy" (기본값: "sqlalchemy")
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import psycopg
from psycopg import AsyncConnection
from psycopg.rows import dict_row
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from shared.errors import DbConnectionError, InfraError
from shared.protocols.transaction import TransactionProtocol


logger = logging.getLogger(__name__)

# ============================================================================
# SQLAlchemy 기본 설정
# ============================================================================

# ORM Base (모든 모델이 상속)
Base = declarative_base()


# ============================================================================
# Transaction Implementations
# ============================================================================

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
            raise InfraError("Failed to rollback transaction", origin_exc=exc)


class SQLAlchemyTransaction(TransactionProtocol):
    """SQLAlchemy 기반 비동기 트랜잭션 구현.
    
    AsyncSession 컨텍스트 매니저로 자동 commit/rollback 관리.
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def commit(self) -> None:
        """트랜잭션 커밋."""
        try:
            await self.session.commit()
        except Exception as exc:
            logger.error(f"Commit failed: {exc}")
            raise InfraError("Failed to commit transaction", origin_exc=exc)
    
    async def rollback(self) -> None:
        """트랜잭션 롤백."""
        try:
            await self.session.rollback()
        except Exception as exc:
            logger.error(f"Rollback failed: {exc}")
            raise InfraError("Failed to rollback transaction", origin_exc=exc)


class DatabasePool:
    """데이터베이스 연결 풀 관리 (psycopg + SQLAlchemy)."""
    
    def __init__(self):
        self._dsn: str | None = None
        self._engine = None
        self._session_factory = None
        self._repository_type: str = os.getenv("REPOSITORY_TYPE", "sqlalchemy")  # "sqlalchemy" | "psycopg"
    
    async def initialize(self) -> None:
        """연결 풀 및 SQLAlchemy engine 초기화."""
        dsn = self._build_connection_string()
        self._dsn = dsn
        
        if self._repository_type == "sqlalchemy":
            try:
                # SQLAlchemy async engine 생성
                # postgresql+asyncpg:// 스키마 사용
                async_dsn = dsn.replace("postgresql://", "postgresql+asyncpg://")
                self._engine = create_async_engine(
                    async_dsn,
                    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
                    future=True,
                    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
                    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
                    pool_pre_ping=True,
                )
                self._session_factory = async_sessionmaker(
                    self._engine,
                    class_=AsyncSession,
                    expire_on_commit=False,
                )
                logger.info("SQLAlchemy async engine initialized")
            except Exception as exc:
                raise DbConnectionError(os.getenv("DB_HOST", "localhost"), origin_exc=exc)
        else:
            logger.info("Using psycopg repository (legacy)")
    
    async def close(self) -> None:
        """연결 풀 종료."""
        if self._engine:
            await self._engine.dispose()
            logger.info("SQLAlchemy engine disposed")
        logger.info("Database pool closed")
    
    async def get_connection(self) -> AsyncConnection:
        """Psycopg 연결 획득 (레거시)."""
        if not self._dsn:
            raise InfraError("Database pool not initialized")
        
        try:
            conn = await psycopg.AsyncConnection.connect(self._dsn, row_factory=dict_row)
            return conn
        except Exception as exc:
            raise InfraError("Failed to get database connection", origin_exc=exc)
    
    async def put_connection(self, conn: AsyncConnection) -> None:
        """Psycopg 연결 반환."""
        try:
            await conn.close()
        except Exception:
            pass
    
    async def get_session(self) -> AsyncSession:
        """SQLAlchemy 세션 획득."""
        if not self._session_factory:
            raise InfraError("SQLAlchemy not initialized")
        return self._session_factory()
    
    @asynccontextmanager
    async def connection(self):
        """Psycopg 연결 컨텍스트 매니저."""
        conn = await self.get_connection()
        try:
            yield conn
        finally:
            await self.put_connection(conn)
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """SQLAlchemy 세션 컨텍스트 매니저."""
        session = await self.get_session()
        try:
            yield session
        finally:
            await session.close()
    
    @staticmethod
    def _build_connection_string() -> str:
        """환경 변수에서 DB 연결 문자열 구성."""
        db_password = os.getenv("DB_PASSWORD")
        if not db_password:
            raise ValueError("DB_PASSWORD environment variable is required")
        
        host = os.getenv("DB_HOST", "")
        port = os.getenv("DB_PORT", "")
        dbname = os.getenv("DB_NAME", "")
        user = os.getenv("DB_USER", "")
        
        return f"postgresql://{user}:{db_password}@{host}:{port}/{dbname}"


# 전역 데이터베이스 풀
db_pool = DatabasePool()


# ============================================================================
# Dependency Injection Factories
# ============================================================================

async def get_transaction(db_pool_instance: DatabasePool | None = None) -> TransactionProtocol:
    """의존성 주입용 트랜잭션 팩토리.
    
    저장소 타입(psycopg/sqlalchemy)에 따라 적절한 트랜잭션 반환.
    """
    pool = db_pool_instance or db_pool
    if pool._repository_type == "sqlalchemy":
        session = await pool.get_session()
        return SQLAlchemyTransaction(session)
    else:
        conn = await pool.get_connection()
        return PsycopgTransaction(conn)


async def get_db_connection() -> AsyncConnection:
    """의존성 주입용 Psycopg 연결 팩토리."""
    return await db_pool.get_connection()


async def get_db_session() -> AsyncSession:
    """의존성 주입용 SQLAlchemy 세션 팩토리."""
    return await db_pool.get_session()
