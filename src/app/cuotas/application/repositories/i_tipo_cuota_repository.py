from abc import ABC, abstractmethod
from typing import List, Optional

from src.app.cuotas.domain.entities import TipoCuota

class ITipoCuotaRepository(ABC):
    @abstractmethod
    async def guardar_varios(self, tipos_cuota: List[TipoCuota]) -> List[TipoCuota]:
        pass

    @abstractmethod
    async def actualizar_varios(self, tipos_cuota: List[TipoCuota]) -> List[TipoCuota]:
        pass

    @abstractmethod
    async def buscar_por_temporada_id(self, temporada_id: int) -> List[TipoCuota]:
        pass

    @abstractmethod
    async def get_tipo_cuota_general(self, temporada_id: int) -> Optional[TipoCuota]:
        pass

    @abstractmethod
    async def get_tipo_cuota_nuevo_socio(self, temporada_id: int) -> Optional[TipoCuota]:
        pass

    @abstractmethod
    async def buscar_por_id(self, tipo_cuota_id: int) -> Optional[TipoCuota]:
        pass
