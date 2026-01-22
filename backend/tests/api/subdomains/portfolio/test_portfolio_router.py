"""
API integration tests for Portfolio router

Tests full HTTP endpoints with real database using Testcontainers
"""

import os
import re
from datetime import date

import pytest
import pytest_asyncio
import psycopg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer

import core.config
from dependencies import set_db_pool
from main import register_exception_handlers
from shared.infra.database import create_psycopg_pool
from subdomains.portfolio.interface.routers import router as portfolio_router


@pytest.fixture(scope="module")
def test_app():
    """Create a test FastAPI app without lifespan"""
    app = FastAPI(title="FastExit Portfolio API Test")

    # 전역 예외 핸들러 등록
    register_exception_handlers(app)

    # Portfolio 라우터 등록
    app.include_router(portfolio_router)

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


@pytest.fixture(scope="module")
def postgres_container():
    """Start PostgreSQL container for API tests"""
    container = PostgresContainer("postgres:17-alpine")
    container.start()
    container.waiting_for(
        re.compile(r".*database system is ready to accept connections.*", re.DOTALL)
    )

    # Set environment variables immediately after container starts
    os.environ["DB_HOST"] = str(container.get_container_host_ip())
    os.environ["DB_PORT"] = str(container.get_exposed_port(5432))
    os.environ["DB_NAME"] = str(container.dbname)
    os.environ["DB_USER"] = str(container.username)
    os.environ["DB_PASSWORD"] = str(container.password)

    # Use psycopg repository type for tests
    os.environ["REPOSITORY_TYPE"] = "psycopg"

    # Reset config cache to pick up new environment variables
    core.config._config = None

    yield container
    container.stop()


@pytest_asyncio.fixture()
async def test_db_pool(postgres_container):
    """Create test database pool with initialized schema"""
    conn_str = postgres_container.get_connection_url()
    # Convert SQLAlchemy-style URL to plain psycopg DSN
    conn_str = conn_str.replace("postgresql+psycopg2", "postgresql").replace(
        "postgresql+psycopg", "postgresql"
    )

    # Initialize schema from SQL files
    async with await psycopg.AsyncConnection.connect(
        conn_str, autocommit=True, row_factory=psycopg.rows.dict_row
    ) as conn:
        # Users table (required for snapshots foreign key)
        async with conn.cursor() as cur:
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    full_name VARCHAR(255),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Insert test user
            await cur.execute(
                """
                INSERT INTO users (username, email, full_name)
                VALUES ('test_user', 'test@example.com', 'Test User')
                ON CONFLICT (username) DO NOTHING
                """
            )

        # Portfolio tables
        async with conn.cursor() as cur:
            # Institutions
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS institutions (
                    institution_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    type VARCHAR(50) NOT NULL CHECK (type IN ('증권사', '은행', '기타')),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Products
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id SERIAL PRIMARY KEY,
                    product_name VARCHAR(255) NOT NULL,
                    asset_class VARCHAR(50) NOT NULL CHECK (asset_class IN ('주식', '채권', '통화', '금', '부동산', '가상자산', '기타자산')),
                    region VARCHAR(50) NOT NULL CHECK (region IN ('대한민국', '미국')),
                    currency VARCHAR(10) NOT NULL CHECK (currency IN ('KRW', 'USD')),
                    investment_type VARCHAR(50) NOT NULL CHECK (investment_type IN ('직접', 'ETF')),
                    characteristics TEXT[] NULL,
                    risk_level VARCHAR(20) NOT NULL CHECK (risk_level IN ('안전', '위험')),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (product_name, asset_class, region, currency, investment_type)
                )
            """
            )

            # Accounts
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id SERIAL PRIMARY KEY,
                    institution_id INTEGER NOT NULL REFERENCES institutions(institution_id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (institution_id, name)
                )
            """
            )

            # Account Groups
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS account_groups (
                    account_group_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Account Group - Account mapping
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS account_group_accounts (
                    account_group_id INTEGER NOT NULL REFERENCES account_groups(account_group_id) ON DELETE CASCADE,
                    account_id INTEGER NOT NULL REFERENCES accounts(account_id) ON DELETE CASCADE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (account_group_id, account_id)
                )
            """
            )

            # Holdings
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS holdings (
                    holding_id SERIAL PRIMARY KEY,
                    account_id INTEGER NOT NULL REFERENCES accounts(account_id) ON DELETE CASCADE,
                    product_id INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
                    is_visible BOOLEAN NOT NULL DEFAULT TRUE,
                    deleted_at TIMESTAMP NULL,
                    deletion_reason TEXT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (account_id, product_id)
                )
            """
            )

            # Snapshots
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS snapshots (
                    snapshot_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    reference_date DATE NOT NULL,
                    status VARCHAR(20) NOT NULL CHECK (status IN ('in_progress', 'locked')),
                    locked_at TIMESTAMP NULL,
                    editable_until TIMESTAMP NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (user_id, reference_date)
                )
            """
            )

            # Snapshot holdings
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS snapshot_holdings (
                    snapshot_holding_id SERIAL PRIMARY KEY,
                    snapshot_id INTEGER NOT NULL REFERENCES snapshots(snapshot_id) ON DELETE CASCADE,
                    holding_id INTEGER NOT NULL REFERENCES holdings(holding_id) ON DELETE CASCADE,
                    valuation_amount NUMERIC(20,4) NOT NULL,
                    data_source VARCHAR(10) NOT NULL CHECK (data_source IN ('auto', 'manual', 'missing')),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (snapshot_id, holding_id)
                )
            """
            )

            # Weekly snapshots
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS weekly_snapshots (
                    weekly_snapshot_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    reference_date DATE NOT NULL,
                    source_snapshot_id INTEGER NOT NULL REFERENCES snapshots(snapshot_id) ON DELETE CASCADE,
                    status VARCHAR(20) NOT NULL DEFAULT 'locked',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (user_id, reference_date)
                )
            """
            )

            # Weekly snapshot holdings
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS weekly_snapshot_holdings (
                    weekly_snapshot_holding_id SERIAL PRIMARY KEY,
                    weekly_snapshot_id INTEGER NOT NULL REFERENCES weekly_snapshots(weekly_snapshot_id) ON DELETE CASCADE,
                    holding_id INTEGER NOT NULL REFERENCES holdings(holding_id) ON DELETE CASCADE,
                    valuation_amount NUMERIC(20,4) NOT NULL,
                    data_source VARCHAR(10) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (weekly_snapshot_id, holding_id)
                )
            """
            )

            # Annual snapshots
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS annual_snapshots (
                    annual_snapshot_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    reference_date DATE NOT NULL,
                    source_snapshot_id INTEGER NOT NULL REFERENCES snapshots(snapshot_id) ON DELETE CASCADE,
                    status VARCHAR(20) NOT NULL DEFAULT 'locked',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (user_id, reference_date)
                )
            """
            )

            # Annual snapshot holdings
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS annual_snapshot_holdings (
                    annual_snapshot_holding_id SERIAL PRIMARY KEY,
                    annual_snapshot_id INTEGER NOT NULL REFERENCES annual_snapshots(annual_snapshot_id) ON DELETE CASCADE,
                    holding_id INTEGER NOT NULL REFERENCES holdings(holding_id) ON DELETE CASCADE,
                    valuation_amount NUMERIC(20,4) NOT NULL,
                    data_source VARCHAR(10) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (annual_snapshot_id, holding_id)
                )
            """
            )

    # Build DSN from container
    dsn = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

    pool = create_psycopg_pool(dsn_write=dsn)
    await pool.initialize()

    yield pool

    await pool.close()


@pytest_asyncio.fixture
async def clean_db(test_db_pool):
    """Clean database before each test"""
    conn_str = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"

    async with await psycopg.AsyncConnection.connect(
        conn_str, autocommit=False, row_factory=psycopg.rows.dict_row
    ) as conn:
        try:
            await conn.rollback()
        except Exception:
            pass
        async with conn.cursor() as cur:
            # Drop tables in reverse dependency order
            await cur.execute(
                "TRUNCATE annual_snapshot_holdings RESTART IDENTITY CASCADE"
            )
            await cur.execute("TRUNCATE annual_snapshots RESTART IDENTITY CASCADE")
            await cur.execute(
                "TRUNCATE weekly_snapshot_holdings RESTART IDENTITY CASCADE"
            )
            await cur.execute("TRUNCATE weekly_snapshots RESTART IDENTITY CASCADE")
            await cur.execute("TRUNCATE snapshot_holdings RESTART IDENTITY CASCADE")
            await cur.execute("TRUNCATE snapshots RESTART IDENTITY CASCADE")
            await cur.execute("TRUNCATE holdings RESTART IDENTITY CASCADE")
            await cur.execute(
                "TRUNCATE account_group_accounts RESTART IDENTITY CASCADE"
            )
            await cur.execute("TRUNCATE account_groups RESTART IDENTITY CASCADE")
            await cur.execute("TRUNCATE accounts RESTART IDENTITY CASCADE")
            await cur.execute("TRUNCATE products RESTART IDENTITY CASCADE")
            await cur.execute("TRUNCATE institutions RESTART IDENTITY CASCADE")
        await conn.commit()

    yield

    # Cleanup after test
    async with await psycopg.AsyncConnection.connect(
        conn_str, autocommit=False, row_factory=psycopg.rows.dict_row
    ) as conn:
        try:
            await conn.rollback()
        except Exception:
            pass


@pytest.fixture
def client(test_app, test_db_pool):
    """Create FastAPI test client with test database"""
    # Override app's database pool
    set_db_pool(test_db_pool)

    # Create TestClient with test app
    with TestClient(test_app) as client:
        yield client


# ============================================================================
# Institution Tests
# ============================================================================


class TestCreateInstitution:
    """Test POST /api/portfolio/institutions endpoint"""

    def test_create_institution_success(self, client, clean_db):
        """Should create institution and return 201"""
        # Arrange
        payload = {"name": "KB증권", "type": "증권사"}

        # Act
        response = client.post("/api/portfolio/institutions", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "success"
        assert data["data"]["name"] == "KB증권"
        assert data["data"]["type"] == "증권사"
        assert data["data"]["institution_id"] is not None

    def test_create_institution_duplicate_name_returns_400(self, client, clean_db):
        """Should return 400 for duplicate institution name"""
        # Arrange
        payload = {"name": "KB증권", "type": "증권사"}

        client.post("/api/portfolio/institutions", json=payload)

        # Act
        response = client.post("/api/portfolio/institutions", json=payload)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["code"] != 0
        assert (
            "duplicate" in data["message"].lower()
            or "exists" in data["message"].lower()
        )

    def test_create_institution_invalid_type_returns_400(self, client, clean_db):
        """Should return 400 for invalid institution type"""
        # Arrange
        payload = {"name": "테스트증권", "type": "잘못된타입"}

        # Act
        response = client.post("/api/portfolio/institutions", json=payload)

        # Assert
        assert response.status_code == 400


# ============================================================================
# Product Tests
# ============================================================================


class TestCreateProduct:
    """Test POST /api/portfolio/products endpoint"""

    def test_create_product_success(self, client, clean_db):
        """Should create product and return 201"""
        # Arrange
        payload = {
            "product_name": "삼성전자",
            "asset_class": "주식",
            "region": "대한민국",
            "currency": "KRW",
            "investment_type": "직접",
            "characteristics": None,
            "risk_level": "위험",
        }

        # Act
        response = client.post("/api/portfolio/products", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "success"
        assert data["data"]["product_name"] == "삼성전자"
        assert data["data"]["asset_class"] == "주식"
        assert data["data"]["product_id"] is not None

    def test_create_product_with_characteristics(self, client, clean_db):
        """Should create product with characteristics array"""
        # Arrange
        payload = {
            "product_name": "KODEX 200",
            "asset_class": "주식",
            "region": "대한민국",
            "currency": "KRW",
            "investment_type": "ETF",
            "characteristics": ["배당", "인덱스"],
            "risk_level": "안전",
        }

        # Act
        response = client.post("/api/portfolio/products", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["data"]["characteristics"] == ["배당", "인덱스"]


# ============================================================================
# Account Tests
# ============================================================================


class TestCreateAccount:
    """Test POST /api/portfolio/accounts endpoint"""

    def test_create_account_success(self, client, clean_db):
        """Should create account and return 201"""
        # Arrange - First create institution
        inst_payload = {"name": "국민은행", "type": "은행"}
        inst_response = client.post("/api/portfolio/institutions", json=inst_payload)
        institution_id = inst_response.json()["data"]["institution_id"]

        # Create account
        payload = {"institution_id": institution_id, "name": "주식계좌", "type": "ISA"}

        # Act
        response = client.post("/api/portfolio/accounts", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "success"
        assert data["data"]["name"] == "주식계좌"
        assert data["data"]["type"] == "ISA"
        assert data["data"]["account_id"] is not None

    def test_create_account_invalid_institution_returns_400(self, client, clean_db):
        """Should return 400 for non-existent institution"""
        # Arrange
        payload = {"institution_id": 99999, "name": "주식계좌", "type": "ISA"}

        # Act
        response = client.post("/api/portfolio/accounts", json=payload)

        # Assert
        assert response.status_code in [400, 404]


# ============================================================================
# Holding Tests
# ============================================================================


class TestCreateHolding:
    """Test POST /api/portfolio/holdings endpoint"""

    def test_create_holding_success(self, client, clean_db):
        """Should create holding and return 201"""
        # Arrange - Create institution, account, and product
        inst_payload = {"name": "KB증권", "type": "증권사"}
        inst_response = client.post("/api/portfolio/institutions", json=inst_payload)
        institution_id = inst_response.json()["data"]["institution_id"]

        acc_payload = {
            "institution_id": institution_id,
            "name": "주식계좌",
            "type": "ISA",
        }
        acc_response = client.post("/api/portfolio/accounts", json=acc_payload)
        account_id = acc_response.json()["data"]["account_id"]

        prod_payload = {
            "product_name": "삼성전자",
            "asset_class": "주식",
            "region": "대한민국",
            "currency": "KRW",
            "investment_type": "직접",
            "characteristics": None,
            "risk_level": "위험",
        }
        prod_response = client.post("/api/portfolio/products", json=prod_payload)
        product_id = prod_response.json()["data"]["product_id"]

        # Create holding
        payload = {"account_id": account_id, "product_id": product_id}

        # Act
        response = client.post("/api/portfolio/holdings", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "success"
        assert data["data"]["holding_id"] is not None
        assert data["data"]["account_id"] == account_id
        assert data["data"]["product_id"] == product_id


# ============================================================================
# Snapshot Tests
# ============================================================================


class TestCreateSnapshot:
    """Test POST /api/portfolio/snapshots endpoint"""

    def test_create_snapshot_success(self, client, clean_db):
        """Should create snapshot and return 201"""
        # Arrange
        payload = {
            "user_id": 1,  # Test user created in fixture
            "reference_date": "2025-01-22",
        }

        # Act
        response = client.post("/api/portfolio/snapshots", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "success"
        assert data["data"]["snapshot_id"] is not None
        assert data["data"]["user_id"] == 1
        assert data["data"]["reference_date"] == "2025-01-22"
        assert data["data"]["status"] == "in_progress"

    def test_create_snapshot_duplicate_returns_400(self, client, clean_db):
        """Should return 400 for duplicate snapshot (same user + reference_date)"""
        # Arrange
        payload = {"user_id": 1, "reference_date": "2025-01-22"}

        client.post("/api/portfolio/snapshots", json=payload)

        # Act
        response = client.post("/api/portfolio/snapshots", json=payload)

        # Assert
        assert response.status_code == 400


# ===========================================================================
# Account Groups
# ===========================================================================


class TestCreateAccountGroup:
    """계좌 그룹 생성 테스트"""

    def test_create_account_group_success(self, client, clean_db):
        """Should create account group with multiple accounts"""
        # Arrange - Create institution and accounts first
        inst_payload = {"name": "KB증권", "type": "증권사"}
        inst_response = client.post("/api/portfolio/institutions", json=inst_payload)
        institution_id = inst_response.json()["data"]["institution_id"]

        acc1 = client.post(
            "/api/portfolio/accounts",
            json={
                "institution_id": institution_id,
                "name": "계좌1",
                "type": "위탁계좌",
            },
        )
        acc2 = client.post(
            "/api/portfolio/accounts",
            json={
                "institution_id": institution_id,
                "name": "계좌2",
                "type": "연금계좌",
            },
        )
        account_ids = [
            acc1.json()["data"]["account_id"],
            acc2.json()["data"]["account_id"],
        ]

        payload = {"name": "주식 계좌 그룹", "account_ids": account_ids}

        # Act
        response = client.post("/api/portfolio/account-groups", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "success"
        assert data["data"]["name"] == "주식 계좌 그룹"
        assert data["data"]["account_ids"] == account_ids
        assert data["data"]["account_group_id"] is not None

    def test_create_account_group_duplicate_name_returns_400(self, client, clean_db):
        """Should return 400 for duplicate group name"""
        # Arrange - Create institution and accounts
        inst_payload = {"name": "KB증권", "type": "증권사"}
        inst_response = client.post("/api/portfolio/institutions", json=inst_payload)
        institution_id = inst_response.json()["data"]["institution_id"]

        acc = client.post(
            "/api/portfolio/accounts",
            json={
                "institution_id": institution_id,
                "name": "계좌1",
                "type": "위탁계좌",
            },
        )
        account_id = acc.json()["data"]["account_id"]

        payload = {"name": "중복그룹", "account_ids": [account_id]}
        client.post("/api/portfolio/account-groups", json=payload)

        # Act
        response = client.post("/api/portfolio/account-groups", json=payload)

        # Assert
        assert response.status_code == 400


# ===========================================================================
# Snapshot Holdings
# ===========================================================================


class TestSnapshotHoldings:
    """스냅샷 보유자산 테스트"""

    def test_upsert_snapshot_holding_success(self, client, clean_db):
        """Should add holding valuation to snapshot"""
        # Arrange - Create full chain: institution -> product, account -> holding -> snapshot
        inst_response = client.post(
            "/api/portfolio/institutions", json={"name": "KB증권", "type": "증권사"}
        )
        institution_id = inst_response.json()["data"]["institution_id"]

        prod_response = client.post(
            "/api/portfolio/products",
            json={
                "product_name": "삼성전자",
                "asset_class": "주식",
                "region": "대한민국",
                "currency": "KRW",
                "investment_type": "직접",
                "risk_level": "위험",
            },
        )
        product_id = prod_response.json()["data"]["product_id"]

        acc_response = client.post(
            "/api/portfolio/accounts",
            json={
                "institution_id": institution_id,
                "name": "계좌1",
                "type": "위탁계좌",
            },
        )
        account_id = acc_response.json()["data"]["account_id"]

        holding_response = client.post(
            "/api/portfolio/holdings",
            json={"account_id": account_id, "product_id": product_id},
        )
        holding_id = holding_response.json()["data"]["holding_id"]

        snapshot_response = client.post(
            "/api/portfolio/snapshots",
            json={"user_id": 1, "reference_date": "2025-01-22"},
        )
        snapshot_id = snapshot_response.json()["data"]["snapshot_id"]

        payload = {
            "holding_id": holding_id,
            "valuation_amount": 1000000.0,
            "data_source": "manual",
        }

        # Act
        response = client.post(
            f"/api/portfolio/snapshots/{snapshot_id}/holdings", json=payload
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["holding_id"] == holding_id
        assert data["data"]["valuation_amount"] == 1000000.0


class TestSnapshotLock:
    """스냅샷 잠금 테스트"""

    def test_lock_snapshot_success(self, client, clean_db):
        """Should lock snapshot for weekly/annual clone"""
        # Arrange
        snapshot_response = client.post(
            "/api/portfolio/snapshots",
            json={"user_id": 1, "reference_date": "2025-01-22"},
        )
        snapshot_id = snapshot_response.json()["data"]["snapshot_id"]

        # Act
        response = client.post(f"/api/portfolio/snapshots/{snapshot_id}/lock")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "locked"


class TestWeeklyAnnualSnapshots:
    """주간/연간 스냅샷 복제 테스트"""

    def test_create_weekly_snapshot_success(self, client, clean_db):
        """Should create weekly snapshot from locked source"""
        # Arrange - Create and lock source snapshot
        source_response = client.post(
            "/api/portfolio/snapshots",
            json={"user_id": 1, "reference_date": "2025-01-15"},
        )
        source_id = source_response.json()["data"]["snapshot_id"]

        client.post(f"/api/portfolio/snapshots/{source_id}/lock")

        payload = {
            "user_id": 1,
            "reference_date": "2025-01-22",
            "source_snapshot_id": source_id,
        }

        # Act
        response = client.post("/api/portfolio/weekly-snapshots", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["weekly_snapshot_id"] is not None

    def test_create_annual_snapshot_success(self, client, clean_db):
        """Should create annual snapshot from locked source"""
        # Arrange
        source_response = client.post(
            "/api/portfolio/snapshots",
            json={"user_id": 1, "reference_date": "2024-12-31"},
        )
        source_id = source_response.json()["data"]["snapshot_id"]

        client.post(f"/api/portfolio/snapshots/{source_id}/lock")

        payload = {
            "user_id": 1,
            "reference_date": "2025-01-01",
            "source_snapshot_id": source_id,
        }

        # Act
        response = client.post("/api/portfolio/annual-snapshots", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["annual_snapshot_id"] is not None


# ===========================================================================
# Reports
# ===========================================================================


class TestReports:
    """리포트 엔드포인트 테스트"""

    def test_weekly_account_report_success(self, client, clean_db):
        """Should return weekly account report"""
        # Act
        response = client.get(
            "/api/portfolio/reports/weekly/accounts",
            params={
                "user_id": 1,
                "start_date": "2025-01-01",
                "end_date": "2025-01-31",
            },
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "data" in data
        assert "items" in data["data"]

    def test_annual_account_report_success(self, client, clean_db):
        """Should return annual account report"""
        # Act
        response = client.get(
            "/api/portfolio/reports/annual/accounts",
            params={"user_id": 1, "year": 2025},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert "data" in data

    def test_weekly_account_group_report_success(self, client, clean_db):
        """Should return weekly account group report"""
        # Act
        response = client.get(
            "/api/portfolio/reports/weekly/account-groups",
            params={
                "user_id": 1,
                "start_date": "2025-01-01",
                "end_date": "2025-01-31",
            },
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0

    def test_asset_class_report_success(self, client, clean_db):
        """Should return asset class report"""
        # Act
        response = client.get(
            "/api/portfolio/reports/asset-class",
            params={"user_id": 1, "snapshot_date": "2025-01-22"},
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
