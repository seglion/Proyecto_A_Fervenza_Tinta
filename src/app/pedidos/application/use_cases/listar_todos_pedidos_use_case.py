from typing import List, Optional

from src.app.pedidos.application.dtos import ListaPedidosAdminDTO, PedidoDetalleAdminDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import AccesoDenegadoException
from src.app.users.domain.entities import User


class ListarTodosPedidosUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        pedido_policy: PedidoPolicy,
    ):
        self.pedido_repository = pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, current_user: User, temporada_id: Optional[int] = None) -> ListaPedidosAdminDTO:
        if not self.pedido_policy.listar_todos_pedidos(current_user):
            raise AccesoDenegadoException("No tiene permiso para listar todos los pedidos.")

        pedidos = await self.pedido_repository.buscar_pedidos_finalizados_por_temporada(temporada_id)
        
        pedidos_dto = [PedidoDetalleAdminDTO.model_validate(pedido) for pedido in pedidos]
        
        return ListaPedidosAdminDTO(pedidos=pedidos_dto)
