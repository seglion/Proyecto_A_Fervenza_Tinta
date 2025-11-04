from uuid import UUID
from typing import Optional

from src.app.pedidos.application.dtos import PedidoDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import AccesoDenegadoException, PedidoNoEncontradoException, PedidoNoValidoException
from src.app.users.domain.entities import User
from src.app.pedidos.domain.value_objects import EstadoPedido


class CancelarPedidoUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        pedido_policy: PedidoPolicy,
    ):
        self.pedido_repository = pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, id_pedido: UUID, current_user: User) -> PedidoDTO:
        if not self.pedido_policy.cancelar_pedido(current_user):
            raise AccesoDenegadoException("No tiene permiso para cancelar pedidos.")

        pedido = await self.pedido_repository.buscar_por_id(id_pedido)
        if not pedido:
            raise PedidoNoEncontradoException("Pedido no encontrado.")

        if pedido.estado == EstadoPedido.COMPLETADO:
            raise PedidoNoValidoException("No se puede cancelar un pedido que ya está completado.")

        pedido.estado = EstadoPedido.CANCELADO

        pedido_actualizado = await self.pedido_repository.guardar_pedido(pedido)

        return PedidoDTO.model_validate(pedido_actualizado)
