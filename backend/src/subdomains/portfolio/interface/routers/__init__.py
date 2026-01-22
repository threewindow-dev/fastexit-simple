"""Portfolio subdomain routers."""

from fastapi import APIRouter

from .portfolio_router import router as portfolio_router

router = APIRouter(prefix="/api/portfolio")
router.include_router(portfolio_router)

__all__ = ["router"]
