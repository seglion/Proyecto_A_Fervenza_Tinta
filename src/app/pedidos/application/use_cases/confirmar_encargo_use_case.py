

from src.app.pedidos.application.dtos import PedidoDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import TemporadaCerradaException, PedidoNoEncontradoException, PedidoVacioException, AccesoDenegadoException
from src.app.users.domain.entities import User
from src.app.pedidos.domain.value_objects import EstadoPedido


class ConfirmarEncargoUseCase:
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

        # 2. Buscar pedido 'borrador'
        pedido_borrador = await self.pedido_repository.buscar_borrador_por_usuario(
            current_user.id
        )
        if not pedido_borrador:
            raise PedidoNoEncontradoException("No se encontró un pedido en borrador para el usuario.")

        # 3. Verificar política de acceso
        if not self.pedido_policy.ver_pedido(current_user, pedido_borrador):
            raise AccesoDenegadoException()

        if not pedido_borrador.lineas:
            raise PedidoVacioException("El pedido no tiene líneas para confirmar.")

        # 4. Actualizar pedido a 'encargado'
        pedido_borrador.estado = EstadoPedido.ENCARGADO
        # metodo_pago se establecerá manualmente por el admin

        pedido_final = await self.pedido_repository.guardar_pedido(pedido_borrador)

        return PedidoDTO.model_validate(pedido_final)
