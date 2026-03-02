-- Create target_allocation_totals table for storing annual total target amount
-- This table stores the total target amount per year (in addition to per-account-group targets)

BEGIN;

CREATE TABLE IF NOT EXISTS target_allocation_totals (
    target_allocation_total_id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    target_amount DECIMAL(15, 2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_target_allocation_totals_year UNIQUE (year),
    CONSTRAINT chk_target_allocation_totals_year CHECK (year >= 2020 AND year <= 2100),
    CONSTRAINT chk_target_allocation_totals_amount CHECK (target_amount >= 0)
);

CREATE INDEX IF NOT EXISTS idx_target_allocation_totals_year
    ON target_allocation_totals(year);

COMMIT;
