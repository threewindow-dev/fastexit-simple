"""SQLAlchemy-based User Repository Implementation."""

from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from subdomains.user.domain.models.user import User
from subdomains.user.infra.repositories.user_repository import UserRepository
from subdomains.user.infra.models import UserORM
from shared.errors import DuplicateUserError, InfraError


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy async User Repository Implementation.
    
    비동기 SQLAlchemy를 사용한 데이터 접근 계층.
    """
    
    def __init__(self, session: AsyncSession):
        """의존성 주입.
        
        Args:
            session: SQLAlchemy AsyncSession 인스턴스
        """
        self.session = session
    
    async def add(self, user: User) -> User:
        """새 사용자 저장.
        
        Args:
            user: 저장할 User 엔티티
        
        Returns:
            id가 설정된 User 엔티티
        
        Raises:
            DuplicateUserError: username/email 중복
            InfraError: DB 오류
        """
        try:
            orm_user = UserORM(
                username=user.username,
                email=user.email,
                full_name=user.full_name,
            )
            self.session.add(orm_user)
            await self.session.flush()  # 즉시 ID 생성
            
            return User(
                id=orm_user.id,
                username=orm_user.username,
                email=orm_user.email,
                full_name=orm_user.full_name,
                created_at=orm_user.created_at,
            )
        except IntegrityError as exc:
            await self.session.rollback()
            raise DuplicateUserError(user.username or user.email, origin_exc=exc)
        except Exception as exc:
            await self.session.rollback()
            raise InfraError("USER_SAVE_FAILED", origin_exc=exc)
    
    async def update(self, user: User) -> User:
        """사용자 정보 업데이트.
        
        Args:
            user: 업데이트할 User 엔티티 (id 필수)
        
        Returns:
            업데이트된 User 엔티티
        
        Raises:
            InfraError: DB 오류
        """
        try:
            stmt = select(UserORM).where(UserORM.id == user.id)
            result = await self.session.execute(stmt)
            orm_user = result.scalars().first()
            
            if not orm_user:
                raise InfraError("USER_NOT_FOUND")
            
            orm_user.full_name = user.full_name
            await self.session.flush()
            
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
            await self.session.rollback()
            raise InfraError("USER_UPDATE_FAILED", origin_exc=exc)
    
    async def remove(self, user_id: int) -> None:
        """사용자 삭제.
        
        Args:
            user_id: 삭제할 사용자 ID
        
        Raises:
            InfraError: DB 오류
        """
        try:
            stmt = select(UserORM).where(UserORM.id == user_id)
            result = await self.session.execute(stmt)
            orm_user = result.scalars().first()
            
            if not orm_user:
                raise InfraError("USER_NOT_FOUND")
            
            await self.session.delete(orm_user)
            await self.session.flush()
        except InfraError:
            raise
        except Exception as exc:
            await self.session.rollback()
            raise InfraError("USER_DELETE_FAILED", origin_exc=exc)
    
    async def find_by_id(self, user_id: int) -> Optional[User]:
        """ID로 사용자 검색.
        
        Args:
            user_id: 조회할 사용자 ID
        
        Returns:
            User 엔티티 또는 None
        
        Raises:
            InfraError: DB 오류
        """
        try:
            stmt = select(UserORM).where(UserORM.id == user_id)
            result = await self.session.execute(stmt)
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
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        """모든 사용자 조회 (페이징).
        
        Args:
            skip: 건너뛸 레코드 수
            limit: 반환할 최대 레코드 수
        
        Returns:
            (User 엔티티 리스트, 전체 개수) 튜플
        
        Raises:
            InfraError: DB 오류
        """
        try:
            # 전체 개수 조회
            count_stmt = select(func.count(UserORM.id))
            count_result = await self.session.execute(count_stmt)
            total = count_result.scalar() or 0
            
            # 페이징된 데이터 조회
            stmt = select(UserORM).offset(skip).limit(limit).order_by(UserORM.id)
            result = await self.session.execute(stmt)
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
    
    async def exists_by_username(self, username: str) -> bool:
        """사용자명 존재 여부 확인.
        
        Args:
            username: 확인할 사용자명
        
        Returns:
            True if 존재, False otherwise
        
        Raises:
            InfraError: DB 오류
        """
        try:
            stmt = select(func.count(UserORM.id)).where(UserORM.username == username)
            result = await self.session.execute(stmt)
            count = result.scalar() or 0
            return count > 0
        except Exception as exc:
            raise InfraError("USER_EXISTS_CHECK_FAILED", origin_exc=exc)
    
    async def exists_by_email(self, email: str) -> bool:
        """이메일 존재 여부 확인.
        
        Args:
            email: 확인할 이메일
        
        Returns:
            True if 존재, False otherwise
        
        Raises:
            InfraError: DB 오류
        """
        try:
            stmt = select(func.count(UserORM.id)).where(UserORM.email == email)
            result = await self.session.execute(stmt)
            count = result.scalar() or 0
            return count > 0
        except Exception as exc:
            raise InfraError("USER_EXISTS_CHECK_FAILED", origin_exc=exc)
