from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.core.services.i_jwt_service import IJWTService
from app.users.application.dtos import IniciarSesionDTO
from app.users.application.dtos.tokens_dto import TokensDTO
from app.users.domain.entities import Token
from app.users.domain.value_objects import TipoToken
from datetime import datetime, timedelta, timezone
import hashlib
from uuid import uuid4
from app.users.application.exceptions import InvalidCredentialsException, EmailNotVerifiedException, AccountInactiveException

class IniciarSesionUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        jwt_service: IJWTService,
        token_repository: ITokenRepository
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_service = jwt_service
        self.token_repository = token_repository

    async def execute(self, dto: IniciarSesionDTO) -> TokensDTO:
        user = await self.user_repository.buscar_por_email(dto.email)

        if not user or not self.password_hasher.verify(dto.contrasena, user.contrasena_hasheada):
            raise InvalidCredentialsException("Invalid credentials.")

        if not user.email_verificado:
            raise EmailNotVerifiedException("Email not verified.")

        if not user.esta_activo:
            raise AccountInactiveException("Account is inactive.")

        access_token, refresh_token = self.jwt_service.generar_tokens(user.id, [user.rol.value])

        # Store refresh token in the database
        hashed_refresh_token = hashlib.sha256(refresh_token.encode()).hexdigest()
        new_token = Token(
            id=uuid4(), # Generate a new UUID for the token
            usuario_id=user.id,
            tipo_token=TipoToken.REFRESH_TOKEN,
            hash_token=hashed_refresh_token,
            fecha_expiracion=datetime.now(timezone.utc) + timedelta(days=7), # Refresh token valid for 7 days
            es_valido=True
        )
        await self.token_repository.crear(new_token)

        return TokensDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
