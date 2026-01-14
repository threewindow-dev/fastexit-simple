"""Shared infrastructure layer - domain-neutral implementations."""

from .database import (
    SQLAlchemyTransaction,
    PsycopgTransaction,
    Base,
    db_pool_factory,
    SQLAlchemyDatabasePool,
    PsycopgDatabasePool,
    SQLAlchemyTransactionManager,
    PsycopgTransactionManager,
)
from ..context import (
    get_current_transaction,
    get_current_connection,
    set_current_transaction,
    clear_current_transaction,
    has_active_transaction,
)
from ..decorators import (
    transactional,
    use_transaction,
    propagates_transaction,
)

__all__ = [
    # Database
    "SQLAlchemyTransaction",
    "PsycopgTransaction",
    "Base",
    "db_pool_factory",
    "SQLAlchemyDatabasePool",
    "PsycopgDatabasePool",
    "SQLAlchemyTransactionManager",
    "PsycopgTransactionManager",
    # Context
    "get_current_transaction",
    "get_current_connection",
    "set_current_transaction",
    "clear_current_transaction",
    "has_active_transaction",
    # Decorators
    "transactional",
    "use_transaction",
    "propagates_transaction",
]
