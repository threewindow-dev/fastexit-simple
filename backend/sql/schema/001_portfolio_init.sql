-- Portfolio domain tables
-- Applies to: PostgreSQL 17
-- Note: keep enums as check constraints for simplicity; align with SQLAlchemy entities

BEGIN;

-- Institutions
CREATE TABLE IF NOT EXISTS institutions (
    institution_id SERIAL PRIMARY KEY,
    name           VARCHAR(255) NOT NULL UNIQUE,
    type           VARCHAR(50)  NOT NULL CHECK (type IN ('증권사', '은행', '기타기관')),
    display_order  INTEGER      NOT NULL DEFAULT 0,
    created_at     TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- Products
CREATE TABLE IF NOT EXISTS products (
    product_id       SERIAL PRIMARY KEY,
    product_name     VARCHAR(255) NOT NULL,
    asset_class      VARCHAR(50)  NOT NULL CHECK (asset_class IN ('주식', '채권', '통화', '금', '부동산', '가상자산', '기타자산')),
    region           VARCHAR(50)  NOT NULL CHECK (region IN ('대한민국', '미국')),
    currency         VARCHAR(10)  NOT NULL CHECK (currency IN ('KRW', 'USD')),
    investment_type  VARCHAR(50)  NOT NULL CHECK (investment_type IN ('직접', 'ETF')),
    characteristics  TEXT[]       NULL,
    risk_level       VARCHAR(20)  NOT NULL CHECK (risk_level IN ('안전', '위험')),
    allow_snapshot_input BOOLEAN  NOT NULL DEFAULT TRUE,
    ticker           VARCHAR(32)  NULL,
    domestic_beta    NUMERIC(12,6) NULL,
    global_beta      NUMERIC(12,6) NULL,
    beta_collected_at TIMESTAMP WITHOUT TIME ZONE NULL,
    display_order    INTEGER      NOT NULL DEFAULT 0,
    created_at       TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE (product_name, asset_class, region, currency, investment_type)
);

-- Accounts
CREATE TABLE IF NOT EXISTS accounts (
    account_id     SERIAL PRIMARY KEY,
    institution_id INTEGER      NOT NULL REFERENCES institutions(institution_id) ON DELETE CASCADE,
    name           VARCHAR(255) NOT NULL,
    type           VARCHAR(100) NOT NULL,
    allow_snapshot_input BOOLEAN NOT NULL DEFAULT TRUE,
    display_order  INTEGER      NOT NULL DEFAULT 0,
    created_at     TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE (institution_id, name)
);
CREATE INDEX IF NOT EXISTS idx_accounts_institution ON accounts(institution_id);

-- Account Groups
CREATE TABLE IF NOT EXISTS account_groups (
    account_group_id SERIAL PRIMARY KEY,
    name             VARCHAR(255) NOT NULL UNIQUE,
    created_at       TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
);

-- Account Group - Account mapping
CREATE TABLE IF NOT EXISTS account_group_accounts (
    account_group_id INTEGER NOT NULL REFERENCES account_groups(account_group_id) ON DELETE CASCADE,
    account_id       INTEGER NOT NULL REFERENCES accounts(account_id) ON DELETE CASCADE,
    created_at       TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (account_group_id, account_id)
);
CREATE INDEX IF NOT EXISTS idx_account_group_accounts_account ON account_group_accounts(account_id);

-- Holdings
CREATE TABLE IF NOT EXISTS holdings (
    holding_id   SERIAL PRIMARY KEY,
    account_id   INTEGER NOT NULL REFERENCES accounts(account_id) ON DELETE CASCADE,
    product_id   INTEGER NOT NULL REFERENCES products(product_id) ON DELETE CASCADE,
    is_visible   BOOLEAN NOT NULL DEFAULT TRUE,
    deleted_at   TIMESTAMP WITHOUT TIME ZONE NULL,
    deletion_reason TEXT NULL,
    created_at   TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE (account_id, product_id)
);
CREATE INDEX IF NOT EXISTS idx_holdings_account ON holdings(account_id);
CREATE INDEX IF NOT EXISTS idx_holdings_product ON holdings(product_id);

-- Snapshots (general)
CREATE TABLE IF NOT EXISTS snapshots (
    snapshot_id    SERIAL PRIMARY KEY,
    user_id        INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reference_date DATE    NOT NULL,
    status         VARCHAR(20) NOT NULL CHECK (status IN ('in_progress', 'locked')),
    locked_at      TIMESTAMP WITHOUT TIME ZONE NULL,
    editable_until TIMESTAMP WITHOUT TIME ZONE NULL,
    created_at     TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, reference_date)
);
CREATE INDEX IF NOT EXISTS idx_snapshots_user ON snapshots(user_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_status ON snapshots(status);

-- Snapshot holdings (valuation per holding per snapshot)
CREATE TABLE IF NOT EXISTS snapshot_holdings (
    snapshot_holding_id SERIAL PRIMARY KEY,
    snapshot_id         INTEGER NOT NULL REFERENCES snapshots(snapshot_id) ON DELETE CASCADE,
    holding_id          INTEGER NOT NULL REFERENCES holdings(holding_id) ON DELETE CASCADE,
    valuation_amount    NUMERIC(20,4) NOT NULL,
    data_source         VARCHAR(10) NOT NULL CHECK (data_source IN ('auto', 'manual', 'missing')),
    created_at          TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE (snapshot_id, holding_id)
);
CREATE INDEX IF NOT EXISTS idx_snapshot_holdings_snapshot ON snapshot_holdings(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_snapshot_holdings_holding ON snapshot_holdings(holding_id);

-- Weekly snapshots
CREATE TABLE IF NOT EXISTS weekly_snapshots (
    weekly_snapshot_id SERIAL PRIMARY KEY,
    user_id            INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reference_date     DATE    NOT NULL,
    source_snapshot_id INTEGER NOT NULL REFERENCES snapshots(snapshot_id) ON DELETE CASCADE,
    status             VARCHAR(20) NOT NULL CHECK (status IN ('in_progress', 'locked')),
    editable_until     TIMESTAMP WITHOUT TIME ZONE NULL,
    created_at         TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, reference_date)
);
CREATE INDEX IF NOT EXISTS idx_weekly_snapshots_user ON weekly_snapshots(user_id);

CREATE TABLE IF NOT EXISTS weekly_snapshot_holdings (
    weekly_snapshot_holding_id SERIAL PRIMARY KEY,
    weekly_snapshot_id         INTEGER NOT NULL REFERENCES weekly_snapshots(weekly_snapshot_id) ON DELETE CASCADE,
    holding_id                 INTEGER NOT NULL REFERENCES holdings(holding_id) ON DELETE CASCADE,
    valuation_amount           NUMERIC(20,4) NOT NULL,
    data_source                VARCHAR(10) NOT NULL CHECK (data_source IN ('auto', 'manual', 'missing')),
    created_at                 TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE (weekly_snapshot_id, holding_id)
);
CREATE INDEX IF NOT EXISTS idx_weekly_snapshot_holdings_snap ON weekly_snapshot_holdings(weekly_snapshot_id);

-- Annual snapshots
CREATE TABLE IF NOT EXISTS annual_snapshots (
    annual_snapshot_id SERIAL PRIMARY KEY,
    user_id            INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reference_date     DATE    NOT NULL,
    source_snapshot_id INTEGER NOT NULL REFERENCES snapshots(snapshot_id) ON DELETE CASCADE,
    status             VARCHAR(20) NOT NULL CHECK (status IN ('locked')),
    editable_until     TIMESTAMP WITHOUT TIME ZONE NULL,
    created_at         TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, reference_date)
);
CREATE INDEX IF NOT EXISTS idx_annual_snapshots_user ON annual_snapshots(user_id);

CREATE TABLE IF NOT EXISTS annual_snapshot_holdings (
    annual_snapshot_holding_id SERIAL PRIMARY KEY,
    annual_snapshot_id         INTEGER NOT NULL REFERENCES annual_snapshots(annual_snapshot_id) ON DELETE CASCADE,
    holding_id                 INTEGER NOT NULL REFERENCES holdings(holding_id) ON DELETE CASCADE,
    valuation_amount           NUMERIC(20,4) NOT NULL,
    data_source                VARCHAR(10) NOT NULL CHECK (data_source IN ('auto', 'manual', 'missing')),
    created_at                 TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE (annual_snapshot_id, holding_id)
);
CREATE INDEX IF NOT EXISTS idx_annual_snapshot_holdings_snap ON annual_snapshot_holdings(annual_snapshot_id);

COMMIT;
