from uuid import UUID
from typing import Optional

from src.app.pedidos.application.dtos import PedidoDetalleAdminDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import AccesoDenegadoException, PedidoNoEncontradoException
from src.app.users.domain.entities import User


class VerDetallePedidoAdminUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        pedido_policy: PedidoPolicy,
    ):
        self.pedido_repository = pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, id_pedido: UUID, current_user: User) -> PedidoDetalleAdminDTO:
        if not self.pedido_policy.es_administrador(current_user):
            raise AccesoDenegadoException("No tiene permiso para ver el detalle de este pedido.")

        pedido = await self.pedido_repository.buscar_por_id_con_detalle(id_pedido)
        if not pedido:
            raise PedidoNoEncontradoException("Pedido no encontrado.")

        return PedidoDetalleAdminDTO.model_validate(pedido)
