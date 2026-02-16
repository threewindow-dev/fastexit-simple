"""
API integration tests for User router

Tests full HTTP endpoints with real database using Testcontainers
"""

import pytest
import pytest_asyncio
import psycopg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient, ASGITransport
from testcontainers.postgres import PostgresContainer

import core.config
from core.config import AppConfig, AuthConfig, DatabaseConfig
from dependencies import set_db_pool

from core.exception_handlers import register_exception_handlers
from shared.infra.database import create_sqlalchemy_pool
from subdomains.user.interface.routers import router as user_router


def _set_test_config() -> None:
    core.config._config = AppConfig(
        repository_type="sqlalchemy",
        database=DatabaseConfig(
            host="localhost",
            port=5432,
            name="test",
            user="test",
            password="test",
            pool_size=5,
            max_overflow=10,
            sql_echo=False,
            readonly_enabled=False,
        ),
        auth=AuthConfig(
            jwt_secret="test-secret",
            jwt_algorithm="HS256",
            jwt_expires_in_minutes=60,
        ),
        log_level="INFO",
        log_json_format=True,
    )


def _get_plain_conn_str(container: PostgresContainer) -> str:
    conn_str = container.get_connection_url()
    return conn_str.replace("postgresql+psycopg2", "postgresql").replace(
        "postgresql+psycopg", "postgresql"
    )


@pytest_asyncio.fixture(scope="function")
async def test_app():
    """Create a test FastAPI app without lifespan"""
    app = FastAPI(title="FastExit API Test")

    _set_test_config()

    # 전역 예외 핸들러 등록
    register_exception_handlers(app)

    # User 라우터 등록
    app.include_router(user_router)

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


@pytest_asyncio.fixture()
async def test_db_pool(postgres_container):
    """Create test database pool with initialized schema"""
    conn_str = _get_plain_conn_str(postgres_container)

    # Initialize schema
    async with await psycopg.AsyncConnection.connect(
        conn_str, autocommit=True, row_factory=psycopg.rows.dict_row
    ) as conn:
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

    pool = create_sqlalchemy_pool(dsn_write=conn_str)
    await pool.initialize()

    yield pool

    await pool.close()


@pytest_asyncio.fixture
async def clean_db(test_db_pool, postgres_container):
    """Clean database before each test"""
    # Use psycopg connection directly for table cleanup
    conn_str = _get_plain_conn_str(postgres_container)

    async with await psycopg.AsyncConnection.connect(
        conn_str, autocommit=False, row_factory=psycopg.rows.dict_row
    ) as conn:
        try:
            await conn.rollback()
        except Exception:
            pass
        async with conn.cursor() as cur:
            await cur.execute("TRUNCATE users RESTART IDENTITY CASCADE")
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
        async with conn.cursor() as cur:
            await cur.execute("TRUNCATE users RESTART IDENTITY CASCADE")
        await conn.commit()


@pytest_asyncio.fixture
async def client(test_app, test_db_pool):
    """Create FastAPI test client with test database"""
    _set_test_config()

    # Override app's database pool
    set_db_pool(test_db_pool)

    # Create TestClient with test app
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://testserver",
        follow_redirects=True,
    ) as client:
        yield client


class TestCreateUser:
    """Test POST /api/users endpoint"""

    async def test_create_user_success(self, client, clean_db):
        """Should create user and return 201"""
        # Arrange
        payload = {
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
        }

        # Act
        response = await client.post("/api/users", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "User created successfully"
        assert data["data"]["username"] == "john_doe"
        assert data["data"]["email"] == "john@example.com"
        assert data["data"]["id"] is not None

    async def test_create_user_duplicate_username_returns_400(self, client, clean_db):
        """Should return 400 for duplicate username"""
        # Arrange
        payload1 = {
            "username": "john_doe",
            "email": "john1@example.com",
            "full_name": "John 1",
        }
        payload2 = {
            "username": "john_doe",
            "email": "john2@example.com",
            "full_name": "John 2",
        }

        await client.post("/api/users", json=payload1)

        # Act
        response = await client.post("/api/users", json=payload2)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["code"] != 0
        assert (
            "duplicate" in data["message"].lower()
            or "already exists" in data["message"].lower()
        )

    async def test_create_user_invalid_username_returns_400(self, client, clean_db):
        """Should return 400 for invalid username (< 3 chars)"""
        # Arrange
        payload = {
            "username": "ab",  # Too short
            "email": "test@example.com",
            "full_name": "Test",
        }

        # Act
        response = await client.post("/api/users", json=payload)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["code"] != 0

    async def test_create_user_invalid_email_returns_422(self, client, clean_db):
        """Should return 422 for invalid email format (Pydantic validation)"""
        # Arrange
        payload = {
            "username": "testuser",
            "email": "invalid-email",  # Invalid format
            "full_name": "Test",
        }

        # Act
        response = await client.post("/api/users", json=payload)

        # Assert
        assert response.status_code == 422  # FastAPI validation error


class TestGetUser:
    """Test GET /api/users/{user_id} endpoint"""

    async def test_get_user_success(self, client, clean_db):
        """Should return user by ID"""
        # Arrange - create user
        create_payload = {
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
        }
        create_response = await client.post("/api/users", json=create_payload)
        user_id = create_response.json()["data"]["id"]

        # Act
        response = await client.get(f"/api/users/{user_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["id"] == user_id
        assert data["data"]["username"] == "john_doe"

    async def test_get_user_not_found_returns_404(self, client, clean_db):
        """Should return 404 for non-existent user"""
        # Act
        response = await client.get("/api/users/999")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["code"] != 0


class TestListUsers:
    """Test GET /api/users endpoint"""

    async def test_list_users_success(self, client, clean_db):
        """Should return list of users with pagination"""
        # Arrange - create 3 users
        for i in range(3):
            payload = {
                "username": f"user_{i}",
                "email": f"user{i}@example.com",
                "full_name": f"User {i}",
            }
            await client.post("/api/users", json=payload)

        # Act
        response = await client.get("/api/users?skip=0&limit=10")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]["items"]) == 3
        assert data["data"]["total_count"] == 3

    async def test_list_users_with_pagination(self, client, clean_db):
        """Should return correct page of users"""
        # Arrange - create 5 users
        for i in range(5):
            payload = {"username": f"user_{i}", "email": f"user{i}@example.com"}
            await client.post("/api/users", json=payload)

        # Act
        response = await client.get("/api/users?skip=2&limit=2")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]["items"]) == 2
        assert data["data"]["total_count"] == 5
        assert data["data"]["skip"] == 2
        assert data["data"]["limit"] == 2

    async def test_list_users_empty_database(self, client, clean_db):
        """Should return empty list for empty database"""
        # Act
        response = await client.get("/api/users")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]["items"]) == 0
        assert data["data"]["total_count"] == 0


class TestUpdateUser:
    """Test PATCH /api/users/{user_id} endpoint"""

    async def test_update_user_success(self, client, clean_db):
        """Should update user full name"""
        # Arrange - create user
        create_payload = {
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
        }
        create_response = await client.post("/api/users", json=create_payload)
        user_id = create_response.json()["data"]["id"]

        update_payload = {"full_name": "Jane Doe"}

        # Act
        response = await client.patch(f"/api/users/{user_id}", json=update_payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "User updated successfully"
        assert data["data"]["full_name"] == "Jane Doe"

    async def test_update_user_not_found_returns_404(self, client, clean_db):
        """Should return 404 for non-existent user"""
        # Arrange
        update_payload = {"full_name": "New Name"}

        # Act
        response = await client.patch("/api/users/999", json=update_payload)

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["code"] != 0

    async def test_update_user_empty_full_name_returns_400(self, client, clean_db):
        """Should return 400 for empty full name"""
        # Arrange - create user
        create_payload = {
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
        }
        create_response = await client.post("/api/users", json=create_payload)
        user_id = create_response.json()["data"]["id"]

        update_payload = {"full_name": ""}  # Empty

        # Act
        response = await client.patch(f"/api/users/{user_id}", json=update_payload)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["code"] != 0


class TestDeleteUser:
    """Test DELETE /api/users/{user_id} endpoint"""

    async def test_delete_user_success(self, client, clean_db):
        """Should delete user and return 200 with response body"""
        # Arrange - create user
        create_payload = {"username": "john_doe", "email": "john@example.com"}
        create_response = await client.post("/api/users", json=create_payload)
        user_id = create_response.json()["data"]["id"]

        # Act
        response = await client.delete(f"/api/users/{user_id}")

        # Assert
        assert response.status_code == 200
        assert response.json()["code"] == 0
        assert response.json()["data"]["id"] == user_id
        assert "deleted_at" in response.json()["data"]

        # Verify user is deleted
        get_response = await client.get(f"/api/users/{user_id}")
        assert get_response.status_code == 404

    async def test_delete_user_not_found_returns_404(self, client, clean_db):
        """Should return 404 for non-existent user"""
        # Act
        response = await client.delete("/api/users/999")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["code"] != 0
