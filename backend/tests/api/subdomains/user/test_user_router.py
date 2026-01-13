"""
API integration tests for User router

Tests full HTTP endpoints with real database using Testcontainers
"""
import pytest
import pytest_asyncio
import psycopg
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from testcontainers.core.waiting_utils import wait_for_logs

from main import app
from shared.infra.database import DatabasePool


@pytest.fixture(scope="module")
def postgres_container():
    """Start PostgreSQL container for API tests"""
    container = PostgresContainer("postgres:17-alpine")
    container.start()
    wait_for_logs(container, "database system is ready to accept connections")
    yield container
    container.stop()


@pytest_asyncio.fixture()
async def test_db_pool(postgres_container):
    """Create test database pool with initialized schema"""
    conn_str = postgres_container.get_connection_url()
    # Convert SQLAlchemy-style URL to plain psycopg DSN
    conn_str = conn_str.replace("postgresql+psycopg2", "postgresql").replace("postgresql+psycopg", "postgresql")
    
    # Initialize schema
    async with await psycopg.AsyncConnection.connect(
        conn_str, autocommit=True, row_factory=psycopg.rows.dict_row
    ) as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    full_name VARCHAR(255),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    # Create pool
    pool = DatabasePool()
    # Override connection string
    import os
    os.environ["DB_HOST"] = str(postgres_container.get_container_host_ip())
    os.environ["DB_PORT"] = str(postgres_container.get_exposed_port(5432))
    os.environ["DB_NAME"] = str(postgres_container.dbname)
    os.environ["DB_USER"] = str(postgres_container.username)
    os.environ["DB_PASSWORD"] = str(postgres_container.password)
    
    await pool.initialize()
    
    yield pool
    
    await pool.close()


@pytest_asyncio.fixture
async def clean_db(test_db_pool):
    """Clean database before each test"""
    async with test_db_pool.connection() as conn:
        try:
            await conn.rollback()
        except Exception:
            pass
        async with conn.cursor() as cur:
            await cur.execute("TRUNCATE users RESTART IDENTITY CASCADE")
        await conn.commit()
    yield
    # Cleanup after test
    async with test_db_pool.connection() as conn:
        try:
            await conn.rollback()
        except Exception:
            pass
        async with conn.cursor() as cur:
            await cur.execute("TRUNCATE users RESTART IDENTITY CASCADE")
        await conn.commit()


@pytest.fixture
def client(test_db_pool):
    """Create FastAPI test client with test database"""
    # Override app's database pool
    app.state.db_pool = test_db_pool
    
    with TestClient(app) as client:
        yield client


class TestCreateUser:
    """Test POST /api/users endpoint"""
    
    def test_create_user_success(self, client, clean_db):
        """Should create user and return 201"""
        # Arrange
        payload = {
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
        }
        
        # Act
        response = client.post("/api/users", json=payload)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "User created successfully"
        assert data["data"]["username"] == "john_doe"
        assert data["data"]["email"] == "john@example.com"
        assert data["data"]["id"] is not None
    
    def test_create_user_duplicate_username_returns_400(self, client, clean_db):
        """Should return 400 for duplicate username"""
        # Arrange
        payload1 = {"username": "john_doe", "email": "john1@example.com", "full_name": "John 1"}
        payload2 = {"username": "john_doe", "email": "john2@example.com", "full_name": "John 2"}
        
        client.post("/api/users", json=payload1)
        
        # Act
        response = client.post("/api/users", json=payload2)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["code"] != 0
        assert "duplicate" in data["message"].lower() or "already exists" in data["message"].lower()
    
    def test_create_user_invalid_username_returns_400(self, client, clean_db):
        """Should return 400 for invalid username (< 3 chars)"""
        # Arrange
        payload = {
            "username": "ab",  # Too short
            "email": "test@example.com",
            "full_name": "Test",
        }
        
        # Act
        response = client.post("/api/users", json=payload)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["code"] != 0
    
    def test_create_user_invalid_email_returns_422(self, client, clean_db):
        """Should return 422 for invalid email format (Pydantic validation)"""
        # Arrange
        payload = {
            "username": "testuser",
            "email": "invalid-email",  # Invalid format
            "full_name": "Test",
        }
        
        # Act
        response = client.post("/api/users", json=payload)
        
        # Assert
        assert response.status_code == 422  # FastAPI validation error


class TestGetUser:
    """Test GET /api/users/{user_id} endpoint"""
    
    def test_get_user_success(self, client, clean_db):
        """Should return user by ID"""
        # Arrange - create user
        create_payload = {
            "username": "john_doe",
            "email": "john@example.com",
            "full_name": "John Doe",
        }
        create_response = client.post("/api/users", json=create_payload)
        user_id = create_response.json()["data"]["id"]
        
        # Act
        response = client.get(f"/api/users/{user_id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["id"] == user_id
        assert data["data"]["username"] == "john_doe"
    
    def test_get_user_not_found_returns_404(self, client, clean_db):
        """Should return 404 for non-existent user"""
        # Act
        response = client.get("/api/users/999")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["code"] != 0


class TestListUsers:
    """Test GET /api/users endpoint"""
    
    def test_list_users_success(self, client, clean_db):
        """Should return list of users with pagination"""
        # Arrange - create 3 users
        for i in range(3):
            payload = {
                "username": f"user_{i}",
                "email": f"user{i}@example.com",
                "full_name": f"User {i}",
            }
            client.post("/api/users", json=payload)
        
        # Act
        response = client.get("/api/users?skip=0&limit=10")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]["items"]) == 3
        assert data["data"]["total_count"] == 3
    
    def test_list_users_with_pagination(self, client, clean_db):
        """Should return correct page of users"""
        # Arrange - create 5 users
        for i in range(5):
            payload = {"username": f"user_{i}", "email": f"user{i}@example.com"}
            client.post("/api/users", json=payload)
        
        # Act
        response = client.get("/api/users?skip=2&limit=2")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]["items"]) == 2
        assert data["data"]["total_count"] == 5
        assert data["data"]["skip"] == 2
        assert data["data"]["limit"] == 2
    
    def test_list_users_empty_database(self, client, clean_db):
        """Should return empty list for empty database"""
        # Act
        response = client.get("/api/users")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert len(data["data"]["items"]) == 0
        assert data["data"]["total_count"] == 0


class TestUpdateUser:
    """Test PATCH /api/users/{user_id} endpoint"""
    
    def test_update_user_success(self, client, clean_db):
        """Should update user full name"""
        # Arrange - create user
        create_payload = {"username": "john_doe", "email": "john@example.com", "full_name": "John Doe"}
        create_response = client.post("/api/users", json=create_payload)
        user_id = create_response.json()["data"]["id"]
        
        update_payload = {"full_name": "Jane Doe"}
        
        # Act
        response = client.patch(f"/api/users/{user_id}", json=update_payload)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["message"] == "User updated successfully"
        assert data["data"]["full_name"] == "Jane Doe"
    
    def test_update_user_not_found_returns_404(self, client, clean_db):
        """Should return 404 for non-existent user"""
        # Arrange
        update_payload = {"full_name": "New Name"}
        
        # Act
        response = client.patch("/api/users/999", json=update_payload)
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["code"] != 0
    
    def test_update_user_empty_full_name_returns_400(self, client, clean_db):
        """Should return 400 for empty full name"""
        # Arrange - create user
        create_payload = {"username": "john_doe", "email": "john@example.com", "full_name": "John Doe"}
        create_response = client.post("/api/users", json=create_payload)
        user_id = create_response.json()["data"]["id"]
        
        update_payload = {"full_name": ""}  # Empty
        
        # Act
        response = client.patch(f"/api/users/{user_id}", json=update_payload)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["code"] != 0


class TestDeleteUser:
    """Test DELETE /api/users/{user_id} endpoint"""
    
    def test_delete_user_success(self, client, clean_db):
        """Should delete user and return 204"""
        # Arrange - create user
        create_payload = {"username": "john_doe", "email": "john@example.com"}
        create_response = client.post("/api/users", json=create_payload)
        user_id = create_response.json()["data"]["id"]
        
        # Act
        response = client.delete(f"/api/users/{user_id}")
        
        # Assert
        assert response.status_code == 204
        
        # Verify user is deleted
        get_response = client.get(f"/api/users/{user_id}")
        assert get_response.status_code == 404
    
    def test_delete_user_not_found_returns_404(self, client, clean_db):
        """Should return 404 for non-existent user"""
        # Act
        response = client.delete("/api/users/999")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["code"] != 0
