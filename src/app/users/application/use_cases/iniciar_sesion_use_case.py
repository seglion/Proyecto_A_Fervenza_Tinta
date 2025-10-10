from app.users.application.repositories.i_user_repository import IUserRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.core.services.i_jwt_service import IJWTService
from app.users.application.dtos import TokensDTO

class IniciarSesionUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        jwt_service: IJWTService
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_service = jwt_service

    async def execute(self, email: str, password: str) -> TokensDTO:
        user = await self.user_repository.buscar_por_email(email)

        if not user or not self.password_hasher.verify(password, user.contrasena_hasheada):
            raise ValueError("Invalid credentials.") # TODO: Specific exception

        if not user.email_verificado:
            raise ValueError("Email not verified.") # TODO: Specific exception

        if not user.esta_activo:
            raise ValueError("User account is inactive.") # TODO: Specific exception

        # Assuming roles are fetched with the user or can be retrieved separately
        # For now, we'll pass an empty list of roles
        access_token, refresh_token = self.jwt_service.generar_tokens(user.id, [])

        return TokensDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
