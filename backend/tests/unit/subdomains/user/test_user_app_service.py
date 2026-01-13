"""
Unit tests for UserAppService

Tests application layer use cases with mocked dependencies
"""
import pytest
from datetime import datetime
from unittest.mock import AsyncMock

from subdomains.user.application.services import UserAppService
from subdomains.user.application.dtos import (
    RegisterUserCommand,
    UpdateUserCommand,
    DeleteUserCommand,
    UserPagedListQuery,
)
from subdomains.user.domain.models import User
from shared.errors import DuplicateUserError, UserNotFoundError, DomainError


class TestCreateUser:
    """Test UserAppService.create_user use case"""
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, mock_user_repository):
        """Should create user when username and email are unique"""
        # Arrange
        command = RegisterUserCommand(
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
        )
        
        created_user = User(
            id=1,
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            created_at=datetime(2025, 1, 11, 10, 30, 0),
        )
        
        mock_user_repository.exists_by_username.return_value = False
        mock_user_repository.exists_by_email.return_value = False
        mock_user_repository.add.return_value = created_user
        
        # transaction_factory 없이 생성 (트랜잭션 관리 없음)
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act
        result = await service.create_user(command)
        
        # Assert
        assert result.id == 1
        assert result.username == "john_doe"
        assert result.email == "john@example.com"
        assert result.full_name == "John Doe"
        
        mock_user_repository.exists_by_username.assert_awaited_once_with("john_doe")
        mock_user_repository.exists_by_email.assert_awaited_once_with("john@example.com")
        mock_user_repository.add.assert_awaited_once()
    
    @pytest.mark.asyncio
    async def test_create_user_duplicate_username_raises_error(
        self, mock_user_repository
    ):
        """Should raise DuplicateUserError when username exists"""
        # Arrange
        command = RegisterUserCommand(
            username="existing_user",
            email="new@example.com",
            full_name="New User",
        )
        
        mock_user_repository.exists_by_username.return_value = True
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act & Assert
        with pytest.raises(DuplicateUserError):
            await service.create_user(command)
        
        mock_user_repository.exists_by_username.assert_awaited_once_with("existing_user")
        mock_user_repository.add.assert_not_awaited()
    
    @pytest.mark.asyncio
    async def test_create_user_duplicate_email_raises_error(
        self, mock_user_repository
    ):
        """Should raise DuplicateUserError when email exists"""
        # Arrange
        command = RegisterUserCommand(
            username="new_user",
            email="existing@example.com",
            full_name="New User",
        )
        
        mock_user_repository.exists_by_username.return_value = False
        mock_user_repository.exists_by_email.return_value = True
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act & Assert
        with pytest.raises(DuplicateUserError):
            await service.create_user(command)
        
        mock_user_repository.exists_by_email.assert_awaited_once_with("existing@example.com")
        mock_user_repository.add.assert_not_awaited()
    
    @pytest.mark.asyncio
    async def test_create_user_with_invalid_username_raises_domain_error(
        self, mock_user_repository
    ):
        """Should raise DomainError for invalid username (< 3 chars)"""
        # Arrange
        command = RegisterUserCommand(
            username="ab",  # Too short
            email="test@example.com",
            full_name="Test",
        )
        
        mock_user_repository.exists_by_username.return_value = False
        mock_user_repository.exists_by_email.return_value = False
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act & Assert
        with pytest.raises(DomainError) as exc_info:
            await service.create_user(command)
        
        assert exc_info.value.code == "USER_INVALID_USERNAME"
        mock_user_repository.add.assert_not_awaited()


class TestUpdateUser:
    """Test UserAppService.update_user use case"""
    
    @pytest.mark.asyncio
    async def test_update_user_success(self, mock_user_repository):
        """Should update user full name successfully"""
        # Arrange
        existing_user = User(
            id=1,
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            created_at=datetime(2025, 1, 11, 10, 30, 0),
        )
        
        updated_user = User(
            id=1,
            username="john_doe",
            email="john@example.com",
            full_name="Jane Doe",
            created_at=datetime(2025, 1, 11, 10, 30, 0),
        )
        
        command = UpdateUserCommand(
            user_id=1,
            full_name="Jane Doe",
        )
        
        mock_user_repository.find_by_id.return_value = existing_user
        mock_user_repository.update.return_value = updated_user
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act
        result = await service.update_user(command)
        
        # Assert
        assert result.full_name == "Jane Doe"
        mock_user_repository.find_by_id.assert_awaited_once_with(1)
        mock_user_repository.update.assert_awaited_once()
    
    @pytest.mark.asyncio
    async def test_update_user_not_found_raises_error(
        self, mock_user_repository
    ):
        """Should raise UserNotFoundError when user doesn't exist"""
        # Arrange
        command = UpdateUserCommand(
            user_id=999,
            full_name="New Name",
        )
        
        mock_user_repository.find_by_id.return_value = None
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await service.update_user(command)
        
        mock_user_repository.update.assert_not_awaited()
    
    @pytest.mark.asyncio
    async def test_update_user_with_empty_full_name_raises_domain_error(
        self, mock_user_repository
    ):
        """Should raise DomainError for empty full name"""
        # Arrange
        existing_user = User(
            id=1,
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            created_at=datetime(2025, 1, 11, 10, 30, 0),
        )
        
        command = UpdateUserCommand(
            user_id=1,
            full_name="",  # Empty
        )
        
        mock_user_repository.find_by_id.return_value = existing_user
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act & Assert
        with pytest.raises(DomainError) as exc_info:
            await service.update_user(command)
        
        assert exc_info.value.code == "USER_INVALID_FULL_NAME"
        mock_user_repository.update.assert_not_awaited()


class TestDeleteUser:
    """Test UserAppService.delete_user use case"""
    
    @pytest.mark.asyncio
    async def test_delete_user_success(self, mock_user_repository):
        """Should delete user successfully"""
        # Arrange
        existing_user = User(
            id=1,
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            created_at=datetime(2025, 1, 11, 10, 30, 0),
        )
        
        command = DeleteUserCommand(user_id=1)
        
        mock_user_repository.find_by_id.return_value = existing_user
        mock_user_repository.remove.return_value = None
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act
        await service.delete_user(command)
        
        # Assert
        mock_user_repository.find_by_id.assert_awaited_once_with(1)
        mock_user_repository.remove.assert_awaited_once_with(1)
    
    @pytest.mark.asyncio
    async def test_delete_user_not_found_raises_error(
        self, mock_user_repository
    ):
        """Should raise UserNotFoundError when user doesn't exist"""
        # Arrange
        command = DeleteUserCommand(user_id=999)
        
        mock_user_repository.find_by_id.return_value = None
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await service.delete_user(command)
        
        mock_user_repository.remove.assert_not_awaited()


class TestGetUser:
    """Test UserAppService.get_user query"""
    
    @pytest.mark.asyncio
    async def test_get_user_success(self, mock_user_repository):
        """Should return user by ID"""
        # Arrange
        existing_user = User(
            id=1,
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            created_at=datetime(2025, 1, 11, 10, 30, 0),
        )
        
        mock_user_repository.find_by_id.return_value = existing_user
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act
        result = await service.get_user(1)
        
        # Assert
        assert result.id == 1
        assert result.username == "john_doe"
        mock_user_repository.find_by_id.assert_awaited_once_with(1)
    
    @pytest.mark.asyncio
    async def test_get_user_not_found_raises_error(
        self, mock_user_repository
    ):
        """Should raise UserNotFoundError when user doesn't exist"""
        # Arrange
        mock_user_repository.find_by_id.return_value = None
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act & Assert
        with pytest.raises(UserNotFoundError):
            await service.get_user(999)


class TestListUsers:
    """Test UserAppService.list_users query"""
    
    @pytest.mark.asyncio
    async def test_list_users_success(
        self, mock_user_repository, sample_users
    ):
        """Should return paginated list of users"""
        # Arrange
        query = UserPagedListQuery(skip=0, limit=10)
        
        mock_user_repository.find_all.return_value = (sample_users[:10], 10)
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act
        result = await service.list_users(query)
        
        # Assert
        assert len(result.items) == 10
        assert result.total_count == 10
        assert result.skip == 0
        assert result.limit == 10
        mock_user_repository.find_all.assert_awaited_once_with(skip=0, limit=10)
    
    @pytest.mark.asyncio
    async def test_list_users_with_pagination(
        self, mock_user_repository, sample_users
    ):
        """Should return correct page of users"""
        # Arrange
        query = UserPagedListQuery(skip=5, limit=5)
        
        mock_user_repository.find_all.return_value = (sample_users[5:10], 10)
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act
        result = await service.list_users(query)
        
        # Assert
        assert len(result.items) == 5
        assert result.total_count == 10
        assert result.skip == 5
        assert result.limit == 5
    
    @pytest.mark.asyncio
    async def test_list_users_empty_result(
        self, mock_user_repository
    ):
        """Should return empty list when no users exist"""
        # Arrange
        query = UserPagedListQuery(skip=0, limit=10)
        
        mock_user_repository.find_all.return_value = ([], 0)
        
        service = UserAppService(mock_user_repository, transaction_factory=None)
        
        # Act
        result = await service.list_users(query)
        
        # Assert
        assert len(result.items) == 0
        assert result.total_count == 0
