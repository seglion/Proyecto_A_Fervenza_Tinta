from app.core.services.i_jwt_service import IJWTService
from typing import Tuple
from uuid import UUID
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

class JWTService(IJWTService):
    def __init__(self, secret_key: str, algorithm: str, access_token_expire_minutes: int, refresh_token_expire_days: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def generar_tokens(self, user_id: UUID, roles: list[str]) -> Tuple[str, str]:
        access_token_expires = timedelta(minutes=self.access_token_expire_minutes)
        refresh_token_expires = timedelta(days=self.refresh_token_expire_days)
        
        access_token = self._create_token(
            data={"sub": str(user_id), "roles": roles, "type": "access"},
            expires_delta=access_token_expires
        )
        
        refresh_token = self._create_token(
            data={"sub": str(user_id), "type": "refresh"},
            expires_delta=refresh_token_expires
        )
        
        return access_token, refresh_token

    def validar_access_token(self, token: str) -> UUID:
        return self._decode_token(token, expected_type="access")

    def validar_refresh_token(self, token: str) -> UUID:
        return self._decode_token(token, expected_type="refresh")

    def _create_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def _decode_token(self, token: str, expected_type: str) -> UUID:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != expected_type:
                raise ValueError("Invalid token type")
            user_id = payload.get("sub")
            if user_id is None:
                raise ValueError("Invalid token")
            return UUID(user_id)
        except JWTError:
            raise ValueError("Invalid token")
