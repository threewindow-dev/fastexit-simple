"""
Transaction context management using ContextVar.

ContextVar를 사용한 트랜잭션 컨텍스트 관리.
비동기 요청별로 격리된 트랜잭션 상태를 유지합니다.
"""

from contextvars import ContextVar

from shared.protocols.transaction import TransactionProtocol, Connection


# ContextVar: 비동기 컨텍스트별로 격리된 트랜잭션 저장
_transaction_context: ContextVar[TransactionProtocol | None] = ContextVar(
    "transaction_context", default=None
)


def get_current_transaction() -> TransactionProtocol | None:
    """현재 활성화된 트랜잭션을 반환합니다.
    
    Returns:
        TransactionProtocol | None: 활성 트랜잭션, 없으면 None
    """
    return _transaction_context.get()


def get_current_connection() -> Connection | None:
    """현재 트랜잭션의 DB 커넥션을 반환합니다.
    
    Returns:
        Connection | None: DB 커넥션, 트랜잭션이 없으면 None
    """
    tx = _transaction_context.get()
    return tx.connection if tx else None


def set_current_transaction(transaction: TransactionProtocol) -> None:
    """현재 트랜잭션을 설정합니다.
    
    Args:
        transaction: 설정할 트랜잭션
    """
    _transaction_context.set(transaction)


def clear_current_transaction() -> None:
    """현재 트랜잭션을 제거합니다."""
    _transaction_context.set(None)


def has_active_transaction() -> bool:
    """현재 활성화된 트랜잭션이 있는지 확인합니다.
    
    Returns:
        bool: 트랜잭션이 있으면 True
    """
    return _transaction_context.get() is not None
