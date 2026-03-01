"""SQLAlchemy ORM entities for portfolio domain."""

from datetime import datetime, timezone
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import ARRAY

from shared.infra.database import Base


def _utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class InstitutionEntity(Base):
    __tablename__ = "institutions"

    institution_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    type = Column(String(50), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (
        CheckConstraint(
            "type in ('증권사','은행','기타기관')", name="chk_institution_type"
        ),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Institution(id={self.institution_id}, name={self.name})>"


class ProductEntity(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    asset_class = Column(String(50), nullable=False)
    region = Column(String(50), nullable=False)
    currency = Column(String(10), nullable=False)
    investment_type = Column(String(50), nullable=False)
    characteristics = Column(ARRAY(String), nullable=True)
    risk_level = Column(String(20), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (
        UniqueConstraint(
            "product_name",
            "asset_class",
            "region",
            "currency",
            "investment_type",
            name="uq_product_identity",
        ),
        CheckConstraint(
            "asset_class in ('주식','채권','통화','금','부동산','가상자산','기타자산')",
            name="chk_product_asset_class",
        ),
        CheckConstraint("region in ('대한민국','미국')", name="chk_product_region"),
        CheckConstraint("currency in ('KRW','USD')", name="chk_product_currency"),
        CheckConstraint(
            "investment_type in ('직접','ETF')", name="chk_product_investment_type"
        ),
        CheckConstraint("risk_level in ('안전','위험')", name="chk_product_risk_level"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Product(id={self.product_id}, name={self.product_name})>"


class AccountEntity(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    institution_id = Column(
        Integer,
        ForeignKey("institutions.institution_id", ondelete="CASCADE"),
        nullable=False,
    )
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (
        UniqueConstraint(
            "institution_id", "name", name="uq_account_name_per_institution"
        ),
        Index("idx_accounts_institution", "institution_id"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Account(id={self.account_id}, name={self.name})>"


class AccountGroupEntity(Base):
    __tablename__ = "account_groups"

    account_group_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    include_in_weekly_report = Column(Boolean, nullable=False, default=False)
    display_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<AccountGroup(id={self.account_group_id}, name={self.name})>"


class AccountGroupAccountEntity(Base):
    __tablename__ = "account_group_accounts"

    account_group_id = Column(
        Integer,
        ForeignKey("account_groups.account_group_id", ondelete="CASCADE"),
        primary_key=True,
    )
    account_id = Column(
        Integer, ForeignKey("accounts.account_id", ondelete="CASCADE"), primary_key=True
    )
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (Index("idx_account_group_accounts_account", "account_id"),)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<AccountGroupAccount(group_id={self.account_group_id}, account_id={self.account_id})>"


class HoldingEntity(Base):
    __tablename__ = "holdings"

    holding_id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(
        Integer, ForeignKey("accounts.account_id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(
        Integer, ForeignKey("products.product_id", ondelete="CASCADE"), nullable=False
    )
    is_visible = Column(Boolean, nullable=False, default=True)
    deleted_at = Column(DateTime, nullable=True)
    deletion_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (
        UniqueConstraint("account_id", "product_id", name="uq_holding_account_product"),
        Index("idx_holdings_account", "account_id"),
        Index("idx_holdings_product", "product_id"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Holding(id={self.holding_id}, account_id={self.account_id}, product_id={self.product_id})>"


class SnapshotEntity(Base):
    __tablename__ = "snapshots"

    snapshot_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    reference_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    locked_at = Column(DateTime, nullable=True)
    editable_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (
        UniqueConstraint(
            "user_id", "reference_date", name="uq_snapshot_user_reference"
        ),
        CheckConstraint(
            "status in ('in_progress','locked')", name="chk_snapshot_status"
        ),
        Index("idx_snapshots_user", "user_id"),
        Index("idx_snapshots_status", "status"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Snapshot(id={self.snapshot_id}, date={self.reference_date}, status={self.status})>"


class SnapshotHoldingEntity(Base):
    __tablename__ = "snapshot_holdings"

    snapshot_holding_id = Column(Integer, primary_key=True, autoincrement=True)
    snapshot_id = Column(
        Integer, ForeignKey("snapshots.snapshot_id", ondelete="CASCADE"), nullable=False
    )
    holding_id = Column(
        Integer, ForeignKey("holdings.holding_id", ondelete="CASCADE"), nullable=False
    )
    valuation_amount = Column(Numeric(20, 4), nullable=False)
    data_source = Column(String(10), nullable=False)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (
        UniqueConstraint("snapshot_id", "holding_id", name="uq_snapshot_holding"),
        CheckConstraint(
            "data_source in ('auto','manual','missing')",
            name="chk_snapshot_data_source",
        ),
        Index("idx_snapshot_holdings_snapshot", "snapshot_id"),
        Index("idx_snapshot_holdings_holding", "holding_id"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<SnapshotHolding(id={self.snapshot_holding_id}, snapshot_id={self.snapshot_id})>"


class WeeklySnapshotEntity(Base):
    __tablename__ = "weekly_snapshots"

    weekly_snapshot_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    reference_date = Column(Date, nullable=False)
    source_snapshot_id = Column(
        Integer, ForeignKey("snapshots.snapshot_id", ondelete="CASCADE"), nullable=False
    )
    status = Column(String(20), nullable=False)
    editable_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (
        UniqueConstraint(
            "user_id", "reference_date", name="uq_weekly_snapshot_user_reference"
        ),
        CheckConstraint(
            "status in ('in_progress','locked')", name="chk_weekly_snapshot_status"
        ),
        Index("idx_weekly_snapshots_user", "user_id"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<WeeklySnapshot(id={self.weekly_snapshot_id}, date={self.reference_date})>"


class WeeklySnapshotHoldingEntity(Base):
    __tablename__ = "weekly_snapshot_holdings"

    weekly_snapshot_holding_id = Column(Integer, primary_key=True, autoincrement=True)
    weekly_snapshot_id = Column(
        Integer,
        ForeignKey("weekly_snapshots.weekly_snapshot_id", ondelete="CASCADE"),
        nullable=False,
    )
    holding_id = Column(
        Integer, ForeignKey("holdings.holding_id", ondelete="CASCADE"), nullable=False
    )
    valuation_amount = Column(Numeric(20, 4), nullable=False)
    data_source = Column(String(10), nullable=False)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (
        UniqueConstraint(
            "weekly_snapshot_id", "holding_id", name="uq_weekly_snapshot_holding"
        ),
        CheckConstraint(
            "data_source in ('auto','manual','missing')",
            name="chk_weekly_snapshot_data_source",
        ),
        Index("idx_weekly_snapshot_holdings_snap", "weekly_snapshot_id"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<WeeklySnapshotHolding(id={self.weekly_snapshot_holding_id}, weekly_snapshot_id={self.weekly_snapshot_id})>"


class AnnualSnapshotEntity(Base):
    __tablename__ = "annual_snapshots"

    annual_snapshot_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    reference_date = Column(Date, nullable=False)
    source_snapshot_id = Column(
        Integer, ForeignKey("snapshots.snapshot_id", ondelete="CASCADE"), nullable=False
    )
    status = Column(String(20), nullable=False)
    editable_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (
        UniqueConstraint(
            "user_id", "reference_date", name="uq_annual_snapshot_user_reference"
        ),
        CheckConstraint("status in ('locked')", name="chk_annual_snapshot_status"),
        Index("idx_annual_snapshots_user", "user_id"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<AnnualSnapshot(id={self.annual_snapshot_id}, date={self.reference_date})>"


class AnnualSnapshotHoldingEntity(Base):
    __tablename__ = "annual_snapshot_holdings"

    annual_snapshot_holding_id = Column(Integer, primary_key=True, autoincrement=True)
    annual_snapshot_id = Column(
        Integer,
        ForeignKey("annual_snapshots.annual_snapshot_id", ondelete="CASCADE"),
        nullable=False,
    )
    holding_id = Column(
        Integer, ForeignKey("holdings.holding_id", ondelete="CASCADE"), nullable=False
    )
    valuation_amount = Column(Numeric(20, 4), nullable=False)
    data_source = Column(String(10), nullable=False)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)

    __table_args__ = (
        UniqueConstraint(
            "annual_snapshot_id", "holding_id", name="uq_annual_snapshot_holding"
        ),
        CheckConstraint(
            "data_source in ('auto','manual','missing')",
            name="chk_annual_snapshot_data_source",
        ),
        Index("idx_annual_snapshot_holdings_snap", "annual_snapshot_id"),
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<AnnualSnapshotHolding(id={self.annual_snapshot_holding_id}, annual_snapshot_id={self.annual_snapshot_id})>"
