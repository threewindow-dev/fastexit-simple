"""
Authentication infrastructure implementations.

JWT 토큰 관리 구현체
"""

import jwt
from datetime import datetime, timezone, timedelta
from typing import dict


class JWTTokenManager:
    """JWT 토큰 생성 및 검증 구현체

    Protocol: shared.protocols.auth.TokenManager
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        """
        Args:
            secret_key: JWT 서명에 사용할 비밀 키
            algorithm: JWT 알고리즘 (기본값: HS256)
        """
        self.secret_key = secret_key
        self.algorithm = algorithm

    def verify_token(self, token: str) -> dict | None:
        """
        토큰 검증 및 payload 추출

        Args:
            token: JWT 토큰 문자열

        Returns:
            성공 시 payload dict, 실패 시 None
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            # 토큰 만료
            return None
        except jwt.InvalidTokenError:
            # 유효하지 않은 토큰
            return None

    def create_token(
        self, user_id: str, role: str | None = None, expires_in_minutes: int = 60
    ) -> str:
        """
        JWT 토큰 생성

        Args:
            user_id: 사용자 ID
            role: 사용자 역할 (선택적)
            expires_in_minutes: 만료 시간 (분 단위)

        Returns:
            JWT 토큰 문자열
        """
        payload = {
            "user_id": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes),
        }
        if role:
            payload["role"] = role

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
