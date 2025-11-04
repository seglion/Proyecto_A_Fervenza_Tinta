import asyncpg
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal

from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.domain.entities import Pedido, LineaDePedido
from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago
from src.app.prendas.domain.entities import Prenda, VariantePrenda
from src.app.pedidos.infrastructure.models import PedidoModel, LineaDePedidoModel


class PostgresPedidoRepository(IPedidoRepository):
    def __init__(self, db_connection: asyncpg.Connection):
        self.db_connection = db_connection

    def _get_metodo_pago_from_value(self, value: str) -> Optional[MetodoPago]:
        if value is None:
            return None
        for member in MetodoPago:
            if member.value == value.strip():
                return member
        return None

    async def _recalcular_total_pedido(self, pedido: Pedido) -> None:
        total = Decimal("0.00")
        for linea in pedido.lineas:
            total += linea.cantidad * linea.precio_unitario_conxelado
        pedido.total_calculado = total

    async def buscar_borrador_por_usuario_y_temporada(self, user_id: UUID, temporada_id: int) -> Optional[Pedido]:
        query = "SELECT id, usuario_id, temporada_id, estado, total_calculado, metodo_pago, id_transaccion_externa, fecha_creacion, fecha_finalizacion FROM pedidos WHERE usuario_id = $1 AND temporada_id = $2 AND estado = $3::estado_pedido_enum"
        row = await self.db_connection.fetchrow(query, user_id, temporada_id, EstadoPedido.BORRADOR.value)
        if row:
            return Pedido(
                id=row['id'],
                usuario_id=row['usuario_id'],
                temporada_id=row['temporada_id'],
                estado=EstadoPedido(row['estado']),
                total_calculado=row['total_calculado'],
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
                id_transaccion_externa=row['id_transaccion_externa'],
                fecha_creacion=row['fecha_creacion'],
                fecha_finalizacion=row['fecha_finalizacion']
            )
        return None

    async def obtener_o_crear_borrador(self, user_id: UUID, temporada_id: int) -> Pedido:
        pedido = await self.buscar_borrador_por_usuario_y_temporada(user_id, temporada_id)
        if not pedido:
            pedido = Pedido(
                id=uuid4(),
                usuario_id=user_id,
                temporada_id=temporada_id,
                estado=EstadoPedido.BORRADOR,
                total_calculado=Decimal("0.00"),
                fecha_creacion=datetime.now()
            )
            await self.guardar_pedido(pedido)
        return pedido

    async def anadir_o_actualizar_linea(self, pedido: Pedido, variante: VariantePrenda, prenda: Prenda, cantidad: int) -> Pedido:
        # Buscar si la línea ya existe
        linea_existente = next((linea for linea in pedido.lineas if linea.variante_prenda_id == variante.id), None)

        if linea_existente:
            linea_existente.cantidad = cantidad
            linea_existente.precio_unitario_conxelado = prenda.precio # Asegurar que el precio se actualiza si cambia
        else:
            nueva_linea = LineaDePedido(
                id=uuid4(),
                pedido_id=pedido.id,
                variante_prenda_id=variante.id,
                cantidad=cantidad,
                precio_unitario_conxelado=prenda.precio,
                desc_variante_conxelada=f"{prenda.nombre} - {variante.genero.value} {variante.talla.value}"
            )
            pedido.lineas.append(nueva_linea)
        
        await self._recalcular_total_pedido(pedido)
        await self.guardar_pedido(pedido) # Guardar pedido y sus líneas
        return pedido

    async def eliminar_linea_y_recalcular(self, pedido: Pedido, linea_a_eliminar_id: UUID) -> Pedido:
        pedido.lineas = [linea for linea in pedido.lineas if linea.id != linea_a_eliminar_id]
        await self._recalcular_total_pedido(pedido)
        await self.guardar_pedido(pedido) # Guardar pedido y sus líneas
        return pedido

    async def guardar_pedido(self, pedido: Pedido) -> Pedido:
        async with self.db_connection.transaction():
            # Comprobar si el pedido ya existe en la base de datos
            existing_pedido_row = await self.db_connection.fetchrow("SELECT id FROM pedidos WHERE id = $1", pedido.id)

            if existing_pedido_row:
                # Actualizar pedido existente
                query = """
                UPDATE pedidos
                SET
                    usuario_id = $1,
                    temporada_id = $2,
                    estado = $3::estado_pedido_enum,
                    total_calculado = $4,
                    metodo_pago = $5::metodo_pago_pedido_enum,
                    id_transaccion_externa = $6,
                    fecha_finalizacion = $7
                WHERE id = $8
                """
                await self.db_connection.execute(
                    query,
                    pedido.usuario_id,
                    pedido.temporada_id,
                    pedido.estado.value,
                    pedido.total_calculado,
                    pedido.metodo_pago.value if pedido.metodo_pago else None,
                    pedido.id_transaccion_externa,
                    pedido.fecha_finalizacion,
                    pedido.id
                )
            else:
                # Insertar nuevo pedido
                # No es necesario generar UUID aquí si ya lo proporciona la entidad
                query = """
                INSERT INTO pedidos (id, usuario_id, temporada_id, estado, total_calculado, metodo_pago, id_transaccion_externa, fecha_creacion, fecha_finalizacion)
                VALUES ($1, $2, $3, $4::estado_pedido_enum, $5, $6::metodo_pago_pedido_enum, $7, $8, $9)
                RETURNING id
                """
                inserted_id = await self.db_connection.fetchval(
                    query,
                    pedido.id, # Usar el ID proporcionado por la entidad
                    pedido.usuario_id,
                    pedido.temporada_id,
                    pedido.estado.value,
                    pedido.total_calculado,
                    pedido.metodo_pago.value if pedido.metodo_pago else None,
                    pedido.id_transaccion_externa,
                    pedido.fecha_creacion,
                    pedido.fecha_finalizacion
                )
                pedido.id = inserted_id # Debería ser el mismo que el proporcionado, pero es una buena práctica asignar el ID devuelto

            # Guardar líneas de pedido
            if pedido.lineas:
                # Eliminar líneas existentes para re-insertar (simplificación para este ejemplo)
                await self.db_connection.execute("DELETE FROM lineadepedidos WHERE pedido_id = $1", pedido.id)
                for linea in pedido.lineas:
                    linea.id = uuid4()
                    query_linea = """
                    INSERT INTO lineadepedidos (id, pedido_id, variante_prenda_id, cantidad, precio_unitario_conxelado, desc_variante_conxelada)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    """
                    await self.db_connection.execute(
                        query_linea,
                        linea.id,
                        pedido.id, # Use the pedido.id that is now guaranteed to be in the DB
                        linea.variante_prenda_id,
                        linea.cantidad,
                        linea.precio_unitario_conxelado,
                        linea.desc_variante_conxelada
                    )
        return pedido

    async def buscar_por_id(self, pedido_id: UUID) -> Optional[Pedido]:
        query = "SELECT id, usuario_id, temporada_id, estado, total_calculado, metodo_pago, id_transaccion_externa, fecha_creacion, fecha_finalizacion FROM pedidos WHERE id = $1"
        row = await self.db_connection.fetchrow(query, pedido_id)
        if row:
            return Pedido(
                id=row['id'],
                usuario_id=row['usuario_id'],
                temporada_id=row['temporada_id'],
                estado=EstadoPedido(row['estado']),
                total_calculado=row['total_calculado'],
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
                id_transaccion_externa=row['id_transaccion_externa'],
                fecha_creacion=row['fecha_creacion'],
                fecha_finalizacion=row['fecha_finalizacion']
            )
        return None

    async def buscar_por_id_con_detalle(self, pedido_id: UUID) -> Optional[Pedido]:
        query_pedido = "SELECT id, usuario_id, temporada_id, estado, total_calculado, metodo_pago, id_transaccion_externa, fecha_creacion, fecha_finalizacion FROM pedidos WHERE id = $1"
        row_pedido = await self.db_connection.fetchrow(query_pedido, pedido_id)

        if not row_pedido:
            return None

        pedido = Pedido(
            id=row_pedido['id'],
            usuario_id=row_pedido['usuario_id'],
            temporada_id=row_pedido['temporada_id'],
            estado=EstadoPedido(row_pedido['estado']),
            total_calculado=row_pedido['total_calculado'],
            metodo_pago=self._get_metodo_pago_from_value(row_pedido['metodo_pago']),
            id_transaccion_externa=row_pedido['id_transaccion_externa'],
            fecha_creacion=row_pedido['fecha_creacion'],
            fecha_finalizacion=row_pedido['fecha_finalizacion']
        )

        query_lineas = "SELECT id, pedido_id, variante_prenda_id, cantidad, precio_unitario_conxelado, desc_variante_conxelada FROM lineadepedidos WHERE pedido_id = $1"
        rows_lineas = await self.db_connection.fetch(query_lineas, pedido_id)
        pedido.lineas = [
            LineaDePedido(
                id=row['id'],
                pedido_id=row['pedido_id'],
                variante_prenda_id=row['variante_prenda_id'],
                cantidad=row['cantidad'],
                precio_unitario_conxelado=row['precio_unitario_conxelado'],
                desc_variante_conxelada=row['desc_variante_conxelada']
            ) for row in rows_lineas
        ]
        return pedido

    async def buscar_borrador_por_usuario(self, user_id: UUID) -> Optional[Pedido]:
        query = "SELECT id, usuario_id, temporada_id, estado, total_calculado, metodo_pago, id_transaccion_externa, fecha_creacion, fecha_finalizacion FROM pedidos WHERE usuario_id = $1 AND estado = $2::estado_pedido_enum"
        row = await self.db_connection.fetchrow(query, user_id, EstadoPedido.BORRADOR.value)
        if row:
            return Pedido(
                id=row['id'],
                usuario_id=row['usuario_id'],
                temporada_id=row['temporada_id'],
                estado=EstadoPedido(row['estado']),
                total_calculado=row['total_calculado'],
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
                id_transaccion_externa=row['id_transaccion_externa'],
                fecha_creacion=row['fecha_creacion'],
                fecha_finalizacion=row['fecha_finalizacion']
            )
        return None

    async def buscar_historial_por_usuario(self, usuario_id: UUID) -> List[Pedido]:
        query = "SELECT id, usuario_id, temporada_id, estado, total_calculado, metodo_pago, id_transaccion_externa, fecha_creacion, fecha_finalizacion FROM pedidos WHERE usuario_id = $1 ORDER BY fecha_creacion DESC"
        rows = await self.db_connection.fetch(query, usuario_id)
        return [
            Pedido(
                id=row['id'],
                usuario_id=row['usuario_id'],
                temporada_id=row['temporada_id'],
                estado=EstadoPedido(row['estado']),
                total_calculado=row['total_calculado'],
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
                id_transaccion_externa=row['id_transaccion_externa'],
                fecha_creacion=row['fecha_creacion'],
                fecha_finalizacion=row['fecha_finalizacion']
            ) for row in rows
        ]

    async def buscar_pedidos_finalizados_por_temporada(self, temporada_id: int) -> List[Pedido]:
        query = "SELECT id, usuario_id, temporada_id, estado, total_calculado, metodo_pago, id_transaccion_externa, fecha_creacion, fecha_finalizacion FROM pedidos WHERE temporada_id = $1 AND estado IN ($2::estado_pedido_enum, $3::estado_pedido_enum) ORDER BY fecha_creacion DESC"
        rows = await self.db_connection.fetch(query, temporada_id, EstadoPedido.COMPLETADO.value, EstadoPedido.ENCARGADO.value)
        return [
            Pedido(
                id=row['id'],
                usuario_id=row['usuario_id'],
                temporada_id=row['temporada_id'],
                estado=EstadoPedido(row['estado']),
                total_calculado=row['total_calculado'],
                metodo_pago=self._get_metodo_pago_from_value(row['metodo_pago']),
                id_transaccion_externa=row['id_transaccion_externa'],
                fecha_creacion=row['fecha_creacion'],
                fecha_finalizacion=row['fecha_finalizacion']
            ) for row in rows
        ]

    async def cancelar_pedidos_borrador(self, temporada_id: int) -> None:
        query = "UPDATE pedidos SET estado = $1::estado_pedido_enum WHERE temporada_id = $2 AND estado = $3::estado_pedido_enum"
        await self.db_connection.execute(query, EstadoPedido.CANCELADO.value, temporada_id, EstadoPedido.BORRADOR.value)