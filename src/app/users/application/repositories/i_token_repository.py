from abc import ABC, abstractmethod
from typing import Optional
from app.users.domain.entities import Token

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
