"""
User Repository Protocol (추상 계약)

인프라 계층 인터페이스: 데이터 접근 추상화
"""
from abc import ABC, abstractmethod
from typing import Optional

from domains.user.domain.models.user import User


class UserRepository(ABC):
    """
    User Repository Protocol
    
    DDD Repository 패턴:
    - Aggregate (User)의 지속성 추상화
    - 모든 구현체가 따라야 할 인터페이스
    - 비즈니스 로직 쿼리만 노출 (exists_by_*, find_by_*)
    """
    
    @abstractmethod
    async def add(self, user: User) -> User:
        """
        새 사용자 저장
        
        Args:
            user: 저장할 User 엔티티
        
        Returns:
            id가 설정된 User 엔티티
        
        Raises:
            DuplicateUserError: 이미 존재하는 username/email
            InfraError: DB 오류
        """
        pass
    
    @abstractmethod
    async def update(self, user: User) -> User:
        """
        사용자 정보 업데이트
        
        Args:
            user: 업데이트할 User 엔티티 (id 필수)
        
        Returns:
            업데이트된 User 엔티티
        
        Raises:
            UserNotFoundError: 존재하지 않는 사용자
            InfraError: DB 오류
        """
        pass
    
    @abstractmethod
    async def remove(self, user_id: int) -> None:
        """
        사용자 삭제
        
        Args:
            user_id: 삭제할 사용자 ID
        
        Raises:
            UserNotFoundError: 존재하지 않는 사용자
            InfraError: DB 오류
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: int) -> Optional[User]:
        """
        ID로 사용자 검색
        
        Args:
            user_id: 조회할 사용자 ID
        
        Returns:
            User 엔티티 또는 None
        
        Raises:
            InfraError: DB 오류
        """
        pass
    
    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        """
        모든 사용자 조회 (페이징 지원)
        
        Args:
            skip: 건너뛸 레코드 수
            limit: 반환할 최대 레코드 수
        
        Returns:
            (User 엔티티 리스트, 전체 개수) 튜플
        
        Raises:
            InfraError: DB 오류
        """
        pass
    
    @abstractmethod
    async def exists_by_username(self, username: str) -> bool:
        """
        사용자명 존재 여부 확인
        
        Args:
            username: 확인할 사용자명
        
        Returns:
            True if 존재, False otherwise
        
        Raises:
            InfraError: DB 오류
        """
        pass
    
    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """
        이메일 존재 여부 확인
        
        Args:
            email: 확인할 이메일
        
        Returns:
            True if 존재, False otherwise
        
        Raises:
            InfraError: DB 오류
        """
        pass


# ============================================================================
# PostgreSQL Implementation
# ============================================================================

import psycopg
import psycopg.errors


class PsycopgUserRepository(UserRepository):
    """PostgreSQL User Repository Implementation"""

    def __init__(self, connection):
        """의존성 주입"""
        self.connection = connection

    async def add(self, user: User) -> User:
        """새 사용자 저장"""
        try:
            async with self.connection.cursor() as cur:
                await cur.execute(
                    "INSERT INTO users (username, email, full_name, created_at) VALUES (%s, %s, %s, %s) RETURNING id, username, email, full_name, created_at",
                    (user.username, user.email, user.full_name, user.created_at),
                )
                row = await cur.fetchone()
        except psycopg.errors.UniqueViolation as exc:
            from shared.errors import DuplicateUserError
            raise DuplicateUserError(user.username or user.email, origin_exc=exc)
        except Exception as exc:
            from shared.errors import InfraError
            raise InfraError(code="USER_SAVE_FAILED", message="Failed to save user", origin_exc=exc)

        if row:
            return User(id=row["id"], username=row["username"], email=row["email"], full_name=row["full_name"], created_at=row["created_at"])
        from shared.errors import InfraError
        raise InfraError(code="USER_SAVE_FAILED", message="Failed to save user")

    async def update(self, user: User) -> User:
        """사용자 정보 업데이트"""
        try:
            async with self.connection.cursor() as cur:
                await cur.execute("UPDATE users SET full_name = %s WHERE id = %s RETURNING id, username, email, full_name, created_at", (user.full_name, user.id))
                row = await cur.fetchone()
        except Exception as exc:
            from shared.errors import InfraError
            raise InfraError(code="USER_UPDATE_FAILED", message="Failed to update user", origin_exc=exc)
        if row:
            return User(id=row["id"], username=row["username"], email=row["email"], full_name=row["full_name"], created_at=row["created_at"])
        from shared.errors import InfraError
        raise InfraError(code="USER_UPDATE_FAILED", message="Failed to update user")

    async def remove(self, user_id: int) -> None:
        """사용자 삭제"""
        try:
            async with self.connection.cursor() as cur:
                await cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        except Exception as exc:
            from shared.errors import InfraError
            raise InfraError(code="USER_DELETE_FAILED", message="Failed to delete user", origin_exc=exc)

    async def find_by_id(self, user_id: int) -> Optional[User]:
        """ID로 사용자 검색"""
        try:
            async with self.connection.cursor() as cur:
                await cur.execute("SELECT id, username, email, full_name, created_at FROM users WHERE id = %s", (user_id,))
                row = await cur.fetchone()
        except Exception as exc:
            from shared.errors import InfraError
            raise InfraError(code="USER_FIND_FAILED", message="Failed to find user", origin_exc=exc)
        if row:
            return User(id=row["id"], username=row["username"], email=row["email"], full_name=row["full_name"], created_at=row["created_at"])
        return None

    async def find_all(self, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        """모든 사용자 조회 (페이징)"""
        try:
            async with self.connection.cursor() as cur:
                await cur.execute("SELECT COUNT(*) as count FROM users")
                count_row = await cur.fetchone()
                total = count_row["count"] if count_row else 0
                await cur.execute("SELECT id, username, email, full_name, created_at FROM users ORDER BY id OFFSET %s LIMIT %s", (skip, limit))
                rows = await cur.fetchall()
        except Exception as exc:
            from shared.errors import InfraError
            raise InfraError(code="USER_LIST_FAILED", message="Failed to list users", origin_exc=exc)
        users = [User(id=row["id"], username=row["username"], email=row["email"], full_name=row["full_name"], created_at=row["created_at"]) for row in rows]
        return users, total

    async def exists_by_username(self, username: str) -> bool:
        """사용자명 존재 여부"""
        try:
            async with self.connection.cursor() as cur:
                await cur.execute("SELECT 1 FROM users WHERE username = %s LIMIT 1", (username,))
                row = await cur.fetchone()
                return row is not None
        except Exception as exc:
            from shared.errors import InfraError
            raise InfraError(code="USER_EXISTS_CHECK_FAILED", message="Failed to check existence", origin_exc=exc)

    async def exists_by_email(self, email: str) -> bool:
        """이메일 존재 여부"""
        try:
            async with self.connection.cursor() as cur:
                await cur.execute("SELECT 1 FROM users WHERE email = %s LIMIT 1", (email,))
                row = await cur.fetchone()
                return row is not None
        except Exception as exc:
            from shared.errors import InfraError
            raise InfraError(code="USER_EXISTS_CHECK_FAILED", message="Failed to check existence", origin_exc=exc)
