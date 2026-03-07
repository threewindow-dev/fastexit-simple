"""SQLAlchemy entity for asset class target allocation table."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.infra.database import Base


class TargetAllocationAssetClassEntity(Base):
    """Asset class target allocation entity."""

    __tablename__ = "target_allocation_asset_classes"

    target_allocation_asset_class_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    asset_class: Mapped[str] = mapped_column(String(100), nullable=False)
    target_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
