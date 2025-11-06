
from typing import List

 # Keep for type hinting if needed elsewhere
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import AccesoDenegadoException
from src.app.users.domain.entities import User
from src.app.pedidos.domain.entities import Pedido # Import Pedido domain entity


class ListarHistorialPedidosUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        pedido_policy: PedidoPolicy,
    ):
        self.pedido_repository = pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, current_user: User) -> List[Pedido]: 
        if not self.pedido_policy.puede_listar_historial(current_user):
            raise AccesoDenegadoException("El usuario no tiene permiso para ver el historial de pedidos.")

        pedidos = await self.pedido_repository.buscar_historial_por_usuario(current_user.id)
        

        return pedidos
