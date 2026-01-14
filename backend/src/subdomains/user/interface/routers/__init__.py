"""
User subdomain routers

모든 user 라우터를 통합하고 prefix를 설정합니다.
main.py에서는 이 router를 import하여 사용합니다.
"""

from fastapi import APIRouter
from .user_router import router as user_router

# User 서브도메인 라우터 (모든 user 관련 엔드포인트 통합)
router = APIRouter(prefix="/api/users")
router.include_router(user_router)

__all__ = ["router"]
