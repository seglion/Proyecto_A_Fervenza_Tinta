from app.users.application.repositories.i_token_repository import ITokenRepository
from app.core.security.i_password_hasher import IPasswordHasher
import hashlib

class CerrarSesionUseCase:
    def __init__(self, token_repository: ITokenRepository, password_hasher: IPasswordHasher):
        self.token_repository = token_repository
        self.password_hasher = password_hasher

    async def execute(self, refresh_token: str) -> None:
        hashed_refresh_token = self.password_hasher.hash(refresh_token)
        await self.token_repository.invalidar_token(hashed_refresh_token)
