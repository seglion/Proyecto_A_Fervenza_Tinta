from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.domain.entities import User
from uuid import UUID
from app.users.application.exceptions import UnauthorizedException

class SolicitarEliminacionUseCase:
    def __init__(self, user_repository: IUserRepository, user_policy: UserPolicy):
        self.user_repository = user_repository
        self.user_policy = user_policy

    async def execute(self, current_user: User, target_user_id: UUID) -> None:
        if not self.user_policy.actualizar_perfil(current_user, target_user_id):
            raise UnauthorizedException("Not authorized to delete this account.")

        await self.user_repository.desactivar_cuenta(target_user_id)
