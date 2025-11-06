from abc import ABC, abstractmethod
from typing import List, Optional

from src.app.cuotas.domain.entities import TemporadaCuota

class ITemporadaCuotaRepository(ABC):
    @abstractmethod
    async def guardar_temporada(self, temporada: TemporadaCuota) -> TemporadaCuota:
        pass

    @abstractmethod
    async def listar_todas(self) -> List[TemporadaCuota]:
        pass

    @abstractmethod
    async def actualizar(self, temporada: TemporadaCuota) -> TemporadaCuota:
        pass

    @abstractmethod
    async def buscar_por_id(self, temporada_id: int) -> Optional[TemporadaCuota]:
        pass

    @abstractmethod
    async def get_temporada_activa(self) -> Optional[TemporadaCuota]:
        pass
