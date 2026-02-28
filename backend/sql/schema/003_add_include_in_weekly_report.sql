-- Add include_in_weekly_report column to account_groups table
-- Applies to: PostgreSQL 17

BEGIN;

-- Add column to account_groups
ALTER TABLE account_groups 
ADD COLUMN IF NOT EXISTS include_in_weekly_report BOOLEAN NOT NULL DEFAULT FALSE;

-- Create index for faster filtering
CREATE INDEX IF NOT EXISTS idx_account_groups_weekly_report 
ON account_groups(include_in_weekly_report) 
WHERE include_in_weekly_report = TRUE;

COMMIT;
