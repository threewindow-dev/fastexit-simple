# Glossary - fastexit 도메인 공통어

간단 설명: fastexit 시스템의 핵심 용어를 명확히 정의하여 팀 전체의 공통 이해를 보장합니다.

---

## 사용자 (User)

**정의**: fastexit에 접근하는 모든 요청을 발생시키는 대상

**동의어**: 없음

**사용 예시**: 웹사이트 방문자, API 호출자

**관련 유스케이스**: -

**API 매핑**: `components/schemas/User`

**소유자**: Product Owner

---

## 로그인한 사용자 (Logged-in User)

**정의**: 외부 계정 서비스를 통해 로그인한 사용자

**동의어**: 인증된 사용자

**사용 예시**: Google 계정으로 로그인한 사용자

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AuthenticatedUser`

**소유자**: Product Owner

---

## 승인된 사용자 (Approved User)

**정의**: 로그인 후 관리자의 승인을 받은 사용자

**동의어**: 활성 사용자

**사용 예시**: 관리자 승인을 받아 자산 현황 조회가 가능한 사용자

**관련 유스케이스**: -

**API 매핑**: `components/schemas/ApprovedUser`

**소유자**: Product Owner

---

## 관리자 (Administrator)

**정의**: 시스템 설치 시 등록되며, 사용자 승인 및 스냅샷 관리 권한을 가진 사용자

**동의어**: Admin, 시스템 관리자

**사용 예시**: 사용자 승인 처리, 스냅샷 변경 권한을 가진 사용자

**관련 유스케이스**: -

**API 매핑**: `components/schemas/Administrator`

**소유자**: Product Owner

---

## 외부 계정 서비스 (External Account Service)

**정의**: 사용자 로그인을 위해 사용하는 외부 인증 서비스

**동의어**: OAuth 제공자, SSO

**사용 예시**: Google, GitHub 등의 OAuth 서비스

**관련 유스케이스**: -

**API 매핑**: `components/schemas/OAuthProvider`

**소유자**: Product Owner

---

## 자산 현황 (Asset Status / Portfolio Snapshot)

**정의**: 사용자의 금융 자산 전체에 대한 특정 기준일의 현황. 금융사, 계좌, 자산(보유 상품), 자산 속성, 평가금액으로 구성됨

**도메인 모델**: `AssetStatus` (Value Object) 또는 `Portfolio` (Aggregate Root)

**인프라 모델**: `AssetStatusEntity`, `PortfolioSnapshotEntity`

**인터페이스**: `AssetStatusResponse`, `PortfolioResponse`

**동의어**: 자산 정보, 포트폴리오, 자산 조회 결과

**사용 예시**: 2025년 1월 22일 기준 삼성증권 ISA 계좌의 TIGER 미국S&P500 ETF 1,500,000원

**관련 유스케이스**: 자산 현황 조회, 자산 변동 추적

**API 매핑**: `components/schemas/AssetStatus`, `components/schemas/Portfolio`

**소유자**: Product Owner

---

## 금융사 (Institution)

**정의**: 사용자의 자산을 보관/관리하는 금융기관

**도메인 모델**: `Institution` (Entity)

**인프라 모델**: `InstitutionEntity`

**인터페이스**: `InstitutionResponse`

**동의어**: 금융회사, 금융기관, 금융회사이름

**사용 예시**: 삼성증권, KB증권, 신한은행, 토스뱅크

**관련 유스케이스**: 자산 조회, 계좌 등록

**API 매핑**: `components/schemas/Institution`, `components/schemas/AssetStatus/properties/institution`

**소유자**: Product Owner

---

## 계좌 (Account)

**정의**: 금융사 내에서 자산을 관리하는 단위. 식별자는 금융사와 계좌번호의 조합

**도메인 모델**: `Account` (Entity)

**인프라 모델**: `AccountEntity`

**인터페이스**: `AccountResponse`

**동의어**: 계좌이름, 없음

**사용 예시**: ISA 계좌, CMA 계좌, 연금저축, 일반 증권 계좌

**관련 유스케이스**: 계좌 등록, 자산 조회

**API 매핑**: `components/schemas/Account`, `components/schemas/AssetStatus/properties/account`

**소유자**: Product Owner

---

## 자산 (Holding)

**정의**: 특정 계좌에서 보유 중인 개별 금융상품의 한 단위

**도메인 모델**: `Holding` (Entity)

**인프라 모델**: `HoldingEntity`

**인터페이스**: `HoldingResponse`

**동의어**: 보유 자산, 자산 항목

**사용 예시**: AAPL 주식 10주, TIGER S&P500 ETF 100주, KB Star 정기예금 500만원

**관련 유스케이스**: 자산 현황 조회, 자산 추적

**API 매핑**: `components/schemas/Holding`, `components/schemas/AssetStatus/properties/holding`

**소유자**: Product Owner

---

## 자산 속성 (Asset Attributes)

**정의**: 상품을 분류하고 분석하기 위한 다차원 속성. 투자 지역, 자산 종류, 화폐, 투자유형, 자산특징, 위험도로 구성됨

**도메인 모델**: `AssetAttributes` (Value Object) — Product에 귀속

**인프라 모델**: 정규화된 별도 테이블 또는 JSON 컬럼으로 저장

**인터페이스**: `AssetAttributesResponse`

**동의어**: 자산 분류, 자산 메타데이터, 자산 정보

**사용 예시**: 한국/주식/원화/직접투자/개별종목/위험 (또는 미국/ETF/달러/지수추종/저위험)

**관련 유스케이스**: 상품 등록, 자산 분류, 포트폴리오 분석, 자산 필터링

**API 매핑**: `components/schemas/AssetAttributes`

**소유자**: Product Owner

---

## 투자 지역 (Investment Region)

**정의**: 자산이 투자된 지역 구분. 한국 또는 미국

**동의어**: 투자 국가

**사용 예시**: 한국, 미국

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetAttributes/properties/region`

**소유자**: Product Owner

---

## 자산 종류 (Asset Type)

**정의**: 자산의 기본 유형 분류

**동의어**: 자산 클래스

**사용 예시**: 주식, 채권, 통화, 금, 부동산, 기타자산

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetAttributes/properties/assetType`

**소유자**: Product Owner

---

## 화폐 (Currency)

**정의**: 자산의 평가 화폐 단위

**동의어**: 통화

**사용 예시**: 원화, 달러

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetAttributes/properties/currency`

**소유자**: Product Owner

---

## 투자유형 (Investment Type)

**정의**: 자산 투자 방식 구분

**동의어**: 없음

**사용 예시**: 직접 투자, ETF

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetAttributes/properties/investmentType`

**소유자**: Product Owner

---

## 자산특징 (Asset Characteristics)

**정의**: 자산의 세부적인 특성

**동의어**: 자산 속성

**사용 예시**: 개별종목, 지수추종, 수시입출금, 소수점투자, 레버리지, 월배당, 예금, 적금

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetAttributes/properties/characteristics`

**소유자**: Product Owner

---

## 위험도 (Risk Level)

**정의**: 자산의 위험 수준 평가

**동의어**: 리스크 레벨

**사용 예시**: 위험, 안전

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetAttributes/properties/riskLevel`

**소유자**: Product Owner

---

## 상품명 (Product Name)

**정의**: 자산 상품의 구체적인 명칭

**동의어**: 종목명

**사용 예시**: TIGER 미국S&P500, 삼성전자, KB Star 정기예금

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetStatus/properties/productName`

**소유자**: Product Owner

---

## 평가금액 (Valuation Amount)

**정의**: 자산의 현재 평가 금액

**동의어**: 평가액, 시가

**사용 예시**: 1,500,000원

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetStatus/properties/valuationAmount`

**소유자**: Product Owner

---

## 스냅샷 (Snapshot)

**정의**: 사용자의 자산 포트폴리오에 대한 특정 기준일의 기록. 기준일 시점의 모든 자산 현황을 캡처하며, 수정 가능 기한 내에는 수정 가능

**도메인 모델**: `PortfolioSnapshot` (Value Object 또는 Aggregate)

**인프라 모델**: `SnapshotEntity`, `PortfolioSnapshotEntity`

**인터페이스**: `SnapshotResponse`, `PortfolioSnapshotResponse`

**동의어**: 자산 스냅샷, 기준일 현황, 포트폴리오 기록

**사용 예시**: 2025년 1월 4일(토) 기준 자산 현황

**수정 정책**:
- 주간 스냅샷: 다음 주간 스냅샷 생성 전까지 수정 가능 (최대 1주)
- 연간 스냅샷: 생성 후 1주일간 수정 가능
- 수정 가능 기한 경과 후 과거 기록으로 확정

**관련 유스케이스**: 자산 추적, 성과 분석, 과거 자산 조회

**API 매핑**: `components/schemas/Snapshot`, `components/schemas/PortfolioSnapshot`

**소유자**: Product Owner

---

## 주간 스냅샷 (Weekly Snapshot)

**정의**: 매주 토요일 자동 생성되는 자산 포트폴리오 스냅샷. 주 단위의 자산 변동을 추적하는 기준

**도메인 모델**: `WeeklySnapshot` (Value Object)

**인프라 모델**: `WeeklySnapshotEntity`

**인터페이스**: `WeeklySnapshotResponse`

**동의어**: 주별 스냅샷, 주간 기록

**사용 예시**: 2025년 1월 4일(토), 2025년 1월 11일(토)

**관련 유스케이스**: 주간 자산 조회, 주 단위 성과 분석

**API 매핑**: `components/schemas/WeeklySnapshot`

**소유자**: Product Owner

---

## 연간 스냅샷 (Annual Snapshot)

**정의**: 매년 1월 1일 자동 생성되는 자산 포트폴리오 스냅샷. 연 단위의 장기 자산 변동을 추적하는 기준

**도메인 모델**: `AnnualSnapshot` (Value Object)

**인프라 모델**: `AnnualSnapshotEntity`

**인터페이스**: `AnnualSnapshotResponse`

**동의어**: 연별 스냅샷, 연초 스냅샷, 연간 기록

**사용 예시**: 2024년 1월 1일, 2025년 1월 1일

**관련 유스케이스**: 연간 자산 조회, 연 단위 성과 분석, 연 초 비교

**API 매핑**: `components/schemas/AnnualSnapshot`

**소유자**: Product Owner

---

## 자산군 (Asset Class)

**정의**: 금융상품을 분류하는 상위 카테고리. 포트폴리오 구성의 기본 분류 단위

**도메인 모델**: `AssetClass` (Value Object, 열거형)

**인프라 모델**: `asset_class` 컬럼 (ENUM 타입)

**인터페이스**: `AssetClassResponse`

**동의어**: 자산 분류, 자산 타입 (상위 카테고리)

**사용 예시**: 주식, 채권, 통화, 금, 부동산, 가상자산, 기타자산

**허용된 값**: 주식, 채권, 통화, 금, 부동산, 가상자산, 기타자산

**관련 유스케이스**: 자산 분류, 포트폴리오 자산군별 집계, 자산 필터링

**API 매핑**: `components/schemas/AssetClass`, `components/schemas/Holding/properties/assetClass`

**소유자**: Product Owner

---

## 상품 (Product)

**정의**: 투자 가능한 금융상품의 마스터 데이터. 자산군 및 분류 속성을 보유하며, 계좌에 편입될 때 자산(Holding)과 연결됨

**도메인 모델**: `Product` (Entity)

**인프라 모델**: `ProductEntity`

**인터페이스**: `ProductResponse`

**동의어**: 금융상품, 종목

**사용 예시**: VOO, TLT, AAPL, 달러, 금현물, BITO, 청약저축, 현금, 정기예금, RP, 발행어음

**주요 속성**: 상품코드, 상품명, 자산군, 자산 속성(지역/화폐/위험도 등)

**관련 유스케이스**: 상품 등록, 자산 추가, 자산 조회

**API 매핑**: `components/schemas/Product`

**소유자**: Product Owner

---

## 계좌 그룹 (Account Group)

**정의**: 관리자가 정의한 논리적 계좌 그룹핑. 서로 다른 금융사의 계좌를 하나의 그룹으로 관리 가능

**도메인 모델**: `AccountGroup` (Entity)

**인프라 모델**: `AccountGroupEntity`

**인터페이스**: `AccountGroupResponse`

**동의어**: 계좌 묶음, 포트폴리오 부분집합

**사용 예시**: "미국 투자 계좌", "장기 저축", "단기 트레이딩"

**주요 속성**:
- 그룹명 (name)
- 포함 계좌 (accounts): 1개 이상의 계좌, 다양한 금융사 가능

**불변식**:
- 같은 사용자 내에서 그룹명은 고유
- 계좌는 여러 그룹에 동시 포함 가능 (M:N 관계)

**관련 유스케이스**: 계좌 그룹화, 그룹별 조회, 그룹별 정렬된 조회

**API 매핑**: `components/schemas/AccountGroup`

**소유자**: Product Owner

**권한**: 관리자만 생성/수정/삭제 가능

---

## 기준일 (Reference Date)

**정의**: 스냅샷이 생성되는 기준이 되는 날짜

**동의어**: 스냅샷 날짜

**사용 예시**: 2025년 1월 4일(토), 2025년 1월 1일

**관련 유스케이스**: -

**API 매핑**: `components/schemas/Snapshot/properties/referenceDate`

**소유자**: Product Owner

---

## 작성/변경 지침
- 각 용어는 `## 용어명 (English Name)` 형식으로 작성하세요.
- 소유자(Owner)를 명시하세요.
- 변경 시 변경 이유와 관련 유스케이스를 함께 기록하세요.
- 용어는 API 스펙, 문서, 테스트 케이스에 동일하게 사용하세요.
- 동의어가 없으면 "없음"으로 표기하세요.
- 새로운 용어가 추가되거나 기존 용어가 변경될 경우, 관련된 모든 문서(유스케이스, API 스펙 등)를 동기화하세요.
