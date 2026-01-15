"""
Authentication middleware for FastAPI.

모든 요청에서 Authorization 헤더를 검증하고
ContextVar에 인증 정보를 저장하는 Middleware
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

from shared.context import (
    AuthenticatedUser,
    set_authenticated_user,
    clear_all_contexts,
)
from shared.protocols.auth import TokenManager

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    모든 요청에서 Authorization 헤더를 검증하고
    ContextVar에 인증 정보를 저장하는 Middleware

    TokenManager Protocol에 의존하여 구체적 구현과 분리됩니다.
    Transaction Context와 함께 요청 생명주기 동안 인증 정보를 관리합니다.

    Attributes:
        token_manager: JWT 토큰 검증을 담당하는 TokenManager

    Example:
        from core.middleware import AuthenticationMiddleware
        from shared.infra.auth import JWTTokenManager

        token_manager = JWTTokenManager(secret_key="your-secret-key")
        app.add_middleware(AuthenticationMiddleware, token_manager=token_manager)
    """

    def __init__(self, app, token_manager: TokenManager):
        """
        Args:
            app: FastAPI 애플리케이션 인스턴스
            token_manager: TokenManager Protocol 구현체
        """
        super().__init__(app)
        self.token_manager = token_manager

    async def dispatch(self, request: Request, call_next):
        """
        요청 처리 및 인증 검증

        1. Authorization 헤더에서 Bearer 토큰 추출
        2. 토큰 검증 및 payload 추출
        3. AuthenticatedUser 생성 및 ContextVar에 저장
        4. 요청 처리
        5. ContextVar 정리

        Args:
            request: FastAPI Request 객체
            call_next: 다음 미들웨어 또는 라우터 핸들러

        Returns:
            Response 객체
        """
        # Authorization 헤더 추출
        auth_header = request.headers.get("Authorization", "")

        # Bearer 토큰 추출
        token = self._extract_bearer_token(auth_header)

        if token:
            # 토큰 검증
            try:
                payload = self.token_manager.verify_token(token)
            except Exception as e:
                # 구현체가 예외를 던지는 경우도 안전하게 처리
                logger.debug(f"Token verification error: {e}")
                payload = None

            if payload:
                # AuthenticatedUser 생성 및 ContextVar에 저장
                authenticated_user = AuthenticatedUser(
                    user_id=payload.get("user_id"),
                    role=payload.get("role"),
                    metadata=payload.get("metadata"),
                )
                set_authenticated_user(authenticated_user)
                logger.debug(f"User authenticated: {authenticated_user.user_id}")
            else:
                logger.debug("Invalid or expired token")
        else:
            logger.debug("No authorization token provided")

        try:
            # 요청 처리
            response = await call_next(request)
            return response
        finally:
            # 응답 후 모든 요청 컨텍스트 초기화 (메모리 누수 방지)
            # 인증 컨텍스트와 트랜잭션 컨텍스트를 함께 초기화합니다.
            clear_all_contexts()

    @staticmethod
    def _extract_bearer_token(auth_header: str) -> str | None:
        """
        Authorization 헤더에서 Bearer 토큰 추출

        Args:
            auth_header: HTTP Authorization 헤더 값

        Returns:
            Bearer 토큰 문자열, 없으면 None

        Example:
            >>> _extract_bearer_token("Bearer abc123")
            'abc123'
            >>> _extract_bearer_token("Basic xyz")
            None
        """
        if not auth_header.startswith("Bearer "):
            return None
        return auth_header[7:]  # 'Bearer ' 이후의 문자열
