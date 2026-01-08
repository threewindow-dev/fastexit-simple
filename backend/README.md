# FastExit Backend

FastAPI 기반 백엔드 서비스

## 개발 환경

### 필수 런타임
- Python: 3.13

### 주요 프레임워크
- FastAPI: 0.115.x

## 로컬 개발

### 의존성 설치
```bash
pip install -r requirements.txt
```

### 환경 변수 설정
```bash
cp .env.example .env
# .env 파일 수정
```

### 실행
```bash
python src/main.py
```

API는 http://localhost:8000 에서 실행됩니다.

### API 문서
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 엔드포인트

- `GET /` - 헬스 체크
- `GET /api/users` - 모든 사용자 조회
- `GET /api/users/{user_id}` - 특정 사용자 조회
- `POST /api/users` - 새 사용자 생성
- `DELETE /api/users/{user_id}` - 사용자 삭제
