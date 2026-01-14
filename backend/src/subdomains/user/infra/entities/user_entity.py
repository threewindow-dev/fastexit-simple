"""SQLAlchemy ORM entity for User."""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime

from shared.infra.database import Base


class UserEntity(Base):
    """User ORM entity mapping to database users table."""

    __tablename__ = "users"

    # Columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    # Use UTC timezone-aware datetime but strip timezone for storage in TIMESTAMP WITHOUT TIME ZONE
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )

    def __repr__(self) -> str:
        return (
            f"<UserEntity(id={self.id}, username={self.username}, email={self.email})>"
        )
