from abc import ABC, abstractmethod
from typing import Tuple
from uuid import UUID

class IJWTService(ABC):
    @abstractmethod
    def generar_tokens(self, user_id: UUID, roles: list[str]) -> Tuple[str, str]:
        pass

    @abstractmethod
    def validar_access_token(self, token: str) -> UUID:
        pass

    @abstractmethod
    def validar_refresh_token(self, token: str) -> UUID:
        pass
