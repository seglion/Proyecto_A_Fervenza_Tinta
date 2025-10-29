import asyncpg
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.domain.entities import TipoCuota
from typing import List, Optional

class PostgresTipoCuotaRepository(ITipoCuotaRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    async def guardar_varios(self, tipos_cuota: List[TipoCuota]) -> List[TipoCuota]:
        if not tipos_cuota:
            return []

        params = []
        for tc in tipos_cuota:
            params.extend([tc.temporada_id, tc.nombre, tc.importe, tc.fecha_creacion])

        num_columns = 4
        num_rows = len(tipos_cuota)
        
        placeholder_groups = []
        for i in range(num_rows):
            start_index = i * num_columns + 1
            group = ", ".join(f"${j}" for j in range(start_index, start_index + num_columns))
            placeholder_groups.append(f"({group})")

        values_clause = ", ".join(placeholder_groups)

        query = f"""
        INSERT INTO tipocuotas (temporada_id, nombre, importe, fecha_creacion)
        VALUES {values_clause}
        RETURNING id
        """
        rows = await self.db_connection.fetch(query, *params)

        for i, row in enumerate(rows):
            tipos_cuota[i].id = row['id']
        
        return tipos_cuota

    async def actualizar_varios(self, tipos_cuota: List[TipoCuota]) -> List[TipoCuota]:
        if not tipos_cuota:
            return []

        for tc in tipos_cuota:
            query = "UPDATE tipocuotas SET nombre = $1, importe = $2 WHERE id = $3"
            await self.db_connection.execute(query, tc.nombre, tc.importe, tc.id)
            
        return tipos_cuota

    async def buscar_por_temporada_id(self, temporada_id: int) -> List[TipoCuota]:
        query = "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipocuotas WHERE temporada_id = $1"
        rows = await self.db_connection.fetch(query, temporada_id)
        return [
            TipoCuota(
                id=row['id'],
                temporada_id=row['temporada_id'],
                nombre=row['nombre'],
                importe=row['importe'],
                fecha_creacion=row['fecha_creacion']
            ) for row in rows
        ]

    async def get_tipo_cuota_general(self, temporada_id: int) -> Optional[TipoCuota]:
        query = "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipocuotas WHERE temporada_id = $1 AND nombre = 'General'"
        row = await self.db_connection.fetchrow(query, temporada_id)
        if row:
            return TipoCuota(
                id=row['id'],
                temporada_id=row['temporada_id'],
                nombre=row['nombre'],
                importe=row['importe'],
                fecha_creacion=row['fecha_creacion']
            )
        return None

    async def get_tipo_cuota_nuevo_socio(self, temporada_id: int) -> Optional[TipoCuota]:
        query = "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipocuotas WHERE temporada_id = $1 AND nombre = 'Nuevo Socio'"
        row = await self.db_connection.fetchrow(query, temporada_id)
        if row:
            return TipoCuota(
                id=row['id'],
                temporada_id=row['temporada_id'],
                nombre=row['nombre'],
                importe=row['importe'],
                fecha_creacion=row['fecha_creacion']
            )
        return None

    async def buscar_por_id(self, tipo_cuota_id: int) -> Optional[TipoCuota]:
        query = "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipocuotas WHERE id = $1"
        row = await self.db_connection.fetchrow(query, tipo_cuota_id)
        if row:
            return TipoCuota(
                id=row['id'],
                temporada_id=row['temporada_id'],
                nombre=row['nombre'],
                importe=row['importe'],
                fecha_creacion=row['fecha_creacion']
            )
        return None
