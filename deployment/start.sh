#!/bin/bash
set -e

echo "==================================="
echo "FastExit Single Container Startup"
echo "==================================="

# 환경 변수 출력 (디버깅용)
echo "Environment Variables:"
echo "  POSTGRES_USER: $POSTGRES_USER"
echo "  POSTGRES_DB: $POSTGRES_DB"
echo "  DB_HOST: $DB_HOST"
echo "  DB_PORT: $DB_PORT"
echo "  BACKEND_URL: $BACKEND_URL"
echo "==================================="

# PostgreSQL 초기화
echo "Step 1: Initializing PostgreSQL..."
/app/deployment/init-db.sh

# 로그 디렉토리 생성 및 권한 설정
echo "Step 2: Setting up log directories..."
mkdir -p /var/log/supervisor
chown -R postgres:postgres /var/log/supervisor

# PostgreSQL 수동 시작 (supervisord 전에 DB가 준비되도록)
echo "Step 3: Starting PostgreSQL..."
su - postgres -c "/usr/lib/postgresql/17/bin/pg_ctl -D /var/lib/postgresql/data -l /var/log/supervisor/postgresql.log start"

# PostgreSQL이 준비될 때까지 대기
echo "Step 4: Waiting for PostgreSQL to be ready..."
for i in {1..30}; do
    if su - postgres -c "psql -lqt" &>/dev/null; then
        echo "PostgreSQL is ready!"
        break
    fi
    echo "Waiting for PostgreSQL... ($i/30)"
    sleep 1
done

# 데이터베이스 생성 (존재하지 않는 경우)
echo "Step 5: Creating database if not exists..."
su - postgres -c "psql -tc \"SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'\" | grep -q 1 || psql -c \"CREATE DATABASE $POSTGRES_DB\""
su - postgres -c "psql -tc \"SELECT 1 FROM pg_roles WHERE rolname = '$POSTGRES_USER'\" | grep -q 1 || psql -c \"CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD'\""
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER\""

echo "Step 6: Database setup complete!"

# PostgreSQL 중지 (supervisord가 관리하도록)
echo "Step 7: Stopping PostgreSQL to let supervisord manage it..."
su - postgres -c "/usr/lib/postgresql/17/bin/pg_ctl -D /var/lib/postgresql/data stop"

# Supervisord로 모든 서비스 시작
echo "Step 8: Starting all services with supervisord..."
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/fastexit.conf
