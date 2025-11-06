from typing import Any
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.users.application.dtos import RegistrarUsuarioDTO, UsuarioCreadoDTO
from app.users.domain.entities import User, Token
from app.core.security.i_password_hasher import IPasswordHasher
from app.core.services.i_email_service import IEmailService
from app.users.domain.value_objects import TipoToken, Password, Rol
from uuid import uuid4 # For generating UUID for new user
from datetime import datetime, timedelta, timezone
import hashlib
from app.users.application.exceptions import UserAlreadyExistsException
import asyncio

class RegistrarUsuarioUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        email_service: IEmailService,
        token_repository: ITokenRepository
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.email_service = email_service
        self.token_repository = token_repository

    async def execute(self, dto: RegistrarUsuarioDTO) -> UsuarioCreadoDTO:
        existing_user = await self.user_repository.buscar_por_email(dto.email)
        if existing_user:
            raise UserAlreadyExistsException("User with this email already exists.")

        password_vo = Password.create(dto.contrasena)

        hashed_password = self.password_hasher.hash(password_vo.value)

        new_user = User(
            id=uuid4(), 
            email=dto.email,
            contrasena_hasheada=hashed_password,
            nombre=dto.nombre,
            apellidos=dto.apellidos,
            apodo=dto.apodo,
            numero_telefono=dto.numero_telefono,
            rol=Rol(dto.rol) 
        )

        created_user = await self.user_repository.crear(new_user)

        verification_token_value = str(uuid4()) # This will be the plain text token sent in email
        hashed_verification_token = hashlib.sha256(verification_token_value.encode()).hexdigest()
        
        new_token = Token(
            id=uuid4(),
            usuario_id=created_user.id,
            tipo_token=TipoToken.VERIFICACION_EMAIL,
            hash_token=hashed_verification_token,
            fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=24) # Token valid for 24 hours
        )
        await self.token_repository.crear(new_token)

        await asyncio.to_thread(self.email_service.send_verification_email, created_user.email, created_user.nombre, verification_token_value)

        return UsuarioCreadoDTO(id=created_user.id, email=created_user.email)
