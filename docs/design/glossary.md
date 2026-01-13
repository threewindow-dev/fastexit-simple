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

## 자산 현황 (Asset Status)

**정의**: 사용자의 금융 자산에 대한 현재 정보. 금융회사이름, 계좌이름, 자산의 속성, 상품명, 평가금액으로 구성됨

**동의어**: 자산 정보

**사용 예시**: 삼성증권 ISA 계좌의 TIGER 미국S&P500 ETF 1,500,000원

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetStatus`

**소유자**: Product Owner

---

## 금융회사이름 (Financial Institution Name)

**정의**: 자산이 보관된 금융회사의 명칭

**동의어**: 금융기관명

**사용 예시**: 삼성증권, KB증권, 신한은행

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetStatus/properties/institutionName`

**소유자**: Product Owner

---

## 계좌이름 (Account Name)

**정의**: 금융회사 내 자산이 속한 계좌의 명칭

**동의어**: 없음

**사용 예시**: ISA 계좌, CMA 계좌, 연금저축

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AssetStatus/properties/accountName`

**소유자**: Product Owner

---

## 자산의 속성 (Asset Attributes)

**정의**: 자산을 분류하기 위한 다차원 속성. 투자 지역, 자산 종류, 화폐, 투자유형, 자산특징, 위험도로 구성됨

**동의어**: 자산 분류, 자산 메타데이터

**사용 예시**: 한국/주식/원화/ETF/지수추종/위험

**관련 유스케이스**: -

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

**정의**: 자산의 특정 기준일의 현황

**동의어**: 자산 스냅샷, 기준일 현황

**사용 예시**: 2025년 1월 4일의 자산 현황

**관련 유스케이스**: -

**API 매핑**: `components/schemas/Snapshot`

**소유자**: Product Owner

---

## 주간 스냅샷 (Weekly Snapshot)

**정의**: 매주 토요일을 기준일로 하는 자산 현황 스냅샷

**동의어**: 주별 스냅샷

**사용 예시**: 2025년 1월 4일(토) 기준 자산 현황

**관련 유스케이스**: -

**API 매핑**: `components/schemas/WeeklySnapshot`

**소유자**: Product Owner

---

## 연간 스냅샷 (Annual Snapshot)

**정의**: 다음 연도 1월 1일을 기준일로 하는 자산 현황 스냅샷

**동의어**: 연별 스냅샷, 연초 스냅샷

**사용 예시**: 2025년 1월 1일 기준 자산 현황

**관련 유스케이스**: -

**API 매핑**: `components/schemas/AnnualSnapshot`

**소유자**: Product Owner

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
