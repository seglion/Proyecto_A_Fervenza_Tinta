from typing import List

from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository


class CerrarPedidosBorradorUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        temporada_pedido_repository: ITemporadaPedidoRepository,
    ):
        self.pedido_repository = pedido_repository
        self.temporada_pedido_repository = temporada_pedido_repository

    async def execute(self) -> None:
        # Este caso de uso es para ser ejecutado por un proceso automático (ej. un cron job).
        # La seguridad no se basa en un usuario logueado, sino en quién puede ejecutar este proceso.
        # Por lo tanto, no se aplica una política de usuario aquí.

        # 1. Buscar temporadas que terminaron y no fueron cerradas
        temporadas_a_cerrar = await self.temporada_pedido_repository.get_temporadas_finalizadas_pendientes_cierre()

        if temporadas_a_cerrar:
            ids_temporadas_a_cerrar: List[int] = []
            # 2. Para cada temporada, cancelar pedidos 'borrador'
            for temporada in temporadas_a_cerrar:
                await self.pedido_repository.cancelar_pedidos_borrador(temporada.id)
                ids_temporadas_a_cerrar.append(temporada.id)
            
            # 3. Marcar la temporada como cerrada
            await self.temporada_pedido_repository.marcar_temporadas_como_cerradas(ids_temporadas_a_cerrar)
