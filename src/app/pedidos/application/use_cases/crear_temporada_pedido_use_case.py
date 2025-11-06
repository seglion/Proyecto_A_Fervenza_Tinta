from datetime import datetime

from src.app.pedidos.application.dtos import DatosTemporadaPedidoDTO, TemporadaPedidoDTO
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import AccesoDenegadoException
from src.app.users.domain.entities import User
from src.app.pedidos.domain.entities import TemporadaPedido


class CrearTemporadaPedidoUseCase:
    def __init__(
        self,
        temporada_pedido_repository: ITemporadaPedidoRepository,
        pedido_policy: PedidoPolicy,
    ):
        self.temporada_pedido_repository = temporada_pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, datos_temporada: DatosTemporadaPedidoDTO, current_user: User) -> TemporadaPedidoDTO:
        if not self.pedido_policy.gestionar_temporadas(current_user):
            raise AccesoDenegadoException("No tiene permiso para gestionar temporadas de pedidos.")

        nueva_temporada = TemporadaPedido(
            id=None, # El ID será asignado por la base de datos
            nombre_temporada=datos_temporada.nombre_temporada,
            fecha_inicio=datos_temporada.fecha_inicio,
            fecha_fin=datos_temporada.fecha_fin,
            esta_activa=False, # Por defecto, no está activa
            fecha_creacion=datetime.now()
        )

        temporada_creada = await self.temporada_pedido_repository.guardar(nueva_temporada)

        return TemporadaPedidoDTO.model_validate(temporada_creada)
