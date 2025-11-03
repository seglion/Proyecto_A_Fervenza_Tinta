from datetime import datetime
from uuid import UUID, uuid4

from src.app.prendas.application.dtos import AnadirVarianteDTO, UsuarioPolicyDTO, VarianteCreadaDTO
from src.app.prendas.application.exceptions import NotAuthorizedError, PrendaNotFoundError
from src.app.prendas.application.policies.prenda_policy import PrendaPolicy
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.prendas.application.repositories.i_variante_prenda_repository import IVariantePrendaRepository
from src.app.prendas.domain.entities import VariantePrenda


class AnadirVarianteUseCase:
    def __init__(self, prenda_repository: IPrendaRepository, variante_prenda_repository: IVariantePrendaRepository, prenda_policy: PrendaPolicy):
        self.prenda_repository = prenda_repository
        self.variante_prenda_repository = variante_prenda_repository
        self.prenda_policy = prenda_policy

    async def execute(self, prenda_id: UUID, data: AnadirVarianteDTO, current_user: UsuarioPolicyDTO) -> VarianteCreadaDTO:
        if not self.prenda_policy.es_administrador(current_user):
            raise NotAuthorizedError("No tienes permiso para añadir variantes a una prenda.")

        prenda = await self.prenda_repository.get_by_id(prenda_id)
        if not prenda:
            raise PrendaNotFoundError("Prenda no encontrada.")

        variante_prenda = VariantePrenda(
            id=uuid4(),
            prenda_id=prenda_id,
            genero=data.genero,
            talla=data.talla,
            fecha_creacion=datetime.now()
        )

        variante_creada = await self.variante_prenda_repository.save(variante_prenda)
        return VarianteCreadaDTO(id=variante_creada.id)
