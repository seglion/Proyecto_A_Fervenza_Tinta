from app.users.application.repositories.i_refresh_token_repository import IRefreshTokenRepository

class CerrarSesionUseCase:
    def __init__(self, refresh_token_repository: IRefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository

    async def execute(self, refresh_token: str) -> None:
        await self.refresh_token_repository.invalidar_token(refresh_token)
