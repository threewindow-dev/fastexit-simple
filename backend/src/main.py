import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.exception_handlers import register_exception_handlers
from shared.schemas import ApiResponse
from core.logging import configure_logging
from shared.infra.database import db_pool_factory
from core.dependencies import set_db_pool
from subdomains.user.interface.routers.user_router import router as user_router

# 로깅 설정
configure_logging(log_level="INFO", json_format=True)
logger = logging.getLogger(__name__)

# DatabasePool 생성 (환경변수 기반 factory)
db_pool = db_pool_factory(os.getenv("REPOSITORY_TYPE", "sqlalchemy"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifespan handler replacing deprecated on_event hooks."""
    # Startup
    await db_pool.initialize()

    # 전역 DatabasePool 설정 (dependencies.py에서 사용)
    set_db_pool(db_pool)

    # 데이터베이스 테이블 초기화 (Psycopg용, SQLAlchemy는 필요 시에만 생성)
    repository_type = os.getenv("REPOSITORY_TYPE", "sqlalchemy")

    if repository_type == "psycopg":
        async with db_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        full_name VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
                await cur.execute("SELECT COUNT(*) FROM users")
                result = await cur.fetchone()
                count = result["count"] if result else 0
                if count == 0:
                    sample_users = [
                        ("john_doe", "john@example.com", "John Doe"),
                        ("jane_smith", "jane@example.com", "Jane Smith"),
                        ("bob_wilson", "bob@example.com", "Bob Wilson"),
                    ]
                    for username, email, full_name in sample_users:
                        await cur.execute(
                            "INSERT INTO users (username, email, full_name) VALUES (%s, %s, %s)",
                            (username, email, full_name),
                        )
                await conn.commit()
    else:
        # SQLAlchemy: create_all 수행
        # Note: DatabasePool exposes write/read engines as _engine_write/_engine_readonly
        engine = getattr(db_pool, "_engine_write", None)
        if engine:
            async with engine.begin() as conn:
                await conn.run_sync(lambda sync_conn: _create_all_tables(sync_conn))

    logger.info(
        f"Database initialized successfully (repository_type={repository_type})"
    )
    try:
        yield
    finally:
        await db_pool.close()
        logger.info("Database pool closed")


def _create_all_tables(sync_conn):
    """SQLAlchemy ORM 모델의 모든 테이블 생성."""
    from shared.infra.database import Base

    # ORM 모델 import하여 메타데이터 등록
    from subdomains.user.infra.models import UserORM  # noqa: F401

    Base.metadata.create_all(sync_conn)


app = FastAPI(title="FastExit API", lifespan=lifespan)

# 전역 예외 핸들러 등록
register_exception_handlers(app)

# User 라우터 등록 (Depends를 통한 DI)
app.include_router(user_router)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """헬스 체크"""
    return ApiResponse(code=0, message="success", data={"status": "healthy"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
