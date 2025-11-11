from app.users.application.exceptions import UnauthorizedException, UserNotFoundException
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from pydantic import BaseModel

from app.users.application.dtos import UsuarioResponseDTO
from app.users.application.use_cases.listar_usuarios_use_case import ListarUsuariosUseCase
from app.users.application.use_cases.ver_mi_perfil_use_case import VerMiPerfilUseCase
from app.users.application.use_cases.ver_perfil_otro_usuario_use_case import VerPerfilOtroUsuarioUseCase
from app.users.application.use_cases.aprobar_usuario_use_case import AprobarUsuarioUseCase
from app.users.application.use_cases.rechazar_usuario_use_case import RechazarUsuarioUseCase
from app.users.application.use_cases.activar_desactivar_usuario_use_case import ActivarDesactivarUsuarioUseCase
from app.users.application.use_cases.modificar_roles_use_case import ModificarRolesUseCase
from app.users.application.use_cases.eliminar_usuario_use_case import EliminarUsuarioUseCase
from app.users.application.use_cases.forzar_reseteo_use_case import ForzarReseteoUseCase
from asyncpg.exceptions import ForeignKeyViolationError

from app.users.infrastructure.postgres_user_repository import PostgresUserRepository
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_email_service
from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from app.users.application.policies.user_policy import UserPolicy
from app.core.services.i_email_service import IEmailService

from app.users.infrastructure.postgres_token_repository import PostgresTokenRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.infrastructure.security.argon2_password_hasher import Argon2PasswordHasher
import typing

router = APIRouter(prefix="/admin/users", tags=["admin"])

class StatusUpdate(BaseModel):
    esta_activo: bool

class RolesUpdate(BaseModel):
    rol: str

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.rol != Rol.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

def get_listar_usuarios_use_case(
    db_connection: typing.Any = Depends(get_db),
) -> ListarUsuariosUseCase:
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return ListarUsuariosUseCase(user_repository, user_policy)

@router.get("", response_model=List[UsuarioResponseDTO])
async def list_users(
    admin_user: User = Depends(get_admin_user),
    use_case: ListarUsuariosUseCase = Depends(get_listar_usuarios_use_case)
):
    response_dto = await use_case.execute(admin_user)
    return response_dto.usuarios

def get_ver_perfil_usuario_use_case(
    db_connection: typing.Any = Depends(get_db),
) -> VerMiPerfilUseCase:
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return VerMiPerfilUseCase(user_repository, user_policy)

def get_ver_perfil_otro_usuario_use_case(
    db_connection: typing.Any = Depends(get_db),
) -> VerPerfilOtroUsuarioUseCase:
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return VerPerfilOtroUsuarioUseCase(user_repository, user_policy)

@router.get("/{user_id}", response_model=UsuarioResponseDTO)
async def get_user_profile(
    user_id: UUID,
    admin_user: User = Depends(get_admin_user),
    use_case: VerPerfilOtroUsuarioUseCase = Depends(get_ver_perfil_otro_usuario_use_case)
):
    try:
        return await use_case.execute(admin_user, user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

def get_aprobar_usuario_use_case(
    db_connection: typing.Any = Depends(get_db),
    email_service: IEmailService = Depends(get_email_service)
) -> AprobarUsuarioUseCase:
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return AprobarUsuarioUseCase(user_repository, user_policy, email_service)

@router.post("/{user_id}/aprobar", status_code=status.HTTP_200_OK)
async def approve_user(
    user_id: UUID,
    admin_user: User = Depends(get_admin_user),
    use_case: AprobarUsuarioUseCase = Depends(get_aprobar_usuario_use_case)
):
    try:
        await use_case.execute(admin_user, user_id)
        return {"message": "User approved successfully."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

def get_rechazar_usuario_use_case(
    db_connection: typing.Any = Depends(get_db),
    email_service: IEmailService = Depends(get_email_service)
) -> RechazarUsuarioUseCase:
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return RechazarUsuarioUseCase(user_repository, user_policy, email_service)

@router.post("/{user_id}/rechazar", status_code=status.HTTP_200_OK)
async def reject_user(
    user_id: UUID,
    admin_user: User = Depends(get_admin_user),
    use_case: RechazarUsuarioUseCase = Depends(get_rechazar_usuario_use_case)
):
    try:
        await use_case.execute(admin_user, user_id)
        return {"message": "User rejected successfully."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

def get_activar_desactivar_usuario_use_case(
    db_connection: typing.Any = Depends(get_db),
) -> ActivarDesactivarUsuarioUseCase:
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return ActivarDesactivarUsuarioUseCase(user_repository, user_policy)

@router.put("/{user_id}/estado", status_code=status.HTTP_200_OK)
async def set_user_status(
    user_id: UUID,
    status_update: StatusUpdate,
    admin_user: User = Depends(get_admin_user),
    use_case: ActivarDesactivarUsuarioUseCase = Depends(get_activar_desactivar_usuario_use_case)
):
    try:
        await use_case.execute(admin_user, user_id, status_update.esta_activo)
        return {"message": "User status updated successfully."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

def get_modificar_roles_use_case(
    db_connection: typing.Any = Depends(get_db),
) -> ModificarRolesUseCase:
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return ModificarRolesUseCase(user_repository, user_policy)

@router.put("/{user_id}/roles", status_code=status.HTTP_200_OK)
async def modify_roles(
    user_id: UUID,
    roles_update: RolesUpdate,
    admin_user: User = Depends(get_admin_user),
    use_case: ModificarRolesUseCase = Depends(get_modificar_roles_use_case)
):
    try:
        await use_case.execute(admin_user, user_id, roles_update.rol)
        return {"message": "User roles updated successfully."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
def get_eliminar_usuario_use_case(
    db_connection: typing.Any = Depends(get_db),
) -> EliminarUsuarioUseCase:
    user_repository = PostgresUserRepository(db_connection)
    user_policy = UserPolicy()
    return EliminarUsuarioUseCase(user_repository, user_policy)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_or_deactivate_user(
    user_id: UUID,
    admin_user: User = Depends(get_admin_user),
    eliminar_use_case: EliminarUsuarioUseCase = Depends(get_eliminar_usuario_use_case),
    toggle_use_case: ActivarDesactivarUsuarioUseCase = Depends(get_activar_desactivar_usuario_use_case)
):
    try:
        # ... (tu lógica de try/except/ForeignKeyViolationError es correcta) ...
        await eliminar_use_case.execute(admin_user, user_id)
    except ForeignKeyViolationError as e:
        if "cuotas_usuario_id_fkey" in str(e) or "pedidos_usuario_id_fkey" in str(e):
            await toggle_use_case.execute(admin_user, user_id, new_status=False)
        else:
            raise HTTPException(status_code=500, detail="apiErrors.databaseConfigurationError")
    except (UnauthorizedException, UserNotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    return 

def get_forzar_reseteo_use_case(
    db_connection: typing.Any = Depends(get_db),
    password_hasher: IPasswordHasher = Depends(Argon2PasswordHasher),
    email_service: IEmailService = Depends(get_email_service)
) -> ForzarReseteoUseCase:
    user_repository = PostgresUserRepository(db_connection)
    token_repository = PostgresTokenRepository(db_connection)
    password_hasher = Argon2PasswordHasher()
    user_policy = UserPolicy()
    return ForzarReseteoUseCase(user_repository, token_repository, password_hasher, user_policy, email_service)

@router.post("/{user_id}/forzar-reseteo", status_code=status.HTTP_200_OK)
async def force_password_reset(
    user_id: UUID,
    admin_user: User = Depends(get_admin_user),
    use_case: ForzarReseteoUseCase = Depends(get_forzar_reseteo_use_case)
):
    try:
        await use_case.execute(admin_user, user_id)
        return {"message": "Password reset forced successfully."}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

