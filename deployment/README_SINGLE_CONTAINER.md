# FastExit - 단일 컨테이너 배포 가이드

## 개요

FastExit 애플리케이션의 모든 구성 요소(PostgreSQL, FastAPI Backend, Next.js Frontend)를 하나의 Docker 이미지로 통합하여 배포합니다.

## 아키텍처

### 단일 컨테이너 구조
```
┌─────────────────────────────────────┐
│   FastExit Single Container         │
├─────────────────────────────────────┤
│  Supervisord (프로세스 관리자)      │
│  ├─ PostgreSQL 17      (포트 5432)  │
│  ├─ FastAPI Backend    (포트 8000)  │
│  └─ Next.js Frontend   (포트 3000)  │
└─────────────────────────────────────┘
```

### 장점
- ✅ **간단한 배포**: 하나의 이미지만 관리
- ✅ **네트워크 오버헤드 감소**: 모든 서비스가 localhost 통신
- ✅ **일관성**: 전체 스택의 버전 관리가 용이
- ✅ **개발/프로덕션 환경 일치**: 동일한 이미지 사용

### 단점
- ⚠️ **스케일링 제한**: 개별 서비스를 독립적으로 확장 불가
- ⚠️ **리소스 격리 불가**: 한 서비스의 문제가 전체에 영향
- ⚠️ **이미지 크기**: 모든 의존성 포함으로 크기 증가

## 빌드 및 실행

### 1. 이미지 빌드

```bash
# 기본 빌드
./scripts/build-single-image.sh

# 커스텀 이미지 이름/태그
IMAGE_NAME=myapp IMAGE_TAG=v1.0.0 ./scripts/build-single-image.sh
```

### 2. 컨테이너 실행

```bash
# 기본 실행
POSTGRES_PASSWORD=your_secure_password ./scripts/run-single-container.sh

# 커스텀 설정
IMAGE_NAME=myapp \
IMAGE_TAG=v1.0.0 \
CONTAINER_NAME=myapp-prod \
POSTGRES_PASSWORD=secure_pass \
./scripts/run-single-container.sh
```

### 3. 수동 실행 (세부 제어)

```bash
docker run -d \
  --name fastexit \
  -p 3001:3000 \
  -p 8001:8000 \
  -p 5433:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=fastexit \
  -e DB_HOST=localhost \
  -e DB_PORT=5432 \
  -e BACKEND_URL=http://localhost:8000 \
  -v fastexit-data:/var/lib/postgresql/data \
  fastexit-monolith:latest
```

## 환경 변수

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `POSTGRES_USER` | PostgreSQL 사용자명 | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL 비밀번호 | `changeme` |
| `POSTGRES_DB` | 데이터베이스 이름 | `fastexit` |
| `DB_HOST` | 데이터베이스 호스트 | `localhost` |
| `DB_PORT` | 데이터베이스 포트 | `5432` |
| `BACKEND_URL` | 백엔드 API URL | `http://localhost:8000` |

## 포트 매핑

| 서비스 | 컨테이너 포트 | 호스트 포트 |
|--------|---------------|-------------|
| Frontend (Next.js) | 3000 | 3001 |
| Backend (FastAPI) | 8000 | 8001 |
| Database (PostgreSQL) | 5432 | 5433 |

## 데이터 영속성

PostgreSQL 데이터는 Docker 볼륨에 저장됩니다:

```bash
# 볼륨 확인
docker volume ls | grep fastexit-data

# 볼륨 백업
docker run --rm -v fastexit-data:/data -v $(pwd):/backup ubuntu tar czf /backup/fastexit-backup.tar.gz -C /data .

# 볼륨 복원
docker run --rm -v fastexit-data:/data -v $(pwd):/backup ubuntu tar xzf /backup/fastexit-backup.tar.gz -C /data
```

## 로그 확인

```bash
# 전체 로그
docker logs -f fastexit

# 특정 서비스 로그 (컨테이너 내부)
docker exec fastexit tail -f /var/log/supervisor/postgresql.out.log
docker exec fastexit tail -f /var/log/supervisor/backend.out.log
docker exec fastexit tail -f /var/log/supervisor/frontend.out.log
```

## 헬스 체크

```bash
# Frontend
curl http://localhost:3001

# Backend
curl http://localhost:8001/docs

# Database
docker exec fastexit psql -U postgres -d fastexit -c "SELECT version();"
```

## 트러블슈팅

### PostgreSQL이 시작되지 않음

```bash
# 로그 확인
docker exec fastexit cat /var/log/supervisor/postgresql.err.log

# 데이터 디렉토리 권한 확인
docker exec fastexit ls -la /var/lib/postgresql/data
```

### Backend가 DB에 연결 실패

```bash
# 환경 변수 확인
docker exec fastexit env | grep DB_

# PostgreSQL 연결 테스트
docker exec fastexit psql -U postgres -h localhost -d fastexit -c "SELECT 1;"
```

### Frontend가 Backend에 연결 실패

```bash
# Backend API 테스트
docker exec fastexit curl http://localhost:8000/docs

# 환경 변수 확인
docker exec fastexit env | grep BACKEND_URL
```

## 프로덕션 배포

### Docker Hub 푸시

```bash
# 태그 지정
docker tag fastexit-monolith:latest yourusername/fastexit:latest
docker tag fastexit-monolith:latest yourusername/fastexit:v1.0.0

# 푸시
docker push yourusername/fastexit:latest
docker push yourusername/fastexit:v1.0.0
```

### AWS ECR 푸시

```bash
# ECR 로그인
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# 태그 및 푸시
docker tag fastexit-monolith:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/fastexit:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/fastexit:latest
```

### 프로덕션 실행 권장 사항

```bash
docker run -d \
  --name fastexit-prod \
  --restart unless-stopped \
  -p 3010:3000 \
  -p 8010:8000 \
  -p 5442:5432 \
  -e POSTGRES_PASSWORD=${SECURE_PASSWORD} \
  -e NODE_ENV=production \
  -v fastexit-data:/var/lib/postgresql/data \
  --memory="2g" \
  --cpus="2" \
  fastexit-monolith:latest
```

## 마이그레이션 (docker-compose에서 단일 컨테이너로)

### 1. 데이터 백업

```bash
# 기존 docker-compose 데이터 백업
docker exec fastexit-postgres pg_dump -U postgres fastexit > backup.sql
```

### 2. 기존 컨테이너 중지

```bash
docker-compose down
```

### 3. 새 이미지로 실행

```bash
./scripts/build-single-image.sh
POSTGRES_PASSWORD=your_password ./scripts/run-single-container.sh
```

### 4. 데이터 복원

```bash
docker cp backup.sql fastexit:/tmp/
docker exec fastexit psql -U postgres -d fastexit -f /tmp/backup.sql
```

## 유지보수

### 컨테이너 업데이트

```bash
# 새 이미지 빌드
./scripts/build-single-image.sh

# 기존 컨테이너 중지 및 제거
docker stop fastexit
docker rm fastexit

# 새 컨테이너 실행 (데이터는 유지됨)
./scripts/run-single-container.sh
```

### 데이터 정리

```bash
# 컨테이너 완전 제거 (데이터 유지)
docker rm -f fastexit

# 볼륨까지 제거 (주의: 데이터 손실)
docker rm -f fastexit
docker volume rm fastexit-data
```

## 파일 구조

```
fastexit-simple/
├── Dockerfile                          # 단일 컨테이너 이미지 정의
├── deployment/
│   ├── supervisord.conf                # 프로세스 관리 설정
│   ├── init-db.sh                      # PostgreSQL 초기화
│   └── start.sh                        # 컨테이너 시작 스크립트
└── scripts/
    ├── build-single-image.sh           # 이미지 빌드 스크립트
    └── run-single-container.sh         # 컨테이너 실행 스크립트
```

## 참고

- 단일 컨테이너는 소규모 애플리케이션이나 개발/스테이징 환경에 적합합니다.
- 대규모 프로덕션 환경에서는 Kubernetes나 docker-compose를 사용한 마이크로서비스 구조를 권장합니다.
- 스케일링이 필요한 경우 기존 [docker-compose.yml](../docker-compose.yml) 구조로 전환하세요.
