from datetime import datetime, timezone
from uuid import UUID
import hashlib

from app.core.security.i_password_hasher import IPasswordHasher
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.domain.entities import Token, User
from app.users.domain.value_objects import TipoToken, Rol
from app.users.application.exceptions import InvalidTokenException, UserNotFoundException, EmailAlreadyVerifiedException

class ConfirmarEmailUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        token_repository: ITokenRepository,
        password_hasher: IPasswordHasher,
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.password_hasher = password_hasher

    async def execute(self, token_texto_plano: str) -> None:
        hashed_token = hashlib.sha256(token_texto_plano.encode()).hexdigest()
        token = await self.token_repository.buscar_por_hash(hashed_token)
        
        
        if not token or token.tipo_token != TipoToken.VERIFICACION_EMAIL or not token.es_valido or token.fecha_expiracion < datetime.now(timezone.utc):
            if token and token.es_valido:
                token.es_valido = False
                await self.token_repository.actualizar(token)
            raise InvalidTokenException("Invalid or expired token.")

        user = await self.user_repository.buscar_por_id(token.usuario_id)
        if not user:
            token.es_valido = False
            await self.token_repository.actualizar(token)
            raise UserNotFoundException("User not found.")

        if user.email_verificado:
            raise EmailAlreadyVerifiedException("Email already verified.")

        

        user.email_verificado = True
        user.fecha_actualizacion = datetime.now(timezone.utc)
        await self.user_repository.actualizar(user)

        token.es_valido = False
        await self.token_repository.actualizar(token)
