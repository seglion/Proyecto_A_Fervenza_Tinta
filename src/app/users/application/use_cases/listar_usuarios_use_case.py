from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.application.dtos import ListaUsuariosResponseDTO, UsuarioResponseDTO
from app.users.domain.entities import User
from app.users.application.exceptions import UnauthorizedException

class ListarUsuariosUseCase:
    def __init__(self, user_repository: IUserRepository, user_policy: UserPolicy):
        self.user_repository = user_repository
        self.user_policy = user_policy

    async def execute(self, current_user: User) -> ListaUsuariosResponseDTO:
        if not self.user_policy.es_administrador(current_user):
            raise UnauthorizedException("Not authorized to list users.")

        users = await self.user_repository.buscar_todos()

        return ListaUsuariosResponseDTO(
            usuarios=[
                UsuarioResponseDTO(
                    id=user.id,
                    email=user.email,
                    nombre=user.nombre,
                    apellidos=user.apellidos,
                    apodo=user.apodo,
                    numero_telefono=user.numero_telefono,
                    url_avatar=user.url_avatar,
                    esta_activo=user.esta_activo,
                    rol = user.rol.value # Assuming no roles for now
                )
                for user in users
            ]
        )
