import pytest
from abc import ABC, abstractmethod

from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository


def test_interface_class_exists():
    try:
        from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    except ImportError:
        pytest.fail("La clase de la interfaz 'ICuotaRepository' no existe.")

def test_all_methods_are_abstract():
    with pytest.raises(TypeError):
        class ConcreteCuotaRepository(ICuotaRepository):
            pass
        ConcreteCuotaRepository()

def test_get_usuarios_inactivos_desde_is_abstract_method():
    with pytest.raises(TypeError):
        class ConcreteCuotaRepository(ICuotaRepository):
            async def listar_todas(self):
                pass
            async def buscar_por_usuario_y_temporada(self, usuario_id, temporada_id):
                pass
            async def guardar(self, cuota):
                pass
            async def buscar_por_id_con_detalle(self, cuota_id):
                pass
            async def buscar_por_id(self, cuota_id):
                pass
            async def actualizar(self, cuota):
                pass
            async def buscar_por_usuario_id_completadas(self, usuario_id):
                pass
            async def ha_pagado_cuota_alta_antes(self, user_id):
                pass
            async def get_usuarios_pendientes_por_temporada(self, temporada_id):
                pass
        ConcreteCuotaRepository()

def test_get_usuarios_pendientes_por_temporada_is_abstract_method():
    with pytest.raises(TypeError):
        class ConcreteCuotaRepository(ICuotaRepository):
            async def listar_todas(self):
                pass
            async def buscar_por_usuario_y_temporada(self, usuario_id, temporada_id):
                pass
            async def guardar(self, cuota):
                pass
            async def buscar_por_id_con_detalle(self, cuota_id):
                pass
            async def buscar_por_id(self, cuota_id):
                pass
            async def actualizar(self, cuota):
                pass
            async def buscar_por_usuario_id_completadas(self, usuario_id):
                pass
            async def ha_pagado_cuota_alta_antes(self, user_id):
                pass
        ConcreteCuotaRepository()
