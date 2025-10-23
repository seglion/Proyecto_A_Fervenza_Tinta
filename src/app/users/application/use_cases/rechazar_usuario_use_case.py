from uuid import UUID
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.core.services.i_email_service import IEmailService
from app.users.domain.entities import User
from app.users.application.exceptions import UnauthorizedException, UserNotFoundException, UserAlreadyApprovedException

class RechazarUsuarioUseCase:
    def __init__(self, user_repository: IUserRepository, user_policy: UserPolicy, email_service: IEmailService):
        self.user_repository = user_repository
        self.user_policy = user_policy
        self.email_service = email_service

    async def execute(self, admin_user: User, user_id: UUID) -> None:
        if not self.user_policy.es_administrador(admin_user):
            raise UnauthorizedException("Not authorized to reject users.")

        user = await self.user_repository.buscar_por_id(user_id)

        if not user:
            raise UserNotFoundException("User not found.")

        if user.aprobado_por_admin:
            raise UserAlreadyApprovedException("User is already approved.")

        await self.user_repository.eliminar_por_id(user_id)
        await self.email_service.enviar_email_rechazo(user.email)
