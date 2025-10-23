from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.core.services.i_email_service import IEmailService
from app.users.domain.entities import User, Token
from app.users.domain.value_objects import TipoToken
from uuid import uuid4
from datetime import datetime, timedelta, timezone
import hashlib
import asyncio

class ReenviarEmailUseCase:
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

        if not user or user.email_verificado:
            # Return silently to prevent email enumeration
            return

        # Invalidate existing verification tokens for this user
        await self.token_repository.invalidar_tokens_por_usuario_y_tipo(user.id, TipoToken.VERIFICACION_EMAIL)

        # Generate new verification token
        plain_token_value = str(uuid4())
        hashed_verification_token = hashlib.sha256(plain_token_value.encode()).hexdigest()
        
        new_token = Token(
            id=uuid4(),
            usuario_id=user.id,
            tipo_token=TipoToken.VERIFICACION_EMAIL,
            hash_token=hashed_verification_token,
            fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=24)
        )
        await self.token_repository.crear(new_token)

        await asyncio.to_thread(self.email_service.send_verification_email, user.email, user.nombre, plain_token_value)
