from uuid import UUID
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from datetime import datetime, timezone
from app.users.application.exceptions import UnauthorizedException, UserNotFoundException

class ModificarRolesUseCase:
    def __init__(self, user_repository: IUserRepository, user_policy: UserPolicy):
        self.user_repository = user_repository
        self.user_policy = user_policy

    async def execute(self, admin_user: User, user_id: UUID, new_rol_str: str) -> None:
        if not self.user_policy.es_administrador(admin_user):
            raise UnauthorizedException("Not authorized to modify roles.")

        user = await self.user_repository.buscar_por_id(user_id)

        if not user:
            raise UserNotFoundException("User not found.")

        # Convert string to Rol enum member
        try:
            new_rol = Rol(new_rol_str.upper())
        except ValueError:
            raise ValueError(f"Invalid role: {new_rol_str}")

        user.rol = new_rol
        user.fecha_actualizacion = datetime.now(timezone.utc)
        await self.user_repository.actualizar(user)