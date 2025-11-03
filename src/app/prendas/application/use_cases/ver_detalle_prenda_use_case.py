from uuid import UUID
from typing import List

from src.app.prendas.application.dtos import PrendaDetalleDTO, VariantePrendaDTO
from src.app.prendas.application.exceptions import PrendaNotFoundError
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository


class VerDetallePrendaUseCase:
    def __init__(self, prenda_repository: IPrendaRepository):
        self.prenda_repository = prenda_repository

    async def execute(self, prenda_id: UUID) -> PrendaDetalleDTO:
        prenda = await self.prenda_repository.get_by_id_con_variantes(prenda_id)
        if not prenda:
            raise PrendaNotFoundError("Prenda no encontrada.")

        variantes_dto = [
            VariantePrendaDTO(
                id=variante.id,
                prenda_id=variante.prenda_id,
                genero=variante.genero,
                talla=variante.talla,
                fecha_creacion=variante.fecha_creacion
            )
            for variante in prenda.variantes
        ]

        return PrendaDetalleDTO(
            id=prenda.id,
            nombre=prenda.nombre,
            descripcion=prenda.descripcion,
            precio=prenda.precio,
            imagen_url=prenda.imagen_url,
            fecha_creacion=prenda.fecha_creacion,
            variantes=variantes_dto
        )
