from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.dtos import UsuarioResponseDTO
from app.users.application.policies.user_policy import UserPolicy
from app.users.domain.entities import User
from uuid import UUID
from app.users.application.exceptions import UnauthorizedException, UserNotFoundException

class VerMiPerfilUseCase:
    def __init__(self, user_repository: IUserRepository, user_policy: UserPolicy):
        self.user_repository = user_repository
        self.user_policy = user_policy

    async def execute(self, current_user: User, target_user_id: UUID) -> UsuarioResponseDTO:
        if not self.user_policy.ver_perfil(current_user, target_user_id):
            raise UnauthorizedException("Not authorized to view this profile.")

        user = await self.user_repository.buscar_por_id(target_user_id)

        if not user:
            raise UserNotFoundException("User not found.")

        return UsuarioResponseDTO(
            id=user.id,
            email=user.email,
            nombre=user.nombre,
            apellidos=user.apellidos,
            apodo=user.apodo,
            numero_telefono=user.numero_telefono,
            url_avatar=user.url_avatar,
            esta_activo=user.esta_activo,
            rol= user.rol,
            email_verificado=user.email_verificado,
            aprobado_por_admin=user.aprobado_por_admin
        )
