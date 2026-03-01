-- Rename include_in_weekly_report to include_in_report
-- Applies to: PostgreSQL 17

BEGIN;

-- Rename the index
DROP INDEX IF EXISTS idx_account_groups_weekly_report;

-- Rename the column
ALTER TABLE account_groups
RENAME COLUMN include_in_weekly_report TO include_in_report;

-- Recreate the index with new name
CREATE INDEX IF NOT EXISTS idx_account_groups_report
ON account_groups(include_in_report)
WHERE include_in_report = TRUE;

COMMIT;
