import asyncpg
from typing import List, Optional


from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.domain.entities import TemporadaPedido



class PostgresTemporadaPedidoRepository(ITemporadaPedidoRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    async def get_temporada_activa(self) -> Optional[TemporadaPedido]:
        query = "SELECT id, nombre_temporada, fecha_inicio, fecha_fin, esta_activa, fecha_creacion FROM temporadapedidos WHERE esta_activa = TRUE LIMIT 1"
        row = await self.db_connection.fetchrow(query)
        if row:
            return TemporadaPedido(
                id=row['id'],
                nombre_temporada=row['nombre_temporada'],
                fecha_inicio=row['fecha_inicio'],
                fecha_fin=row['fecha_fin'],
                esta_activa=row['esta_activa'],
                fecha_creacion=row['fecha_creacion']
            )
        return None

    async def get_all(self) -> List[TemporadaPedido]:
        query = "SELECT id, nombre_temporada, fecha_inicio, fecha_fin, esta_activa, fecha_creacion FROM temporadapedidos ORDER BY fecha_inicio DESC"
        rows = await self.db_connection.fetch(query)
        return [TemporadaPedido(**row) for row in rows]

    async def get_by_id(self, temporada_id: int) -> Optional[TemporadaPedido]:
        query = "SELECT id, nombre_temporada, fecha_inicio, fecha_fin, esta_activa, fecha_creacion FROM temporadapedidos WHERE id = $1"
        row = await self.db_connection.fetchrow(query, temporada_id)
        if row:
            return TemporadaPedido(**row)
        return None

    async def guardar(self, temporada: TemporadaPedido) -> TemporadaPedido:
        # Comprobar si la temporada ya existe en la base de datos
        existing_temporada_row = await self.db_connection.fetchrow("SELECT id FROM temporadapedidos WHERE id = $1", temporada.id)

        if existing_temporada_row:
            # Actualizar temporada existente
            query = """
            UPDATE temporadapedidos
            SET
                nombre_temporada = $1,
                fecha_inicio = $2,
                fecha_fin = $3,
                esta_activa = $4
            WHERE id = $5
            """
            await self.db_connection.execute(
                query,
                temporada.nombre_temporada,
                temporada.fecha_inicio,
                temporada.fecha_fin,
                temporada.esta_activa,
                temporada.id
            )
        else:
            # Insertar nueva temporada
            query = """
            INSERT INTO temporadapedidos (nombre_temporada, fecha_inicio, fecha_fin, esta_activa, fecha_creacion)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id
            """
            inserted_id = await self.db_connection.fetchval(
                query,
                temporada.nombre_temporada,
                temporada.fecha_inicio,
                temporada.fecha_fin,
                temporada.esta_activa,
                temporada.fecha_creacion
            )
            temporada.id = inserted_id # Asignar el ID devuelto por la base de datos
        return temporada

    async def marcar_temporadas_como_cerradas(self, lista_ids_temporadas: List[int]):
        query = "UPDATE temporadapedidos SET esta_activa = FALSE WHERE id = ANY($1::int[])"
        await self.db_connection.execute(query, lista_ids_temporadas)

    async def get_temporadas_finalizadas_pendientes_cierre(self) -> List[TemporadaPedido]:
        query = "SELECT id, nombre_temporada, fecha_inicio, fecha_fin, esta_activa, fecha_creacion FROM temporadapedidos WHERE fecha_fin < NOW() AND esta_activa = TRUE"
        rows = await self.db_connection.fetch(query)
        return [
            TemporadaPedido(
                id=row['id'],
                nombre_temporada=row['nombre_temporada'],
                fecha_inicio=row['fecha_inicio'],
                fecha_fin=row['fecha_fin'],
                esta_activa=row['esta_activa'],
                fecha_creacion=row['fecha_creacion']
            ) for row in rows
        ]
