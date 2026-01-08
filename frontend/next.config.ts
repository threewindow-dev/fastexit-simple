import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'standalone',
  // API 라우트를 통해 BFF 패턴 구현
  async rewrites() {
    return [
      // 모든 /api/* 요청은 Next.js API Routes로 처리
      // API Routes에서 FastAPI로 프록시
    ]
  },
}

export default nextConfig
