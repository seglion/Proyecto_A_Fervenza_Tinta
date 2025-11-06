from uuid import UUID
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.domain.entities import User
from app.users.application.exceptions import UnauthorizedException

class EliminarUsuarioUseCase:
    def __init__(self, user_repository: IUserRepository, user_policy: UserPolicy):
        self.user_repository = user_repository
        self.user_policy = user_policy

    async def execute(self, admin_user: User, user_id: UUID) -> None:
        if not self.user_policy.es_administrador(admin_user):
            raise UnauthorizedException("Not authorized to delete users.")

        await self.user_repository.eliminar_por_id(user_id)