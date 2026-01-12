"""
Structured logging configuration.

기준: .dev-standards/python/ERROR_HANDLING.md
필수 필드: trace_id, request_id, exception_type, code, path, method, elapsed_ms
"""

import logging
import logging.config
import json
from datetime import datetime, timezone
from typing import Any


class StructuredFormatter(logging.Formatter):
    """JSON 형식의 구조화된 로그 포매터."""
    
    def format(self, record: logging.LogRecord) -> str:
        """로그 레코드를 JSON 문자열로 변환."""
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # 추가 필드 (extra에서 전달된 것)
        if hasattr(record, "__dict__"):
            for key, value in record.__dict__.items():
                if key not in [
                    "name",
                    "msg",
                    "args",
                    "created",
                    "msecs",
                    "levelname",
                    "levelno",
                    "pathname",
                    "filename",
                    "module",
                    "exc_info",
                    "exc_text",
                    "stack_info",
                    "lineno",
                    "funcName",
                    "getMessage",
                ]:
                    log_data[key] = value
        
        # 예외 정보
        if record.exc_info:
            log_data["exc_info"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


def configure_logging(
    log_level: str = "INFO",
    json_format: bool = True,
) -> None:
    """애플리케이션 로깅 설정.
    
    Args:
        log_level: 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: JSON 포맷 사용 여부
    """
    
    formatter = (
        StructuredFormatter() if json_format
        else logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    )
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(formatter)
    
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.addHandler(console_handler)
    
    # 외부 라이브러리 로그 레벨 조정 (노이즈 감소)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("psycopg").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)


class RequestContextLogger:
    """요청 컨텍스트 기반 로깅 헬퍼.
    
    trace_id, request_id 등을 로그에 자동 추가.
    """
    
    def __init__(self, logger: logging.Logger, trace_id: str | None = None):
        self.logger = logger
        self.trace_id = trace_id or self._generate_id()
        self.extra = {"trace_id": self.trace_id}
    
    @staticmethod
    def _generate_id() -> str:
        """간단한 ID 생성 (프로덕션에서는 UUID 권장)."""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def info(self, message: str, **kwargs) -> None:
        """INFO 레벨 로그."""
        extra = {**self.extra, **kwargs}
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, **kwargs) -> None:
        """WARNING 레벨 로그."""
        extra = {**self.extra, **kwargs}
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, **kwargs) -> None:
        """ERROR 레벨 로그."""
        extra = {**self.extra, **kwargs}
        self.logger.error(message, extra=extra)
    
    def debug(self, message: str, **kwargs) -> None:
        """DEBUG 레벨 로그."""
        extra = {**self.extra, **kwargs}
        self.logger.debug(message, extra=extra)
