-- Create target_allocation_accounts table for storing account-level goal amounts
-- Applies to: PostgreSQL 17

BEGIN;

CREATE TABLE IF NOT EXISTS target_allocation_accounts (
    target_allocation_account_id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    target_amount DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_target_allocation_accounts_account FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    CONSTRAINT uq_target_allocation_account_year_account UNIQUE (year, account_id),
    CONSTRAINT chk_target_allocation_account_amount CHECK (target_amount >= 0),
    CONSTRAINT chk_target_allocation_account_year CHECK (year >= 2020 AND year <= 2100)
);

-- Create index for querying by year
CREATE INDEX IF NOT EXISTS idx_target_allocation_accounts_year ON target_allocation_accounts(year);

-- Create index for querying by account_id
CREATE INDEX IF NOT EXISTS idx_target_allocation_accounts_account ON target_allocation_accounts(account_id);

COMMIT;
