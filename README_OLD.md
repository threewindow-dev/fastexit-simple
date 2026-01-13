# FastExit Simple

특정 일, 주, 년 단위로 개인 자산 상태를 확인하고, 시계열 차트로 자산의 변동을 확인할 수 있는 기능을 제공하는 FastExit 서비스의 단일 레포지토리입니다.

## 프로젝트 구조

```
fastexit-simple/
├── backend/                 # FastAPI 백엔드
│   ├── src/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/                # React 프론트엔드
│   ├── src/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── public/
│   └── package.json
├── deployment/              # 배포 설정
│   └── docker/
│       ├── backend.Dockerfile
│       ├── frontend.Dockerfile
│       └── nginx.conf
├── docs/                    # 설계 문서
│   └── design/
├── docker-compose.yml       # Docker Compose 설정
├── .tool-versions          # 런타임 버전 정의
└── README.md
```

## 개발 환경

### 필수 런타임
- Node.js: 24.x (LTS)
- Python: 3.13
- PostgreSQL: 17

### 주요 프레임워크
- FastAPI: 0.127.x (Backend)
- React: 19.x (Frontend)
- Next.js: 15.x (선택사항)

## 빠른 시작

### Docker Compose로 실행 (권장)

1. 데이터 디렉토리 생성:
```bash
mkdir -p ~/data/fast-exit
```

2. 환경 변수 설정:
```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env

# .env 파일을 편집하여 안전한 패스워드 설정
nano .env  # 또는 vim, vi 등 사용
```

3. 서비스 시작:
```bash
docker-compose up -d
```

4. 서비스 접속:
- Frontend: http://localhost
- Backend API: http://localhost:8001
- API 문서: http://localhost:8001/docs

5. 서비스 중지:
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

# PostgreSQL 실행 (Docker)
docker run -d \
  --name fastexit-postgres \
  -e POSTGRES_PASSWORD=your_secure_password \
  -e POSTGRES_DB=fastexit \
  -p 5433:5432 \
  -v ~/data/fast-exit:/var/lib/postgresql/data \
  postgres:17-alpine

# 서버 실행
python src/main.py
```

Backend는 http://localhost:8001 에서 실행됩니다.

#### Frontend 개발

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm start
```

Frontend는 http://localhost:3000 에서 실행됩니다.

## 기능

### 현재 구현된 기능
- ✅ 사용자 관리 시스템
  - 사용자 목록 조회
  - 새 사용자 생성
  - 사용자 삭제
- ✅ PostgreSQL 데이터베이스 연동
- ✅ Docker Compose 배포 설정

### 향후 구현 예정
- 📋 개인 자산 관리
- 📋 시계열 차트 시각화
- 📋 일/주/년 단위 자산 조회

## API 엔드포인트

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | 헬스 체크 |
| GET | `/api/users` | 모든 사용자 조회 |
| GET | `/api/users/{user_id}` | 특정 사용자 조회 |
| POST | `/api/users` | 새 사용자 생성 |
| DELETE | `/api/users/{user_id}` | 사용자 삭제 |

자세한 API 문서는 http://localhost:8001/docs 에서 확인할 수 있습니다.

## 데이터베이스 스키마

### users 테이블
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 개발 표준

이 프로젝트는 [dev-standards](https://github.com/threewindow-dev/dev-standards)를 따릅니다:
- [프로젝트 구조 표준](.dev-standards/PROJECT_STRUCTURE_STANDARDS.md)
- [런타임 버전 선택 표준](.dev-standards/RUNTIME_VERSION_STANDARDS.md)
- [VS Code 개발 표준](.dev-standards/VSCODE_DEVELOPMENT_GUIDELINES.md)

## 문제 해결

### 환경 변수 설정 누락
```bash
# .env 파일이 없는 경우
cp .env.example .env

# POSTGRES_PASSWORD가 설정되지 않은 경우 에러 발생
Error: POSTGRES_PASSWORD must be set
```

### 포트가 이미 사용 중인 경우
```bash
# 포트 확인
lsof -i :80
lsof -i :8000
lsof -i :5432

# 프로세스 종료
kill -9 <PID>
```

### Docker 컨테이너 재시작
```bash
docker-compose restart
```

### 데이터베이스 초기화
```bash
docker-compose down -v
rm -rf ~/data/fast-exit/*
docker-compose up -d
```

## 라이선스

MIT 
