"""
Shared exception hierarchy for application error handling.

기준: .dev-standards/python/ERROR_HANDLING.md
계층: Domain → Application → Infra → Interface
"""


class BaseAppError(Exception):
    """Base exception class for application errors.
    
    모든 애플리케이션 예외의 기본 클래스.
    origin_exc를 통해 저수준 오류 추적 가능.
    """
    code: str = "APP_ERROR"
    
    def __init__(self, message: str, origin_exc: Exception | None = None, code: str | None = None):
        super().__init__(message)
        # 표준 응답/테스트 호환을 위해 message 필드를 노출
        self.message = message
        # 필요 시 상위에서 전달한 세부 코드로 덮어쓰기 허용
        if code:
            self.code = code
        self.origin_exc = origin_exc  # 디버깅/로깅용 (응답에는 노출하지 않음)


class DomainError(BaseAppError):
    """Domain layer exception.
    
    비즈니스 규칙 위반에만 사용.
    HTTP/DB 세부사항 금지.
    예: InvalidEmailError, InsufficientBalanceError
    """
    code = "DOMAIN_ERROR"
    
    def __init__(self, message: str, origin_exc: Exception | None = None, code: str | None = None):
        super().__init__(message, origin_exc, code)


class ApplicationError(BaseAppError):
    """Application layer exception.
    
    유스케이스/애플리케이션 로직 실패를 표현.
    트랜잭션 경계 안에서 발생.
    재시도하지 않는 논리 오류.
    예: DuplicateUserError, UnauthorizedActionError
    """
    code = "APPLICATION_ERROR"
    
    def __init__(self, message: str, origin_exc: Exception | None = None, code: str | None = None):
        super().__init__(message, origin_exc, code)


class InfraError(BaseAppError):
    """Infrastructure layer exception.
    
    DB/외부 API/메시지 브로커 등 기술적 실패를 래핑.
    드라이버/네트워크/타임아웃 등.
    예: DbTimeoutError, ExternalServiceError
    """
    code = "INFRA_ERROR"
    
    def __init__(self, message: str, origin_exc: Exception | None = None, code: str | None = None):
        super().__init__(message, origin_exc, code)


class ValidationError(BaseAppError):
    """Validation exception.
    
    스키마/DTO/입력 검증 실패.
    Pydantic ValidationError는 전역 핸들러에서 변환.
    """
    code = "VALIDATION_ERROR"
    
    def __init__(self, message: str, details: list | None = None, origin_exc: Exception | None = None, code: str | None = None):
        super().__init__(message, origin_exc, code)
        self.details = details or []


# ============================================================================
# Domain Errors 예시
# ============================================================================

class InvalidEmailError(DomainError):
    code = "INVALID_EMAIL"
    
    def __init__(self, email: str, origin_exc: Exception | None = None):
        super().__init__(f"Invalid email format: {email}", origin_exc)


class InsufficientBalanceError(DomainError):
    code = "INSUFFICIENT_BALANCE"
    
    def __init__(self, balance: float, required: float, origin_exc: Exception | None = None):
        super().__init__(
            f"Insufficient balance: {balance}, required: {required}",
            origin_exc
        )


# ============================================================================
# Application Errors 예시
# ============================================================================

class DuplicateUserError(ApplicationError):
    code = "USER_CREATE_DUPLICATED"
    
    def __init__(self, identifier: str, origin_exc: Exception | None = None):
        super().__init__(f"User already exists: {identifier}", origin_exc)


class UserNotFoundError(ApplicationError):
    code = "USER_GET_NOT_FOUND"
    
    def __init__(self, user_id: int, origin_exc: Exception | None = None):
        super().__init__(f"User not found: {user_id}", origin_exc)


class UnauthorizedActionError(ApplicationError):
    code = "UNAUTHORIZED_ACTION"
    
    def __init__(self, action: str, reason: str, origin_exc: Exception | None = None):
        super().__init__(f"Unauthorized action '{action}': {reason}", origin_exc)


# ============================================================================
# Infra Errors 예시
# ============================================================================

class DbTimeoutError(InfraError):
    code = "DB_TIMEOUT"
    
    def __init__(self, timeout_sec: float, origin_exc: Exception | None = None):
        super().__init__(f"Database operation timeout: {timeout_sec}s", origin_exc)


class DbConnectionError(InfraError):
    code = "DB_CONNECTION_FAILED"
    
    def __init__(self, host: str, origin_exc: Exception | None = None):
        super().__init__(f"Failed to connect to database at {host}", origin_exc)


class ExternalServiceError(InfraError):
    code = "EXTERNAL_SERVICE_ERROR"
    
    def __init__(self, service: str, status: int | None = None, origin_exc: Exception | None = None):
        msg = f"External service error: {service}"
        if status:
            msg += f" (HTTP {status})"
        super().__init__(msg, origin_exc)
