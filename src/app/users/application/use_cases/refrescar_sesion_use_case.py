from app.users.application.repositories.i_user_repository import IUserRepository
from app.core.services.i_jwt_service import IJWTService
from app.users.application.dtos import TokensDTO

class RefrescarSesionUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        jwt_service: IJWTService
    ):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def execute(self, refresh_token: str) -> TokensDTO:
        user_id = self.jwt_service.validar_refresh_token(refresh_token)
        user = await self.user_repository.buscar_por_id(user_id)

        if not user or not user.esta_activo:
            raise ValueError("Invalid token or inactive user.") # TODO: Specific exception

        # Assuming roles are fetched with the user or can be retrieved separately
        # For now, we'll pass an empty list of roles
        new_access_token, _ = self.jwt_service.generar_tokens(user.id, [])

        return TokensDTO(
            access_token=new_access_token,
            refresh_token=refresh_token, # The same refresh token is returned
            token_type="bearer"
        )
