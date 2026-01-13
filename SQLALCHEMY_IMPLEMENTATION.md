# FastExit SQLAlchemy Repository Implementation

## 개요

FastAPI 애플리케이션에 SQLAlchemy async ORM을 기반한 데이터 접근 계층을 구현했습니다.

### 주요 변경사항

#### 1. 폴더 구조 정규화
- `domains` → `subdomains`로 리네임 (표준 준수)
- 각 서브도메인의 4개 레이어 명확화:
  - `application/`: 서비스, DTO
  - `domain/`: 모델, 프로토콜
  - `infra/`: 저장소 구현, ORM 모델
  - `interface/`: 라우터, 스키마

#### 2. 데이터베이스 계층 (database.py)
- **SQLAlchemy async engine** 초기화
- **두 가지 트랜잭션 구현체**:
  - `SQLAlchemyTransaction`: async 세션 기반
  - `PsycopgTransaction`: psycopg 연결 기반 (레거시)
- **저장소 선택**: `REPOSITORY_TYPE` 환경변수로 전환
  - `sqlalchemy` (기본값): 새로운 구현
  - `psycopg`: 기존 레거시 구현

#### 3. 저장소 구현
- **SQLAlchemyUserRepository**: 새로운 async ORM 기반 구현
  - SQLAlchemy AsyncSession 사용
  - `sqlalchemy/select`, `func` 등 현대적 쿼리 API
  - 페이징, 중복 검사 등 모든 메서드 구현
- **PsycopgUserRepository**: 기존 구현 유지
  - 비교 테스트 가능
  - 단계적 마이그레이션 지원

#### 4. 응용 계층 (AppService)
- **트랜잭션 경계**: 메서드 단위 (per use-case)
- `transaction_factory` 콜러블로 DI
  - 트랜잭션 팩토리 함수를 AppService에 주입
  - 커맨드(쓰기)에서는 자동 commit/rollback
  - 쿼리(읽기)에서는 트랜잭션 불필요
- 모든 비즈니스 로직은 트랜잭션 경계 내에서 실행

#### 5. 인터페이스 계층 (Router)
- **저장소 선택 자동화**
  - `db_pool._repository_type` 확인 후 적절한 저장소/트랜잭션 주입
  - 환경변수로 전환 가능
- **DI 헬퍼**: `get_service()` 내부 함수로 서비스 인스턴스 생성
  - 각 요청마다 새로운 세션/연결 획득
  - 자동 cleanup 처리

## 설정 (환경변수)

```bash
# 데이터베이스 연결
DB_HOST=localhost          # 기본값: localhost
DB_PORT=5433              # 기본값: 5433
DB_NAME=fastexit-simple   # 기본값: fastexit-simple
DB_USER=postgres          # 기본값: postgres
DB_PASSWORD=              # 필수

# 저장소 타입
REPOSITORY_TYPE=sqlalchemy  # "sqlalchemy" | "psycopg"

# SQLAlchemy 설정
SQL_ECHO=false            # 기본값: false
DB_POOL_SIZE=5            # 기본값: 5
DB_MAX_OVERFLOW=10        # 기본값: 10
```

## 테스트 결과

### 단위 테스트 (28/28 ✅)
```bash
PYTHONPATH=backend/src pytest tests/unit/ -v

# 결과:
# - test_user_model.py: 14/14 PASSED
# - test_user_app_service.py: 14/14 PASSED
```

### 통합 테스트 (준비 예정)
```bash
# Testcontainers를 사용한 실제 PostgreSQL DB 테스트
# repository 선택: SQLAlchemy vs Psycopg 비교
PYTHONPATH=backend/src pytest tests/api/ -v
```

## 코드 예시

### 1. Repository 선택 자동 전환
```python
# database.py
if db_pool._repository_type == "sqlalchemy":
    session = await db_pool.get_session()
    repository = SQLAlchemyUserRepository(session)
else:
    conn = await db_pool.get_connection()
    repository = PsycopgUserRepository(conn)
```

### 2. 트랜잭션 경계 (AppService)
```python
# user_app_service.py
async def create_user(self, command: RegisterUserCommand) -> RegisterUserCommandResult:
    async def _execute():
        # 비즈니스 로직
        if await self.user_repository.exists_by_username(command.username):
            raise DuplicateUserError(...)
        user = User.create(...)
        return await self.user_repository.add(user)
    
    # 트랜잭션으로 감싼 실행
    return await self._run_with_transaction(_execute)

async def _run_with_transaction(self, func):
    if self.transaction_factory is None:
        return await func()  # 트랜잭션 없이
    
    tx = await self.transaction_factory()
    async with tx:  # 자동 commit/rollback
        return await func()
```

### 3. ORM 모델
```python
# infra/models/user_orm.py
class UserORM(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
```

### 4. SQLAlchemy Repository 쿼리
```python
# SQLAlchemy 현대적 쿼리 API 사용
stmt = select(UserORM).where(UserORM.username == username)
result = await self.session.execute(stmt)
user = result.scalars().first()

# 페이징
count_stmt = select(func.count(UserORM.id))
count_result = await self.session.execute(count_stmt)
total = count_result.scalar() or 0
```

## 마이그레이션 전략

### 현재 상태 (Hybrid)
- SQLAlchemy: 기본 (신규)
- Psycopg: 선택 가능 (레거시)

### 향후 계획
1. **통합 테스트**: SQLAlchemy vs Psycopg 성능 비교
2. **단계적 전환**: 다른 도메인으로 확대
3. **완전 마이그레이션**: Psycopg 제거

## 패키지 의존성

```
fastapi==0.127.1
sqlalchemy==2.0.41         # ← 신규
asyncpg==0.30.0           # ← 신규 (SQLAlchemy asyncpg 드라이버)
psycopg[binary]==3.2.3    # (기존 유지)
pydantic==2.12.5
python-dotenv==1.0.1
```

## 표준 준수

- ✅ [FASTAPI_DEVELOPMENT_STANDARDS.md](.dev-standards/python/FASTAPI_DEVELOPMENT_STANDARDS.md)
- ✅ [TRANSACTION_MANAGEMENT.md](.dev-standards/python/TRANSACTION_MANAGEMENT.md)
- ✅ DDD 4-layer architecture
- ✅ Dependency Inversion (Protocol-based)
- ✅ Async/await 전체 스택
