from abc import ABC, abstractmethod

class IRefreshTokenRepository(ABC):
    @abstractmethod
    async def invalidar_token(self, refresh_token: str) -> None:
        pass
