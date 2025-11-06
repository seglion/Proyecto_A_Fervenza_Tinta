from uuid import UUID


from src.app.pedidos.application.dtos import PedidoDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import TemporadaCerradaException, PedidoNoEncontradoException, AccesoDenegadoException
from src.app.users.domain.entities import User


class EliminarPrendaPedidoUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        temporada_pedido_repository: ITemporadaPedidoRepository,
        pedido_policy: PedidoPolicy,
    ):
        self.pedido_repository = pedido_repository
        self.temporada_pedido_repository = temporada_pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, current_user: User, id_linea: UUID) -> PedidoDTO:
        # 1. Comprobar temporada activa
        temporada_activa = await self.temporada_pedido_repository.get_temporada_activa()
        if not temporada_activa or not temporada_activa.esta_activa:
            raise TemporadaCerradaException("No hay temporada de pedidos activa o está cerrada.")

        # 2. Buscar el pedido 'borrador' del usuario
        pedido_borrador = await self.pedido_repository.buscar_borrador_por_usuario(
            current_user.id
        )
        if not pedido_borrador:
            raise PedidoNoEncontradoException("No se encontró un pedido en borrador para el usuario.")

        # 3. Verificar política de acceso
        if not self.pedido_policy.ver_pedido(current_user, pedido_borrador):
            raise AccesoDenegadoException()

        # 4. Eliminar línea y recalcular
        pedido_actualizado = await self.pedido_repository.eliminar_linea_y_recalcular(
            pedido_borrador,
            id_linea
        )

        # 5. Guardar el pedido actualizado
        pedido_final = await self.pedido_repository.guardar_pedido(pedido_actualizado)

        return PedidoDTO.model_validate(pedido_final)
