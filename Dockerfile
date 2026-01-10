# 단일 컨테이너에 PostgreSQL, FastAPI Backend, Next.js Frontend 통합
# Python 3.13을 베이스로 사용
FROM python:3.13-bookworm AS base

# Node.js 24.x 설치
RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get update && apt-get install -y nodejs

# PostgreSQL 공식 리포지토리 추가
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    lsb-release \
    && wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/postgresql-keyring.gpg] http://apt.postgresql.org/pub/repos/apt bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# 시스템 패키지 설치 (PostgreSQL, supervisord 등)
RUN apt-get update && apt-get install -y \
    postgresql-17 \
    postgresql-contrib-17 \
    supervisor \
    nginx \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# ============================================
# Stage 1: Frontend Build
# ============================================
FROM base AS frontend-builder

WORKDIR /app/frontend

# Frontend 의존성 설치 및 빌드
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# ============================================
# Stage 2: Final Image
# ============================================
FROM base AS runner

# 환경 변수 설정
ENV NODE_ENV=production
ENV PYTHONUNBUFFERED=1
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=changeme
ENV POSTGRES_DB=fastexit
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV BACKEND_URL=http://localhost:8000

# PostgreSQL 데이터 디렉토리 설정
RUN mkdir -p /var/lib/postgresql/data && \
    chown -R postgres:postgres /var/lib/postgresql

# Python 가상환경 생성 및 백엔드 의존성 설치
WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# 백엔드 코드 복사
COPY backend/ ./

# Frontend standalone 빌드 복사
WORKDIR /app/frontend
COPY --from=frontend-builder /app/frontend/public ./public
COPY --from=frontend-builder /app/frontend/.next/standalone ./
COPY --from=frontend-builder /app/frontend/.next/static ./.next/static

# Supervisord 설정 복사
WORKDIR /app
COPY deployment/supervisord.conf /etc/supervisor/conf.d/fastexit.conf

# PostgreSQL 초기화 스크립트 복사
COPY deployment/init-db.sh /app/deployment/init-db.sh
RUN chmod +x /app/deployment/init-db.sh

# 시작 스크립트 생성
COPY deployment/start.sh /app/start.sh
RUN chmod +x /app/start.sh

# 포트 노출
EXPOSE 3000 8000 5432

# 볼륨 설정 (DB 데이터 영속성)
VOLUME ["/var/lib/postgresql/data"]

# 애플리케이션 시작
CMD ["/app/start.sh"]
