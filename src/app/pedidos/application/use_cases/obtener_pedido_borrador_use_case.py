from uuid import UUID

from datetime import datetime
from decimal import Decimal

from src.app.pedidos.application.dtos import PedidoDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User
from src.app.pedidos.application.exceptions import TemporadaCerradaException, AccesoDenegadoException
from src.app.pedidos.domain.value_objects import EstadoPedido


class ObtenerPedidoBorradorUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        temporada_pedido_repository: ITemporadaPedidoRepository,
        pedido_policy: PedidoPolicy,
    ):
        self.pedido_repository = pedido_repository
        self.temporada_pedido_repository = temporada_pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, current_user: User) -> PedidoDTO:
        # 1. Comprobar temporada activa
        temporada_activa = await self.temporada_pedido_repository.get_temporada_activa()
        if not temporada_activa or not temporada_activa.esta_activa:
            raise TemporadaCerradaException("No hay temporada de pedidos activa o está cerrada.")

        # 2. Obtener pedido en borrador
        pedido_borrador = await self.pedido_repository.buscar_borrador_por_usuario_y_temporada(
            current_user.id,
            temporada_activa.id
        )

        if pedido_borrador:
            # 3. Verificar política de acceso (el usuario debe ser el dueño o admin)
            if not self.pedido_policy.ver_pedido(current_user, pedido_borrador):
                raise AccesoDenegadoException()
            return PedidoDTO.model_validate(pedido_borrador)
        else:
         
            return PedidoDTO(
                id=UUID('00000000-0000-0000-0000-000000000000'), # Placeholder para un ID vacío
                usuario_id=current_user.id,
                temporada_id=temporada_activa.id,
                estado=EstadoPedido.BORRADOR,
                total_calculado=Decimal('0.00'),
                fecha_creacion=datetime.now(),
                lineas=[]
            )