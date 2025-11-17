from abc import ABC, abstractmethod
from typing import Any, List, Optional
from uuid import UUID
from datetime import date

from src.app.cuotas.domain.entities import Cuota
from src.app.users.domain.entities import User

class ICuotaRepository(ABC):
    @abstractmethod
    async def listar_todas(self) -> List[Cuota]:
        pass

    @abstractmethod
    async def buscar_cualquier_cuota_por_usuario_y_temporada(self, usuario_id: UUID, temporada_id: int) -> Optional[Cuota]:
        pass

    @abstractmethod
    async def guardar(self, cuota: Cuota) -> Cuota:
        pass

    @abstractmethod
    async def buscar_por_id(self, cuota_id: UUID) -> Optional[Cuota]:
        pass

    @abstractmethod
    async def actualizar(self, cuota: Cuota) -> Cuota:
        pass

    @abstractmethod
    async def buscar_por_usuario_id(self, usuario_id: UUID) -> List[Cuota]:
        pass

    @abstractmethod
    async def ha_pagado_cuota_alta_antes(self, usuario_id: UUID) -> bool:
        pass

    @abstractmethod
    async def get_usuarios_pendientes_por_temporada(self, temporada_id: int) -> List[User]:
        pass

    @abstractmethod
    async def get_usuarios_inactivos_desde(self, fecha_limite: date) -> List[UUID]:
        pass
    @abstractmethod
    async def listar_recientes_completadas_con_detalle(self,limit:int)->List[Any]:
        pass


