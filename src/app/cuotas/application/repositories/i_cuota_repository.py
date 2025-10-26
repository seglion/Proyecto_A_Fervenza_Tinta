from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.app.cuotas.domain.entities import Cuota

class ICuotaRepository(ABC):
    @abstractmethod
    async def listar_todas(self) -> List[Cuota]:
        pass

    @abstractmethod
    async def buscar_por_usuario_y_temporada(self, usuario_id: UUID, temporada_id: int) -> Optional[Cuota]:
        pass

    @abstractmethod
    async def guardar(self, cuota: Cuota) -> Cuota:
        pass

    @abstractmethod
    async def buscar_por_id_con_detalle(self, cuota_id: UUID) -> Optional[Cuota]:
        pass

    @abstractmethod
    async def buscar_por_id(self, cuota_id: UUID) -> Optional[Cuota]:
        pass

    @abstractmethod
    async def actualizar(self, cuota: Cuota) -> Cuota:
        pass

    @abstractmethod
    async def buscar_por_usuario_id_completadas(self, usuario_id: UUID) -> List[Cuota]:
        pass

    @abstractmethod
    async def ha_pagado_cuota_alta_antes(self, usuario_id: UUID) -> bool:
        pass
