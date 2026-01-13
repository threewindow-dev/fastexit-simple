# Backend 표준화 로드맵

**분석 대상**: `/backend/src/main.py` 기반 간단한 CRUD 구조  
**표준 기준**: `.dev-standards/python/` 문서들 (네이밍, 에러처리, 트랜잭션, 테스트)

---

## 1. 현재 상태 분석

### 1.1 강점
✅ FastAPI 기반 REST API 구현  
✅ 기본 CRUD 엔드포인트 (GET/POST/DELETE)  
✅ Pydantic 스키마 사용  
✅ 환경 변수 기반 DB 설정  
✅ 기본 에러 처리 구조  

### 1.2 표준과의 차이점

| 항목 | 현재 | 표준 | 영향도 |
|------|------|------|--------|
| 폴더 구조 | 단일 main.py | Domain/App/Infra/Interface 계층 분리 | 🔴 높음 |
| 에러 처리 | HTTPException + 문자열 | DomainError/ApplicationError/InfraError | 🔴 높음 |
| DB 연결 | 수동 연결 관리 | TransactionProtocol 패턴 | 🔴 높음 |
| 파일 네이밍 | schemas/services 폴더만 | 계층별 네이밍 규칙 적용 | 🟡 중간 |
| 비즈니스 로직 | Router에 직접 | AppService 분리 | 🟡 중간 |
| 테스트 | 미작성 | Unit + API(Testcontainers) | 🔴 높음 |
| 응답 포맷 | 기본 JSON | {code/message/data} 통일 | 🟡 중간 |

### 1.3 코드 구조 현황
```
backend/src/
├── main.py              # 모든 로직 포함 (라우터+서비스+스키마+DB)
├── schemas/             # 비어있음
├── services/            # 비어있음
├── repositories/        # 비어있음
└── routers/             # 비어있음
```

---

## 2. 표준화 필요 영역 (우선순위)

### Phase 1: 기반 인프라 (1주)
**목표**: 공유 모듈/에러/트랜잭션 패턴 정립

| 작업 | 파일 | 설명 |
|------|------|------|
| 에러 기초 | `shared/errors.py` | DomainError, ApplicationError, InfraError, ValidationError 정의 |
| 에러 핸들러 | `core/exception_handlers.py` | FastAPI 전역 핸들러 + 응답 변환 |
| 트랜잭션 | `shared/protocols/transaction.py` | TransactionProtocol 정의 |
| DB 연결 | `infra/database.py` | async PostgreSQL 세션 관리 (SqlAlchemy or psycopg) |
| 로깅 | `core/logging.py` | 구조화된 로깅 설정 (trace_id, exception_type 등) |

**산출물**: 
- shared/errors.py (100줄)
- core/exception_handlers.py (150줄)
- shared/protocols/transaction.py (50줄)
- infra/database.py (100줄)

---

### Phase 2: User 도메인 표준화 (2주)
**목표**: 하나의 도메인(User)을 완전히 표준화해 패턴 수립

| 계층 | 파일 | 설명 |
|------|------|------|
| **Domain** | `domains/user/domain/models/user.py` | User 도메인 모델 (비즈니스 규칙) |
| | `domains/user/domain/protocols/user_repository_protocol.py` | UserRepository 인터페이스 |
| **Application** | `domains/user/application/dtos/user_dto.py` | CreateUserCommand, GetUserResult 등 |
| | `domains/user/application/services/user_app_service.py` | create/get/update/delete 유스케이스 |
| **Interface** | `domains/user/interface/routers/user_router.py` | GET/POST/DELETE 엔드포인트 |
| | `domains/user/interface/schemas/user_schema.py` | PostUserRequest, GetUserResponse |
| **Infra** | `domains/user/infra/repositories/user_repository.py` | UserRepositoryProtocol 구현 |
| | `domains/user/infra/orm/user_entity.py` | SQLAlchemy ORM 모델 (선택) |

**산출물**: ~1000줄 (User 도메인 완전 표준화)

**데이터 흐름 예시**
```
PostUserRequest (Schema)
  ↓ (Router에서 validation)
CreateUserCommand (DTO)
  ↓ (AppService에서 변환)
User (Domain Model, 비즈니스 규칙 적용)
  ↓ (Repository에서 변환)
UserEntity (ORM, DB 저장)
  ↓ (조회 시 역방향)
GetUserResult (DTO)
  ↓ (Router에서 포장)
GetUserResponse (Schema)
  → {code: "OK", message: "...", data: {...}}
```

---

### Phase 3: 테스트 작성 (1.5주)
**목표**: User 도메인 기반 단위/API 테스트 작성

| 테스트 종류 | 위치 | 예시 |
|------------|------|------|
| 단위 테스트 | `tests/unit/domains/user/...` | `test_user_model.py`, `test_user_app_service.py` |
| API 테스트 | `tests/api/domains/user/...` | `test_user_router.py` (Testcontainers) |
| 리포지토리 | `tests/api/infra/user_repository_integration.py` | Repository + DB 통합 |

**산출물**: ~500줄 (테스트 커버리지 70%+)

---

### Phase 4: 추가 도메인 적용 (향후)
**목표**: 다른 도메인도 동일 패턴 적용

| 예상 도메인 | 우선순위 |
|-----------|---------|
| Product | 1순위 |
| Order | 2순위 |
| Payment | 3순위 |

---

## 3. 표준화 체크리스트 (Phase 1+2 완료 후)

### 에러 처리
- [ ] 모든 예외가 DomainError/ApplicationError/InfraError 중 하나
- [ ] HTTPException 사용 없음 (전역 핸들러에서 변환)
- [ ] 응답이 {code/message/data} 포맷
- [ ] InfraError는 사용자 메시지 마스킹 (Internal server error)
- [ ] 원본 예외는 origin_exc에 캡슐화

### 계층 분리
- [ ] Domain은 비즈니스 로직만, DB/HTTP 지식 없음
- [ ] Application은 Domain 프로토콜만 의존, HTTPException 금지
- [ ] Infra는 Protocol 구현, 로깅 금지
- [ ] Interface는 예외를 표준 응답으로 변환, 유일한 로깅 지점

### 트랜잭션
- [ ] `async with transaction:` 패턴 사용
- [ ] 예외 발생 시 자동 롤백
- [ ] Repository 여러 개도 동일 세션에서 작동

### 네이밍
- [ ] 파일명: snake_case + 접미사 (_schema.py, _dto.py, _service.py, _repository.py)
- [ ] 클래스명: PascalCase
- [ ] 에러 코드: DOMAIN_ACTION_REASON (예: USER_CREATE_DUPLICATED)

### 테스트
- [ ] 단위 테스트: Mock 기반, DB 미사용
- [ ] API 테스트: Testcontainers PostgreSQL, 실제 HTTP 호출
- [ ] 커버리지: 70%+ (주요 경로)

---

## 4. 마이그레이션 전략

### Step 1: Phase 1 적용 (현재 main.py 유지)
- 에러/트랜잭션 기반 구현
- 기존 코드는 점진적으로 변환

### Step 2: User 도메인 분리 (Phase 2)
- 새 구조로 User 도메인 구현
- 기존 `/api/users` 엔드포인트 점진적 이전

### Step 3: 통합 (Phase 3)
- User 테스트 완성
- 기존 main.py 제거

### Step 4: 다른 도메인 (Phase 4)
- 동일 패턴 반복

---

## 5. 예상 산출물 및 시간

| Phase | 산출물 | 예상 시간 | 복잡도 |
|-------|--------|---------|--------|
| 1 | shared + core 모듈 | 3-4시간 | 낮음 |
| 2 | User 도메인 | 6-8시간 | 중간 |
| 3 | 테스트 | 4-6시간 | 중간 |
| 4 | Product 도메인 | 4-5시간 | 중간 |
| **총** | **4개 도메인 표준화** | **17-23시간** | **중간** |

---

## 6. 리스크 및 고려사항

### 리스크
- 🔴 **큰 변경**: 기존 API 호출 패턴 변경 필요 (클라이언트 반영)
- 🟡 **성능**: ORM(SQLAlchemy) 도입 시 성능 검증 필요
- 🟡 **복잡도**: 초반에 네이밍/구조 학습곡선 있음

### 완화 전략
- Phase 1/2를 먼저 작은 도메인에서 검증
- 성능 테스트 (벤치마크)
- 팀 문서 및 리뷰 정례화

---

## 7. 다음 단계

**즉시 진행**: Phase 1 기반 구현 (shared/errors.py, core/exception_handlers.py 등)  
**확인 후 진행**: User 도메인 완전 표준화 (Phase 2)

**질문**: Phase 1부터 시작할까요? 구체적 세부사항은?
