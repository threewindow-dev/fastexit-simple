"""
FastAPI Dependency Injection.

기준: .dev-standards/python/FASTAPI_DEVELOPMENT_STANDARDS.md
- Router에서 구체적 구현체 직접 참조 제거
- 환경변수 기반 저장소 타입 선택
- FastAPI Depends()로 의존성 주입
"""

import os
from typing import AsyncGenerator, Callable, Awaitable

from infra.database import DatabasePool
from shared.protocols.transaction import TransactionProtocol
from subdomains.user.infra.repositories.user_repository import UserRepository
from subdomains.user.infra.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from subdomains.user.infra.repositories.psycopg_user_repository import PsycopgUserRepository
from subdomains.user.application.services.user_app_service import UserAppService
from infra.database import SQLAlchemyTransaction, PsycopgTransaction


# ============================================================================
# 전역 DatabasePool 인스턴스
# ============================================================================

_db_pool: DatabasePool | None = None


def set_db_pool(pool: DatabasePool) -> None:
    """DatabasePool 전역 인스턴스 설정 (main.py에서 호출)."""
    global _db_pool
    _db_pool = pool


def get_db_pool() -> DatabasePool:
    """DatabasePool 인스턴스 반환."""
    if _db_pool is None:
        raise RuntimeError("DatabasePool not initialized. Call set_db_pool() first.")
    return _db_pool


# ============================================================================
# Application Service 의존성
# ============================================================================

async def get_user_app_service() -> AsyncGenerator[UserAppService, None]:
    """
    UserAppService 인스턴스 생성 및 의존성 주입.
    
    - repository: 환경변수 기반 자동 선택
    - transaction_factory: 환경변수 기반 자동 선택
    - Repository와 Transaction이 동일한 세션/연결 사용
    
    사용 예시 (Router):
        @router.post("/users")
        async def create_user(
            command: RegisterUserCommand,
            service: UserAppService = Depends(get_user_app_service)
        ):
            result = await service.create_user(command)
            return result
    """
    db_pool = get_db_pool()
    repository_type = os.getenv("REPOSITORY_TYPE", "sqlalchemy")
    
    if repository_type == "sqlalchemy":
        # SQLAlchemy: 동일한 세션 사용
        session = await db_pool.get_session()
        try:
            repository = SQLAlchemyUserRepository(session)
            
            async def tx_factory() -> TransactionProtocol:
                return SQLAlchemyTransaction(session)
            
            service = UserAppService(
                user_repository=repository,
                transaction_factory=tx_factory
            )
            yield service
        finally:
            await session.close()
    else:
        # Psycopg: 동일한 연결 사용
        conn = await db_pool.get_connection()
        try:
            repository = PsycopgUserRepository(conn)
            
            async def tx_factory() -> TransactionProtocol:
                return PsycopgTransaction(conn)
            
            service = UserAppService(
                user_repository=repository,
                transaction_factory=tx_factory
            )
            yield service
        finally:
            await conn.close()
