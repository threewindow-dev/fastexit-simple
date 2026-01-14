"""
User Repository Protocol (추상 계약)

도메인 계층: Repository 인터페이스 정의
"""

from abc import ABC, abstractmethod

from subdomains.user.domain.models.user import User
from shared.protocols.transaction import Connection


class UserRepository(ABC):
    """
    User Repository Protocol

    DDD Repository 패턴:
    - Aggregate (User)의 지속성 추상화
    - 모든 구현체가 따라야 할 인터페이스
    - 비즈니스 로직 쿼리만 노출 (exists_by_*, find_by_*)
    - Connection을 첫 번째 파라미터로 받아 트랜잭션 내에서 동작
    """

    @abstractmethod
    async def add(self, conn: Connection, user: User) -> User:
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
    async def update(self, conn: Connection, user: User) -> User:
        """
        사용자 정보 업데이트

        Args:
            conn: DB 연결
            user: 업데이트할 User 엔티티 (id 필수)

        Returns:
            업데이트된 User 엔티티

        Raises:
            UserNotFoundError: 존재하지 않는 사용자
            InfraError: DB 오류
        """
        pass

    @abstractmethod
    async def remove(self, conn: Connection, user_id: int) -> None:
        """
        사용자 삭제

        Args:
            conn: DB 연결
            user_id: 삭제할 사용자 ID

        Raises:
            UserNotFoundError: 존재하지 않는 사용자
            InfraError: DB 오류
        """
        pass

    @abstractmethod
    async def find_by_id(self, conn: Connection, user_id: int) -> User | None:
        """
        ID로 사용자 검색

        Args:
            conn: DB 연결
            user_id: 조회할 사용자 ID

        Returns:
            User 엔티티 또는 None

        Raises:
            InfraError: DB 오류
        """
        pass

    @abstractmethod
    async def find_all(
        self, conn: Connection, skip: int = 0, limit: int = 100
    ) -> tuple[list[User], int]:
        """
        모든 사용자 조회 (페이징 지원)

        Args:
            conn: DB 연결
            skip: 건너뛸 레코드 수
            limit: 반환할 최대 레코드 수

        Returns:
            (User 엔티티 리스트, 전체 개수) 튜플

        Raises:
            InfraError: DB 오류
        """
        pass

    @abstractmethod
    async def exists_by_username(self, conn: Connection, username: str) -> bool:
        """
        사용자명 존재 여부 확인

        Args:
            conn: DB 연결
            username: 확인할 사용자명

        Returns:
            True if 존재, False otherwise

        Raises:
            InfraError: DB 오류
        """
        pass

    @abstractmethod
    async def exists_by_email(self, conn: Connection, email: str) -> bool:
        """
        이메일 존재 여부 확인

        Args:
            conn: DB 연결
            email: 확인할 이메일

        Returns:
            True if 존재, False otherwise

        Raises:
            InfraError: DB 오류
        """
        pass
