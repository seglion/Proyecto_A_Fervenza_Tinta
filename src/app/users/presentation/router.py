from __future__ import annotations

import typing
from unittest.mock import Mock

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from app.users.application.dtos import (
    RegistrarUsuarioDTO, UsuarioCreadoDTO, IniciarSesionDTO,
    UsuarioResponseDTO, ActualizarMiPerfilDTO, CambiarContrasenaDTO,
    ConfirmarNuevaContrasenaDTO
)
from app.users.application.dtos.tokens_dto import TokensDTO


from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.core.services.i_jwt_service import IJWTService
from app.infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
from app.users.infrastructure.postgres_user_repository import PostgresUserRepository
from app.users.infrastructure.postgres_token_repository import PostgresTokenRepository
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.users.infrastructure.postgres_token_repository import PostgresTokenRepository


from app.core.services.email_service import EmailService
from app.infrastructure.security.jwt_service import get_jwt_service
from app.core.database import get_db

from app.core.dependencies import get_current_user
from app.users.domain.entities import User
from app.users.application.policies.user_policy import UserPolicy
from app.users.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase
from app.users.application.use_cases.iniciar_sesion_use_case import IniciarSesionUseCase
from app.users.application.use_cases.confirmar_email_use_case import ConfirmarEmailUseCase

from app.users.application.use_cases.ver_mi_perfil_use_case import VerMiPerfilUseCase
from app.users.application.use_cases.actualizar_mi_perfil_use_case import ActualizarMiPerfilUseCase
from app.users.application.use_cases.cambiar_contrasena_use_case import CambiarContrasenaUseCase
from app.users.application.use_cases.solicitar_eliminacion_use_case import SolicitarEliminacionUseCase
from app.users.application.use_cases.reenviar_email_use_case import ReenviarEmailUseCase
from app.users.application.use_cases.confirmar_nueva_contrasena_use_case import ConfirmarNuevaContrasenaUseCase
from app.users.application.use_cases.refrescar_sesion_use_case import RefrescarSesionUseCase

from app.users.application.use_cases.solicitar_reseteo_contrasena_use_case import SolicitarReseteoContrasenaUseCase

from app.users.application.dtos.tokens_dto import TokensDTO


def get_token_repository(db_connection: typing.Any = Depends(get_db)) -> ITokenRepository:
    return Mock(spec=ITokenRepository)


router = APIRouter(prefix="/users", tags=["users"])

class ReenviarEmailRequest(BaseModel):
    email: EmailStr

class SolicitarReseteoRequest(BaseModel):
    email: EmailStr

class RefrescarSesionRequest(BaseModel):
    refresh_token: str

# Nota: si también defines TokensDTO en app.users.application.dtos, puedes eliminar esta clase local.

def get_registrar_usuario_use_case(
    db_connection: typing.Any = Depends(get_db),
    password_hasher: IPasswordHasher = Depends(Argon2PasswordHasher),
) -> "RegistrarUsuarioUseCase":
    # import local para evitar importación circular / side-effects en import time


    user_repository = PostgresUserRepository(db_connection)
    token_repository = PostgresTokenRepository(db_connection)
    email_service = EmailService()
    return RegistrarUsuarioUseCase(user_repository, password_hasher, email_service, token_repository)

@router.post("/register", response_model=UsuarioCreadoDTO, status_code=status.HTTP_201_CREATED)
async def register_user(
    dto: RegistrarUsuarioDTO,
    use_case: "RegistrarUsuarioUseCase" = Depends(get_registrar_usuario_use_case)
):
    # Temporarily removed try-except block for debugging
    return await use_case.execute(dto)

def get_iniciar_sesion_use_case(
    db_connection: typing.Any = Depends(get_db),
    password_hasher: IPasswordHasher = Depends(Argon2PasswordHasher),
    jwt_service: IJWTService = Depends(get_jwt_service),
    token_repository: ITokenRepository = Depends(get_token_repository),
) -> "IniciarSesionUseCase":
    # import local para evitar importaciones circulares
    from app.users.application.use_cases.iniciar_sesion_use_case import IniciarSesionUseCase
    user_repository = PostgresUserRepository(db_connection)
    return IniciarSesionUseCase(user_repository, password_hasher, jwt_service, token_repository)


def get_confirmar_email_use_case(
    db_connection: typing.Any = Depends(get_db),
    password_hasher: IPasswordHasher = Depends(Argon2PasswordHasher),
) -> "ConfirmarEmailUseCase":

    user_repository = PostgresUserRepository(db_connection)
    token_repository = PostgresTokenRepository(db_connection)
    return ConfirmarEmailUseCase(user_repository, token_repository, password_hasher)

@router.get("/verificar-email", status_code=status.HTTP_200_OK)
async def confirmar_email(
    token: str,
    use_case: "ConfirmarEmailUseCase" = Depends(get_confirmar_email_use_case)
):
    try:
        await use_case.execute(token)
        return {"message": "Email verified successfully."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

def get_ver_mi_perfil_use_case(
    db_connection: typing.Any = Depends(get_db),
) -> "VerMiPerfilUseCase":
    
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return VerMiPerfilUseCase(user_repository, user_policy)

@router.get("/me", response_model=UsuarioResponseDTO, status_code=status.HTTP_200_OK)
async def ver_mi_perfil(
    current_user: User = Depends(get_current_user),
    use_case: "VerMiPerfilUseCase" = Depends(get_ver_mi_perfil_use_case)
):
    try:
        return await use_case.execute(current_user, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

def get_actualizar_mi_perfil_use_case(
    db_connection: typing.Any = Depends(get_db),
) -> "ActualizarMiPerfilUseCase":
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return ActualizarMiPerfilUseCase(user_repository, user_policy)

@router.put("/me", response_model=UsuarioResponseDTO, status_code=status.HTTP_200_OK)
async def actualizar_mi_perfil(
    dto: ActualizarMiPerfilDTO,
    current_user: User = Depends(get_current_user),
    use_case: "ActualizarMiPerfilUseCase" = Depends(get_actualizar_mi_perfil_use_case)
):
    try:
        return await use_case.execute(current_user, current_user.id, dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
 
def get_cambiar_contrasena_use_case(
    db_connection: typing.Any = Depends(get_db),
    password_hasher: IPasswordHasher = Depends(Argon2PasswordHasher),
) -> "CambiarContrasenaUseCase":
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return CambiarContrasenaUseCase(user_repository, password_hasher, user_policy)

@router.put("/me/password", status_code=status.HTTP_200_OK)
async def cambiar_contrasena(
    dto: CambiarContrasenaDTO,
    current_user: User = Depends(get_current_user),
    use_case: "CambiarContrasenaUseCase" = Depends(get_cambiar_contrasena_use_case)
):
    try:
        await use_case.execute(current_user, current_user.id, dto)
        return {"message": "Password updated successfully."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

def get_solicitar_eliminacion_use_case(
    db_connection: typing.Any = Depends(get_db),
) -> "SolicitarEliminacionUseCase":
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return SolicitarEliminacionUseCase(user_repository, user_policy)

@router.delete("/me", status_code=status.HTTP_200_OK)
async def solicitar_eliminacion(
    current_user: User = Depends(get_current_user),
    use_case: "SolicitarEliminacionUseCase" = Depends(get_solicitar_eliminacion_use_case)
):
    try:
        await use_case.execute(current_user, current_user.id)
        return {"message": "Deletion request sent successfully."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

def get_reenviar_email_use_case(
    db_connection: typing.Any = Depends(get_db),
    password_hasher: IPasswordHasher = Depends(Argon2PasswordHasher),
) -> "ReenviarEmailUseCase":

    user_repository = PostgresUserRepository(db_connection)
    token_repository = PostgresTokenRepository(db_connection)
    email_service = EmailService()
    return ReenviarEmailUseCase(user_repository, token_repository, password_hasher, email_service)

@router.post("/reenviar-verificacion", status_code=status.HTTP_200_OK)
async def reenviar_email_verificacion(
    request: ReenviarEmailRequest,
    use_case: "ReenviarEmailUseCase" = Depends(get_reenviar_email_use_case)
):
    try:
        await use_case.execute(request.email)
        return {"message": "Verification email sent."}
    except Exception:
        # To prevent user enumeration, always return a success message
        return {"message": "Verification email sent."}
def get_solicitar_reseteo_contrasena_use_case(
    db_connection: typing.Any = Depends(get_db),
    password_hasher: IPasswordHasher = Depends(Argon2PasswordHasher),
) -> "SolicitarReseteoContrasenaUseCase":

    user_repository = PostgresUserRepository(db_connection)
    token_repository = PostgresTokenRepository(db_connection)
    email_service = EmailService()
    return SolicitarReseteoContrasenaUseCase(user_repository, token_repository, email_service, password_hasher)

@router.post("/solicitar-reseteo", status_code=status.HTTP_200_OK)
async def solicitar_reseteo_contrasena(
    request: SolicitarReseteoRequest,
    use_case: "SolicitarReseteoContrasenaUseCase" = Depends(get_solicitar_reseteo_contrasena_use_case)
):
    try:
        await use_case.execute(request.email)
        return {"message": "Password reset email sent."}
    except Exception:
        # To prevent user enumeration, always return a success message
        return {"message": "Password reset email sent."}

def get_confirmar_nueva_contrasena_use_case(
    db_connection: typing.Any = Depends(get_db),
    password_hasher: IPasswordHasher = Depends(Argon2PasswordHasher),
) -> "ConfirmarNuevaContrasenaUseCase":
    
    user_repository = PostgresUserRepository(db_connection)
    token_repository = PostgresTokenRepository(db_connection)
    return ConfirmarNuevaContrasenaUseCase(token_repository, user_repository, password_hasher)

@router.post("/confirmar-reseteo", status_code=status.HTTP_200_OK)
async def confirmar_nueva_contrasena(
    dto: ConfirmarNuevaContrasenaDTO,
    use_case: "ConfirmarNuevaContrasenaUseCase" = Depends(get_confirmar_nueva_contrasena_use_case)
):
    try:
        await use_case.execute(dto.token, dto.nueva_contrasena)
        return {"message": "Password has been reset successfully."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
def get_refrescar_sesion_use_case(
    db_connection: typing.Any = Depends(get_db),
    jwt_service: IJWTService = Depends(get_jwt_service),
    token_repository: ITokenRepository = Depends(get_token_repository),
    password_hasher: IPasswordHasher = Depends(Argon2PasswordHasher),
) -> "RefrescarSesionUseCase":
    from app.users.application.use_cases.refrescar_sesion_use_case import RefrescarSesionUseCase
    user_repository = PostgresUserRepository(db_connection)
    return RefrescarSesionUseCase(user_repository, jwt_service, token_repository, password_hasher)

@router.post("/auth/refresh", response_model=TokensDTO, status_code=status.HTTP_200_OK)
async def refrescar_sesion(
    request: RefrescarSesionRequest,
    use_case: RefrescarSesionUseCase = Depends(get_refrescar_sesion_use_case)
) -> TokensDTO:
    try:
        return await use_case.execute(request.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
@router.post("/auth/token", response_model=TokensDTO, status_code=status.HTTP_200_OK)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: IniciarSesionUseCase = Depends(get_iniciar_sesion_use_case)
) -> TokensDTO:
    dto = IniciarSesionDTO(email=form_data.username, contrasena=form_data.password)
    try:
        return await use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
