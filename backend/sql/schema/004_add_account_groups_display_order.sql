-- Add display_order column to account_groups table
-- Applies to: PostgreSQL 17

BEGIN;

ALTER TABLE account_groups
    ADD COLUMN IF NOT EXISTS display_order INTEGER NOT NULL DEFAULT 0;

COMMIT;
