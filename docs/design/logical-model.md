# 논리 모델 (Logical Data Model) - fastexit

**목적**: 개념 모델을 정규화된 테이블 구조로 구체화하여 물리 설계(PostgreSQL DDL) 이전의 기준을 제시합니다.

**작성일**: 2026-01-22

**소유자**: Product Owner, Development Team

---

## 설계 원칙
- 식별자: 모든 엔티티는 시스템 생성 ID를 사용.
- 정규화: 자산군/속성 등 참조 데이터는 enum 또는 lookup 테이블로 관리 가능.
- 상태/잠금: 스냅샷 계열은 status + locked_at + editable_until로 수정 가능 기한을 표현.
- 불변식: locked 이후 업데이트 금지(애플리케이션/DB 제약으로 강제).

---

## 엔티티별 테이블 정의

### 1) User (사용자)
- `user_id` (PK, bigint, generated)
- `username` (varchar, unique)
- `email` (varchar, unique)
- `role` (varchar) — admin | user
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

### 2) Institution (금융사)
- `institution_id` (PK, bigint, generated)
- `name` (varchar)
- `type` (varchar) — 증권사/은행/기타
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

### 3) Account (계좌)
- `account_id` (PK, bigint, generated)
- `institution_id` (FK → Institution)
- `name` (varchar)
- `type` (varchar)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

고유 제약: (institution_id, name) 필요 시 유니크. 식별은 account_id.

### 4) AccountGroup (계좌 그룹)
- `account_group_id` (PK, bigint, generated)
- `name` (varchar)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

### 5) AccountGroupAccount (M:N 브리지)
- `account_group_id` (FK → AccountGroup)
- `account_id` (FK → Account)
- PK: (account_group_id, account_id)
- `added_at` (timestamptz)

### 6) Product (상품)
- `product_id` (PK, bigint, generated)
- `product_name` (varchar)
- `asset_class` (varchar) — 주식/채권/통화/금/부동산/가상자산/기타
- `region` (varchar) — 대한민국/미국
- `currency` (varchar) — KRW/USD
- `investment_type` (varchar) — 직접/ETF
- `characteristics` (varchar[]) — 개별종목/수시입출금/지수추종/월배당/소수점투자/현물/레버리지/예금/적금
- `risk_level` (varchar) — 위험/안전
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

### 7) Holding (자산)
- `holding_id` (PK, bigint, generated)
- `account_id` (FK → Account)
- `product_id` (FK → Product)
- `is_visible` (boolean, default true)
- `hidden_at` (timestamptz, nullable)
- `deleted_at` (timestamptz, nullable)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

고유 제약: (account_id, product_id) 유니크 (동일 계좌-상품 중복 방지)

### 8) Snapshot (일반 스냅샷)
- `snapshot_id` (PK, bigint, generated)
- `user_id` (FK → User)
- `reference_date` (date)
- `status` (varchar) — in_progress | locked
- `editable_until` (timestamptz, nullable)
- `locked_at` (timestamptz, nullable)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

고유 제약: (user_id, reference_date, type='general') 유니크 가정 (type 컬럼 사용 시 포함)

### 9) SnapshotHolding (일반 스냅샷 내 자산 상태)
- `snapshot_holding_id` (PK, bigint, generated)
- `snapshot_id` (FK → Snapshot)
- `holding_id` (FK → Holding)
- `valuation_amount` (numeric)
- `data_source` (varchar) — auto | manual | missing
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

고유 제약: (snapshot_id, holding_id)

### 10) WeeklySnapshot
- `weekly_snapshot_id` (PK, bigint, generated)
- `user_id` (FK → User)
- `reference_date` (date) — 토요일
- `source_snapshot_id` (FK → Snapshot) — 원본 일반 스냅샷 (locked)
- `status` (varchar) — locked (생성 후 수정 가능 기한만 허용)
- `editable_until` (timestamptz, nullable)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

고유 제약: (user_id, reference_date) 유니크

### 11) WeeklySnapshotHolding
- `weekly_snapshot_holding_id` (PK, bigint, generated)
- `weekly_snapshot_id` (FK → WeeklySnapshot)
- `holding_id` (FK → Holding)
- `valuation_amount` (numeric)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

고유 제약: (weekly_snapshot_id, holding_id)

### 12) AnnualSnapshot
- `annual_snapshot_id` (PK, bigint, generated)
- `user_id` (FK → User)
- `reference_date` (date) — 1월 1일
- `source_snapshot_id` (FK → Snapshot) — 1/1 인근 locked 일반 스냅샷
- `status` (varchar) — locked (생성 후 수정 가능 기한만 허용)
- `editable_until` (timestamptz, nullable)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

고유 제약: (user_id, reference_date) 유니크

### 13) AnnualSnapshotHolding
- `annual_snapshot_holding_id` (PK, bigint, generated)
- `annual_snapshot_id` (FK → AnnualSnapshot)
- `holding_id` (FK → Holding)
- `valuation_amount` (numeric)
- `created_at` (timestamptz)
- `updated_at` (timestamptz)

고유 제약: (annual_snapshot_id, holding_id)

---

## 제약 및 인덱스 제안
- FK 인덱스: 모든 FK 컬럼에 인덱스 생성 (institution_id, account_id, product_id, snapshot_id 등).
- 조회 패턴 인덱스:
  - Snapshot: (user_id, reference_date, status)
  - WeeklySnapshot/AnnualSnapshot: (user_id, reference_date)
  - Holding: (account_id, product_id) 유니크 + account_id 인덱스
- 체크 제약:
  - snapshot.status ∈ {in_progress, locked}
  - locked_at IS NOT NULL WHEN status = 'locked'
  - editable_until >= created_at (nullable 허용)

---

## 열거/참조 데이터 전략
- `asset_class`, `region`, `currency`, `investment_type`, `risk_level`: enum 또는 lookup 테이블 선택 가능
- `characteristics`: 배열(varchar[]) 사용, 필요 시 별도 테이블로 정규화 가능

---

## 스냅샷 생성/수정 정책 반영 포인트
- 일반 스냅샷은 in_progress 상태에서 자산별 부분 입력 가능, locked 이후 수정 금지
- 주간/연간 스냅샷은 각각 일반 스냅샷을 원본으로 생성하며 editable_until 내에서만 수정 가능
- 원본 스냅샷(source_snapshot_id) FK로 추적하여 감사/재생성 근거 확보

---

## 다음 단계
1) 열거형을 enum vs lookup 테이블 중 선택
2) 정밀 타입 선정 (numeric precision/scale, varchar 길이)
3) DDL 스크립트(PostgreSQL) 작성 및 마이그레이션 도구 반영
4) 상태/잠금 제약을 트리거 또는 체크 제약으로 구체화
