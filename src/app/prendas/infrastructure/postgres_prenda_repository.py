import asyncpg
from typing import List, Optional
from uuid import UUID

from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.prendas.domain.entities import Prenda

class PostgresPrendaRepository(IPrendaRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    async def listar_todas(self) -> List[Prenda]:
        query = "SELECT id, nombre, descripcion, precio, imagen_url, fecha_creacion FROM prendas"
        rows = await self.db_connection.fetch(query)
        return [
            Prenda(
                id=row['id'],
                nombre=row['nombre'],
                descripcion=row['descripcion'],
                precio=row['precio'],
                imagen_url=row['imagen_url'],
                fecha_creacion=row['fecha_creacion']
            ) for row in rows
        ]

    async def buscar_por_id_con_variantes(self, prenda_id: UUID) -> Optional[Prenda]:
        pass

    async def guardar(self, prenda: Prenda) -> Prenda:
        pass

    async def actualizar(self, prenda: Prenda) -> Prenda:
        pass

    async def eliminar_por_id(self, prenda_id: UUID) -> None:
        pass