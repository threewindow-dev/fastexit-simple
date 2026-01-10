#!/bin/bash
set -e

# PostgreSQL 초기화 스크립트

echo "Initializing PostgreSQL database..."

# PostgreSQL 데이터 디렉토리가 비어있는지 확인
if [ ! -s "/var/lib/postgresql/data/PG_VERSION" ]; then
    echo "PostgreSQL data directory is empty. Initializing..."
    
    # postgres 사용자로 데이터베이스 초기화
    su - postgres -c "/usr/lib/postgresql/17/bin/initdb -D /var/lib/postgresql/data"
    
    # postgresql.conf 설정
    cat >> /var/lib/postgresql/data/postgresql.conf <<EOF

# Custom configuration
listen_addresses = 'localhost'
port = 5432
max_connections = 100
shared_buffers = 128MB
EOF

    # pg_hba.conf 설정 (로컬 연결 허용)
    cat > /var/lib/postgresql/data/pg_hba.conf <<EOF
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust
EOF

    echo "PostgreSQL initialization complete."
else
    echo "PostgreSQL data directory already exists. Skipping initialization."
fi
