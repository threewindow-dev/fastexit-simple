"""
FastAPI exception handlers for standardized response format.

기준: .dev-standards/python/ERROR_HANDLING.md
응답 포맷: {code, message, data}
"""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError

from shared.errors import (
    DomainError,
    ApplicationError,
    InfraError,
    ValidationError,
)
from subdomains.user.domain.errors import UserNotFoundError


logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """FastAPI 애플리케이션에 전역 예외 핸들러 등록."""

    @app.exception_handler(DomainError)
    async def handle_domain_error(request: Request, exc: DomainError):
        """비즈니스 규칙 위반 (400 Bad Request)."""
        return JSONResponse(
            status_code=400,
            content={
                "code": exc.code,
                "message": str(exc),
                "data": None,
            },
        )

    @app.exception_handler(ApplicationError)
    async def handle_application_error(request: Request, exc: ApplicationError):
        """유스케이스/애플리케이션 실패 (400 Bad Request)."""
        return JSONResponse(
            status_code=400,
            content={
                "code": exc.code,
                "message": str(exc),
                "data": None,
            },
        )

    @app.exception_handler(UserNotFoundError)
    async def handle_user_not_found_error(request: Request, exc: UserNotFoundError):
        """리소스 미존재 (404 Not Found)."""
        return JSONResponse(
            status_code=404,
            content={
                "code": exc.code,
                "message": str(exc),
                "data": None,
            },
        )

    @app.exception_handler(InfraError)
    async def handle_infra_error(request: Request, exc: InfraError):
        """기술적 장애 (503 Service Unavailable)."""
        # 클라이언트 노이즈 감소: 상세 메시지 제거, 로그만 남김
        logger.error(
            f"Infrastructure error: {exc.code}",
            extra={
                "exception_type": "InfraError",
                "code": exc.code,
                "error_details": str(exc),
                "origin_exc": str(exc.origin_exc) if exc.origin_exc else None,
            },
        )
        return JSONResponse(
            status_code=503,
            content={
                "code": exc.code,
                "message": "Temporary service error",
                "data": None,
            },
        )

    @app.exception_handler(ValidationError)
    async def handle_validation_error(request: Request, exc: ValidationError):
        """입력 검증 실패 (400 Bad Request)."""
        return JSONResponse(
            status_code=400,
            content={
                "code": exc.code,
                "message": str(exc),
                "data": exc.details if exc.details else None,
            },
        )

    @app.exception_handler(PydanticValidationError)
    async def handle_pydantic_validation_error(
        request: Request, exc: PydanticValidationError
    ):
        """Pydantic 스키마 검증 실패 (400 Bad Request)."""
        # errors()는 복잡한 중첩 구조이므로 요약/필드 기준으로 가공
        simplified = [
            {
                "loc": ".".join(map(str, err.get("loc", []))),
                "msg": err.get("msg", "validation error"),
                "type": err.get("type", ""),
            }
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=400,
            content={
                "code": "INVALID_REQUEST",
                "message": "Request validation failed",
                "data": simplified,
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception):
        """미처리 예외 (500 Internal Server Error)."""
        logger.error(
            f"Unexpected error: {type(exc).__name__}",
            exc_info=True,
            extra={
                "exception_type": type(exc).__name__,
                "error_details": str(exc),
            },
        )
        return JSONResponse(
            status_code=500,
            content={
                "code": "UNEXPECTED_ERROR",
                "message": "Internal server error",
                "data": None,
            },
        )
