# FastExit Frontend

React + TypeScript 기반 프론트엔드

## 개발 환경

### 필수 런타임
- Node.js: 24.x (LTS)

### 주요 프레임워크
- React: 18.x
- TypeScript: 5.x

## 로컬 개발

### 의존성 설치
```bash
npm install
```

### 환경 변수 설정
`.env` 파일을 생성하여 API URL을 설정합니다:
```bash
REACT_APP_API_URL=http://localhost:8000
```

### 실행
```bash
npm start
```

애플리케이션은 http://localhost:3000 에서 실행됩니다.

### 빌드
```bash
npm run build
```

## 기능

- 사용자 목록 조회
- 새 사용자 생성
- 사용자 삭제
- 실시간 데이터 새로고침
