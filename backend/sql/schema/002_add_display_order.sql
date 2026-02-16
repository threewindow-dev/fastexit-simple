-- Add display order columns for institutions and accounts
-- Applies to: PostgreSQL 17

BEGIN;

ALTER TABLE institutions
    ADD COLUMN IF NOT EXISTS display_order INTEGER NOT NULL DEFAULT 0;

ALTER TABLE accounts
    ADD COLUMN IF NOT EXISTS display_order INTEGER NOT NULL DEFAULT 0;

COMMIT;
