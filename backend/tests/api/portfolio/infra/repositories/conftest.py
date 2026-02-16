"""Portfolio integration test configuration and fixtures"""

import pytest
import pytest_asyncio
import psycopg
from pathlib import Path


def _get_schema_files() -> list[Path]:
    """Get all SQL schema files in order (numerically sorted)"""
    schema_dir = Path(__file__).resolve().parents[5] / "sql" / "schema"
    if not schema_dir.exists():
        raise FileNotFoundError(f"Schema directory not found: {schema_dir}")

    sql_files = sorted(schema_dir.glob("*.sql"))
    if not sql_files:
        raise FileNotFoundError(f"No SQL files found in {schema_dir}")

    return sql_files


async def _initialize_schema(conn: psycopg.AsyncConnection) -> None:
    """Initialize database schema by executing all SQL files"""
    schema_files = _get_schema_files()

    async with conn.cursor() as cur:
        for sql_file in schema_files:
            sql_content = sql_file.read_text()
            if "BEGIN;" in sql_content or "begin;" in sql_content.lower():
                await cur.execute(sql_content)
            else:
                statements = [
                    s.strip()
                    for s in sql_content.split(";")
                    if s.strip() and not s.strip().startswith("--")
                ]
                for stmt in statements:
                    try:
                        await cur.execute(stmt)
                    except Exception as e:
                        if (
                            "already exists" not in str(e).lower()
                            and "duplicate key" not in str(e).lower()
                        ):
                            raise

    await conn.commit()


@pytest_asyncio.fixture()
async def db_connection(postgres_container):
    """Create database connection and initialize schema from SQL files"""
    conn_str = postgres_container.get_connection_url()
    conn_str = conn_str.replace("postgresql+psycopg2", "postgresql").replace(
        "postgresql+psycopg", "postgresql"
    )

    async with await psycopg.AsyncConnection.connect(
        conn_str, autocommit=False, row_factory=psycopg.rows.dict_row
    ) as conn:
        await _initialize_schema(conn)
        yield conn


@pytest_asyncio.fixture
async def clean_db(db_connection):
    """Clean database before each test"""
    try:
        await db_connection.rollback()
    except Exception:
        pass

    async with db_connection.cursor() as cur:
        # Drop all tables in dependency order
        await cur.execute("DROP TABLE IF EXISTS annual_snapshot_holdings CASCADE")
        await cur.execute("DROP TABLE IF EXISTS annual_snapshots CASCADE")
        await cur.execute("DROP TABLE IF EXISTS weekly_snapshot_holdings CASCADE")
        await cur.execute("DROP TABLE IF EXISTS weekly_snapshots CASCADE")
        await cur.execute("DROP TABLE IF EXISTS snapshot_holdings CASCADE")
        await cur.execute("DROP TABLE IF EXISTS snapshots CASCADE")
        await cur.execute("DROP TABLE IF EXISTS holdings CASCADE")
        await cur.execute("DROP TABLE IF EXISTS account_group_accounts CASCADE")
        await cur.execute("DROP TABLE IF EXISTS account_groups CASCADE")
        await cur.execute("DROP TABLE IF EXISTS accounts CASCADE")
        await cur.execute("DROP TABLE IF EXISTS products CASCADE")
        await cur.execute("DROP TABLE IF EXISTS institutions CASCADE")
        await cur.execute("DROP TABLE IF EXISTS users CASCADE")

    await db_connection.commit()

    # Re-initialize schema
    await _initialize_schema(db_connection)

    yield

    # Cleanup after test
    try:
        await db_connection.rollback()
    except Exception:
        pass
