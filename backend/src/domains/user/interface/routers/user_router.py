"""
User API Router (FastAPI endpoints)

인터페이스 계층: HTTP 엔드포인트
"""
from fastapi import APIRouter, status
from fastapi import Path, Query

from domains.user.application.dtos import (
    RegisterUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
    UserPagedListQuery,
)
from domains.user.application.services import UserAppService
from domains.user.interface.schemas import (
    PostUserRequest,
    PatchUserRequest,
    GetUserPagedListResponse,
    GetUserResponse,
    GetUserPagedListRequest,
)
from core.exception_handlers import create_ok_response
from core.common_responses import common_responses
from domains.user.infra.repositories import PsycopgUserRepository
from infra.database import PsycopgTransaction


def create_user_router(db_pool) -> APIRouter:
    """
    User 라우터 팩토리 함수
    
    DB 풀을 의존성으로 주입받아 라우터 생성
    
    Args:
        db_pool: DatabasePool 인스턴스
    
    Returns:
        설정된 APIRouter
    """
    router = APIRouter(
        prefix="/api/users",
        tags=["users"],
        responses={400: {"description": "Bad request"}, 500: {"description": "Server error"}},
    )
    
    # ========================================================================
    # API Endpoints
    # ========================================================================
    
    @router.post(
        "",
        response_model=dict,
        status_code=status.HTTP_201_CREATED,
        summary="Create User",
        description=(
            "## 기능\n"
            "새 사용자를 생성합니다.\n\n"
            "## 권한\n"
            "인증 필요\n\n"
            "## 파라미터\n"
            "요청 바디 필드는 설명에서 제외됩니다."
        ),
        responses={**common_responses},
    )
    async def create_user(request: PostUserRequest) -> dict:
        """
        사용자 생성 엔드포인트
        
        요청 바디:
        - username: 사용자명 (3글자 이상, 고유)
        - email: 이메일 (고유)
        - full_name: 전체 이름 (선택)
        
        응답:
        - code: 0 (성공)
        - message: 성공 메시지
        - data: 생성된 사용자 정보
        """
        async with db_pool.connection() as conn:
            tx = PsycopgTransaction(conn)
            repository = PsycopgUserRepository(conn)
            service = UserAppService(repository, tx)
            try:
                command = RegisterUserCommand(
                    username=request.username,
                    email=request.email,
                    full_name=request.full_name,
                )
                result = await service.create_user(command)
                await tx.commit()
            except Exception:
                await tx.rollback()
                raise

            return create_ok_response(
                result.to_dict(),
                message="User created successfully",
            )
    
    
    @router.get(
        "",
        response_model=dict,
        summary="List Users",
        description=(
            "## 기능\n"
            "사용자 목록을 조회합니다 (페이징 지원).\n\n"
            "## 권한\n"
            "인증 필요\n\n"
            "## 페이징 파라미터\n"
            "- skip: 건너뛸 개수\n"
            "- limit: 조회할 개수"
        ),
        responses={**common_responses},
    )
    async def list_users(
        skip: int = Query(0, ge=0, examples=[0, 10], description="건너뛸 개수"),
        limit: int = Query(100, ge=1, le=1000, examples=[50, 100], description="조회할 개수 (1-1000)"),
    ) -> dict:
        """
        사용자 목록 조회 엔드포인트
        
        쿼리 파라미터:
        - skip: 건너뛸 개수 (기본값: 0)
        - limit: 조회할 개수 (기본값: 100, 최대 1000)
        
        응답:
        - code: 0 (성공)
        - message: 성공 메시지
        - data: {items, total, skip, limit}
        """
        # limit 제한
        if limit > 1000:
            limit = 1000
        
        async with db_pool.connection() as conn:
            tx = PsycopgTransaction(conn)
            repository = PsycopgUserRepository(conn)
            service = UserAppService(repository, tx)
            
            query = UserPagedListQuery(skip=skip, limit=limit)
            result = await service.list_users(query)
            
            return create_ok_response(result.to_dict())
    
    
    @router.get(
        "/{user_id}",
        response_model=dict,
        summary="Get User",
        description=(
            "## 기능\n"
            "특정 사용자를 조회합니다.\n\n"
            "## 권한\n"
            "인증 필요\n\n"
            "## Path 파라미터\n"
            "- user_id: 사용자 ID"
        ),
        responses={**common_responses},
    )
    async def get_user(user_id: int = Path(..., examples=[1, 2], description="사용자 ID")) -> dict:
        """
        사용자 단건 조회 엔드포인트
        
        경로 파라미터:
        - user_id: 사용자 ID
        
        응답:
        - code: 0 (성공)
        - message: 성공 메시지
        - data: 사용자 정보
        """
        async with db_pool.connection() as conn:
            tx = PsycopgTransaction(conn)
            repository = PsycopgUserRepository(conn)
            service = UserAppService(repository, tx)

            result = await service.get_user(user_id)
            
            return create_ok_response(result.to_dict())
    
    
    @router.patch(
        "/{user_id}",
        response_model=dict,
        summary="Update User",
        description=(
            "## 기능\n"
            "사용자 정보를 업데이트합니다.\n\n"
            "## 권한\n"
            "인증 필요\n\n"
            "## Path 파라미터\n"
            "- user_id: 사용자 ID"
        ),
        responses={**common_responses},
    )
    async def update_user(
        request: PatchUserRequest,
        user_id: int = Path(..., examples=[1], description="사용자 ID"),
    ) -> dict:
        """
        사용자 업데이트 엔드포인트
        
        경로 파라미터:
        - user_id: 사용자 ID
        
        요청 바디:
        - full_name: 전체 이름
        
        응답:
        - code: 0 (성공)
        - message: 성공 메시지
        - data: 업데이트된 사용자 정보
        """
        async with db_pool.connection() as conn:
            tx = PsycopgTransaction(conn)
            repository = PsycopgUserRepository(conn)
            service = UserAppService(repository, tx)
            try:
                command = UpdateUserCommand(
                    user_id=user_id,
                    full_name=request.full_name,
                )
                result = await service.update_user(command)
                await tx.commit()
            except Exception:
                await tx.rollback()
                raise

            return create_ok_response(
                result.to_dict(),
                message="User updated successfully",
            )
    
    
    @router.delete(
        "/{user_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Delete User",
        description=(
            "## 기능\n"
            "사용자를 삭제합니다.\n\n"
            "## 권한\n"
            "인증 필요\n\n"
            "## Path 파라미터\n"
            "- user_id: 사용자 ID"
        ),
        responses={**common_responses},
    )
    async def delete_user(user_id: int = Path(..., examples=[1], description="사용자 ID")) -> None:
        """
        사용자 삭제 엔드포인트
        
        경로 파라미터:
        - user_id: 사용자 ID
        
        응답:
        - 204 No Content (성공)
        """
        async with db_pool.connection() as conn:
            tx = PsycopgTransaction(conn)
            repository = PsycopgUserRepository(conn)
            service = UserAppService(repository, tx)
            try:
                command = DeleteUserCommand(user_id=user_id)
                await service.delete_user(command)
                await tx.commit()
            except Exception:
                await tx.rollback()
                raise

            return None
    
    return router
