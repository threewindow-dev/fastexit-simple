BEGIN;

ALTER TABLE accounts
ADD COLUMN IF NOT EXISTS allow_snapshot_input BOOLEAN NOT NULL DEFAULT TRUE;

-- 사용 중단 계좌는 스냅샷 평가금액 입력 화면에서 숨김 처리
UPDATE accounts
SET allow_snapshot_input = FALSE
WHERE name IN ('우리은행 정기예금', '신한은행 신한쏠편한적금');

COMMIT;
