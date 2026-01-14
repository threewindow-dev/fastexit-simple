"""SQLAlchemy-based User Repository Implementation."""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from subdomains.user.domain.models.user import User
from subdomains.user.domain.protocols.user_repository_protocol import UserRepository
from subdomains.user.domain.errors import DuplicateUserError
from subdomains.user.infra.entities.user_entity import UserEntity
from shared.errors import InfraError
from shared.decorators import use_transaction


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy async User Repository Implementation.

    비동기 SQLAlchemy를 사용한 데이터 접근 계층.
    @use_transaction 데코레이터를 통해 자동으로 커넥션을 주입받습니다.
    """

    @use_transaction()
    async def add(self, conn: AsyncSession, user: User) -> User:
        """새 사용자 저장.

        Args:
            conn: DB 연결 (AsyncSession)
            user: 저장할 User 엔티티

        Returns:
            id가 설정된 User 엔티티

        Raises:
            DuplicateUserError: username/email 중복
            InfraError: DB 오류
        """
        try:
            orm_user = UserEntity(
                username=user.username,
                email=user.email,
                full_name=user.full_name,
            )
            conn.add(orm_user)
            await conn.flush()  # 즉시 ID 생성

            return User(
                id=orm_user.id,
                username=orm_user.username,
                email=orm_user.email,
                full_name=orm_user.full_name,
                created_at=orm_user.created_at,
            )
        except IntegrityError as exc:
            await conn.rollback()
            raise DuplicateUserError(user.username or user.email, origin_exc=exc)
        except Exception as exc:
            await conn.rollback()
            raise InfraError("USER_SAVE_FAILED", origin_exc=exc)

    @use_transaction()
    async def update(self, conn: AsyncSession, user: User) -> User:
        """사용자 정보 업데이트.

        Args:
            conn: DB 연결 (AsyncSession)
            user: 업데이트할 User 엔티티 (id 필수)

        Returns:
            업데이트된 User 엔티티

        Raises:
            InfraError: DB 오류
        """
        try:
            stmt = select(UserEntity).where(UserEntity.id == user.id)
            result = await conn.execute(stmt)
            orm_user = result.scalars().first()

            if not orm_user:
                raise InfraError("USER_NOT_FOUND")

            orm_user.full_name = user.full_name
            await conn.flush()

            return User(
                id=orm_user.id,
                username=orm_user.username,
                email=orm_user.email,
                full_name=orm_user.full_name,
                created_at=orm_user.created_at,
            )
        except InfraError:
            raise
        except Exception as exc:
            await conn.rollback()
            raise InfraError("USER_UPDATE_FAILED", origin_exc=exc)

    @use_transaction()
    async def remove(self, conn: AsyncSession, user_id: int) -> None:
        """사용자 삭제.

        Args:
            conn: DB 연결 (AsyncSession)
            user_id: 삭제할 사용자 ID

        Raises:
            InfraError: DB 오류
        """
        try:
            stmt = select(UserEntity).where(UserEntity.id == user_id)
            result = await conn.execute(stmt)
            orm_user = result.scalars().first()

            if not orm_user:
                raise InfraError("USER_NOT_FOUND")

            await conn.delete(orm_user)
            await conn.flush()
        except InfraError:
            raise
        except Exception as exc:
            await conn.rollback()
            raise InfraError("USER_DELETE_FAILED", origin_exc=exc)

    @use_transaction()
    async def find_by_id(self, conn: AsyncSession, user_id: int) -> User | None:
        """ID로 사용자 검색.

        Args:
            conn: DB 연결 (AsyncSession)
            user_id: 조회할 사용자 ID

        Returns:
            User 엔티티 또는 None

        Raises:
            InfraError: DB 오류
        """
        try:
            stmt = select(UserEntity).where(UserEntity.id == user_id)
            result = await conn.execute(stmt)
            orm_user = result.scalars().first()

            if not orm_user:
                return None

            return User(
                id=orm_user.id,
                username=orm_user.username,
                email=orm_user.email,
                full_name=orm_user.full_name,
                created_at=orm_user.created_at,
            )
        except Exception as exc:
            raise InfraError("USER_FIND_FAILED", origin_exc=exc)

    @use_transaction()
    async def find_all(
        self, conn: AsyncSession, skip: int = 0, limit: int = 100
    ) -> tuple[list[User], int]:
        """모든 사용자 조회 (페이징).

        Args:
            conn: DB 연결 (AsyncSession)
            skip: 건너뛸 레코드 수
            limit: 반환할 최대 레코드 수

        Returns:
            (User 엔티티 리스트, 전체 개수) 튜플

        Raises:
            InfraError: DB 오류
        """
        try:
            # 전체 개수 조회
            count_stmt = select(func.count(UserEntity.id))
            count_result = await conn.execute(count_stmt)
            total = count_result.scalar() or 0

            # 페이징된 데이터 조회
            stmt = select(UserEntity).offset(skip).limit(limit).order_by(UserEntity.id)
            result = await conn.execute(stmt)
            orm_users = result.scalars().all()

            users = [
                User(
                    id=u.id,
                    username=u.username,
                    email=u.email,
                    full_name=u.full_name,
                    created_at=u.created_at,
                )
                for u in orm_users
            ]
            return users, total
        except Exception as exc:
            raise InfraError("USER_LIST_FAILED", origin_exc=exc)

    @use_transaction()
    async def exists_by_username(self, conn: AsyncSession, username: str) -> bool:
        """사용자명 존재 여부 확인.

        Args:
            conn: DB 연결 (AsyncSession)
            username: 확인할 사용자명

        Returns:
            True if 존재, False otherwise

        Raises:
            InfraError: DB 오류
        """
        try:
            stmt = select(func.count(UserEntity.id)).where(
                UserEntity.username == username
            )
            result = await conn.execute(stmt)
            count = result.scalar() or 0
            return count > 0
        except Exception as exc:
            raise InfraError("USER_EXISTS_CHECK_FAILED", origin_exc=exc)

    @use_transaction()
    async def exists_by_email(self, conn: AsyncSession, email: str) -> bool:
        """이메일 존재 여부 확인.

        Args:
            conn: DB 연결 (AsyncSession)
            email: 확인할 이메일

        Returns:
            True if 존재, False otherwise

        Raises:
            InfraError: DB 오류
        """
        try:
            stmt = select(func.count(UserEntity.id)).where(UserEntity.email == email)
            result = await conn.execute(stmt)
            count = result.scalar() or 0
            return count > 0
        except Exception as exc:
            raise InfraError("USER_EXISTS_CHECK_FAILED", origin_exc=exc)
