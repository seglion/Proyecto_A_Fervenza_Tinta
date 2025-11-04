from uuid import UUID
from typing import Optional
from datetime import datetime

from src.app.pedidos.application.dtos import DatosPagoManualDTO, PedidoCompletadoDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.core.services.i_email_service import IEmailService
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import AccesoDenegadoException, PedidoNoEncontradoException, PedidoNoValidoException
from src.app.users.domain.entities import User
from src.app.pedidos.domain.value_objects import EstadoPedido


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

    async def execute(self, id_pedido: UUID, datos_pago_manual: DatosPagoManualDTO, current_user: User) -> PedidoCompletadoDTO:
        if not self.pedido_policy.marcar_pagado(current_user):
            raise AccesoDenegadoException("No tiene permiso para marcar pedidos como pagados manualmente.")

        pedido = await self.pedido_repository.buscar_por_id_con_detalle(id_pedido)
        if not pedido:
            raise PedidoNoEncontradoException("Pedido no encontrado.")

        if pedido.estado != EstadoPedido.ENCARGADO:
            raise PedidoNoValidoException(f"El pedido no está en estado '{EstadoPedido.ENCARGADO.value}' para ser marcado como pagado.")

        pedido.estado = EstadoPedido.COMPLETADO
        pedido.metodo_pago = datos_pago_manual.metodo_pago
        pedido.fecha_finalizacion = datetime.now()

        pedido_actualizado = await self.pedido_repository.guardar_pedido(pedido)

        # Opcional: Enviar email de confirmación
        user_email = await self.user_repository.buscar_email_por_id(pedido.usuario_id)
        if user_email:
            await self.email_service.enviar_confirmacion_pago_pedido(user_email, pedido_actualizado)

        return PedidoCompletadoDTO.model_validate(pedido_actualizado)
