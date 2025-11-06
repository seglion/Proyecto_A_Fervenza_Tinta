from typing import List

from src.app.pedidos.application.dtos import TemporadaPedidoDTO
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User
from src.app.pedidos.application.exceptions import AccesoDenegadoException


class ListarTemporadasPedidoUseCase:
    def __init__(self, temporada_pedido_repository: ITemporadaPedidoRepository, pedido_policy: PedidoPolicy):
        self.temporada_pedido_repository = temporada_pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, current_user: User) -> List[TemporadaPedidoDTO]:
        if not self.pedido_policy.gestionar_temporadas(current_user):
            raise AccesoDenegadoException("No tiene permiso para listar las temporadas de pedidos.")

        temporadas = await self.temporada_pedido_repository.get_all()
        return [TemporadaPedidoDTO.model_validate(t) for t in temporadas]
