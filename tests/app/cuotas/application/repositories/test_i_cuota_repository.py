import pytest
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from datetime import date # Importar date

from src.app.cuotas.domain.entities import Cuota
from src.app.users.domain.entities import User


def test_interface_class_exists():
    try:
        from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    except ImportError:
        pytest.fail("La clase de la interfaz 'ICuotaRepository' no existe.")

def test_all_methods_are_abstract():
    from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    with pytest.raises(TypeError):
        class ConcreteCuotaRepository(ICuotaRepository):
            pass
        ConcreteCuotaRepository()

def test_buscar_por_usuario_id_is_abstract_method():
    from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    with pytest.raises(TypeError):
        class ConcreteCuotaRepository(ICuotaRepository):
            async def listar_todas(self) -> List[Cuota]:
                pass
            async def buscar_por_usuario_y_temporada(self, usuario_id: UUID, temporada_id: int) -> Optional[Cuota]:
                pass
            async def guardar(self, cuota: Cuota) -> Cuota:
                pass
            async def buscar_por_id(self, cuota_id: UUID) -> Optional[Cuota]:
                pass
            async def actualizar(self, cuota: Cuota) -> Cuota:
                pass
            async def buscar_por_usuario_id_completadas(self, usuario_id: UUID) -> List[Cuota]:
                pass
            async def ha_pagado_cuota_alta_antes(self, usuario_id: UUID) -> bool:
                pass
            async def get_usuarios_pendientes_por_temporada(self, temporada_id: int) -> List[User]:
                pass
            async def get_usuarios_inactivos_desde(self, fecha_limite: date) -> List[UUID]:
                pass
            async def buscar_cuota_pendiente_por_usuario_y_tipo_cuota(self, usuario_id: UUID, tipo_cuota_id: int) -> Optional[Cuota]:
                pass
        ConcreteCuotaRepository()
