import logging
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.exception_handlers import register_exception_handlers, create_ok_response
from core.logging import configure_logging
from infra.database import db_pool
from domains.user.interface.routers import create_user_router

# 로깅 설정
configure_logging(log_level="INFO", json_format=True)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifespan handler replacing deprecated on_event hooks."""
    # Startup
    await db_pool.initialize()
    # 데이터베이스 테이블 초기화
    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    full_name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
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
    logger.info("Database initialized successfully")
    try:
        yield
    finally:
        await db_pool.close()
        logger.info("Database pool closed")


app = FastAPI(title="FastExit API", lifespan=lifespan)

# 전역 예외 핸들러 등록
register_exception_handlers(app)

# User 라우터 등록 (DB 풀 주입)
app.include_router(create_user_router(db_pool))

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# (Deprecated on_event handlers removed; handled by lifespan)


# ============================================================================
# Pydantic Schemas
# ============================================================================

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    full_name: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None


@app.get("/")
async def root():
    """헬스 체크"""
    return create_ok_response({"status": "healthy"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
