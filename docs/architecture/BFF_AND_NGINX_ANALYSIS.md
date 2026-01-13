# Next.js BFF 아키텍처와 Gateway 전략

## 구현된 아키텍처

### 개발 환경 (로컬)
```
Browser → Next.js Server (포트 3000)
            ├─ React 19 UI (SSR/CSR)
            └─ API Routes (BFF)
                 ↓
          FastAPI Backend (포트 8000)
                 ↓
          PostgreSQL (포트 5432)
```

### 프로덕션 환경
```
Browser → Gateway (Nginx/Kong/AWS ALB 등)
            ├─ SSL/TLS Termination
            ├─ Load Balancing
            ├─ Rate Limiting
            └─ Caching
                 ↓
          Next.js Server (포트 3000)
            ├─ React 19 UI
            └─ API Routes (BFF)
                 ↓
          FastAPI Backend (포트 8000)
                 ↓
          PostgreSQL (포트 5432)
```

### 주요 구성요소

1. **Next.js 15 (프론트엔드 + BFF)**
   - React 19 UI 컴포넌트 (클라이언트/서버)
   - API Routes (`/api/users`, `/api/users/[id]`)
   - 자체 Node.js 서버 (standalone 모드)
   - BFF 패턴으로 백엔드 추상화

2. **FastAPI (백엔드)**
   - 데이터베이스 로직
   - 비즈니스 로직
   - PostgreSQL 연결
   - RESTful API

3. **PostgreSQL 17**
   - 데이터 저장소

4. **Gateway (프로덕션 전용)**
   - Nginx, Kong, Traefik, AWS ALB 등
   - 로컬 개발 환경에서는 불필요

## 환경별 전략

### 로컬 개발 환경

#### 특징
- ✅ **Gateway 없음** - 불필요
- ✅ **단순한 구조** - 빠른 개발 사이클
- ✅ **직접 접근** - http://localhost:3000
- ✅ **개발 도구** - Hot Reload, Source Maps

#### 이유
- Next.js 자체 개발 서버가 충분히 강력함
- SSL/TLS 불필요 (localhost)
- 로드 밸런싱 불필요 (단일 인스턴스)
- 설정 복잡도 최소화

### 프로덕션 환경

#### Gateway 필수 구성 요소

1. **SSL/TLS Termination**
   - HTTPS 인증서 관리
   - TLS 1.3 지원
   - 자동 인증서 갱신 (Let's Encrypt)

2. **Load Balancing**
   - 여러 Next.js 인스턴스 분산
   - Health Check
   - Session Affinity (필요 시)

3. **보안 기능**
   - Rate Limiting (DDoS 방어)
   - IP Whitelisting/Blacklisting
   - WAF (Web Application Firewall)
   - Security Headers (HSTS, CSP 등)

4. **성능 최적화**
   - Static Asset Caching
   - Gzip/Brotli Compression
   - HTTP/2, HTTP/3 지원
   - CDN 연동

#### Gateway 옵션 비교

| Gateway | 장점 | 단점 | 적합한 환경 |
|---------|------|------|------------|
| **Nginx** | 가볍고 빠름, 설정 단순 | 동적 설정 어려움 | 소규모~중규모 |
| **Kong** | API Gateway 특화, 플러그인 풍부 | 리소스 많이 사용 | 마이크로서비스 |
| **Traefik** | 자동 설정, Docker 친화적 | 학습 곡선 | 컨테이너 환경 |
| **AWS ALB** | 관리형, AWS 통합 | 비용, 벤더 종속 | AWS 환경 |
| **Cloudflare** | CDN + 보안, 글로벌 | 벤더 종속 | 글로벌 서비스 |

#### 프로덕션 Nginx 예제
```yaml
# docker-compose.prod.yml
services:
  gateway:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
    restart: always

  frontend:
    build:
      context: ./frontend
    expose:
      - "3000"
    environment:
      NODE_ENV: production
    deploy:
      replicas: 3  # Load balancing
    restart: always

  backend:
    build:
      context: ./backend
    expose:
      - "8000"
    restart: always
```

```nginx
# nginx.conf (프로덕션)
upstream nextjs_backend {
    least_conn;
    server frontend_1:3000;
    server frontend_2:3000;
    server frontend_3:3000;
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    location / {
        proxy_pass http://nextjs_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://nextjs_backend;
    }
}
```

## BFF 패턴의 장점

1. **보안 강화**
   - 백엔드 URL을 클라이언트에 노출하지 않음
   - API 키, 시크릿을 서버 측에서 안전하게 관리
   - CORS 문제 해결

2. **유연한 API 설계**
   - 프론트엔드 요구사항에 맞춰 커스터마이징
   - 여러 백엔드 API를 하나로 통합
   - 응답 데이터 변환/가공

3. **성능 최적화**
   - 서버 측에서 여러 API 병렬 호출
   - 캐싱 전략 구현
   - 불필요한 데이터 필터링

4. **타입 안전성**
   - TypeScript로 프론트엔드-BFF 완벽 통합
   - 컴파일 타임 에러 검증
   - IDE 자동완성 지원

## 배포 전략

### 로컬 개발
```bash
# Gateway 없이 직접 실행
docker-compose up -d
# 접속: http://localhost:3000
```

### 프로덕션
```bash
# Gateway 포함 배포
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
# 접속: https://example.com
```

## 결론

### ✅ 로컬 개발 환경
- **Gateway 불필요**
- Next.js 직접 접근 (http://localhost:3000)
- 단순하고 빠른 개발 환경

### 📌 프로덕션 환경
- **Gateway 필수 배포**
- 보안, 성능, 확장성 확보
- SSL/TLS, Load Balancing, Rate Limiting 등
- Nginx, Kong, Traefik, AWS ALB 중 선택

### 🎯 권장사항
- 로컬: Gateway 신경쓰지 않고 개발에 집중
- 프로덕션: Infrastructure 팀이 Gateway 구성 관리
- 개발자는 BFF API Routes 개발에 집중
