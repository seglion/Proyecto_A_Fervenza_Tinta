from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.core.services.i_email_service import IEmailService
from app.users.domain.entities import User, Token
from app.users.domain.value_objects import TipoToken
from uuid import uuid4
from datetime import datetime, timedelta, timezone
import asyncio

class SolicitarReseteoContrasenaUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        token_repository: ITokenRepository,
        password_hasher: IPasswordHasher,
        email_service: IEmailService
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.password_hasher = password_hasher
        self.email_service = email_service

    async def execute(self, email: str) -> None:
        user = await self.user_repository.buscar_por_email(email)

        if not user:
            # Return silently to prevent email enumeration
            return

        # Invalidate existing password reset tokens for this user
        await self.token_repository.invalidar_tokens_por_usuario_y_tipo(user.id, TipoToken.RESETEO_CONTRASENA)

        # Generate new password reset token
        plain_token_value = str(uuid4())
        hashed_reset_token = self.password_hasher.hash(plain_token_value)
        
        new_token = Token(
            id=uuid4(),
            usuario_id=user.id,
            tipo_token=TipoToken.RESETEO_CONTRASENA,
            hash_token=hashed_reset_token,
            fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1) # Token valid for 1 hour
        )
        await self.token_repository.crear(new_token)

        await asyncio.to_thread(self.email_service.send_reset_password_email, user.email, plain_token_value)
