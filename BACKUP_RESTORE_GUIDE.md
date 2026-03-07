# FastExit Database Backup & Restore Guide

## 백업 파일 정보

생성 일시: 2026-03-07 16:03:40

### 백업 파일 목록

1. **SQL 덤프 백업** (논리적 백업)
   - 파일: `fastexit-backup-20260307_160340.sql`
   - 크기: 47KB
   - 용도: 데이터만 복원 (스키마 + 데이터)
   - 장점: 사람이 읽을 수 있음, 버전 간 호환성 높음

2. **볼륨 전체 백업** (물리적 백업)
   - 파일: `fastexit-data-20260307_160340.tar.gz`
   - 크기: 6.6MB
   - 용도: PostgreSQL 데이터 디렉터리 전체 복원
   - 장점: 빠른 복원, 완전한 상태 보존

## 복원 방법

### 방법 1: SQL 덤프 복원 (권장)

```bash
# 1. 컨테이너가 실행 중인지 확인
docker ps | grep fastexit

# 2. 기존 데이터베이스 초기화 (선택사항 - 완전히 새로 시작하려면)
docker exec -i fastexit psql -U postgres -d fastexit << EOF
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;
EOF

# 3. SQL 덤프 복원
docker exec -i fastexit psql -U postgres -d fastexit < fastexit-backup-20260307_160340.sql

# 4. 복원 확인
docker exec fastexit psql -U postgres -d fastexit -c "
SELECT 
  (SELECT COUNT(*) FROM institutions) as institutions,
  (SELECT COUNT(*) FROM products) as products,
  (SELECT COUNT(*) FROM accounts) as accounts,
  (SELECT COUNT(*) FROM account_groups) as account_groups,
  (SELECT COUNT(*) FROM holdings) as holdings,
  (SELECT COUNT(*) FROM snapshots) as snapshots;
"
```

### 방법 2: 볼륨 전체 복원 (완전 복구)

```bash
# 1. 컨테이너 중지
docker stop fastexit

# 2. 기존 볼륨 삭제 (주의: 현재 데이터 손실!)
docker volume rm fastexit-data

# 3. 새 볼륨 생성
docker volume create fastexit-data

# 4. 백업 파일 복원
docker run --rm \
  -v fastexit-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/fastexit-data-20260307_160340.tar.gz -C /data

# 5. 컨테이너 재시작
docker start fastexit

# 6. 로그 확인
docker logs fastexit --tail 50
```

## 정기 백업 스크립트

```bash
#!/bin/bash
# 파일명: scripts/backup-db.sh

BACKUP_DIR="/home/ubuntu/workspaces/fastexit-simple/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "Creating SQL backup..."
docker exec fastexit pg_dump -U postgres fastexit > "$BACKUP_DIR/fastexit-backup-${TIMESTAMP}.sql"

echo "Creating volume backup..."
docker run --rm \
  -v fastexit-data:/data \
  -v "$BACKUP_DIR":/backup \
  alpine tar czf /backup/fastexit-data-${TIMESTAMP}.tar.gz -C /data .

# 7일 이상 된 백업 삭제
find "$BACKUP_DIR" -name "fastexit-*.sql" -mtime +7 -delete
find "$BACKUP_DIR" -name "fastexit-data-*.tar.gz" -mtime +7 -delete

echo "Backup completed:"
ls -lh "$BACKUP_DIR" | tail -5
```

## 백업 전 체크리스트

- [ ] 현재 컨테이너가 정상 실행 중인지 확인
- [ ] 디스크 용량 충분한지 확인 (최소 100MB 여유 필요)
- [ ] 백업 파일 저장 경로 쓰기 권한 확인
- [ ] 중요 트랜잭션 수행 중이 아닌지 확인

## 복원 전 체크리스트

- [ ] 백업 파일 무결성 확인 (파일 크기 0이 아닌지)
- [ ] 현재 데이터 별도 백업 완료
- [ ] 복원 후 애플리케이션 재시작 계획 수립
- [ ] 데이터베이스 버전 호환성 확인

## 문제 해결

### SQL 복원 시 에러 발생

```bash
# 에러 로그 확인
docker exec fastexit psql -U postgres -d fastexit < backup.sql 2>&1 | tee restore.log

# 테이블별 수동 복원 (필요시)
docker exec -i fastexit psql -U postgres -d fastexit << EOF
-- 특정 테이블만 먼저 복원
\i /path/to/partial/backup.sql
EOF
```

### 볼륨 복원 후 권한 문제

```bash
# PostgreSQL 데이터 디렉터리 권한 수정
docker exec fastexit chown -R postgres:postgres /var/lib/postgresql/data
docker restart fastexit
```

## 백업 파일 관리

### 로컬 보관
- 위치: `/home/ubuntu/workspaces/fastexit-simple/`
- 보관 기간: 7일 (정기 백업 스크립트 기준)

### 외부 백업 권장사항
- 클라우드 스토리지 (AWS S3, Google Cloud Storage 등)
- 별도 서버로 rsync/scp 전송
- Git LFS를 통한 버전 관리 (작은 SQL 덤프 파일의 경우)

```bash
# 예: 외부 서버로 전송
scp fastexit-backup-20260307_160340.sql user@backup-server:/backups/fastexit/
```

## 백업 검증

```bash
# SQL 백업 파일 검사 (구문 오류 체크)
docker exec -i fastexit psql -U postgres -d template1 << EOF
CREATE DATABASE backup_test;
EOF

docker exec -i fastexit psql -U postgres -d backup_test < fastexit-backup-20260307_160340.sql

docker exec fastexit psql -U postgres -d template1 -c "DROP DATABASE backup_test;"
```

## 추가 정보

- PostgreSQL 버전: 17.9
- 백업 방식: pg_dump (plain SQL format)
- 압축: gzip (볼륨 백업)
- 문자 인코딩: SQL_ASCII/UTF-8

---

**⚠️ 중요 알림**

이전에 백업 없이 볼륨을 삭제한 사례가 있었습니다.  
재발 방지를 위해 다음 규칙을 준수하세요:

1. **배포 전 필수 백업**: 빌드/배포 스크립트 실행 전 반드시 백업
2. **볼륨 삭제 금지**: `docker volume rm`은 백업 확인 후에만 실행
3. **자동화된 백업**: cron 또는 systemd timer로 일일 자동 백업 설정

```bash
# Cron 예시 (매일 새벽 3시 백업)
0 3 * * * /home/ubuntu/workspaces/fastexit-simple/scripts/backup-db.sh
```
