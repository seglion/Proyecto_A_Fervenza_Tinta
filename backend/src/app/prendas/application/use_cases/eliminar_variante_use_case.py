from uuid import UUID

from src.app.prendas.application.dtos import UsuarioPolicyDTO
from src.app.prendas.application.exceptions import NotAuthorizedError, PrendaNotFoundError
from src.app.prendas.application.policies.prenda_policy import PrendaPolicy
from src.app.prendas.application.repositories.i_variante_prenda_repository import IVariantePrendaRepository
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository


class EliminarVarianteUseCase:
    def __init__(self, prenda_repository: IPrendaRepository, variante_prenda_repository: IVariantePrendaRepository, prenda_policy: PrendaPolicy):
        self.prenda_repository = prenda_repository
        self.variante_prenda_repository = variante_prenda_repository
        self.prenda_policy = prenda_policy

    async def execute(self, prenda_id: UUID, variante_id: UUID, current_user: UsuarioPolicyDTO) -> None:
        user_policy_dto = UsuarioPolicyDTO(rol=current_user.rol.value, esta_activo=current_user.esta_activo)
        if not self.prenda_policy.es_administrador(user_policy_dto):
            raise NotAuthorizedError("No tienes permiso para eliminar una variante de prenda.")

        prenda = await self.prenda_repository.buscar_por_id_con_variantes(prenda_id)
        if not prenda:
            raise PrendaNotFoundError("Prenda no encontrada.")

        variante_prenda = await self.variante_prenda_repository.buscar_por_id(variante_id)
        if not variante_prenda or variante_prenda.prenda_id != prenda_id:
            raise PrendaNotFoundError("Variante de prenda no encontrada para la prenda especificada.")

        await self.variante_prenda_repository.eliminar_por_id(variante_prenda.id)
