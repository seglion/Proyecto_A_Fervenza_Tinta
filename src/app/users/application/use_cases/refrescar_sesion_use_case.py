from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.core.services.i_jwt_service import IJWTService
from app.core.security.i_password_hasher import IPasswordHasher
from app.users.application.dtos.tokens_dto import TokensDTO
from app.users.domain.entities import User, Token
from app.users.domain.value_objects import TipoToken
from datetime import datetime, timedelta, timezone
import hashlib
from uuid import uuid4

class RefrescarSesionUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        jwt_service: IJWTService,
        token_repository: ITokenRepository,
        password_hasher: IPasswordHasher
    ):
        self.user_repository = user_repository
        self.jwt_service = jwt_service
        self.token_repository = token_repository
        self.password_hasher = password_hasher

    async def execute(self, refresh_token: str) -> TokensDTO:
        user_id = self.jwt_service.validar_refresh_token(refresh_token)

        user = await self.user_repository.buscar_por_id(user_id)

        if not user or not user.esta_activo:
            raise ValueError("Invalid token or inactive user.") # TODO: Specific exception

        # Invalidate the old refresh token
        hashed_old_refresh_token = hashlib.sha256(refresh_token.encode()).hexdigest()
        await self.token_repository.invalidar_token(hashed_old_refresh_token)

        access_token, new_refresh_token = self.jwt_service.generar_tokens(user.id, [user.rol.value])

        # Store the new refresh token in the database
        hashed_new_refresh_token = hashlib.sha256(new_refresh_token.encode()).hexdigest()
        new_token_entity = Token(
            id=uuid4(),
            usuario_id=user.id,
            tipo_token=TipoToken.REFRESH_TOKEN,
            hash_token=hashed_new_refresh_token,
            fecha_expiracion=datetime.now(timezone.utc) + timedelta(days=7), # Refresh token valid for 7 days
            es_valido=True
        )
        await self.token_repository.crear(new_token_entity)

        return TokensDTO(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )