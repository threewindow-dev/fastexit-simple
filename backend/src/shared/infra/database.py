"""
Database connection and session management.

기준: .dev-standards/python/DATABASE_STANDARDS.md
현재: psycopg + SQLAlchemy async 모두 지원
- 설정은 외부(dependencies/main)에서 주입받음
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import psycopg
from psycopg import AsyncConnection
from psycopg.rows import dict_row
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from shared.errors import DbConnectionError, InfraError
from shared.protocols.transaction import (
    TransactionProtocol,
    TransactionMode,
    TransactionManager,
    Connection,
)
from shared.protocols.database import DatabasePool

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
            await self._conn.commit()
        except Exception as exc:
            logger.error(f"Commit failed: {exc}")
            raise InfraError("Failed to commit transaction", origin_exc=exc)

    async def rollback(self) -> None:
        """트랜잭션 롤백."""
        try:
            await self._conn.rollback()
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


# ============================================================================
# Database Pool Implementations
# ============================================================================


class SQLAlchemyDatabasePool(DatabasePool):
    """SQLAlchemy 기반 데이터베이스 연결 풀.

    - writable / readonly 엔진 분리 지원
    - AsyncSession 기반 트랜잭션 관리
    """

    def __init__(
        self,
        dsn_write: str,
        dsn_readonly: str | None = None,
        pool_size: int = 5,
        max_overflow: int = 10,
        sql_echo: bool = False,
    ):
        """
        Args:
            dsn_write: Writable DB 연결 문자열
            dsn_readonly: Readonly DB 연결 문자열 (None이면 dsn_write 사용)
            pool_size: 연결 풀 크기
            max_overflow: 최대 오버플로우 연결 수
            sql_echo: SQL 쿼리 로깅 여부
        """
        self._dsn_write = dsn_write
        self._dsn_readonly = dsn_readonly or dsn_write
        self._pool_size = pool_size
        self._max_overflow = max_overflow
        self._sql_echo = sql_echo
        self._engine_write = None
        self._engine_readonly = None
        self._session_factory_write = None
        self._session_factory_readonly = None

    async def initialize(self) -> None:
        """SQLAlchemy 엔진 및 세션 팩토리 초기화."""
        try:
            # SQLAlchemy async engine 생성 (writable)
            async_dsn = self._dsn_write.replace(
                "postgresql://", "postgresql+asyncpg://"
            )
            self._engine_write = create_async_engine(
                async_dsn,
                echo=self._sql_echo,
                future=True,
                pool_size=self._pool_size,
                max_overflow=self._max_overflow,
                pool_pre_ping=True,
            )
            self._session_factory_write = async_sessionmaker(
                self._engine_write,
                class_=AsyncSession,
                expire_on_commit=False,
            )
            logger.info("SQLAlchemy async engine (writable) initialized")

            # SQLAlchemy async engine (readonly) - 별도 설정 시 분리, 없으면 동일 엔진 사용
            if self._dsn_readonly != self._dsn_write:
                async_dsn_ro = self._dsn_readonly.replace(
                    "postgresql://", "postgresql+asyncpg://"
                )
                self._engine_readonly = create_async_engine(
                    async_dsn_ro,
                    echo=self._sql_echo,
                    future=True,
                    pool_size=self._pool_size,
                    max_overflow=self._max_overflow,
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
            # DSN에서 호스트 추출 시도
            host = "unknown"
            try:
                host = self._dsn_write.split("@")[1].split(":")[0]
            except Exception:
                pass
            raise DbConnectionError(host, origin_exc=exc)

    async def close(self) -> None:
        """SQLAlchemy 엔진 종료."""
        engines = {"write": self._engine_write, "readonly": self._engine_readonly}
        disposed = set()
        for name, engine in engines.items():
            if engine and engine not in disposed:
                await engine.dispose()
                disposed.add(engine)
                logger.info("SQLAlchemy engine (%s) disposed", name)
        logger.info("SQLAlchemy database pool closed")

    async def get_connection(self, mode: TransactionMode = "writable") -> AsyncSession:
        """SQLAlchemy 세션 획득."""
        factory = (
            self._session_factory_readonly
            if mode == "readonly"
            else self._session_factory_write
        )
        if not factory:
            raise InfraError("SQLAlchemy not initialized")
        return factory()

    @asynccontextmanager
    async def connection(
        self, mode: TransactionMode = "writable"
    ) -> AsyncGenerator[AsyncSession, None]:
        """SQLAlchemy 세션 컨텍스트 매니저."""
        session = await self.get_connection(mode=mode)
        try:
            yield session
        finally:
            await session.close()


class PsycopgDatabasePool(DatabasePool):
    """Psycopg 기반 데이터베이스 연결 풀 (레거시).

    - writable / readonly 연결 분리 지원
    - AsyncConnection 기반 트랜잭션 관리
    """

    def __init__(self, dsn_write: str, dsn_readonly: str | None = None):
        """
        Args:
            dsn_write: Writable DB 연결 문자열
            dsn_readonly: Readonly DB 연결 문자열 (None이면 dsn_write 사용)
        """
        self._dsn_write = dsn_write
        self._dsn_readonly = dsn_readonly or dsn_write

    async def initialize(self) -> None:
        """Psycopg DSN 초기화."""
        logger.info("Psycopg database pool initialized (legacy)")

    async def close(self) -> None:
        """Psycopg 풀 종료 (연결은 각각 종료됨)."""
        logger.info("Psycopg database pool closed")

    async def get_connection(
        self, mode: TransactionMode = "writable"
    ) -> AsyncConnection:
        """Psycopg 연결 획득."""
        target_dsn = self._dsn_readonly if mode == "readonly" else self._dsn_write
        if not target_dsn:
            raise InfraError("Database pool not initialized")

        try:
            conn = await psycopg.AsyncConnection.connect(
                target_dsn, row_factory=dict_row
            )
            return conn
        except Exception as exc:
            raise InfraError("Failed to get database connection", origin_exc=exc)

    @asynccontextmanager
    async def connection(
        self, mode: TransactionMode = "writable"
    ) -> AsyncGenerator[AsyncConnection, None]:
        """Psycopg 연결 컨텍스트 매니저."""
        conn = await self.get_connection(mode=mode)
        try:
            yield conn
        finally:
            try:
                await conn.close()
            except Exception:
                pass


# ============================================================================
# Database Pool Factory
# ============================================================================


def create_sqlalchemy_pool(
    dsn_write: str,
    dsn_readonly: str | None = None,
    pool_size: int = 5,
    max_overflow: int = 10,
    sql_echo: bool = False,
) -> SQLAlchemyDatabasePool:
    """SQLAlchemy DatabasePool 생성.

    Args:
        dsn_write: Writable DB 연결 문자열
        dsn_readonly: Readonly DB 연결 문자열 (None이면 dsn_write 사용)
        pool_size: 연결 풀 크기
        max_overflow: 최대 오버플로우 연결 수
        sql_echo: SQL 쿼리 로깅 여부

    Returns:
        SQLAlchemyDatabasePool 인스턴스
    """
    return SQLAlchemyDatabasePool(
        dsn_write=dsn_write,
        dsn_readonly=dsn_readonly,
        pool_size=pool_size,
        max_overflow=max_overflow,
        sql_echo=sql_echo,
    )


def create_psycopg_pool(
    dsn_write: str, dsn_readonly: str | None = None
) -> PsycopgDatabasePool:
    """Psycopg DatabasePool 생성.

    Args:
        dsn_write: Writable DB 연결 문자열
        dsn_readonly: Readonly DB 연결 문자열 (None이면 dsn_write 사용)

    Returns:
        PsycopgDatabasePool 인스턴스
    """
    return PsycopgDatabasePool(dsn_write=dsn_write, dsn_readonly=dsn_readonly)


# ============================================================================
# Transaction Manager Implementations
# ============================================================================


class SQLAlchemyTransactionManager(TransactionManager):
    """SQLAlchemy 기반 트랜잭션 매니저."""

    def __init__(self, db_pool: DatabasePool):
        self._db_pool = db_pool

    async def create_readonly_transaction(self) -> TransactionProtocol:
        """읽기 전용 트랜잭션 생성."""
        session = await self._db_pool.get_connection(mode="readonly")
        return SQLAlchemyTransaction(session, mode="readonly")

    async def create_writable_transaction(self) -> TransactionProtocol:
        """쓰기 트랜잭션 생성."""
        session = await self._db_pool.get_connection(mode="writable")
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
