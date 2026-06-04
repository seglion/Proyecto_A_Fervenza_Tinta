from fastapi import Depends, HTTPException, status
from app.core.security.oauth2 import oauth2_scheme
from app.core.services.i_jwt_service import IJWTService
from app.users.domain.entities import User
from app.users.infrastructure.postgres_user_repository import PostgresUserRepository
from app.infrastructure.security.jwt_service import get_jwt_service
from app.core.database import get_db
import typing

from app.core.services.i_email_service import IEmailService
from app.core.services.sendgrid_email_service import SendgridEmailService
from app.core.services.i_storage_service import IStorageService
from app.core.services.minio_storage_service import MinioStorageService
from app.core.config import settings as _settings


def get_storage_service() -> IStorageService:
    return MinioStorageService(_settings)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    jwt_service: IJWTService = Depends(get_jwt_service),
    db_connection: typing.Any = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = jwt_service.validar_access_token(token)
    except ValueError:
        raise credentials_exception

    user_repository = PostgresUserRepository(db_connection)
    user = await user_repository.buscar_por_id(user_id)
    if user is None:
        raise credentials_exception
    if not user.esta_activo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    if not user.email_verificado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not verified")

    return user


def get_email_service() -> IEmailService:
    return SendgridEmailService()
