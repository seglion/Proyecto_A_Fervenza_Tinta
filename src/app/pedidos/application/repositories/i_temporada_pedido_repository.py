from abc import ABC, abstractmethod
from typing import Optional, List

from src.app.pedidos.domain.entities import TemporadaPedido


class ITemporadaPedidoRepository(ABC):
    @abstractmethod
    async def get_temporada_activa(self) -> Optional[TemporadaPedido]:
        pass

    @abstractmethod
    async def guardar(self, temporada: TemporadaPedido) -> TemporadaPedido:
        pass

    @abstractmethod
    async def marcar_temporadas_como_cerradas(self, lista_ids_temporadas: List[int]):
        pass
