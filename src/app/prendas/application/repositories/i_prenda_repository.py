from abc import ABC, abstractmethod
from typing import List
from src.app.prendas.domain.entities import Prenda

class IPrendaRepository(ABC):
    @abstractmethod
    async def listar_todas(self) -> List[Prenda]:
        pass