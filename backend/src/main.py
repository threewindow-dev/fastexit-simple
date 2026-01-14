import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.exception_handlers import register_exception_handlers
from shared.schemas import ApiResponse
from core.logging import configure_logging
from shared.infra.database import db_pool_factory
from dependencies import set_db_pool
from subdomains.user.interface.routers import router as user_router

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
        # SQL 파일에서 스키마 로드
        await _initialize_schema_from_sql(db_pool)
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


async def _initialize_schema_from_sql(db_pool):
    """SQL 파일에서 데이터베이스 스키마 초기화.

    sql/schema/ 폴더의 SQL 파일을 숫자 순서대로 실행합니다.
    파일명 형식: NNN_tablename_description.sql (예: 000_users_init.sql)
    """
    # SQL 스키마 파일 경로 (backend/sql/schema/)
    backend_dir = Path(__file__).parent.parent
    schema_dir = backend_dir / "sql" / "schema"

    if not schema_dir.exists():
        logger.warning(f"Schema directory not found: {schema_dir}")
        return

    # SQL 파일을 숫자 순서대로 정렬
    sql_files = sorted(schema_dir.glob("*.sql"))

    if not sql_files:
        logger.warning(f"No SQL files found in {schema_dir}")
        return

    logger.info(f"Initializing database schema from {len(sql_files)} SQL files")

    async with db_pool.connection() as conn:
        async with conn.cursor() as cur:
            for sql_file in sql_files:
                logger.info(f"Executing SQL file: {sql_file.name}")
                sql_content = sql_file.read_text(encoding="utf-8")

                # SQL 파일을 세미콜론으로 분리하여 개별 명령 실행
                for statement in sql_content.split(";"):
                    statement = statement.strip()
                    if statement and not statement.startswith("--"):
                        try:
                            await cur.execute(statement)
                        except Exception as e:
                            logger.error(
                                f"Error executing statement in {sql_file.name}: {e}"
                            )
                            logger.error(f"Statement: {statement[:100]}...")
                            raise

            await conn.commit()
            logger.info("Schema initialization completed successfully")


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
