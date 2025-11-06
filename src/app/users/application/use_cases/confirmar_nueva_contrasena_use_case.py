from app.users.application.repositories.i_token_repository import ITokenRepository
from app.users.application.repositories.i_user_repository import IUserRepository
from app.core.security.i_password_hasher import IPasswordHasher

from app.users.domain.value_objects import TipoToken, Password
from datetime import datetime, timezone
import hashlib


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

    async def execute(self, token_texto_plano: str, nueva_contrasena_str: str) -> None:
        try:
            hashed_token = hashlib.sha256(token_texto_plano.encode()).hexdigest()
            token = await self.token_repository.buscar_por_hash(hashed_token)

            if not token or token.tipo_token != TipoToken.RESETEO_CONTRASENA or not token.es_valido or token.fecha_expiracion < datetime.now(timezone.utc):
                if token and token.es_valido:
                    token.es_valido = False
                    await self.token_repository.actualizar(token)
                raise ValueError("Invalid or expired token.")

            user = await self.user_repository.buscar_por_id(token.usuario_id)
            if not user:
                token.es_valido = False
                await self.token_repository.actualizar(token)
                raise ValueError("User not found.")

            password_vo = Password.create(nueva_contrasena_str)

            try:
                hashed_new_password = self.password_hasher.hash(password_vo.value)
            except Exception as e:
                raise ValueError(f"Error hashing new password: {e}")

            await self.user_repository.actualizar_contrasena(user.id, hashed_new_password)

            token.es_valido = False
            await self.token_repository.actualizar(token)
        except Exception as e:
            raise ValueError(f"An unexpected error occurred during password reset confirmation: {e}")
