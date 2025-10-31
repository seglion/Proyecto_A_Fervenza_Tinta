import asyncpg
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.domain.entities import Cuota
from src.app.users.domain.entities import User
from typing import List, Optional
from uuid import UUID
from datetime import date, datetime

from src.app.cuotas.domain.value_objects import MetodoPago, EstadoPago, NombreTipoCuota # Import MetodoPago from domain

class PostgresCuotaRepository(ICuotaRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    def _get_metodo_pago_from_value(self, value: str) -> Optional[MetodoPago]:
        if value is None:
            return None
        for member in MetodoPago:
            if member.value == value.strip():
                return member
        return None # Should not happen if DB values are consistent with Enum

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
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
                id_transaccion_externa=row['id_transaccion_externa'],
                notas_admin=row['notas_admin'],
                fecha_creacion=row['fecha_creacion']
            ) for row in rows
        ]

    async def buscar_por_usuario_y_temporada(self, usuario_id: UUID, tipo_cuota_id: int) -> Optional[Cuota]:
        query = "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE usuario_id = $1 AND tipo_de_cuota_id = $2"
        row = await self.db_connection.fetchrow(query, usuario_id, tipo_cuota_id)
        if row:
            return Cuota(
                id=row['id'],
                usuario_id=row['usuario_id'],
                tipo_de_cuota_id=row['tipo_de_cuota_id'],
                importe_pagado=row['importe_pagado'],
                estado_pago=EstadoPago(row['estado_pago']),
                fecha_pago=row['fecha_pago'],
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
                id_transaccion_externa=row['id_transaccion_externa'],
                notas_admin=row['notas_admin'],
                fecha_creacion=row['fecha_creacion']
            )
        return None

    async def buscar_cualquier_cuota_por_usuario_y_temporada(self, usuario_id: UUID, temporada_id: int) -> Optional[Cuota]:
        query = """
        SELECT c.id, c.usuario_id, c.tipo_de_cuota_id, c.importe_pagado, c.estado_pago, c.fecha_pago, c.metodo_pago, c.id_transaccion_externa, c.notas_admin, c.fecha_creacion
        FROM cuotas c
        JOIN tipocuotas tc ON c.tipo_de_cuota_id = tc.id
        WHERE c.usuario_id = $1 AND tc.temporada_id = $2
        LIMIT 1
        """
        row = await self.db_connection.fetchrow(query, usuario_id, temporada_id)
        if row:
            return Cuota(
                id=row['id'],
                usuario_id=row['usuario_id'],
                tipo_de_cuota_id=row['tipo_de_cuota_id'],
                importe_pagado=row['importe_pagado'],
                estado_pago=EstadoPago(row['estado_pago']),
                fecha_pago=row['fecha_pago'],
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
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
            cuota.estado_pago.value,
            cuota.fecha_pago,
            cuota.metodo_pago.value if cuota.metodo_pago else None,
            cuota.id_transaccion_externa,
            cuota.notas_admin,
            cuota.fecha_creacion
        )
        return cuota

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
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
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

    async def buscar_por_usuario_id(self, usuario_id: UUID) -> List[Cuota]:
        query = "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE usuario_id = $1"
        rows = await self.db_connection.fetch(query, usuario_id)
        return [
            Cuota(
                id=row['id'],
                usuario_id=row['usuario_id'],
                tipo_de_cuota_id=row['tipo_de_cuota_id'],
                importe_pagado=row['importe_pagado'],
                estado_pago=EstadoPago(row['estado_pago']),
                fecha_pago=row['fecha_pago'],
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
                id_transaccion_externa=row['id_transaccion_externa'],
                notas_admin=row['notas_admin'],
                fecha_creacion=row['fecha_creacion']
            ) for row in rows
        ]

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
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
                id_transaccion_externa=row['id_transaccion_externa'],
                notas_admin=row['notas_admin'],
                fecha_creacion=row['fecha_creacion']
            ) for row in rows
        ]

    async def ha_pagado_cuota_alta_antes(self, usuario_id: UUID) -> bool:
        query = "SELECT COUNT(*) FROM cuotas c JOIN tipocuotas tc ON c.tipo_de_cuota_id = tc.id WHERE c.usuario_id = $1 AND tc.nombre = $2 AND c.estado_pago = $3"
        count = await self.db_connection.fetchval(query, usuario_id, NombreTipoCuota.ALTA.value, EstadoPago.COMPLETADO.value)
        return count > 0

    async def get_usuarios_pendientes_por_temporada(self, temporada_id: int) -> List[User]:
        query = """
        SELECT u.id, u.email, u.contrasena_hasheada, u.nombre, u.apellidos, u.numero_telefono, u.rol, u.apodo, u.url_avatar, u.esta_activo, u.email_verificado, u.aprobado_por_admin, u.fecha_creacion, u.fecha_actualizacion
        FROM usuarios u
        WHERE u.id IN (
            SELECT c.usuario_id
            FROM cuotas c
            JOIN tipocuotas tc ON c.tipo_de_cuota_id = tc.id
            WHERE tc.temporada_id = $1
            GROUP BY c.usuario_id
            HAVING COUNT(CASE WHEN c.estado_pago = $2 THEN 1 ELSE NULL END) = 0
        )
        """
        rows = await self.db_connection.fetch(query, temporada_id, EstadoPago.COMPLETADO.value)
        return [
            User(
                id=row['id'],
                email=row['email'],
                contrasena_hasheada=row['contrasena_hasheada'],
                nombre=row['nombre'],
                apellidos=row['apellidos'],
                numero_telefono=row['numero_telefono'],
                rol=row['rol'],
                apodo=row['apodo'],
                url_avatar=row['url_avatar'],
                esta_activo=row['esta_activo'],
                email_verificado=row['email_verificado'],
                aprobado_por_admin=row['aprobado_por_admin'],
                fecha_creacion=row['fecha_creacion'],
                fecha_actualizacion=row['fecha_actualizacion']
            ) for row in rows
        ]

    async def get_usuarios_inactivos_desde(self, fecha_limite: date) -> List[UUID]:
        query = """
        SELECT u.id
        FROM usuarios u
        LEFT JOIN cuotas c ON u.id = c.usuario_id
        WHERE u.activo = FALSE
        AND u.ultimo_acceso < $1
        GROUP BY u.id
        HAVING COUNT(c.id) = 0
        """
        rows = await self.db_connection.fetch(query, fecha_limite)
        return [row['id'] for row in rows]

    async def buscar_cuota_pendiente_por_usuario_y_tipo_cuota(self, usuario_id: UUID, tipo_cuota_id: int) -> Optional[Cuota]:
        query = "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE usuario_id = $1 AND tipo_de_cuota_id = $2 AND estado_pago = $3"
        row = await self.db_connection.fetchrow(query, usuario_id, tipo_cuota_id, EstadoPago.PENDIENTE.value)
        if row:
            return Cuota(
                id=row['id'],
                usuario_id=row['usuario_id'],
                tipo_de_cuota_id=row['tipo_de_cuota_id'],
                importe_pagado=row['importe_pagado'],
                estado_pago=EstadoPago(row['estado_pago']),
                fecha_pago=row['fecha_pago'],
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
                id_transaccion_externa=row['id_transaccion_externa'],
                notas_admin=row['notas_admin'],
                fecha_creacion=row['fecha_creacion']
            )
        return None
