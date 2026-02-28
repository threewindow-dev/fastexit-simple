"""Portfolio domain errors."""

from shared.errors import DomainError


class DuplicateEntityError(DomainError):
    def __init__(self, entity: str, key: str):
        super().__init__(
            code=f"{entity.upper()}_DUPLICATE",
            message=f"{entity} with key '{key}' already exists",
        )


class NotFoundError(DomainError):
    def __init__(self, entity: str, key: str | int):
        super().__init__(
            code=f"{entity.upper()}_NOT_FOUND",
            message=f"{entity} '{key}' not found",
        )


class InvalidStateError(DomainError):
    def __init__(self, entity: str, message: str):
        super().__init__(code=f"{entity.upper()}_INVALID_STATE", message=message)


class SnapshotLockedError(DomainError):
    def __init__(self, snapshot_id: int):
        super().__init__(
            code="SNAPSHOT_LOCKED",
            message=f"Snapshot {snapshot_id} is locked and cannot be modified",
        )


class SnapshotUnlockNotAllowedError(DomainError):
    def __init__(self, snapshot_id: int, reason: str):
        super().__init__(
            code="SNAPSHOT_UNLOCK_NOT_ALLOWED",
            message=f"Snapshot {snapshot_id} cannot be unlocked: {reason}",
        )


class DeletionConflictError(DomainError):
    def __init__(self, entity: str, reason: str):
        super().__init__(code=f"{entity.upper()}_DELETE_CONFLICT", message=reason)
