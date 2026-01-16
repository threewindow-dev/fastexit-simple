"""
Application Configuration.

모든 환경변수 기본값 및 설정을 중앙 관리합니다.
기준: .dev-standards/python/CONFIGURATION_STANDARDS.md
"""

import os
from dataclasses import dataclass
from typing import Literal


@dataclass
class DatabaseConfig:
    """데이터베이스 연결 설정."""

    # Primary (Writable) Database
    host: str
    port: int
    name: str
    user: str
    password: str

    # Pool 설정
    pool_size: int
    max_overflow: int
    sql_echo: bool

    # Readonly Database (선택적)
    readonly_enabled: bool
    readonly_host: str | None = None
    readonly_port: int | None = None
    readonly_name: str | None = None
    readonly_user: str | None = None
    readonly_password: str | None = None

    @classmethod
    def from_env(cls, prefix: str = "DB_") -> "DatabaseConfig":
        """환경변수에서 데이터베이스 설정 로드.

        Args:
            prefix: 환경변수 접두사 (예: "DB_", "DB_READONLY_")

        Returns:
            DatabaseConfig 인스턴스
        """
        password = os.getenv(f"{prefix}PASSWORD")
        if not password and prefix == "DB_":
            raise ValueError(f"{prefix}PASSWORD environment variable is required")

        # Primary DB 설정 (폴백: DB_* 환경변수)
        host = os.getenv(f"{prefix}HOST", os.getenv("DB_HOST", "localhost"))
        port = int(os.getenv(f"{prefix}PORT", os.getenv("DB_PORT", "5432")))
        name = os.getenv(f"{prefix}NAME", os.getenv("DB_NAME", "fastexit"))
        user = os.getenv(f"{prefix}USER", os.getenv("DB_USER", "postgres"))

        # Pool 설정
        pool_size = int(os.getenv("DB_POOL_SIZE", "5"))
        max_overflow = int(os.getenv("DB_MAX_OVERFLOW", "10"))
        sql_echo = os.getenv("SQL_ECHO", "false").lower() == "true"

        # Readonly DB 설정
        readonly_enabled = os.getenv("DB_READONLY_ENABLED", "false").lower() == "true"

        config = cls(
            host=host,
            port=port,
            name=name,
            user=user,
            password=password or "",
            pool_size=pool_size,
            max_overflow=max_overflow,
            sql_echo=sql_echo,
            readonly_enabled=readonly_enabled,
        )

        # Readonly 설정 로드
        if readonly_enabled:
            config.readonly_host = os.getenv("DB_READONLY_HOST", host)
            config.readonly_port = int(os.getenv("DB_READONLY_PORT", str(port)))
            config.readonly_name = os.getenv("DB_READONLY_NAME", name)
            config.readonly_user = os.getenv("DB_READONLY_USER", user)
            config.readonly_password = os.getenv("DB_READONLY_PASSWORD", password or "")

        return config

    def get_connection_string(self, readonly: bool = False) -> str:
        """PostgreSQL 연결 문자열 생성.

        Args:
            readonly: True면 readonly DB 연결 문자열 반환

        Returns:
            postgresql://user:password@host:port/dbname
        """
        if readonly and self.readonly_enabled:
            host = self.readonly_host or self.host
            port = self.readonly_port or self.port
            name = self.readonly_name or self.name
            user = self.readonly_user or self.user
            password = self.readonly_password or self.password
        else:
            host = self.host
            port = self.port
            name = self.name
            user = self.user
            password = self.password

        return f"postgresql://{user}:{password}@{host}:{port}/{name}"


@dataclass
class AuthConfig:
    """인증 설정."""

    jwt_secret: str
    jwt_algorithm: str
    jwt_expires_in_minutes: int

    @classmethod
    def from_env(cls) -> "AuthConfig":
        """환경변수에서 인증 설정 로드."""
        jwt_secret = os.getenv("JWT_SECRET", "dev-secret-key-change-in-production")
        jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        jwt_expires_in_minutes = int(os.getenv("JWT_EXPIRES_IN_MINUTES", "60"))

        return cls(
            jwt_secret=jwt_secret,
            jwt_algorithm=jwt_algorithm,
            jwt_expires_in_minutes=jwt_expires_in_minutes,
        )


@dataclass
class AppConfig:
    """애플리케이션 전체 설정."""

    # Repository 타입
    repository_type: Literal["sqlalchemy", "psycopg"]

    # Database 설정
    database: DatabaseConfig

    # Auth 설정
    auth: AuthConfig

    # Logging 설정
    log_level: str
    log_json_format: bool

    @classmethod
    def from_env(cls) -> "AppConfig":
        """환경변수에서 전체 설정 로드."""
        repository_type = os.getenv("REPOSITORY_TYPE", "sqlalchemy")
        if repository_type not in ("sqlalchemy", "psycopg"):
            raise ValueError(
                f"Invalid REPOSITORY_TYPE: {repository_type}. "
                "Must be 'sqlalchemy' or 'psycopg'"
            )

        return cls(
            repository_type=repository_type,  # type: ignore
            database=DatabaseConfig.from_env(),
            auth=AuthConfig.from_env(),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_json_format=os.getenv("LOG_JSON_FORMAT", "true").lower() == "true",
        )


# 전역 설정 인스턴스
_config: AppConfig | None = None


def get_config() -> AppConfig:
    """전역 설정 인스턴스 반환.

    처음 호출 시 환경변수에서 로드하여 캐싱합니다.
    """
    global _config
    if _config is None:
        _config = AppConfig.from_env()
    return _config
