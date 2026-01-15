"""
Shared decorators for transaction and authentication control.

ContextVar를 사용한 트랜잭션 데코레이터와 인증 데코레이터.
AppService와 Repository에서 트랜잭션을 자동으로 관리하고,
엔드포인트에서 인증을 검증합니다.
"""

from functools import wraps
from typing import Callable, Any

from fastapi import HTTPException, status

from shared.context import (
    get_current_transaction,
    get_current_connection,
    set_current_transaction,
    clear_current_transaction,
    has_active_transaction,
    get_authenticated_user,
)
from shared.protocols.transaction import TransactionManager, TransactionMode, Connection
from shared.errors import InfraError


def transactional(mode: TransactionMode = "writable", required: bool = True):
    """AppService 메서드에서 트랜잭션을 자동으로 관리하는 데코레이터.

    이미 활성화된 트랜잭션이 있으면 재사용하고,
    없으면 새로운 트랜잭션을 시작합니다.

    Args:
        mode: 트랜잭션 모드 ("readonly" | "writable")
        required: 트랜잭션이 필수인지 여부

    Example:
        class UserAppService:
            def __init__(self, tx_manager: TransactionManager, user_repo: UserRepository):
                self._txm = tx_manager
                self._user_repo = user_repo

            @transactional(mode="writable")
            async def create_user(self, cmd: CreateUserCommand) -> UserDTO:
                # 자동으로 트랜잭션 시작
                user = User.create(cmd.username, cmd.email)
                saved = await self._user_repo.add(user)
                return UserDTO.from_domain(saved)

            @transactional(mode="readonly")
            async def get_user(self, user_id: int) -> UserDTO:
                # 읽기 전용 트랜잭션
                user = await self._user_repo.find_by_id(user_id)
                if not user:
                    raise UserNotFoundError(user_id)
                return UserDTO.from_domain(user)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> Any:
            # 이미 활성화된 트랜잭션이 있으면 재사용
            if has_active_transaction():
                return await func(self, *args, **kwargs)

            # TransactionManager가 없으면 에러
            if not hasattr(self, "_txm"):
                if required:
                    raise InfraError(
                        f"{self.__class__.__name__} must have '_txm' attribute for @transactional decorator"
                    )
                # required=False면 트랜잭션 없이 실행
                return await func(self, *args, **kwargs)

            tx_manager: TransactionManager = self._txm

            # 새로운 트랜잭션 시작
            if mode == "readonly":
                tx = await tx_manager.create_readonly_transaction()
            else:
                tx = await tx_manager.create_writable_transaction()

            # ContextVar에 트랜잭션 설정
            set_current_transaction(tx)

            try:
                async with tx:
                    result = await func(self, *args, **kwargs)
                    return result
            finally:
                # 트랜잭션 정리
                clear_current_transaction()

        return wrapper

    return decorator


def use_transaction(required: bool = True):
    """Repository 메서드에서 현재 트랜잭션의 커넥션을 자동으로 획득하는 데코레이터.

    ContextVar에서 현재 활성 트랜잭션의 커넥션을 가져와서
    첫 번째 파라미터로 주입합니다.

    Args:
        required: 트랜잭션이 필수인지 여부

    Example:
        class UserRepository:
            @use_transaction()
            async def find_by_id(self, user_id: int) -> User | None:
                # 실제 시그니처는 find_by_id(self, conn: Connection, user_id: int)
                # conn이 자동으로 첫 번째 파라미터로 주입됨
                pass

            async def find_by_id(self, conn: Connection, user_id: int) -> User | None:
                # 실제 구현 - conn을 첫 번째 파라미터로 받음
                result = await conn.execute(
                    select(UserEntity).where(UserEntity.id == user_id)
                )
                orm = result.scalar_one_or_none()
                return self._to_domain(orm) if orm else None
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> Any:
            conn = get_current_connection()

            if conn is None:
                if required:
                    raise InfraError(
                        f"No active transaction for {func.__name__}. "
                        f"Use @transactional decorator in AppService method."
                    )
                # required=False면 커넥션 없이 실행 (테스트용)
                return await func(self, *args, **kwargs)

            # 커넥션을 첫 번째 파라미터로 주입
            return await func(self, conn, *args, **kwargs)

        return wrapper

    return decorator


def propagates_transaction(func: Callable) -> Callable:
    """다른 AppService를 호출할 때 트랜잭션을 전파하는 데코레이터.

    이미 트랜잭션이 있으면 그대로 사용하고,
    없으면 호출된 AppService에서 새로 시작합니다.

    이 데코레이터는 실제로는 @transactional이 자동으로 처리하므로
    명시적 표현을 위한 문서화 목적으로 사용합니다.

    Example:
        class OrderAppService:
            @transactional(mode="writable")
            async def create_order(self, cmd: CreateOrderCommand) -> OrderDTO:
                # UserAppService 호출 - 같은 트랜잭션 사용
                user = await self._user_app_service.get_user(cmd.user_id)

                order = Order.create(user_id=user.id, items=cmd.items)
                saved = await self._order_repo.add(order)
                return OrderDTO.from_domain(saved)

        class UserAppService:
            @propagates_transaction  # 명시적 문서화
            @transactional(mode="readonly")
            async def get_user(self, user_id: int) -> UserDTO:
                user = await self._user_repo.find_by_id(user_id)
                if not user:
                    raise UserNotFoundError(user_id)
                return UserDTO.from_domain(user)
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs) -> Any:
        # 그냥 원래 함수 실행 (@transactional이 처리함)
        return await func(self, *args, **kwargs)

    return wrapper


# ============================================================================
# 인증 관련 데코레이터
# ============================================================================


def authenticate_required(func: Callable) -> Callable:
    """
    인증된 사용자만 접근 가능한 엔드포인트를 표시하는 데코레이터

    ContextVar에서 현재 인증된 사용자 정보를 확인하고,
    없으면 401 Unauthorized 에러를 반환합니다.

    Usage:
        @router.get("/protected")
        @authenticate_required
        async def protected_endpoint():
            user = get_authenticated_user()
            return {"user_id": user.user_id}

    Args:
        func: 데코레이팅할 엔드포인트 함수

    Returns:
        인증 검증이 추가된 래퍼 함수
    """

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        authenticated_user = get_authenticated_user()

        if not authenticated_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증이 필요합니다",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return await func(*args, **kwargs)

    return wrapper


def role_required(*allowed_roles: str) -> Callable:
    """
    특정 역할을 가진 사용자만 접근 가능한 엔드포인트를 표시하는 데코레이터

    ContextVar에서 현재 인증된 사용자의 역할을 확인하고,
    필요한 역할이 없으면 403 Forbidden 에러를 반환합니다.

    Usage:
        @router.delete("/admin-only")
        @role_required("admin", "superuser")
        async def admin_endpoint():
            user = get_authenticated_user()
            return {"deleted": True}

    Args:
        *allowed_roles: 접근이 허용되는 역할들

    Returns:
        역할 검증이 추가된 데코레이터
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            authenticated_user = get_authenticated_user()

            # 1. 먼저 인증 여부 확인
            if not authenticated_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="인증이 필요합니다",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # 2. 사용자의 역할이 허용된 역할에 포함되는지 확인
            if authenticated_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"이 작업을 수행할 권한이 없습니다. 필요 역할: {', '.join(allowed_roles)}",
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
