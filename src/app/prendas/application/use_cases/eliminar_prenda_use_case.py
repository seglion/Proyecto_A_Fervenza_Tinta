from uuid import UUID

from src.app.prendas.application.dtos import UsuarioPolicyDTO
from src.app.prendas.application.exceptions import NotAuthorizedError, PrendaNotFoundError
from src.app.prendas.application.policies.prenda_policy import PrendaPolicy
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.users.domain.entities import User # Importar User


class EliminarPrendaUseCase:
    def __init__(self, prenda_repository: IPrendaRepository, prenda_policy: PrendaPolicy):
        self.prenda_repository = prenda_repository
        self.prenda_policy = prenda_policy

    async def execute(self, prenda_id: UUID, current_user: User) -> None:
        user_policy_dto = UsuarioPolicyDTO(rol=current_user.rol.value, esta_activo=current_user.esta_activo)
        if not self.prenda_policy.es_administrador(user_policy_dto):
            raise NotAuthorizedError("No tienes permiso para eliminar una prenda.")

        prenda = await self.prenda_repository.buscar_por_id_con_variantes(prenda_id)
        if not prenda:
            raise PrendaNotFoundError("Prenda no encontrada.")

        await self.prenda_repository.eliminar_por_id(prenda_id)
