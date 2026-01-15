"""
컨텍스트 관리 통합 모듈 (Facade Pattern)

모든 ContextVar 관련 기능을 한 곳에서 import 가능하도록 Facade 제공.
Transaction Context와 Auth Context를 통합 관리합니다.

Usage:
    from shared.context import (
        get_authenticated_user,
        get_transaction,
        clear_all_contexts
    )
"""

# Auth Context
from .auth_context import (
    AuthenticatedUser,
    authenticated_user_context,
    get_authenticated_user,
    set_authenticated_user,
    clear_authenticated_user,
)

# Transaction Context
from .transaction_context import (
    transaction_context,
    get_transaction,
    get_connection,
    set_transaction,
    clear_transaction,
    has_active_transaction,
    # 하위 호환성을 위한 별칭
    get_current_transaction,
    get_current_connection,
    set_current_transaction,
    clear_current_transaction,
)


def clear_all_contexts() -> None:
    """모든 요청 컨텍스트를 초기화합니다.
    
    Middleware에서 요청 종료 시 호출하여 메모리 누수를 방지합니다.
    """
    clear_authenticated_user()
    clear_transaction()


__all__ = [
    # Auth Context
    "AuthenticatedUser",
    "authenticated_user_context",
    "get_authenticated_user",
    "set_authenticated_user",
    "clear_authenticated_user",
    # Transaction Context
    "transaction_context",
    "get_transaction",
    "get_connection",
    "set_transaction",
    "clear_transaction",
    "has_active_transaction",
    # 하위 호환성
    "get_current_transaction",
    "get_current_connection",
    "set_current_transaction",
    "clear_current_transaction",
    # Utilities
    "clear_all_contexts",
]
