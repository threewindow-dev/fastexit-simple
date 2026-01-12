"""
Unit tests for User domain model

Tests domain logic and business rules without external dependencies
"""
import pytest
from datetime import datetime

from domains.user.domain.models import User
from shared.errors import DomainError


class TestUserFactory:
    """Test User.create factory method"""
    
    def test_create_user_with_valid_data(self):
        """Should create user with valid username and email"""
        user = User.create(
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
        )
        
        assert user.id is None
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.full_name == "John Doe"
        assert isinstance(user.created_at, datetime)
    
    def test_create_user_without_full_name(self):
        """Should create user without full name"""
        user = User.create(
            username="alice",
            email="alice@example.com",
        )
        
        assert user.full_name is None
        assert user.username == "alice"
    
    def test_create_user_with_short_username_raises_error(self):
        """Should raise DomainError for username < 3 chars"""
        with pytest.raises(DomainError) as exc_info:
            User.create(
                username="ab",
                email="test@example.com",
            )
        
        assert exc_info.value.code == "USER_INVALID_USERNAME"
        assert "at least 3 characters" in exc_info.value.message
    
    def test_create_user_with_empty_username_raises_error(self):
        """Should raise DomainError for empty username"""
        with pytest.raises(DomainError) as exc_info:
            User.create(
                username="",
                email="test@example.com",
            )
        
        assert exc_info.value.code == "USER_INVALID_USERNAME"
    
    def test_create_user_with_invalid_email_raises_error(self):
        """Should raise DomainError for invalid email format"""
        invalid_emails = [
            "notanemail",
            "no-at-sign.com",
            "no-domain@",
            "@no-local-part.com",
            "no-dot@example",
        ]
        
        for invalid_email in invalid_emails:
            with pytest.raises(DomainError) as exc_info:
                User.create(
                    username="testuser",
                    email=invalid_email,
                )
            
            assert exc_info.value.code == "USER_INVALID_EMAIL"
            assert "Invalid email format" in exc_info.value.message


class TestUserValidation:
    """Test User validation methods"""
    
    def test_is_valid_returns_true_for_valid_user(self, sample_user):
        """Should return True for valid user"""
        assert sample_user.is_valid() is True
    
    def test_is_valid_returns_false_for_invalid_username(self):
        """Should return False for invalid username"""
        user = User(
            id=1,
            username="ab",  # Too short
            email="test@example.com",
            full_name="Test",
            created_at=datetime.now(),
        )
        # Note: validation runs in __post_init__, so this would raise
        # Testing the is_valid method directly
        try:
            user._validate_username()
            is_valid = True
        except DomainError:
            is_valid = False
        
        assert is_valid is False
    
    def test_is_valid_returns_false_for_invalid_email(self):
        """Should return False for invalid email"""
        user = User(
            id=1,
            username="testuser",
            email="invalid",  # No @ or .
            full_name="Test",
            created_at=datetime.now(),
        )
        
        try:
            user._validate_email()
            is_valid = True
        except DomainError:
            is_valid = False
        
        assert is_valid is False


class TestUserChangeFullName:
    """Test User.change_full_name method"""
    
    def test_change_full_name_with_valid_name(self, sample_user):
        """Should update full name successfully"""
        new_name = "Jane Doe"
        sample_user.change_full_name(new_name)
        
        assert sample_user.full_name == new_name
    
    def test_change_full_name_with_empty_string_raises_error(self, sample_user):
        """Should raise DomainError for empty full name"""
        with pytest.raises(DomainError) as exc_info:
            sample_user.change_full_name("")
        
        assert exc_info.value.code == "USER_INVALID_FULL_NAME"
        assert "cannot be empty" in exc_info.value.message
    
    def test_change_full_name_preserves_other_fields(self, sample_user):
        """Should only change full name, not other fields"""
        original_username = sample_user.username
        original_email = sample_user.email
        original_id = sample_user.id
        
        sample_user.change_full_name("New Name")
        
        assert sample_user.username == original_username
        assert sample_user.email == original_email
        assert sample_user.id == original_id


class TestUserToDictMethod:
    """Test User.to_dict serialization"""
    
    def test_to_dict_returns_correct_structure(self, sample_user):
        """Should return dict with all user fields"""
        result = sample_user.to_dict()
        
        assert isinstance(result, dict)
        assert result["id"] == sample_user.id
        assert result["username"] == sample_user.username
        assert result["email"] == sample_user.email
        assert result["full_name"] == sample_user.full_name
        assert result["created_at"] == sample_user.created_at.isoformat()
    
    def test_to_dict_handles_none_values(self):
        """Should handle None values correctly"""
        user = User.create(
            username="testuser",
            email="test@example.com",
            full_name=None,
        )
        
        result = user.to_dict()
        
        assert result["full_name"] is None
        assert result["id"] is None
    
    def test_to_dict_formats_datetime_as_iso(self, sample_user):
        """Should format datetime as ISO 8601 string"""
        result = sample_user.to_dict()
        
        assert isinstance(result["created_at"], str)
        assert "T" in result["created_at"]  # ISO format includes T separator
