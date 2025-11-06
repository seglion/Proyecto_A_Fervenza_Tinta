from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.app.prendas.domain.entities import Prenda

class IPrendaRepository(ABC):
    @abstractmethod
    async def listar_todas(self) -> List[Prenda]:
        pass

    @abstractmethod
    async def buscar_por_id_con_variantes(self, prenda_id: UUID) -> Optional[Prenda]:
        pass

    @abstractmethod
    async def guardar(self, prenda: Prenda) -> Prenda:
        pass

    @abstractmethod
    async def actualizar(self, prenda: Prenda) -> Prenda:
        pass

    @abstractmethod
    async def eliminar_por_id(self, prenda_id: UUID) -> None:
        pass