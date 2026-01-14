"""
User Repository Implementation (PostgreSQL with Psycopg)

인프라 계층: 실제 데이터 접근 구현
"""

from datetime import datetime

import psycopg
import psycopg.errors

from subdomains.user.domain.models.user import User
from subdomains.user.domain.protocols.user_repository_protocol import UserRepository
from subdomains.user.domain.errors import DuplicateUserError
from shared.errors import InfraError
from shared.protocols.transaction import Connection


class PsycopgUserRepository(UserRepository):
    """
    PostgreSQL User Repository Implementation

    psycopg (async PostgreSQL driver) 사용
    Connection을 메서드 파라미터로 받아 동작.
    """

    async def add(self, conn: Connection, user: User) -> User:
        """새 사용자 저장"""
        connection = conn
        try:
            async with connection.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO users (username, email, full_name, created_at)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id, username, email, full_name, created_at
                    """,
                    (user.username, user.email, user.full_name, user.created_at),
                )
                row = await cur.fetchone()

        except psycopg.errors.UniqueViolation as exc:
            raise DuplicateUserError(
                user.username or user.email,
                origin_exc=exc,
            )
        except Exception as exc:
            raise InfraError(
                code="USER_SAVE_FAILED",
                message="Failed to save user to database",
                origin_exc=exc,
            )

        if row:
            return User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                full_name=row["full_name"],
                created_at=row["created_at"],
            )

        raise InfraError(
            code="USER_SAVE_FAILED",
            message="Failed to save user: no row returned",
        )

    async def update(self, conn: Connection, user: User) -> User:
        """사용자 정보 업데이트"""
        connection = conn
        try:
            async with connection.cursor() as cur:
                await cur.execute(
                    """
                    UPDATE users
                    SET full_name = %s
                    WHERE id = %s
                    RETURNING id, username, email, full_name, created_at
                    """,
                    (user.full_name, user.id),
                )
                row = await cur.fetchone()

        except Exception as exc:
            raise InfraError(
                code="USER_UPDATE_FAILED",
                message="Failed to update user in database",
                origin_exc=exc,
            )

        if row:
            return User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                full_name=row["full_name"],
                created_at=row["created_at"],
            )

        raise InfraError(
            code="USER_UPDATE_FAILED",
            message="Failed to update user: no row returned",
        )

    async def remove(self, conn: Connection, user_id: int) -> None:
        """사용자 삭제"""
        connection = conn
        try:
            async with connection.cursor() as cur:
                await cur.execute(
                    "DELETE FROM users WHERE id = %s",
                    (user_id,),
                )
        except Exception as exc:
            raise InfraError(
                code="USER_DELETE_FAILED",
                message="Failed to delete user from database",
                origin_exc=exc,
            )

    async def find_by_id(self, conn: Connection, user_id: int) -> User | None:
        """ID로 사용자 검색"""
        connection = conn
        try:
            async with connection.cursor() as cur:
                await cur.execute(
                    "SELECT id, username, email, full_name, created_at FROM users WHERE id = %s",
                    (user_id,),
                )
                row = await cur.fetchone()
        except Exception as exc:
            raise InfraError(
                code="USER_FIND_FAILED",
                message="Failed to find user in database",
                origin_exc=exc,
            )

        if row:
            return User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                full_name=row["full_name"],
                created_at=row["created_at"],
            )

        return None

    async def find_all(
        self, conn: Connection, skip: int = 0, limit: int = 100
    ) -> tuple[list[User], int]:
        """모든 사용자 조회 (페이징)"""
        connection = conn
        try:
            async with connection.cursor() as cur:
                # 전체 개수 조회
                await cur.execute("SELECT COUNT(*) as count FROM users")
                count_row = await cur.fetchone()
                total = count_row["count"] if count_row else 0

                # 페이지별 조회
                await cur.execute(
                    "SELECT id, username, email, full_name, created_at FROM users ORDER BY id OFFSET %s LIMIT %s",
                    (skip, limit),
                )
                rows = await cur.fetchall()
        except Exception as exc:
            raise InfraError(
                code="USER_LIST_FAILED",
                message="Failed to list users from database",
                origin_exc=exc,
            )

        users = [
            User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                full_name=row["full_name"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

        return users, total

    async def exists_by_username(self, conn: Connection, username: str) -> bool:
        """사용자명 존재 여부"""
        connection = conn
        try:
            async with connection.cursor() as cur:
                await cur.execute(
                    "SELECT 1 FROM users WHERE username = %s LIMIT 1",
                    (username,),
                )
                row = await cur.fetchone()
                return row is not None
        except Exception as exc:
            raise InfraError(
                code="USER_EXISTS_CHECK_FAILED",
                message="Failed to check username existence",
                origin_exc=exc,
            )

    async def exists_by_email(self, conn: Connection, email: str) -> bool:
        """이메일 존재 여부"""
        connection = conn
        try:
            async with connection.cursor() as cur:
                await cur.execute(
                    "SELECT 1 FROM users WHERE email = %s LIMIT 1",
                    (email,),
                )
                row = await cur.fetchone()
                return row is not None
        except Exception as exc:
            raise InfraError(
                code="USER_EXISTS_CHECK_FAILED",
                message="Failed to check email existence",
                origin_exc=exc,
            )
