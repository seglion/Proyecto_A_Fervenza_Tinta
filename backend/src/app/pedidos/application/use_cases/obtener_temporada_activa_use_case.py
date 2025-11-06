

from src.app.pedidos.application.dtos import TemporadaPedidoDTO
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.application.exceptions import TemporadaPedidoNoEncontradaException, AccesoDenegadoException
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User


class ObtenerTemporadaActivaUseCase:
    def __init__(self, temporada_pedido_repository: ITemporadaPedidoRepository, pedido_policy: PedidoPolicy):
        self.temporada_pedido_repository = temporada_pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, current_user: User) -> TemporadaPedidoDTO:
        if not self.pedido_policy.gestionar_temporadas(current_user):
            raise AccesoDenegadoException("No tiene permiso para obtener la temporada de pedidos activa.")

        temporada_activa = await self.temporada_pedido_repository.get_temporada_activa()
        if not temporada_activa:
            raise TemporadaPedidoNoEncontradaException("No se encontró ninguna temporada de pedidos activa.")

        return TemporadaPedidoDTO.model_validate(temporada_activa)
