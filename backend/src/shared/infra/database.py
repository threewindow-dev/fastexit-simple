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
from shared.protocols.transaction import TransactionProtocol, TransactionMode, TransactionManager, Connection


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
    
    def __init__(self, conn: AsyncConnection, mode: TransactionMode = "writable"):
        self._conn = conn
        self.mode = mode
    
    @property
    def connection(self) -> Connection:
        """트랜잭션이 관리하는 DB 연결."""
        return self._conn
    
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
    
    def __init__(self, session: AsyncSession, mode: TransactionMode = "writable"):
        self._session = session
        self.mode = mode
    
    @property
    def connection(self) -> Connection:
        """트랜잭션이 관리하는 DB 연결."""
        return self._session
    
    async def commit(self) -> None:
        """트랜잭션 커밋."""
        try:
            await self._session.commit()
        except Exception as exc:
            logger.error(f"Commit failed: {exc}")
            raise InfraError("Failed to commit transaction", origin_exc=exc)
    
    async def rollback(self) -> None:
        """트랜잭션 롤백."""
        try:
            await self._session.rollback()
        except Exception as exc:
            logger.error(f"Rollback failed: {exc}")
            raise InfraError("Failed to rollback transaction", origin_exc=exc)


class DatabasePool:
    """데이터베이스 연결 풀 관리 (psycopg + SQLAlchemy).

    - writable / readonly DSN을 모두 지원하며, readonly 설정이 없으면 writable로 폴백한다.
    """
    
    def __init__(self):
        self._dsn_write: str | None = None
        self._dsn_readonly: str | None = None
        self._engine_write = None
        self._engine_readonly = None
        self._session_factory_write = None
        self._session_factory_readonly = None
        self._repository_type: str = os.getenv("REPOSITORY_TYPE", "sqlalchemy")  # "sqlalchemy" | "psycopg"
    
    async def initialize(self) -> None:
        """연결 풀 및 SQLAlchemy engine 초기화."""
        self._dsn_write = self._build_connection_string(prefix="DB_")
        # readonly 구성: READONLY가 명시되지 않으면 write DSN을 재사용
        readonly_enabled = os.getenv("DB_READONLY_ENABLED", "false").lower() == "true"
        if readonly_enabled:
            try:
                self._dsn_readonly = self._build_connection_string(prefix="DB_READONLY_", require_password=False)
            except Exception as exc:
                logger.warning("Readonly DSN 구성 실패, write DSN으로 폴백합니다: %s", exc)
                self._dsn_readonly = None
        if not self._dsn_readonly:
            self._dsn_readonly = self._dsn_write
        
        if self._repository_type == "sqlalchemy":
            try:
                # SQLAlchemy async engine 생성 (writable)
                async_dsn = self._dsn_write.replace("postgresql://", "postgresql+asyncpg://")
                self._engine_write = create_async_engine(
                    async_dsn,
                    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
                    future=True,
                    pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
                    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
                    pool_pre_ping=True,
                )
                self._session_factory_write = async_sessionmaker(
                    self._engine_write,
                    class_=AsyncSession,
                    expire_on_commit=False,
                )
                logger.info("SQLAlchemy async engine (writable) initialized")
                
                # SQLAlchemy async engine (readonly) - 별도 설정 시 분리, 없으면 동일 엔진 사용
                if self._dsn_readonly and self._dsn_readonly != self._dsn_write:
                    async_dsn_ro = self._dsn_readonly.replace("postgresql://", "postgresql+asyncpg://")
                    self._engine_readonly = create_async_engine(
                        async_dsn_ro,
                        echo=os.getenv("SQL_ECHO", "false").lower() == "true",
                        future=True,
                        pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
                        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
                        pool_pre_ping=True,
                    )
                    self._session_factory_readonly = async_sessionmaker(
                        self._engine_readonly,
                        class_=AsyncSession,
                        expire_on_commit=False,
                    )
                    logger.info("SQLAlchemy async engine (readonly) initialized")
                else:
                    self._engine_readonly = self._engine_write
                    self._session_factory_readonly = self._session_factory_write
            except Exception as exc:
                raise DbConnectionError(os.getenv("DB_HOST", "localhost"), origin_exc=exc)
        else:
            logger.info("Using psycopg repository (legacy)")
    
    async def close(self) -> None:
        """연결 풀 종료."""
        engines = {"write": self._engine_write, "readonly": self._engine_readonly}
        disposed = set()
        for name, engine in engines.items():
            if engine and engine not in disposed:
                await engine.dispose()
                disposed.add(engine)
                logger.info("SQLAlchemy engine (%s) disposed", name)
        logger.info("Database pool closed")
    
    async def get_connection(self, mode: TransactionMode = "writable") -> AsyncConnection:
        """Psycopg 연결 획득 (레거시)."""
        target_dsn = self._dsn_readonly if mode == "readonly" else self._dsn_write
        if not target_dsn:
            raise InfraError("Database pool not initialized")
        
        try:
            conn = await psycopg.AsyncConnection.connect(target_dsn, row_factory=dict_row)
            return conn
        except Exception as exc:
            raise InfraError("Failed to get database connection", origin_exc=exc)
    
    async def put_connection(self, conn: AsyncConnection) -> None:
        """Psycopg 연결 반환."""
        try:
            await conn.close()
        except Exception:
            pass
    
    async def get_session(self, mode: TransactionMode = "writable") -> AsyncSession:
        """SQLAlchemy 세션 획득."""
        factory = self._session_factory_readonly if mode == "readonly" else self._session_factory_write
        if not factory:
            raise InfraError("SQLAlchemy not initialized")
        return factory()
    
    @asynccontextmanager
    async def connection(self, mode: TransactionMode = "writable"):
        """Psycopg 연결 컨텍스트 매니저."""
        conn = await self.get_connection(mode=mode)
        try:
            yield conn
        finally:
            await self.put_connection(conn)
    
    @asynccontextmanager
    async def session(self, mode: TransactionMode = "writable") -> AsyncGenerator[AsyncSession, None]:
        """SQLAlchemy 세션 컨텍스트 매니저."""
        session = await self.get_session(mode=mode)
        try:
            yield session
        finally:
            await session.close()
    
    @staticmethod
    def _build_connection_string(prefix: str = "DB_", require_password: bool = True) -> str:
        """환경 변수에서 DB 연결 문자열 구성.

        prefix 예: "DB_" (writable), "DB_READONLY_" (readonly)
        """
        password_env = f"{prefix}PASSWORD"
        db_password = os.getenv(password_env)
        if require_password and not db_password:
            raise ValueError(f"{password_env} environment variable is required")
        
        host = os.getenv(f"{prefix}HOST", os.getenv("DB_HOST", ""))
        port = os.getenv(f"{prefix}PORT", os.getenv("DB_PORT", ""))
        dbname = os.getenv(f"{prefix}NAME", os.getenv("DB_NAME", ""))
        user = os.getenv(f"{prefix}USER", os.getenv("DB_USER", ""))
        password = db_password or os.getenv("DB_PASSWORD", "")
        
        return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


# 전역 데이터베이스 풀
db_pool = DatabasePool()


# ============================================================================
# Transaction Manager Implementations
# ============================================================================

class SQLAlchemyTransactionManager(TransactionManager):
    """SQLAlchemy 기반 트랜잭션 매니저."""
    
    def __init__(self, db_pool: DatabasePool):
        self._db_pool = db_pool
    
    async def create_readonly_transaction(self) -> TransactionProtocol:
        """읽기 전용 트랜잭션 생성."""
        session = await self._db_pool.get_session(mode="readonly")
        return SQLAlchemyTransaction(session, mode="readonly")
    
    async def create_writable_transaction(self) -> TransactionProtocol:
        """쓰기 트랜잭션 생성."""
        session = await self._db_pool.get_session(mode="writable")
        return SQLAlchemyTransaction(session, mode="writable")


class PsycopgTransactionManager(TransactionManager):
    """Psycopg 기반 트랜잭션 매니저."""
    
    def __init__(self, db_pool: DatabasePool):
        self._db_pool = db_pool
    
    async def create_readonly_transaction(self) -> TransactionProtocol:
        """읽기 전용 트랜잭션 생성."""
        conn = await self._db_pool.get_connection(mode="readonly")
        return PsycopgTransaction(conn, mode="readonly")
    
    async def create_writable_transaction(self) -> TransactionProtocol:
        """쓰기 트랜잭션 생성."""
        conn = await self._db_pool.get_connection(mode="writable")
        return PsycopgTransaction(conn, mode="writable")


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
        return SQLAlchemyTransaction(session, mode="writable")
    else:
        conn = await pool.get_connection()
        return PsycopgTransaction(conn, mode="writable")


async def get_db_connection() -> AsyncConnection:
    """의존성 주입용 Psycopg 연결 팩토리."""
    return await db_pool.get_connection()


async def get_db_session() -> AsyncSession:
    """의존성 주입용 SQLAlchemy 세션 팩토리."""
    return await db_pool.get_session()
