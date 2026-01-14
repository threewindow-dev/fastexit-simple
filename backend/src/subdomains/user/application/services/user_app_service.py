"""
User Application Service (Use Cases)

애플리케이션 계층: 비즈니스 프로세스 조율
- 트랜잭션 경계 관리 (per use-case)
- Domain Model과 Repository 조율
"""

from typing import Callable, Awaitable

from subdomains.user.application.dtos import (
    RegisterUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
    UserPagedListQuery,
    RegisterUserCommandResult,
    UserPagedListQueryResult,
)
from subdomains.user.domain.models import User
from subdomains.user.domain.protocols import UserRepository
from shared.errors import DuplicateUserError, UserNotFoundError
from shared.protocols.transaction import TransactionManager


class UserAppService:
    """
    User Application Service

    DDD Application Service 패턴:
    - Use Case (Command/Query) 처리
    - 메서드별 트랜잭션 경계 관리 (per use-case)
    - Domain Model과 Repository 조율
    - DTO 변환

    트랜잭션 관리:
    - 커맨드(쓰기): 트랜잭션으로 감싸짐 (자동 commit/rollback)
    - 쿼리(읽기): 읽기 전용 트랜잭션
    """

    def __init__(
        self,
        user_repository: UserRepository,
        transaction_manager: TransactionManager,
    ):
        """
        의존성 주입

        Args:
            user_repository: User 저장소
            transaction_manager: 트랜잭션 매니저 (readonly/writable 트랜잭션 생성)
        """
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager

    # ========================================================================
    # Commands (쓰기 작업) - 트랜잭션으로 감싸짐
    # ========================================================================

    async def create_user(
        self, command: RegisterUserCommand
    ) -> RegisterUserCommandResult:
        """
        Register User Use Case

        트랜잭션 경계:
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

        async def _execute(conn):
            # 1. 중복 검사
            if await self.user_repository.exists_by_username(conn, command.username):
                raise DuplicateUserError(command.username)

            if await self.user_repository.exists_by_email(conn, command.email):
                raise DuplicateUserError(command.email)

            # 2. Domain Model 생성 (팩토리 메서드는 비즈니스 규칙 검증)
            user = User.create(
                username=command.username,
                email=command.email,
                full_name=command.full_name,
            )

            # 3. Repository에 저장
            saved_user = await self.user_repository.add(conn, user)

            # 4. DTO 변환
            return RegisterUserCommandResult.from_domain(saved_user)

        return await self._run_writable(_execute)

    async def update_user(
        self, command: UpdateUserCommand
    ) -> RegisterUserCommandResult:
        """
        Update User Use Case

        트랜잭션 경계:
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

        async def _execute(conn):
            # 1. 사용자 조회
            user = await self.user_repository.find_by_id(conn, command.user_id)
            if user is None:
                raise UserNotFoundError(command.user_id)

            # 2. Domain Model 업데이트
            if command.full_name is not None:
                user.change_full_name(command.full_name)

            # 3. Repository에 저장
            updated_user = await self.user_repository.update(conn, user)

            # 4. DTO 변환
            return RegisterUserCommandResult.from_domain(updated_user)

        return await self._run_writable(_execute)

    async def delete_user(self, command: DeleteUserCommand) -> None:
        """
        Delete User Use Case

        트랜잭션 경계:
        1. 사용자 존재 확인
        2. Repository에서 삭제

        Args:
            command: DeleteUserCommand

        Raises:
            UserNotFoundError: 사용자 미존재
            InfraError: DB 오류
        """

        async def _execute(conn):
            # 1. 사용자 존재 확인
            user = await self.user_repository.find_by_id(conn, command.user_id)
            if user is None:
                raise UserNotFoundError(command.user_id)

            # 2. Repository에서 삭제
            await self.user_repository.remove(conn, command.user_id)

        await self._run_writable(_execute)

    # ========================================================================
    # Queries (읽기 작업) - 트랜잭션 불필요
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

        async def _execute(conn):
            user = await self.user_repository.find_by_id(conn, user_id)
            if user is None:
                raise UserNotFoundError(user_id)

            return RegisterUserCommandResult.from_domain(user)

        return await self._run_readonly(_execute)

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

        async def _execute(conn):
            users, total = await self.user_repository.find_all(
                conn,
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

        return await self._run_readonly(_execute)

    # ========================================================================
    # Transaction Management
    # ========================================================================

    async def _run_readonly(self, func: Callable) -> any:
        """읽기 전용 트랜잭션으로 함수 실행."""
        tx = await self.transaction_manager.create_readonly_transaction()
        async with tx:
            return await func(tx.connection)

    async def _run_writable(self, func: Callable) -> any:
        """쓰기 트랜잭션으로 함수 실행."""
        tx = await self.transaction_manager.create_writable_transaction()
        async with tx:
            return await func(tx.connection)
