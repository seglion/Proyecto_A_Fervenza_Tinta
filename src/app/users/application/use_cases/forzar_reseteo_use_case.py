from uuid import UUID, uuid4
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.users.application.policies.user_policy import UserPolicy
from app.core.services.i_email_service import IEmailService
from app.users.domain.entities import User, Token
from app.users.domain.value_objects import TipoToken
from datetime import datetime, timedelta, timezone
import hashlib
from app.users.application.exceptions import UnauthorizedException, UserNotFoundException

class ForzarReseteoUseCase:
    def __init__(self, user_repository: IUserRepository, token_repository: ITokenRepository, password_hasher: IPasswordHasher, user_policy: UserPolicy, email_service: IEmailService):
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.password_hasher = password_hasher
        self.user_policy = user_policy
        self.email_service = email_service

    async def execute(self, admin_user: User, user_id: UUID) -> None:
        if not self.user_policy.es_administrador(admin_user):
            raise UnauthorizedException("Not authorized to force password reset.")

        user = await self.user_repository.buscar_por_id(user_id)

        if not user:
            raise UserNotFoundException("User not found.")

        plain_token_value = str(uuid4())
        hashed_reset_token = hashlib.sha256(plain_token_value.encode()).hexdigest()
        
        new_token = Token(
            id=uuid4(),
            usuario_id=user.id,
            tipo_token=TipoToken.RESETEO_CONTRASENA,
            hash_token=hashed_reset_token,
            fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1) # Token valid for 1 hour
        )
        await self.token_repository.crear(new_token)

        await self.email_service.send_reset_password_email(user.email, plain_token_value)