BEGIN;

ALTER TABLE products
ADD COLUMN IF NOT EXISTS allow_snapshot_input BOOLEAN NOT NULL DEFAULT TRUE;

UPDATE products
SET allow_snapshot_input = FALSE
WHERE product_name = '평가금액 보정';

COMMIT;
