from uuid import UUID

from datetime import datetime

from src.app.pedidos.application.dtos import DatosPagoManualDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.core.services.i_email_service import IEmailService
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import AccesoDenegadoException, PedidoNoEncontradoException, PedidoNoModificableException
from src.app.users.domain.entities import User
from src.app.pedidos.domain.entities import Pedido
from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago


class MarcarPagoManualPedidoUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        user_repository: IUserRepository,
        email_service: IEmailService,
        pedido_policy: PedidoPolicy,
    ):
        self.pedido_repository = pedido_repository
        self.user_repository = user_repository
        self.email_service = email_service
        self.pedido_policy = pedido_policy

    async def execute(self, id_pedido: UUID, datos_pago_manual: DatosPagoManualDTO, current_user: User) -> Pedido:
        if not self.pedido_policy.marcar_pagado(current_user):
            raise AccesoDenegadoException("No tiene permiso para marcar pedidos como pagados manualmente.")

        pedido = await self.pedido_repository.buscar_por_id_con_detalle(id_pedido)
        if not pedido:
            raise PedidoNoEncontradoException("Pedido no encontrado.")

        if pedido.estado != EstadoPedido.ENCARGADO:
            raise PedidoNoModificableException(f"El pedido no está en estado '{EstadoPedido.ENCARGADO.value}' para ser marcado como pagado.")

        pedido.estado = EstadoPedido.COMPLETADO
        pedido.metodo_pago = MetodoPago(datos_pago_manual.metodo_pago)
        pedido.fecha_finalizacion = datetime.now()

        pedido_actualizado = await self.pedido_repository.guardar_pedido(pedido)


        user = await self.user_repository.buscar_por_id(pedido.usuario_id)
        if user:
            pedido_info = {
                "name": user.nombre,
                "pedido_id": str(pedido_actualizado.id),
                "total": str(pedido_actualizado.total_calculado),
                "estado": pedido_actualizado.estado.value,
                "fecha_finalizacion": pedido_actualizado.fecha_finalizacion.isoformat() if pedido_actualizado.fecha_finalizacion else None,
            }
            self.email_service.enviar_confirmacion_pago_pedido(user.email, pedido_info)

        return pedido_actualizado
