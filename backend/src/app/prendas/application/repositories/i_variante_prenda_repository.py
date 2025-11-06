from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.app.prendas.domain.entities import VariantePrenda

class IVariantePrendaRepository(ABC):
    @abstractmethod
    async def guardar(self, variante_prenda: VariantePrenda) -> VariantePrenda:
        pass

    @abstractmethod
    async def eliminar_por_id(self, variante_prenda_id: UUID) -> None:
        pass

    @abstractmethod
    async def buscar_por_id(self, variante_prenda_id: UUID) -> Optional[VariantePrenda]:
        pass

    @abstractmethod
    async def listar_por_prenda_id(self, prenda_id: UUID) -> List[VariantePrenda]:
        pass