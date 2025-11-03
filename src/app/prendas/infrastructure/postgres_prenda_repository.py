import asyncpg
from typing import List, Optional
from uuid import UUID
import inspect

from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.prendas.domain.entities import Prenda, VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda

class PostgresPrendaRepository(IPrendaRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    def _get_genero_prenda_from_value(self, value: str) -> Optional[GeneroPrenda]:
        if value is None:
            return None
        for member in GeneroPrenda:
            if member.value == value.strip():
                return member
        return None

    def _get_talla_prenda_from_value(self, value: str) -> Optional[TallaPrenda]:
        if value is None:
            return None
        for member in TallaPrenda:
            if member.value == value.strip():
                return member
        return None

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
        query = inspect.cleandoc("""
            SELECT
                p.id AS prenda_id,
                p.nombre,
                p.descripcion,
                p.precio,
                p.imagen_url,
                p.fecha_creacion,
                vp.id AS variante_id,
                vp.genero,
                vp.talla,
                vp.fecha_creacion AS variante_fecha_creacion
            FROM prendas p
            LEFT JOIN varianteprendas vp ON p.id = vp.prenda_id
            WHERE p.id = $1
        """)
        rows = await self.db_connection.fetch(query, prenda_id)

        if not rows:
            return None

        prenda_data = {
            'id': rows[0]['prenda_id'],
            'nombre': rows[0]['nombre'],
            'descripcion': rows[0]['descripcion'],
            'precio': rows[0]['precio'],
            'imagen_url': rows[0]['imagen_url'],
            'fecha_creacion': rows[0]['fecha_creacion']
        }
        
        variantes = []
        for row in rows:
            if row['variante_id']:
                variantes.append(
                    VariantePrenda(
                        id=row['variante_id'],
                        prenda_id=row['prenda_id'],
                        genero=self._get_genero_prenda_from_value(row['genero']),
                        talla=self._get_talla_prenda_from_value(row['talla']),
                        fecha_creacion=row['variante_fecha_creacion']
                    )
                )
        
        return Prenda(**prenda_data, variantes=variantes)

    async def guardar(self, prenda: Prenda) -> Prenda:
        query = inspect.cleandoc("""
            INSERT INTO prendas (id, nombre, descripcion, precio, imagen_url, fecha_creacion)
            VALUES ($1, $2, $3, $4, $5, $6)
        """)
        await self.db_connection.execute(
            query,
            prenda.id,
            prenda.nombre,
            prenda.descripcion,
            prenda.precio,
            prenda.imagen_url,
            prenda.fecha_creacion
        )
        return prenda

    async def actualizar(self, prenda: Prenda) -> Prenda:
        query = inspect.cleandoc("""
            UPDATE prendas
            SET nombre = $1, descripcion = $2, precio = $3, imagen_url = $4
            WHERE id = $5
        """)
        await self.db_connection.execute(
            query,
            prenda.nombre,
            prenda.descripcion,
            prenda.precio,
            prenda.imagen_url,
            prenda.id
        )
        return prenda

    async def eliminar_por_id(self, prenda_id: UUID) -> None:
        query = "DELETE FROM prendas WHERE id = $1"
        await self.db_connection.execute(query, prenda_id)