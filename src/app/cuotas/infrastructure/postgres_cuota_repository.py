import asyncpg
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.domain.entities import Cuota
from src.app.users.domain.entities import User
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from src.app.cuotas.application.dtos import CuotaDetalleResponseDTO
from src.app.cuotas.domain.value_objects import MetodoPago, EstadoPago # Import MetodoPago from domain

class PostgresCuotaRepository(ICuotaRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    async def listar_todas(self) -> List[Cuota]:
        query = "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas"
        rows = await self.db_connection.fetch(query)
        return [
            Cuota(
                id=row['id'],
                usuario_id=row['usuario_id'],
                tipo_de_cuota_id=row['tipo_de_cuota_id'],
                importe_pagado=row['importe_pagado'],
                estado_pago=EstadoPago(row['estado_pago']),
                fecha_pago=row['fecha_pago'],
                metodo_pago=MetodoPago(row['metodo_pago']) if row['metodo_pago'] else None,
                id_transaccion_externa=row['id_transaccion_externa'],
                notas_admin=row['notas_admin'],
                fecha_creacion=row['fecha_creacion']
            ) for row in rows
        ]

    async def buscar_por_usuario_y_temporada(self, usuario_id: UUID, temporada_id: int) -> Optional[Cuota]:
        query = "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE usuario_id = $1 AND tipo_de_cuota_id = $2"
        row = await self.db_connection.fetchrow(query, usuario_id, temporada_id)
        if row:
            return Cuota(
                id=row['id'],
                usuario_id=row['usuario_id'],
                tipo_de_cuota_id=row['tipo_de_cuota_id'],
                importe_pagado=row['importe_pagado'],
                estado_pago=EstadoPago(row['estado_pago']),
                fecha_pago=row['fecha_pago'],
                metodo_pago=MetodoPago(row['metodo_pago']) if row['metodo_pago'] else None,
                id_transaccion_externa=row['id_transaccion_externa'],
                notas_admin=row['notas_admin'],
                fecha_creacion=row['fecha_creacion']
            )
        return None

    async def guardar(self, cuota: Cuota) -> Cuota:
        query = """
        INSERT INTO cuotas (id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion)
        VALUES ($1, $2, $3, $4, $5, $6, $7::tipo_metodo_pago, $8, $9, $10)
        """
        await self.db_connection.execute(
            query,
            cuota.id,
            cuota.usuario_id,
            cuota.tipo_de_cuota_id,
            cuota.importe_pagado,
            cuota.estado_pago,
            cuota.fecha_pago,
            cuota.metodo_pago.value if cuota.metodo_pago else None,
            cuota.id_transaccion_externa,
            cuota.notas_admin,
            cuota.fecha_creacion
        )
        return cuota

    async def buscar_por_id_con_detalle(self, cuota_id: UUID) -> Optional[CuotaDetalleResponseDTO]:
        query = """
        SELECT
            c.id, c.usuario_id, c.tipo_de_cuota_id, c.importe_pagado, c.estado_pago, c.fecha_pago, c.metodo_pago, c.id_transaccion_externa, c.notas_admin, c.fecha_creacion,
            u.nombre AS usuario_nombre, u.apellidos AS usuario_apellidos,
            tc.nombre AS tipo_cuota_nombre,
            ts.nombre_temporada AS temporada_nombre
        FROM cuotas c
        JOIN usuarios u ON c.usuario_id = u.id
        JOIN tipos_de_cuota tc ON c.tipo_de_cuota_id = tc.id
        JOIN temporadas_cuota ts ON tc.temporada_id = ts.id
        WHERE c.id = $1
        """
        row = await self.db_connection.fetchrow(query, cuota_id)
        if row:
            return CuotaDetalleResponseDTO(
                id=row['id'],
                usuario_id=row['usuario_id'],
                tipo_de_cuota_id=row['tipo_de_cuota_id'],
                importe_pagado=row['importe_pagado'],
                estado_pago=EstadoPago(row['estado_pago']),
                fecha_pago=row['fecha_pago'],
                metodo_pago=MetodoPago(row['metodo_pago']) if row['metodo_pago'] else None,
                id_transaccion_externa=row['id_transaccion_externa'],
                notas_admin=row['notas_admin'],
                fecha_creacion=row['fecha_creacion'],
                usuario_nombre=row['usuario_nombre'],
                usuario_apellidos=row['usuario_apellidos'],
                tipo_cuota_nombre=row['tipo_cuota_nombre'],
                temporada_nombre=row['temporada_nombre']
            )
        return None

    async def buscar_por_id(self, cuota_id: UUID) -> Optional[Cuota]:
        query = "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE id = $1"
        row = await self.db_connection.fetchrow(query, cuota_id)
        if row:
            return Cuota(
                id=row['id'],
                usuario_id=row['usuario_id'],
                tipo_de_cuota_id=row['tipo_de_cuota_id'],
                importe_pagado=row['importe_pagado'],
                estado_pago=EstadoPago(row['estado_pago']),
                fecha_pago=row['fecha_pago'],
                metodo_pago=MetodoPago(row['metodo_pago']) if row['metodo_pago'] else None,
                id_transaccion_externa=row['id_transaccion_externa'],
                notas_admin=row['notas_admin'],
                fecha_creacion=row['fecha_creacion']
            )
        return None

    async def actualizar(self, cuota: Cuota) -> Cuota:
        query = """
        UPDATE cuotas
        SET
            importe_pagado = $1,
            estado_pago = $2,
            fecha_pago = $3,
            metodo_pago = $4::tipo_metodo_pago,
            id_transaccion_externa = $5,
            notas_admin = $6
        WHERE id = $7
        """
        await self.db_connection.execute(
            query,
            cuota.importe_pagado,
            cuota.estado_pago.value,
            cuota.fecha_pago,
            cuota.metodo_pago.value if cuota.metodo_pago else None,
            cuota.id_transaccion_externa,
            cuota.notas_admin,
            cuota.id
        )
        return cuota

    async def buscar_por_usuario_id_completadas(self, usuario_id: UUID) -> List[Cuota]:
        query = "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE usuario_id = $1 AND estado_pago = $2"
        rows = await self.db_connection.fetch(query, usuario_id, EstadoPago.COMPLETADO.value)
        return [
            Cuota(
                id=row['id'],
                usuario_id=row['usuario_id'],
                tipo_de_cuota_id=row['tipo_de_cuota_id'],
                importe_pagado=row['importe_pagado'],
                estado_pago=EstadoPago(row['estado_pago']),
                fecha_pago=row['fecha_pago'],
                metodo_pago=MetodoPago(row['metodo_pago']) if row['metodo_pago'] else None,
                id_transaccion_externa=row['id_transaccion_externa'],
                notas_admin=row['notas_admin'],
                fecha_creacion=row['fecha_creacion']
            ) for row in rows
        ]

    async def ha_pagado_cuota_alta_antes(self, usuario_id: UUID) -> bool:
        query = "SELECT COUNT(*) FROM cuotas c JOIN tipos_de_cuota tc ON c.tipo_de_cuota_id = tc.id WHERE c.usuario_id = $1 AND tc.nombre = 'Cuota de Alta' AND c.estado_pago = $2"
        count = await self.db_connection.fetchval(query, usuario_id, EstadoPago.COMPLETADO.value)
        return count > 0

    async def get_usuarios_pendientes_por_temporada(self, temporada_id: int) -> List[User]:
        pass

    async def get_usuarios_inactivos_desde(self, fecha_limite: date) -> List[UUID]:
        pass