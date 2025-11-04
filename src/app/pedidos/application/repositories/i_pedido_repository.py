from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

from src.app.pedidos.domain.entities import Pedido, TemporadaPedido, LineaDePedido
from src.app.prendas.domain.entities import Prenda, VariantePrenda


class IPedidoRepository(ABC):
    @abstractmethod
    async def buscar_borrador_por_usuario_y_temporada(self, user_id: UUID, temporada_id: int) -> Optional[Pedido]:
        pass

    @abstractmethod
    async def obtener_o_crear_borrador(self, user_id: UUID, temporada_id: int) -> Pedido:
        pass

    @abstractmethod
    async def anadir_o_actualizar_linea(self, pedido: Pedido, variante: VariantePrenda, prenda: Prenda, cantidad: int) -> Pedido:
        pass

    @abstractmethod
    async def guardar_pedido(self, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    async def buscar_borrador_por_usuario(self, user_id: UUID) -> Optional[Pedido]:
        pass

    @abstractmethod
    async def buscar_historial_por_usuario(self, user_id: UUID) -> List[Pedido]:
        pass

    @abstractmethod
    async def buscar_pedidos_finalizados_por_temporada(self, temporada_id: int) -> List[Pedido]:
        pass

    @abstractmethod
    async def buscar_por_id_con_detalle(self, id_pedido: UUID) -> Optional[Pedido]:
        pass

    @abstractmethod
    async def buscar_por_id(self, id_pedido: UUID) -> Optional[Pedido]:
        pass

    @abstractmethod
    async def cancelar_pedidos_borrador(self, temporada_id: int):
        pass

    @abstractmethod
    async def eliminar_linea_y_recalcular(self, pedido: Pedido, linea_a_eliminar_id: UUID) -> Pedido:
        pass
