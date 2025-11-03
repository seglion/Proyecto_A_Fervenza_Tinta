from uuid import UUID

from src.app.prendas.application.dtos import UsuarioPolicyDTO
from src.app.prendas.application.exceptions import NotAuthorizedError, PrendaNotFoundError
from src.app.prendas.application.policies.prenda_policy import PrendaPolicy
from src.app.prendas.application.repositories.i_variante_prenda_repository import IVariantePrendaRepository


class EliminarVarianteUseCase:
    def __init__(self, variante_prenda_repository: IVariantePrendaRepository, prenda_policy: PrendaPolicy):
        self.variante_prenda_repository = variante_prenda_repository
        self.prenda_policy = prenda_policy

    async def execute(self, variante_id: UUID, current_user: UsuarioPolicyDTO) -> None:
        if not self.prenda_policy.es_administrador(current_user):
            raise NotAuthorizedError("No tienes permiso para eliminar una variante de prenda.")

        variante_prenda = await self.variante_prenda_repository.get_by_id(variante_id)
        if not variante_prenda:
            raise PrendaNotFoundError("Variante de prenda no encontrada.")

        await self.variante_prenda_repository.delete(variante_prenda)
