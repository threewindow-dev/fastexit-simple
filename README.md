# FastExit - User Management System

Next.js (BFF) + FastAPI + PostgreSQL로 구성된 현대적인 웹 애플리케이션입니다.

## 기술 스택

### Frontend (BFF Pattern)
- **Next.js 15.x** - React 프레임워크 (App Router)
- **React 19.x** - UI 라이브러리
- **TypeScript 5.x** - 타입 안전성
- **API Routes** - BFF (Backend For Frontend) 구현

### Backend
- **FastAPI 0.127.x** - Python 웹 프레임워크
- **Python 3.13** - 프로그래밍 언어
- **psycopg3** - PostgreSQL 드라이버

### Database
- **PostgreSQL 17** - 관계형 데이터베이스

### Deployment
- **Docker Compose** - 컨테이너 오케스트레이션
- **Node.js 24.x LTS** - 프론트엔드 런타임
- **No Nginx** - Next.js 자체 서버 사용

## 아키텍처

### 로컬 개발 환경
```
Browser → Next.js Server (포트 3000)
            ├─ React UI (SSR/CSR)
            └─ API Routes (/api/*)
                 ↓
          FastAPI Backend (포트 8000)
                 ↓
          PostgreSQL (포트 5432)
```

**로컬 개발에서 Gateway 불필요:**
- Next.js 자체 개발 서버 사용
- API Routes로 BFF 패턴 구현
- 단순한 구조로 빠른 개발 사이클
- http://localhost:3000 직접 접근

### 프로덕션 환경
```
Browser → Gateway (Nginx/Kong/AWS ALB 등)
            ├─ SSL/TLS Termination
            ├─ Load Balancing
            ├─ Rate Limiting
            └─ Caching
                 ↓
          Next.js Server (포트 3000)
            └─ API Routes (/api/*)
                 ↓
          FastAPI Backend (포트 8000)
                 ↓
          PostgreSQL (포트 5432)
```

**프로덕션에서 Gateway 필수:**
- SSL/TLS 인증서 관리
- 여러 인스턴스 로드 밸런싱
- DDoS 방어 및 Rate Limiting
- 정적 자산 캐싱 및 압축

**Gateway 옵션:** Nginx, Kong, Traefik, AWS ALB, Cloudflare 등

자세한 분석: [docs/architecture/BFF_AND_NGINX_ANALYSIS.md](docs/architecture/BFF_AND_NGINX_ANALYSIS.md)

## 프로젝트 구조

```
fastexit-simple/
├── backend/                    # FastAPI 백엔드
│   ├── src/
│   │   └── main.py            # FastAPI 애플리케이션
│   ├── tests/
│   └── requirements.txt
├── frontend/                   # Next.js 프론트엔드 (BFF)
│   ├── src/
│   │   ├── app/
│   │   │   ├── api/           # API Routes (BFF)
│   │   │   │   └── users/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx       # 메인 페이지
│   │   └── ...
│   ├── public/
│   ├── next.config.ts
│   └── package.json
├── deployment/                 # 배포 설정
│   └── docker/
│       ├── backend.Dockerfile
│       └── frontend.Dockerfile
├── docs/                       # 설계 문서
│   ├── architecture/
│   │   └── BFF_AND_NGINX_ANALYSIS.md
│   └── design/
├── docker-compose.yml          # Docker Compose 설정
├── .tool-versions             # 런타임 버전 정의
├── .env.example               # 환경 변수 템플릿
└── README.md
```

## 빠른 시작

### Docker Compose로 실행 (권장)

1. **환경 변수 설정:**
```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env

# .env 파일을 편집하여 안전한 패스워드 설정
nano .env
```

`.env` 파일 내용:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password_here  # 반드시 변경!
POSTGRES_DB=fastexit
```

2. **서비스 시작:**
```bash
docker-compose up -d
```

3. **서비스 접속:**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API 문서**: http://localhost:8001/docs
- **PostgreSQL**: localhost:5433

4. **서비스 중지:**
```bash
docker-compose down
```

### 로컬 개발

#### Backend 개발

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export DB_PASSWORD=your_secure_password
export DB_HOST=localhost
export DB_PORT=5433

# 서버 실행
uvicorn src.main:app --reload --port 8000
```

#### Frontend 개발

```bash
cd frontend

# 의존성 설치
npm install

# 환경 변수 설정 (선택)
export BACKEND_URL=http://localhost:8000

# 개발 서버 실행
npm run dev
```

Frontend는 http://localhost:3000 에서 실행됩니다.

## 기능

### 현재 구현된 기능
- ✅ Next.js BFF 패턴 구현
- ✅ 사용자 관리 시스템
  - 사용자 목록 조회 (GET /api/users)
  - 새 사용자 생성 (POST /api/users)
  - 사용자 삭제 (DELETE /api/users/:id)
- ✅ PostgreSQL 데이터베이스 연동
- ✅ Docker Compose 배포 설정
- ✅ TypeScript 5.x + React 19
- ✅ 환경 변수 기반 보안 설정

### 향후 구현 예정
- 📋 개인 자산 관리
- 📋 시계열 차트 시각화
- 📋 일/주/년 단위 자산 조회

## API 구조

### Frontend API Routes (BFF)
프론트엔드 → Next.js API Routes → FastAPI

| Method | Frontend Route | Backend Route | Description |
|--------|---------------|---------------|-------------|
| GET | `/api/users` | `/api/users` | 모든 사용자 조회 |
| POST | `/api/users` | `/api/users` | 새 사용자 생성 |
| DELETE | `/api/users/:id` | `/api/users/:id` | 사용자 삭제 |

### Backend API Endpoints (FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | 헬스 체크 |
| GET | `/api/users` | 모든 사용자 조회 |
| GET | `/api/users/{user_id}` | 특정 사용자 조회 |
| POST | `/api/users` | 새 사용자 생성 |
| DELETE | `/api/users/{user_id}` | 사용자 삭제 |

자세한 API 문서: http://localhost:8001/docs

## 데이터베이스 스키마

### users 테이블
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 환경 변수

### Backend (.env 또는 docker-compose.yml)
- `DB_HOST`: PostgreSQL 호스트 (기본: postgres)
- `DB_PORT`: PostgreSQL 포트 (기본: 5432)
- `DB_NAME`: 데이터베이스 이름 (기본: fastexit)
- `DB_USER`: 데이터베이스 사용자 (기본: postgres)
- `DB_PASSWORD`: 데이터베이스 비밀번호 (필수)

### Frontend
- `BACKEND_URL`: FastAPI 백엔드 URL (기본: http://backend:8000)
- `NODE_ENV`: Node 환경 (production/development)

## 개발 표준

프로젝트는 다음 개발 표준을 따릅니다:
- [Runtime Version Standards](.dev-standards/RUNTIME_VERSION_STANDARDS.md)
- [Project Structure Standards](.dev-standards/PROJECT_STRUCTURE_STANDARDS.md)

## 트러블슈팅

### 포트 충돌
기본 포트가 이미 사용 중인 경우 `docker-compose.yml`에서 포트를 변경하세요:
```yaml
frontend:
  ports:
    - "3001:3000"  # 3000 대신 3001 사용
```

### 데이터베이스 연결 실패
1. PostgreSQL 컨테이너가 정상 실행 중인지 확인:
   ```bash
   docker ps | grep postgres
   ```

2. 환경 변수가 올바르게 설정되었는지 확인:
   ```bash
   docker logs fastexit-backend
   ```

### Next.js 빌드 오류
캐시를 삭제하고 재빌드:
```bash
cd frontend
rm -rf .next node_modules
npm install
npm run build
```

## 라이선스

이 프로젝트는 내부 개발 목적으로 사용됩니다.
