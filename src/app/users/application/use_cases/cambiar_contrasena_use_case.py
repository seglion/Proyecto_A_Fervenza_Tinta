from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.core.security.i_password_hasher import IPasswordHasher
from app.users.application.dtos import CambiarContrasenaDTO
from app.users.domain.entities import User
from app.users.domain.value_objects import Password
from uuid import UUID
from app.users.application.exceptions import UnauthorizedException, UserNotFoundException, InvalidOldPasswordException

class CambiarContrasenaUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        password_hasher: IPasswordHasher,
        user_policy: UserPolicy
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.user_policy = user_policy

    async def execute(self, current_user: User, target_user_id: UUID, dto: CambiarContrasenaDTO) -> None:
        if not self.user_policy.actualizar_perfil(current_user, target_user_id):
            raise UnauthorizedException("Not authorized to change this password.")

        user = await self.user_repository.buscar_por_id(target_user_id)

        if not user:
            raise UserNotFoundException("User not found.")

        if not self.password_hasher.verify(dto.contrasena_antigua, user.contrasena_hasheada):
            raise InvalidOldPasswordException("Invalid old password.")

        # Validate new password using Value Object
        new_password_vo = Password.create(dto.contrasena_nueva)

        new_hashed_password = self.password_hasher.hash(new_password_vo.value)
        await self.user_repository.actualizar_contrasena(user.id, new_hashed_password)
