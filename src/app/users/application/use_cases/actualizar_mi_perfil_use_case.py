from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.application.dtos import ActualizarMiPerfilDTO, UsuarioResponseDTO
from app.users.domain.entities import User
from uuid import UUID
from app.users.application.exceptions import UnauthorizedException, UserNotFoundException

class ActualizarMiPerfilUseCase:
    def __init__(self, user_repository: IUserRepository, user_policy: UserPolicy):
        self.user_repository = user_repository
        self.user_policy = user_policy

    async def execute(self, current_user: User, target_user_id: UUID, dto: ActualizarMiPerfilDTO) -> UsuarioResponseDTO:
        if not self.user_policy.actualizar_perfil(current_user, target_user_id):
            raise UnauthorizedException("Not authorized to update this profile.")

        user = await self.user_repository.buscar_por_id(target_user_id)

        if not user:
            raise UserNotFoundException("User not found.")

        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        updated_user = await self.user_repository.actualizar(user)

        return UsuarioResponseDTO(
            id=updated_user.id,
            email=updated_user.email,
            nombre=updated_user.nombre,
            apellidos=updated_user.apellidos,
            apodo=updated_user.apodo,
            numero_telefono=updated_user.numero_telefono,
            url_avatar=updated_user.url_avatar,
            esta_activo=updated_user.esta_activo,
            rol=updated_user.rol.value, # Assuming no roles for now
        )
