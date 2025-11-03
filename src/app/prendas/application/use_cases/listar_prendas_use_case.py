from typing import List

from src.app.prendas.application.dtos import ListaPrendasDTO, PrendaDTO, VariantePrendaDTO
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository


class ListarPrendasUseCase:
    def __init__(self, prenda_repository: IPrendaRepository):
        self.prenda_repository = prenda_repository

    async def execute(self) -> ListaPrendasDTO:
        prendas = await self.prenda_repository.get_all()
        prendas_dto = []
        for prenda in prendas:
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
            prendas_dto.append(
                PrendaDTO(
                    id=prenda.id,
                    nombre=prenda.nombre,
                    descripcion=prenda.descripcion,
                    precio=prenda.precio,
                    imagen_url=prenda.imagen_url,
                    fecha_creacion=prenda.fecha_creacion,
                    variantes=variantes_dto
                )
            )
        return ListaPrendasDTO(prendas=prendas_dto)
