import asyncpg
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.domain.entities import TemporadaCuota
from typing import List, Optional
from datetime import date, datetime

class PostgresTemporadaCuotaRepository(ITemporadaCuotaRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    async def guardar_temporada(self, temporada: TemporadaCuota) -> TemporadaCuota:
        query = """
        INSERT INTO temporadacuotas (nombre_temporada, fecha_inicio, fecha_fin, fecha_creacion)
        VALUES ($1, $2, $3, $4)
        RETURNING id
        """
        # Execute the query and retrieve the generated ID
        # Assuming the ID is autoincremental and returned by the RETURNING clause
        # For asyncpg, fetchval is used to get a single value (like an ID)
        temporada_id = await self.db_connection.fetchval(
            query,
            temporada.nombre_temporada,
            temporada.fecha_inicio,
            temporada.fecha_fin,
            temporada.fecha_creacion
        )
        # Assign the retrieved ID to the temporada object
        temporada.id = temporada_id
        return temporada

    async def listar_todas(self) -> List[TemporadaCuota]:
        query = "SELECT id, nombre_temporada, fecha_inicio, fecha_fin, fecha_creacion FROM temporadacuotas ORDER BY fecha_inicio DESC"
        rows = await self.db_connection.fetch(query)
        return [
            TemporadaCuota(
                id=row['id'],
                nombre_temporada=row['nombre_temporada'],
                fecha_inicio=row['fecha_inicio'],
                fecha_fin=row['fecha_fin'],
                fecha_creacion=row['fecha_creacion']
            ) for row in rows
        ]

    async def actualizar(self, temporada: TemporadaCuota) -> TemporadaCuota:
        query = """
        UPDATE temporadacuotas
        SET nombre_temporada = $1, fecha_inicio = $2, fecha_fin = $3
        WHERE id = $4
        """
        await self.db_connection.execute(
            query,
            temporada.nombre_temporada,
            temporada.fecha_inicio,
            temporada.fecha_fin,
            temporada.id
        )
        return temporada

    async def get_temporada_activa(self) -> Optional[TemporadaCuota]:
        query = "SELECT id, nombre_temporada, fecha_inicio, fecha_fin, fecha_creacion FROM temporadacuotas WHERE fecha_inicio <= CURRENT_DATE AND fecha_fin >= CURRENT_DATE"
        row = await self.db_connection.fetchrow(query)
        if row:
            return TemporadaCuota(
                id=row['id'],
                nombre_temporada=row['nombre_temporada'],
                fecha_inicio=row['fecha_inicio'],
                fecha_fin=row['fecha_fin'],
                fecha_creacion=row['fecha_creacion']
            )
        return None