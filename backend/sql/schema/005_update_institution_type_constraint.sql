-- Add '기타기관' to institution type constraint and remove '기타'
-- Applies to: PostgreSQL 17

BEGIN;

-- Update existing '기타' type to '기타기관'
UPDATE institutions SET type = '기타기관' WHERE type = '기타';

-- Drop existing constraint
ALTER TABLE institutions DROP CONSTRAINT IF EXISTS chk_institution_type;

-- Add new constraint with only '증권사', '은행', '기타기관'
ALTER TABLE institutions ADD CONSTRAINT chk_institution_type 
    CHECK (type IN ('증권사', '은행', '기타기관'));

COMMIT;
