"""
User API Router (FastAPI endpoints)

인터페이스 계층: HTTP 엔드포인트
- 환경변수 REPOSITORY_TYPE으로 저장소 선택 (sqlalchemy | psycopg)
- FastAPI Depends()를 통한 DI (core/dependencies.py)
- 구체적 구현체 참조 제거 (개발 표준 준수)
"""

from fastapi import APIRouter, status, Depends
from fastapi import Path, Query

from subdomains.user.application.dtos import (
    RegisterUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
    UserPagedListQuery,
)
from subdomains.user.application.services import UserAppService
from subdomains.user.interface.schemas import (
    PostUserRequest,
    PostUserResponse,
    PostUserResponseData,
    PatchUserRequest,
    PatchUserResponse,
    PatchUserResponseData,
    GetUserPagedListResponse,
    GetUserPagedListResponseData,
    GetUserPagedListItemInfo,
    GetUserResponse,
    GetUserResponseItemInfo,
    GetUserPagedListRequest,
    DeleteUserResponse,
    DeleteUserResponseData,
)
from shared.schemas import ApiResponse
from core.common_responses import common_responses
from dependencies import get_user_app_service


# ============================================================================
# Router 정의
# ============================================================================

router = APIRouter(
    tags=["users"],
    responses={
        400: {"description": "Bad request"},
        500: {"description": "Server error"},
    },
)

# ============================================================================
# API Endpoints
# ============================================================================


@router.post(
    "/",
    response_model=PostUserResponse,
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
async def create_user(
    request: PostUserRequest,
    service: UserAppService = Depends(get_user_app_service),
) -> PostUserResponse:
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
    command = RegisterUserCommand(
        username=request.username,
        email=request.email,
        full_name=request.full_name,
    )
    result = await service.create_user(command)

    data = PostUserResponseData(
        id=result.id,
        username=result.username,
        email=result.email,
        full_name=result.full_name,
        created_at=(
            result.created_at.isoformat()
            if hasattr(result.created_at, "isoformat")
            else str(result.created_at)
        ),
    )
    return PostUserResponse(code=0, message="User created successfully", data=data)


@router.get(
    "/",
    response_model=GetUserPagedListResponse,
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
    limit: int = Query(
        100, ge=1, le=1000, examples=[50, 100], description="조회할 개수 (1-1000)"
    ),
    service: UserAppService = Depends(get_user_app_service),
) -> GetUserPagedListResponse:
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

    query = UserPagedListQuery(skip=skip, limit=limit)
    result = await service.list_users(query)

    items_data = [
        GetUserPagedListItemInfo(
            id=item.id,
            username=item.username,
            email=item.email,
            full_name=item.full_name,
            created_at=(
                item.created_at.isoformat()
                if hasattr(item.created_at, "isoformat")
                else str(item.created_at)
            ),
        )
        for item in result.items
    ]
    data = GetUserPagedListResponseData(
        items=items_data,
        total_count=result.total_count,
        skip=skip,
        limit=limit,
    )
    return GetUserPagedListResponse(code=0, message="success", data=data)


@router.get(
    "/{user_id}",
    response_model=GetUserResponse,
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
async def get_user(
    user_id: int = Path(..., examples=[1, 2], description="사용자 ID"),
    service: UserAppService = Depends(get_user_app_service),
) -> GetUserResponse:
    """
    사용자 단건 조회 엔드포인트

    경로 파라미터:
    - user_id: 사용자 ID

    응답:
    - code: 0 (성공)
    - message: 성공 메시지
    - data: 사용자 정보
    """
    result = await service.get_user(user_id)

    data = GetUserResponseItemInfo(
        id=result.id,
        username=result.username,
        email=result.email,
        full_name=result.full_name,
        created_at=(
            result.created_at.isoformat()
            if hasattr(result.created_at, "isoformat")
            else str(result.created_at)
        ),
    )
    return GetUserResponse(code=0, message="success", data=data)


@router.patch(
    "/{user_id}",
    response_model=PatchUserResponse,
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
    service: UserAppService = Depends(get_user_app_service),
) -> PatchUserResponse:
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
    command = UpdateUserCommand(
        user_id=user_id,
        full_name=request.full_name,
    )
    result = await service.update_user(command)

    data = PatchUserResponseData(
        id=result.id,
        username=result.username,
        email=result.email,
        full_name=result.full_name,
        updated_at=(
            result.created_at.isoformat()
            if hasattr(result.created_at, "isoformat")
            else str(result.created_at)
        ),
    )
    return PatchUserResponse(code=0, message="User updated successfully", data=data)


@router.delete(
    "/{user_id}",
    response_model=DeleteUserResponse,
    status_code=status.HTTP_200_OK,
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
async def delete_user(
    user_id: int = Path(..., examples=[1], description="사용자 ID"),
    service: UserAppService = Depends(get_user_app_service),
) -> DeleteUserResponse:
    """
    사용자 삭제 엔드포인트

    경로 파라미터:
    - user_id: 사용자 ID

    응답:
    - 204 No Content (성공)
    """
    command = DeleteUserCommand(user_id=user_id)
    await service.delete_user(command)

    from datetime import datetime, timezone

    data = DeleteUserResponseData(
        id=user_id,
        deleted_at=datetime.now(timezone.utc).isoformat(),
    )
    return DeleteUserResponse(code=0, message="User deleted successfully", data=data)
