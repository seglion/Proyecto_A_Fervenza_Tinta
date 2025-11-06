import asyncpg
from typing import List, Optional
from uuid import UUID
import inspect

from src.app.prendas.application.repositories.i_variante_prenda_repository import IVariantePrendaRepository
from src.app.prendas.domain.entities import VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda

class PostgresVariantePrendaRepository(IVariantePrendaRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    async def guardar(self, variante_prenda: VariantePrenda) -> VariantePrenda:
        query = inspect.cleandoc("""
            INSERT INTO varianteprendas (id, prenda_id, genero, talla, fecha_creacion)
            VALUES ($1, $2, $3::genero_prenda_enum, $4::talla_prenda_enum, $5)
        """)
        await self.db_connection.execute(
            query,
            variante_prenda.id,
            variante_prenda.prenda_id,
            variante_prenda.genero.value,
            variante_prenda.talla.value,
            variante_prenda.fecha_creacion
        )
        return variante_prenda

    async def eliminar_por_id(self, variante_prenda_id: UUID) -> None:
        query = "DELETE FROM varianteprendas WHERE id = $1"
        await self.db_connection.execute(query, variante_prenda_id)

    async def buscar_por_id(self, variante_prenda_id: UUID) -> Optional[VariantePrenda]:
        query = "SELECT id, prenda_id, genero, talla, fecha_creacion FROM varianteprendas WHERE id = $1"
        row = await self.db_connection.fetchrow(query, variante_prenda_id)
        if row:
            return VariantePrenda(
                id=row['id'],
                prenda_id=row['prenda_id'],
                genero=GeneroPrenda(row['genero']),
                talla=TallaPrenda(row['talla']),
                fecha_creacion=row['fecha_creacion']
            )
        return None

    async def listar_por_prenda_id(self, prenda_id: UUID) -> List[VariantePrenda]:
        query = "SELECT id, prenda_id, genero, talla, fecha_creacion FROM varianteprendas WHERE prenda_id = $1"
        rows = await self.db_connection.fetch(query, prenda_id)
        return [
            VariantePrenda(
                id=row['id'],
                prenda_id=row['prenda_id'],
                genero=GeneroPrenda(row['genero']),
                talla=TallaPrenda(row['talla']),
                fecha_creacion=row['fecha_creacion']
            ) for row in rows
        ]