from uuid import UUID
from typing import Optional

from src.app.prendas.application.dtos import ActualizarPrendaDTO, PrendaActualizadaDTO, UsuarioPolicyDTO
from src.app.prendas.application.exceptions import NotAuthorizedError, PrendaNotFoundError
from src.app.prendas.application.policies.prenda_policy import PrendaPolicy
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository


class ActualizarPrendaUseCase:
    def __init__(self, prenda_repository: IPrendaRepository, prenda_policy: PrendaPolicy):
        self.prenda_repository = prenda_repository
        self.prenda_policy = prenda_policy

    async def execute(self, prenda_id: UUID, data: ActualizarPrendaDTO, current_user: UsuarioPolicyDTO) -> PrendaActualizadaDTO:
        if not self.prenda_policy.es_administrador(current_user):
            raise NotAuthorizedError("No tienes permiso para actualizar una prenda.")

        prenda = await self.prenda_repository.get_by_id(prenda_id)
        if not prenda:
            raise PrendaNotFoundError("Prenda no encontrada.")

        if data.nombre is not None:
            prenda.nombre = data.nombre
        if data.descripcion is not None:
            prenda.descripcion = data.descripcion
        if data.precio is not None:
            prenda.precio = data.precio
        if data.imagen_url is not None:
            prenda.imagen_url = data.imagen_url

        await self.prenda_repository.save(prenda)
        return PrendaActualizadaDTO(id=prenda.id)
