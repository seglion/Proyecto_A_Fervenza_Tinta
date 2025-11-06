from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.users.domain.entities import Token
from app.users.domain.value_objects import TipoToken

class ITokenRepository(ABC):
    @abstractmethod
    async def crear(self, token: Token) -> Token:
        pass

    @abstractmethod
    async def buscar_por_hash(self, hash_token: str) -> Optional[Token]:
        pass

    @abstractmethod
    async def actualizar(self, token: Token) -> Token:
        pass

    @abstractmethod
    async def invalidar_token(self, refresh_token_hash: str) -> None:
        pass

    @abstractmethod
    async def invalidar_tokens_por_usuario_y_tipo(self, user_id: UUID, token_type: TipoToken) -> None:
        pass