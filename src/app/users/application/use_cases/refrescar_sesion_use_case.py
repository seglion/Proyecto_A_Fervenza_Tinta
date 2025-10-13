from app.users.application.repositories.i_user_repository import IUserRepository
from app.core.services.i_jwt_service import IJWTService
from app.users.application.dtos import TokensDTO
from app.users.domain.entities import User
from uuid import UUID

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

        access_token, new_refresh_token = self.jwt_service.generar_tokens(user.id, [user.rol.value])

        return TokensDTO(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )