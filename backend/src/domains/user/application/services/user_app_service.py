"""
User Application Service (Use Cases)

애플리케이션 계층: 비즈니스 프로세스 조율
"""
from typing import Optional

from domains.user.application.dtos import (
    RegisterUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
    UserPagedListQuery,
    RegisterUserCommandResult,
    UserPagedListQueryResult,
)
from domains.user.domain.models import User
from domains.user.infra.repositories import UserRepository
from shared.errors import DuplicateUserError, UserNotFoundError
from shared.protocols.transaction import TransactionProtocol


class UserAppService:
    """
    User Application Service
    
    DDD Application Service 패턴:
    - Use Case (Command/Query) 처리
    - Domain Model과 Repository 조율
    - Transaction 관리
    - DTO 변환
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        transaction: TransactionProtocol,
    ):
        """
        의존성 주입
        
        Args:
            user_repository: User 저장소
            transaction: 트랜잭션 관리자
        """
        self.user_repository = user_repository
        self.transaction = transaction
    
    # ========================================================================
    # Commands (쓰기 작업)
    # ========================================================================
    
    async def create_user(self, command: RegisterUserCommand) -> RegisterUserCommandResult:
        """
        Register User Use Case
        
        프로세스:
        1. 중복 검사 (username, email)
        2. Domain Model 생성 (비즈니스 규칙 검증)
        3. Repository에 저장
        4. 결과를 DTO로 변환
        
        Args:
            command: CreateUserCommand
        
        Returns:
            생성된 UserResult
        
        Raises:
            DuplicateUserError: username/email 중복
            DomainError: 비즈니스 규칙 위반
            InfraError: DB 오류
        """
        # 1. 중복 검사
        if await self.user_repository.exists_by_username(command.username):
            raise DuplicateUserError(command.username)
        
        if await self.user_repository.exists_by_email(command.email):
            raise DuplicateUserError(command.email)
        
        # 2. Domain Model 생성 (팩토리 메서드는 비즈니스 규칙 검증)
        user = User.create(
            username=command.username,
            email=command.email,
            full_name=command.full_name,
        )
        
        # 3. Repository에 저장
        saved_user = await self.user_repository.add(user)
        
        # 4. DTO 변환
        return RegisterUserCommandResult.from_domain(saved_user)
    
    async def update_user(self, command: UpdateUserCommand) -> RegisterUserCommandResult:
        """
        Update User Use Case
        
        프로세스:
        1. 사용자 조회
        2. Domain Model 업데이트 (비즈니스 규칙 검증)
        3. Repository에 저장
        4. 결과를 DTO로 변환
        
        Args:
            command: UpdateUserCommand
        
        Returns:
            업데이트된 UserResult
        
        Raises:
            UserNotFoundError: 사용자 미존재
            DomainError: 비즈니스 규칙 위반
            InfraError: DB 오류
        """
        # 1. 사용자 조회
        user = await self.user_repository.find_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError(command.user_id)
        
        # 2. Domain Model 업데이트
        if command.full_name is not None:
            user.change_full_name(command.full_name)
        
        # 3. Repository에 저장
        updated_user = await self.user_repository.update(user)
        
        # 4. DTO 변환
        return RegisterUserCommandResult.from_domain(updated_user)
    
    async def delete_user(self, command: DeleteUserCommand) -> None:
        """
        Delete User Use Case
        
        프로세스:
        1. 사용자 존재 확인
        2. Repository에서 삭제
        
        Args:
            command: DeleteUserCommand
        
        Raises:
            UserNotFoundError: 사용자 미존재
            InfraError: DB 오류
        """
        # 1. 사용자 존재 확인
        user = await self.user_repository.find_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError(command.user_id)
        
        # 2. Repository에서 삭제
        await self.user_repository.remove(command.user_id)
    
    # ========================================================================
    # Queries (읽기 작업)
    # ========================================================================
    
    async def get_user(self, user_id: int) -> RegisterUserCommandResult:
        """
        Get User By ID Use Case
        
        Args:
            user_id: 사용자 ID
        
        Returns:
            RegisterUserCommandResult
        
        Raises:
            UserNotFoundError: 사용자 미존재
            InfraError: DB 오류
        """
        user = await self.user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        
        return RegisterUserCommandResult.from_domain(user)
    
    async def list_users(self, query: UserPagedListQuery) -> UserPagedListQueryResult:
        """
        List All Users Use Case
        
        Args:
            query: UserPagedListQuery
        
        Returns:
            UserPagedListQueryResult
        
        Raises:
            InfraError: DB 오류
        """
        users, total = await self.user_repository.find_all(
            skip=query.skip,
            limit=query.limit,
        )
        
        results = [RegisterUserCommandResult.from_domain(user) for user in users]
        
        return UserPagedListQueryResult(
            items=results,
            total_count=total,
            skip=query.skip,
            limit=query.limit,
        )
