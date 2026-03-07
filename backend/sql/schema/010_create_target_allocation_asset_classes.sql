-- Create target_allocation_asset_classes table for storing asset class percentage targets
-- Applies to: PostgreSQL 17

BEGIN;

CREATE TABLE IF NOT EXISTS target_allocation_asset_classes (
    target_allocation_asset_class_id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    asset_class VARCHAR(100) NOT NULL,
    target_percentage DECIMAL(5, 2) NOT NULL CHECK (target_percentage >= 0 AND target_percentage <= 100),
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_target_allocation_asset_class_year UNIQUE (year, asset_class)
);

-- Create index for querying by year
CREATE INDEX IF NOT EXISTS idx_target_allocation_asset_classes_year ON target_allocation_asset_classes(year);

-- Create index for querying by asset_class
CREATE INDEX IF NOT EXISTS idx_target_allocation_asset_classes_asset_class ON target_allocation_asset_classes(asset_class);

COMMIT;
