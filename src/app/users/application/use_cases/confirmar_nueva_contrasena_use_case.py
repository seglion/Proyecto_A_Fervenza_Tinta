from app.users.application.repositories.i_token_repository import ITokenRepository
from app.users.application.repositories.i_user_repository import IUserRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.users.domain.entities import Token
from app.users.domain.value_objects import TipoToken
from datetime import datetime, timezone

class ConfirmarNuevaContrasenaUseCase:
    def __init__(
        self,
        token_repository: ITokenRepository,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher
    ):
        self.token_repository = token_repository
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    async def execute(self, plain_token: str, new_plain_password: str) -> None:
        hashed_token = self.password_hasher.hash(plain_token)
        token = await self.token_repository.buscar_por_hash(hashed_token)

        if not token or token.tipo_token != TipoToken.RESETEO_CONTRASENA or not token.es_valido or token.fecha_expiracion < datetime.now(timezone.utc):
            raise ValueError("Invalid or expired token.") # TODO: Specific exception

        user = await self.user_repository.buscar_por_id(token.usuario_id)

        if not user:
            raise ValueError("User not found.") # TODO: Specific exception

        new_hashed_password = self.password_hasher.hash(new_plain_password)
        await self.user_repository.actualizar_contrasena(user.id, new_hashed_password)

        token.es_valido = False
        await self.token_repository.actualizar(token)
