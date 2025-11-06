from uuid import UUID
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.application.dtos import UsuarioResponseDTO
from app.users.domain.entities import User
from app.users.application.exceptions import UnauthorizedException, UserNotFoundException

class VerPerfilOtroUsuarioUseCase:
    def __init__(self, user_repository: IUserRepository, user_policy: UserPolicy):
        self.user_repository = user_repository
        self.user_policy = user_policy

    async def execute(self, admin_user: User, user_id: UUID) -> UsuarioResponseDTO:
        if not self.user_policy.es_administrador(admin_user):
            raise UnauthorizedException("Not authorized to view other user's profile.")

        user = await self.user_repository.buscar_por_id(user_id)

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
            rol=user.rol.value
        )
