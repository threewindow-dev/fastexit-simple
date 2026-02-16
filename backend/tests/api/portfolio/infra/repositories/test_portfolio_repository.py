"""
Integration tests for Portfolio repositories

Tests portfolio repositories (Institution, Product, Account, etc.)
with actual PostgreSQL database using Testcontainers
"""

import pytest
import pytest_asyncio
import psycopg
from datetime import date
from pathlib import Path
from contextvars import ContextVar

from subdomains.portfolio.domain.models import (
    Institution,
    Product,
    Account,
    AccountGroup,
    Holding,
    Snapshot,
)
from subdomains.portfolio.domain.errors import DuplicateEntityError, NotFoundError
from subdomains.portfolio.infra.repositories import (
    PsycopgInstitutionRepository,
    PsycopgProductRepository,
    PsycopgAccountRepository,
    PsycopgAccountGroupRepository,
    PsycopgHoldingRepository,
    PsycopgSnapshotRepository,
)
from shared.context.transaction_context import transaction_context


class MockTransaction:
    """Mock transaction for testing - wraps psycopg connection"""

    def __init__(self, connection):
        self.connection = connection

    async def begin(self):
        pass

    async def commit(self):
        await self.connection.commit()

    async def rollback(self):
        await self.connection.rollback()

    def get_connection(self):
        return self.connection


def _get_schema_files() -> list[Path]:
    """Get all SQL schema files in order (numerically sorted)"""
    schema_dir = Path(__file__).resolve().parents[5] / "sql" / "schema"
    if not schema_dir.exists():
        raise FileNotFoundError(f"Schema directory not found: {schema_dir}")

    sql_files = sorted(schema_dir.glob("*.sql"))
    if not sql_files:
        raise FileNotFoundError(f"No SQL files found in {schema_dir}")

    return sql_files


async def _initialize_schema(conn: psycopg.AsyncConnection) -> None:
    """Initialize database schema by executing all SQL files"""
    schema_files = _get_schema_files()

    for sql_file in schema_files:
        sql_content = sql_file.read_text()

        # Remove comment lines
        lines = []
        for line in sql_content.split("\n"):
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith("--"):
                lines.append(line)

        sql_content = "\n".join(lines)

        # Split by semicolon to handle multiple statements
        statements = [s.strip() for s in sql_content.split(";") if s.strip()]

        # Separate CREATE TABLE and CREATE INDEX statements
        create_tables = [s for s in statements if s.upper().startswith("CREATE TABLE")]
        create_indexes = [s for s in statements if s.upper().startswith("CREATE INDEX")]
        inserts = [s for s in statements if s.upper().startswith("INSERT")]
        others = [
            s
            for s in statements
            if not (
                s.upper().startswith("CREATE TABLE")
                or s.upper().startswith("CREATE INDEX")
                or s.upper().startswith("INSERT")
            )
        ]

        # Execute in order: tables, others, indexes, inserts
        for stmt in create_tables + others + create_indexes + inserts:
            try:
                await conn.execute(stmt)
            except Exception as e:
                # Continue on index/constraint errors (they may already exist)
                error_msg = str(e).lower()
                if (
                    "already exists" not in error_msg
                    and "duplicate key" not in error_msg
                    and "relation" not in error_msg
                ):
                    raise


@pytest_asyncio.fixture()
async def db_connection(postgres_container):
    """Create database connection and initialize schema from SQL files"""
    conn_str = postgres_container.get_connection_url()
    # Remove psycopg2 driver spec if present
    conn_str = conn_str.replace("+psycopg2", "").replace("+psycopg", "")
    if not conn_str.startswith("postgresql://"):
        conn_str = conn_str.replace("postgresql+", "postgresql://")

    conn = await psycopg.AsyncConnection.connect(
        conn_str,
        autocommit=True,  # Use autocommit for schema initialization
        row_factory=psycopg.rows.dict_row,  # Return rows as dictionaries
    )

    # Initialize schema
    await _initialize_schema(conn)

    yield conn

    await conn.close()


@pytest_asyncio.fixture
async def clean_db(db_connection):
    """Clean database before each test by rolling back and reinitializing"""
    # Rollback any pending transaction
    try:
        await db_connection.rollback()
    except Exception:
        pass

    # Drop all tables in reverse dependency order
    async with db_connection.cursor() as cur:
        tables = [
            "annual_snapshot_holdings",
            "annual_snapshots",
            "weekly_snapshot_holdings",
            "weekly_snapshots",
            "snapshot_holdings",
            "snapshots",
            "holdings",
            "account_group_accounts",
            "account_groups",
            "accounts",
            "products",
            "institutions",
        ]
        for table in tables:
            try:
                await cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
            except Exception:
                pass

    await db_connection.commit()

    # Reinitialize schema
    await _initialize_schema(db_connection)

    yield

    # Cleanup after test
    try:
        await db_connection.rollback()
    except Exception:
        pass


# ============================================================================
# Institution Tests
# ============================================================================


class TestInstitutionRepository:
    @pytest.mark.asyncio
    async def test_add_institution_success(self, db_connection, clean_db):
        """Should add institution and return with ID"""
        # Set transaction context for @use_transaction decorator
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        repo = PsycopgInstitutionRepository()
        institution = Institution.create(name="KB증권", type="증권사")

        # @use_transaction will inject connection automatically
        result = await repo.add(institution)

        assert result.institution_id is not None
        assert result.name == "KB증권"
        assert result.type == "증권사"

    @pytest.mark.asyncio
    async def test_find_institution_by_id(self, db_connection, clean_db):
        """Should find institution by ID"""
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        repo = PsycopgInstitutionRepository()
        institution = Institution.create(name="국민은행", type="은행")
        saved = await repo.add(institution)

        result = await repo.find_by_id(saved.institution_id)

        assert result is not None
        assert result.name == "국민은행"

    @pytest.mark.asyncio
    async def test_exists_by_name(self, db_connection, clean_db):
        """Should check institution existence by name"""
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        repo = PsycopgInstitutionRepository()
        institution = Institution.create(name="삼성증권", type="증권사")
        await repo.add(institution)

        exists = await repo.exists_by_name("삼성증권")
        not_exists = await repo.exists_by_name("없는증권")

        assert exists is True
        assert not_exists is False


# ============================================================================
# Product Tests
# ============================================================================


class TestProductRepository:
    @pytest.mark.asyncio
    async def test_add_product_success(self, db_connection, clean_db):
        """Should add product and return with ID"""
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        repo = PsycopgProductRepository()
        product = Product.create(
            product_name="삼성전자",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=None,
            risk_level="위험",
        )

        result = await repo.add(product)

        assert result.product_id is not None
        assert result.product_name == "삼성전자"
        assert result.asset_class == "주식"

    @pytest.mark.asyncio
    async def test_find_product_by_id(self, db_connection, clean_db):
        """Should find product by ID"""
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        repo = PsycopgProductRepository()
        product = Product.create(
            product_name="LG전자",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=None,
            risk_level="위험",
        )
        saved = await repo.add(product)

        result = await repo.find_by_id(saved.product_id)

        assert result is not None
        assert result.product_name == "LG전자"


# ============================================================================
# Account Tests
# ============================================================================


class TestAccountRepository:
    @pytest.mark.asyncio
    async def test_add_account_success(self, db_connection, clean_db):
        """Should add account and return with ID"""
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        # First add institution
        inst_repo = PsycopgInstitutionRepository()
        institution = Institution.create(name="국민은행", type="은행")
        inst = await inst_repo.add(institution)

        # Then add account
        repo = PsycopgAccountRepository()
        account = Account.create(
            institution_id=inst.institution_id, name="주식계좌", type="ISA"
        )

        result = await repo.add(account)

        assert result.account_id is not None
        assert result.name == "주식계좌"
        assert result.type == "ISA"

    @pytest.mark.asyncio
    async def test_find_account_by_id(self, db_connection, clean_db):
        """Should find account by ID"""
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        # Setup
        inst_repo = PsycopgInstitutionRepository()
        institution = Institution.create(name="국민은행", type="은행")
        inst = await inst_repo.add(institution)

        repo = PsycopgAccountRepository()
        account = Account.create(
            institution_id=inst.institution_id, name="예금계좌", type="CMA"
        )
        saved = await repo.add(account)

        # Test
        result = await repo.find_by_id(saved.account_id)

        assert result is not None
        assert result.name == "예금계좌"


# ============================================================================
# Holding Tests
# ============================================================================


class TestHoldingRepository:
    @pytest.mark.asyncio
    async def test_add_holding_success(self, db_connection, clean_db):
        """Should add holding and return with ID"""
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        # Setup: institution -> account -> product
        inst_repo = PsycopgInstitutionRepository()
        institution = Institution.create(name="국민은행", type="은행")
        inst = await inst_repo.add(institution)

        prod_repo = PsycopgProductRepository()
        product = Product.create(
            product_name="삼성전자",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=None,
            risk_level="위험",
        )
        prod = await prod_repo.add(product)

        acc_repo = PsycopgAccountRepository()
        account = Account.create(
            institution_id=inst.institution_id, name="주식계좌", type="ISA"
        )
        acc = await acc_repo.add(account)

        # Test: add holding
        repo = PsycopgHoldingRepository()
        holding = Holding.create(account_id=acc.account_id, product_id=prod.product_id)

        result = await repo.add(holding)

        assert result.holding_id is not None
        assert result.account_id == acc.account_id

    @pytest.mark.asyncio
    async def test_find_holding_by_id(self, db_connection, clean_db):
        """Should find holding by ID"""
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        # Setup
        inst_repo = PsycopgInstitutionRepository()
        institution = Institution.create(name="국민은행", type="은행")
        inst = await inst_repo.add(institution)

        prod_repo = PsycopgProductRepository()
        product = Product.create(
            product_name="LG전자",
            asset_class="주식",
            region="대한민국",
            currency="KRW",
            investment_type="직접",
            characteristics=None,
            risk_level="위험",
        )
        prod = await prod_repo.add(product)

        acc_repo = PsycopgAccountRepository()
        account = Account.create(
            institution_id=inst.institution_id, name="예금계좌", type="CMA"
        )
        acc = await acc_repo.add(account)

        repo = PsycopgHoldingRepository()
        holding = Holding.create(account_id=acc.account_id, product_id=prod.product_id)
        saved = await repo.add(holding)

        # Test
        result = await repo.find_by_id(saved.holding_id)

        assert result is not None
        assert result.product_id == prod.product_id


# ============================================================================
# Snapshot Tests
# ============================================================================


class TestSnapshotRepository:
    @pytest.mark.asyncio
    async def test_add_snapshot_success(self, db_connection, clean_db):
        """Should add snapshot and return with ID"""
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        repo = PsycopgSnapshotRepository()
        snapshot = Snapshot.create(
            user_id=1,  # Assuming user_id=1 exists (from users table)
            reference_date=date(2025, 1, 22),
        )

        result = await repo.add(snapshot)

        assert result.snapshot_id is not None
        assert result.status == "in_progress"

    @pytest.mark.asyncio
    async def test_find_snapshot_by_id(self, db_connection, clean_db):
        """Should find snapshot by ID"""
        mock_tx = MockTransaction(db_connection)
        transaction_context.set(mock_tx)

        repo = PsycopgSnapshotRepository()
        snapshot = Snapshot.create(
            user_id=1,  # Assuming user_id=1 exists (from users table)
            reference_date=date(2025, 1, 21),
        )
        saved = await repo.add(snapshot)

        result = await repo.find_by_id(saved.snapshot_id)

        assert result is not None
        assert result.status == "in_progress"
