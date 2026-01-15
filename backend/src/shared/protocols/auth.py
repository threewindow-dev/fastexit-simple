"""
Authentication protocols.

인증 관련 Protocol 정의 (의존성 역전 원칙 적용)
"""

from typing import Protocol, dict


class TokenManager(Protocol):
    """
    JWT 토큰 생성 및 검증을 담당하는 Protocol
    
    구현체: shared.infra.auth.JWTTokenManager
    """
    
    def verify_token(self, token: str) -> dict | None:
        """
        토큰 검증 및 payload 추출
        
        Args:
            token: JWT 토큰 문자열
            
        Returns:
            성공 시 payload dict, 실패 시 None
            
        Raises:
            jwt.ExpiredSignatureError: 토큰 만료
            jwt.InvalidTokenError: 유효하지 않은 토큰
        """
        ...
    
    def create_token(self, user_id: str, role: str | None = None, 
                    expires_in_minutes: int = 60) -> str:
        """
        JWT 토큰 생성
        
        Args:
            user_id: 사용자 ID
            role: 사용자 역할 (선택적)
            expires_in_minutes: 만료 시간 (분 단위)
            
        Returns:
            JWT 토큰 문자열
        """
        ...
