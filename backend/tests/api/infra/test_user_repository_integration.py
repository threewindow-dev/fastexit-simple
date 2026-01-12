"""
Integration tests for PsycopgUserRepository

Tests repository with actual PostgreSQL database using Testcontainers
"""
import pytest
import pytest_asyncio
import psycopg
from datetime import datetime
from testcontainers.postgres import PostgresContainer

from domains.user.domain.models import User
from domains.user.infra.repositories import PsycopgUserRepository
from shared.errors import DuplicateUserError, InfraError


@pytest.fixture(scope="module")
def postgres_container():
    """Start PostgreSQL container for integration tests"""
    with PostgresContainer("postgres:17-alpine") as postgres:
        yield postgres


@pytest_asyncio.fixture()
async def db_connection(postgres_container):
    """Create database connection and initialize schema"""
    conn_str = postgres_container.get_connection_url()
    # Convert SQLAlchemy-style URL to plain psycopg DSN
    conn_str = conn_str.replace("postgresql+psycopg2", "postgresql").replace("postgresql+psycopg", "postgresql")
    
    async with await psycopg.AsyncConnection.connect(
        conn_str, autocommit=False, row_factory=psycopg.rows.dict_row
    ) as conn:
        # Create users table
        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    full_name VARCHAR(255),
                    created_at TIMESTAMP NOT NULL
                )
            """)
        await conn.commit()
        
        yield conn


@pytest_asyncio.fixture
async def clean_db(db_connection):
    """Clean database before each test"""
    # Ensure we are not in aborted transaction from previous operations
    try:
        await db_connection.rollback()
    except Exception:
        pass
    async with db_connection.cursor() as cur:
        await cur.execute("TRUNCATE users RESTART IDENTITY CASCADE")
    await db_connection.commit()
    yield
    # Cleanup after test
    try:
        await db_connection.rollback()
    except Exception:
        pass
    async with db_connection.cursor() as cur:
        await cur.execute("TRUNCATE users RESTART IDENTITY CASCADE")
    await db_connection.commit()


@pytest_asyncio.fixture
async def repository(db_connection):
    """Create repository instance"""
    return PsycopgUserRepository(db_connection)


class TestAddUser:
    """Test PsycopgUserRepository.add method"""
    
    @pytest.mark.asyncio
    async def test_add_user_success(self, repository, clean_db):
        """Should add user and return user with ID"""
        # Arrange
        user = User.create(
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
        )
        
        # Act
        saved_user = await repository.add(user)
        
        # Assert
        assert saved_user.id is not None
        assert saved_user.username == "john_doe"
        assert saved_user.email == "john@example.com"
        assert saved_user.full_name == "John Doe"
        assert isinstance(saved_user.created_at, datetime)
    
    @pytest.mark.asyncio
    async def test_add_user_duplicate_username_raises_error(
        self, repository, clean_db
    ):
        """Should raise DuplicateUserError for duplicate username"""
        # Arrange
        user1 = User.create(username="john_doe", email="john1@example.com")
        user2 = User.create(username="john_doe", email="john2@example.com")
        
        await repository.add(user1)
        
        # Act & Assert
        with pytest.raises(DuplicateUserError):
            await repository.add(user2)
    
    @pytest.mark.asyncio
    async def test_add_user_duplicate_email_raises_error(
        self, repository, clean_db
    ):
        """Should raise DuplicateUserError for duplicate email"""
        # Arrange
        user1 = User.create(username="john1", email="john@example.com")
        user2 = User.create(username="john2", email="john@example.com")
        
        await repository.add(user1)
        
        # Act & Assert
        with pytest.raises(DuplicateUserError):
            await repository.add(user2)


class TestUpdateUser:
    """Test PsycopgUserRepository.update method"""
    
    @pytest.mark.asyncio
    async def test_update_user_success(self, repository, clean_db):
        """Should update user successfully"""
        # Arrange
        user = User.create(username="john_doe", email="john@example.com", full_name="John Doe")
        saved_user = await repository.add(user)
        
        saved_user.change_full_name("Jane Doe")
        
        # Act
        updated_user = await repository.update(saved_user)
        
        # Assert
        assert updated_user.full_name == "Jane Doe"
        assert updated_user.id == saved_user.id
        assert updated_user.username == saved_user.username
    
    @pytest.mark.asyncio
    async def test_update_user_not_found_raises_error(self, repository, clean_db):
        """Should raise InfraError for non-existent user"""
        # Arrange
        user = User(
            id=999,
            username="nonexistent",
            email="nonexistent@example.com",
            full_name="Test",
            created_at=datetime.now(),
        )
        
        # Act & Assert
        with pytest.raises(InfraError):
            await repository.update(user)


class TestRemoveUser:
    """Test PsycopgUserRepository.remove method"""
    
    @pytest.mark.asyncio
    async def test_remove_user_success(self, repository, clean_db):
        """Should remove user successfully"""
        # Arrange
        user = User.create(username="john_doe", email="john@example.com")
        saved_user = await repository.add(user)
        
        # Act
        await repository.remove(saved_user.id)
        
        # Assert - verify user is deleted
        result = await repository.find_by_id(saved_user.id)
        assert result is None
    
    @pytest.mark.asyncio
    async def test_remove_user_nonexistent_completes(self, repository, clean_db):
        """Should complete without error for non-existent user"""
        # Act & Assert - should not raise error
        await repository.remove(999)


class TestFindById:
    """Test PsycopgUserRepository.find_by_id method"""
    
    @pytest.mark.asyncio
    async def test_find_by_id_success(self, repository, clean_db):
        """Should find user by ID"""
        # Arrange
        user = User.create(username="john_doe", email="john@example.com", full_name="John Doe")
        saved_user = await repository.add(user)
        
        # Act
        found_user = await repository.find_by_id(saved_user.id)
        
        # Assert
        assert found_user is not None
        assert found_user.id == saved_user.id
        assert found_user.username == "john_doe"
        assert found_user.email == "john@example.com"
    
    @pytest.mark.asyncio
    async def test_find_by_id_not_found_returns_none(self, repository, clean_db):
        """Should return None for non-existent user"""
        # Act
        result = await repository.find_by_id(999)
        
        # Assert
        assert result is None


class TestFindAll:
    """Test PsycopgUserRepository.find_all method"""
    
    @pytest.mark.asyncio
    async def test_find_all_returns_all_users(self, repository, clean_db):
        """Should return all users with pagination"""
        # Arrange - create 5 users
        for i in range(5):
            user = User.create(
                username=f"user_{i}",
                email=f"user{i}@example.com",
                full_name=f"User {i}",
            )
            await repository.add(user)
        
        # Act
        users, total = await repository.find_all(skip=0, limit=10)
        
        # Assert
        assert len(users) == 5
        assert total == 5
    
    @pytest.mark.asyncio
    async def test_find_all_with_pagination(self, repository, clean_db):
        """Should return correct page of users"""
        # Arrange - create 10 users
        for i in range(10):
            user = User.create(username=f"user_{i}", email=f"user{i}@example.com")
            await repository.add(user)
        
        # Act
        users, total = await repository.find_all(skip=5, limit=3)
        
        # Assert
        assert len(users) == 3
        assert total == 10
        assert users[0].username == "user_5"
    
    @pytest.mark.asyncio
    async def test_find_all_empty_database(self, repository, clean_db):
        """Should return empty list for empty database"""
        # Act
        users, total = await repository.find_all(skip=0, limit=10)
        
        # Assert
        assert len(users) == 0
        assert total == 0


class TestExistsByUsername:
    """Test PsycopgUserRepository.exists_by_username method"""
    
    @pytest.mark.asyncio
    async def test_exists_by_username_returns_true_when_exists(
        self, repository, clean_db
    ):
        """Should return True when username exists"""
        # Arrange
        user = User.create(username="john_doe", email="john@example.com")
        await repository.add(user)
        
        # Act
        exists = await repository.exists_by_username("john_doe")
        
        # Assert
        assert exists is True
    
    @pytest.mark.asyncio
    async def test_exists_by_username_returns_false_when_not_exists(
        self, repository, clean_db
    ):
        """Should return False when username doesn't exist"""
        # Act
        exists = await repository.exists_by_username("nonexistent")
        
        # Assert
        assert exists is False


class TestExistsByEmail:
    """Test PsycopgUserRepository.exists_by_email method"""
    
    @pytest.mark.asyncio
    async def test_exists_by_email_returns_true_when_exists(
        self, repository, clean_db
    ):
        """Should return True when email exists"""
        # Arrange
        user = User.create(username="john_doe", email="john@example.com")
        await repository.add(user)
        
        # Act
        exists = await repository.exists_by_email("john@example.com")
        
        # Assert
        assert exists is True
    
    @pytest.mark.asyncio
    async def test_exists_by_email_returns_false_when_not_exists(
        self, repository, clean_db
    ):
        """Should return False when email doesn't exist"""
        # Act
        exists = await repository.exists_by_email("nonexistent@example.com")
        
        # Assert
        assert exists is False
