-- Create target_allocations table for storing goal asset allocations
-- Applies to: PostgreSQL 17

BEGIN;

CREATE TABLE IF NOT EXISTS target_allocations (
    target_allocation_id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    account_group_id INTEGER NOT NULL,
    target_amount DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_target_allocations_account_group FOREIGN KEY (account_group_id) REFERENCES account_groups(account_group_id) ON DELETE CASCADE,
    CONSTRAINT uq_target_allocation_year_group UNIQUE (year, account_group_id)
);

-- Create index for querying by year
CREATE INDEX IF NOT EXISTS idx_target_allocations_year ON target_allocations(year);

-- Create index for querying by account_group_id
CREATE INDEX IF NOT EXISTS idx_target_allocations_account_group ON target_allocations(account_group_id);

COMMIT;
