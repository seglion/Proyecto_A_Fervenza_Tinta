from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.application.repositories.i_user_repository import IUserRepository
from uuid import UUID
from src.app.pedidos.application.dtos import PedidoDetalleDTO
from src.app.pedidos.application.exceptions import PedidoNoEncontradoException, AccesoDenegadoException
from src.app.users.application.exceptions import UserNotFoundException

class VerDetalleMiPedidoUseCase:
    def __init__(self, pedido_repository: IPedidoRepository, pedido_policy: PedidoPolicy, user_repository: IUserRepository):
        self.pedido_repository = pedido_repository
        self.pedido_policy = pedido_policy
        self.user_repository = user_repository

    async def execute(self, pedido_id: UUID, usuario_id: UUID) -> PedidoDetalleDTO:
        pedido = await self.pedido_repository.buscar_por_id_con_detalle(pedido_id)

        if not pedido:
            raise PedidoNoEncontradoException()

        current_user = await self.user_repository.buscar_por_id(usuario_id)

        if not current_user:
            raise UserNotFoundException()

        if not self.pedido_policy.ver_pedido(current_user, pedido):
            raise AccesoDenegadoException()

        return PedidoDetalleDTO.model_validate(pedido)
