"""
FastAPI Dependency Injection.

기준: .dev-standards/python/FASTAPI_DEVELOPMENT_STANDARDS.md
- Router에서 구체적 구현체 직접 참조 제거
- core에서 설정 읽기, shared에 주입
- FastAPI Depends()로 의존성 주입
"""

from typing import AsyncGenerator

from fastapi.security import OAuth2PasswordBearer

from core.config import get_config
from shared.protocols.database import DatabasePool
from shared.protocols.auth import TokenManager
from shared.infra.database import (
    SQLAlchemyTransactionManager,
    PsycopgTransactionManager,
)
from shared.infra.auth import JWTTokenManager
from subdomains.user.infra.repositories import (
    SQLAlchemyUserRepository,
    PsycopgUserRepository,
)
from subdomains.user.application.services.user_app_service import UserAppService


# ============================================================================
# 전역 인스턴스
# ============================================================================

_db_pool: DatabasePool | None = None
_token_manager: TokenManager | None = None
_oauth2_scheme: OAuth2PasswordBearer | None = None


def set_db_pool(pool: DatabasePool) -> None:
    """DatabasePool 전역 인스턴스 설정 (main.py에서 호출)."""
    global _db_pool
    _db_pool = pool


def get_db_pool() -> DatabasePool:
    """DatabasePool 인스턴스 반환."""
    if _db_pool is None:
        raise RuntimeError("DatabasePool not initialized. Call set_db_pool() first.")
    return _db_pool


def get_token_manager() -> TokenManager:
    """TokenManager 인스턴스 반환 (싱글톤)."""
    global _token_manager
    if _token_manager is None:
        config = get_config()
        _token_manager = JWTTokenManager(
            secret_key=config.auth.jwt_secret,
            algorithm=config.auth.jwt_algorithm,
        )
    return _token_manager


def get_oauth2_scheme() -> OAuth2PasswordBearer:
    """OAuth2PasswordBearer 인스턴스 반환 (싱글톤).

    Swagger UI의 Authorize 버튼을 표시하기 위해 데코레이터에서 사용되며,
    tokenUrl은 실제 토큰 엔드포인트 경로로 설정됩니다.

    Returns:
        OAuth2PasswordBearer: Bearer 토큰 기반 보안 스킴

    Raises:
        RuntimeError: JWT 설정이 없는 경우
    """
    global _oauth2_scheme
    if _oauth2_scheme is None:
        config = get_config()
        if not hasattr(config, "auth") or not hasattr(config.auth, "token_url"):
            raise RuntimeError(
                "OAuth2 configuration not found. "
                "Ensure AUTH_TOKEN_URL is set in environment."
            )
        _oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.auth.token_url, scopes={})
    return _oauth2_scheme


# ============================================================================
# Application Service 의존성
# ============================================================================


async def get_user_app_service() -> AsyncGenerator[UserAppService, None]:
    """
    UserAppService 인스턴스 생성 및 의존성 주입.

    - repository: 설정 기반 자동 선택
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
    config = get_config()
    db_pool = get_db_pool()

    if config.repository_type == "sqlalchemy":
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
