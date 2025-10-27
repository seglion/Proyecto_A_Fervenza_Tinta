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

        # Construir la parte VALUES de la consulta dinámicamente
        values_placeholders = []
        params = []
        for i, tipo_cuota in enumerate(tipos_cuota):
            # $1, $2, $3, $4 para el primer tipo_cuota, luego $5, $6, $7, $8 para el segundo, etc.
            offset = i * 4
            values_placeholders.append(f"(${{{offset + 1}}}, ${{{offset + 2}}}, ${{{offset + 3}}}, ${{{offset + 4}}})")
            params.extend([
                tipo_cuota.temporada_id,
                tipo_cuota.nombre,
                tipo_cuota.importe,
                tipo_cuota.fecha_creacion
            ])

        query = f"""
        INSERT INTO tipos_de_cuota (temporada_id, nombre, importe, fecha_creacion)
        VALUES {', '.join(values_placeholders)}
        RETURNING id, temporada_id, nombre, importe, fecha_creacion
        """
        rows = await self.db_connection.fetch(query, *params)

        # Mapear los resultados a entidades TipoCuota y asignar los IDs generados
        guardados = []
        for i, row in enumerate(rows):
            tipos_cuota[i].id = row['id']
            guardados.append(tipos_cuota[i])
        return guardados

    async def actualizar_varios(self, tipos_cuota: List[TipoCuota]) -> List[TipoCuota]:
        if not tipos_cuota:
            return []

        # Construir las cláusulas CASE dinámicamente para nombre e importe
        nombre_case_clauses = []
        importe_case_clauses = []
        ids_to_update = []
        params = []
        param_counter = 1

        for tipo_cuota in tipos_cuota:
            nombre_case_clauses.append(f"WHEN ${{{param_counter}}} THEN ${{{param_counter + 1}}}")
            params.extend([tipo_cuota.id, tipo_cuota.nombre])
            param_counter += 2

            importe_case_clauses.append(f"WHEN ${{{param_counter}}} THEN ${{{param_counter + 1}}}")
            params.extend([tipo_cuota.id, tipo_cuota.importe])
            param_counter += 2

            ids_to_update.append(tipo_cuota.id)

        # Añadir los IDs al final de los parámetros para la cláusula WHERE IN
        for tipo_id in ids_to_update:
            params.append(tipo_id)

        # Construir la consulta UPDATE
        query = f"""
        UPDATE tipos_de_cuota
        SET
            nombre = CASE id
                {' '.join(nombre_case_clauses)}
            END,
            importe = CASE id
                {' '.join(importe_case_clauses)}
            END
        WHERE id IN ({', '.join([f'${{{param_counter + i}}}' for i, _ in enumerate(ids_to_update)])})
        """
        await self.db_connection.execute(query, *params)
        return tipos_cuota

    async def get_tipo_cuota_general(self, temporada_id: int) -> Optional[TipoCuota]:
        query = "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipos_de_cuota WHERE temporada_id = $1 AND nombre = 'General'"
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
        query = "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipos_de_cuota WHERE temporada_id = $1 AND nombre = 'Nuevo Socio'"
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
