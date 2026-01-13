"""SQLAlchemy ORM model for User entity."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from shared.infra.database import Base


class UserORM(Base):
    """User ORM model mapping to database users table."""
    
    __tablename__ = "users"
    
    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<UserORM(id={self.id}, username={self.username}, email={self.email})>"
