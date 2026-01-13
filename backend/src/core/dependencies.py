"""
FastAPI Dependency Injection.

기준: .dev-standards/python/FASTAPI_DEVELOPMENT_STANDARDS.md
- Router에서 구체적 구현체 직접 참조 제거
- 환경변수 기반 저장소 타입 선택
- FastAPI Depends()로 의존성 주입
"""

import os
from typing import AsyncGenerator

from shared.infra.database import DatabasePool, SQLAlchemyTransactionManager, PsycopgTransactionManager
from subdomains.user.infra.repositories import SQLAlchemyUserRepository, PsycopgUserRepository
from subdomains.user.application.services.user_app_service import UserAppService


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
    - transaction_manager: readonly/writable 트랜잭션 생성 관리
    
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
        # SQLAlchemy: TransactionManager가 세션 생성 관리
        tx_manager = SQLAlchemyTransactionManager(db_pool)
        repository = SQLAlchemyUserRepository()
        
        service = UserAppService(
            user_repository=repository,
            transaction_manager=tx_manager,
        )
        yield service
    else:
        # Psycopg: TransactionManager가 연결 생성 관리
        tx_manager = PsycopgTransactionManager(db_pool)
        repository = PsycopgUserRepository()
        
        service = UserAppService(
            user_repository=repository,
            transaction_manager=tx_manager,
        )
        yield service
