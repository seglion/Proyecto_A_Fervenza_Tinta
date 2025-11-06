
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.application.dtos import ActualizarTemporadaPedidoDTO, TemporadaPedidoDTO
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User
from src.app.pedidos.application.exceptions import AccesoDenegadoException, TemporadaPedidoNoEncontradaException

class ActualizarTemporadaPedidoUseCase:
    def __init__(self, temporada_pedido_repository: ITemporadaPedidoRepository, pedido_policy: PedidoPolicy):
        self.temporada_pedido_repository = temporada_pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, temporada_id: int, datos_actualizacion: ActualizarTemporadaPedidoDTO, current_user: User) -> TemporadaPedidoDTO:
        if not self.pedido_policy.gestionar_temporadas(current_user):
            raise AccesoDenegadoException("No tiene permiso para actualizar temporadas de pedidos.")

        # Si se va a activar esta temporada, primero desactivamos la que esté activa
        if datos_actualizacion.esta_activa is True:
            temporada_activa_actual = await self.temporada_pedido_repository.get_temporada_activa()
            if temporada_activa_actual and temporada_activa_actual.id != temporada_id:
                temporada_activa_actual.esta_activa = False
                await self.temporada_pedido_repository.guardar(temporada_activa_actual)

        # Obtenemos y actualizamos la temporada deseada
        temporada_a_actualizar = await self.temporada_pedido_repository.get_by_id(temporada_id)
        if not temporada_a_actualizar:
            raise TemporadaPedidoNoEncontradaException("La temporada de pedidos no fue encontrada.")

        # Aplicamos las actualizaciones
        update_data = datos_actualizacion.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(temporada_a_actualizar, key, value)

        temporada_actualizada = await self.temporada_pedido_repository.guardar(temporada_a_actualizar)

        return TemporadaPedidoDTO.model_validate(temporada_actualizada)
