import pytest
from typing import List, Optional
from uuid import UUID

from src.app.cuotas.domain.entities import Cuota

def test_cuota_repository_interface_file_exists():
    """
    Tests if the cuota repository interface file exists.
    """
    try:
        from src.app.cuotas.application.repositories import i_cuota_repository
    except ImportError:
        pytest.fail("Cuota repository interface file does not exist: src/app/cuotas/application/repositories/i_cuota_repository.py")

def test_cuota_repository_interface_class_exists():
    """
    Tests if the ICuotaRepository class exists in the interface file.
    """
    try:
        from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    except ImportError:
        pytest.fail("ICuotaRepository class does not exist in i_cuota_repository.py")

def test_icuotarepository_has_listar_todas_method():
    from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    assert hasattr(ICuotaRepository, 'listar_todas')
    assert ICuotaRepository.listar_todas.__annotations__['return'] == List[Cuota]

def test_icuotarepository_has_buscar_por_usuario_y_temporada_method():
    from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    assert hasattr(ICuotaRepository, 'buscar_por_usuario_y_temporada')
    assert ICuotaRepository.buscar_por_usuario_y_temporada.__annotations__['usuario_id'] == UUID
    assert ICuotaRepository.buscar_por_usuario_y_temporada.__annotations__['temporada_id'] == int
    assert ICuotaRepository.buscar_por_usuario_y_temporada.__annotations__['return'] == Optional[Cuota]

def test_icuotarepository_has_guardar_method():
    from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    assert hasattr(ICuotaRepository, 'guardar')
    assert ICuotaRepository.guardar.__annotations__['cuota'] == Cuota
    assert ICuotaRepository.guardar.__annotations__['return'] == Cuota

def test_icuotarepository_has_buscar_por_id_con_detalle_method():
    from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    assert hasattr(ICuotaRepository, 'buscar_por_id_con_detalle')
    assert ICuotaRepository.buscar_por_id_con_detalle.__annotations__['cuota_id'] == UUID
    assert ICuotaRepository.buscar_por_id_con_detalle.__annotations__['return'] == Optional[Cuota]

def test_icuotarepository_has_buscar_por_id_method():
    from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    assert hasattr(ICuotaRepository, 'buscar_por_id')
    assert ICuotaRepository.buscar_por_id.__annotations__['cuota_id'] == UUID
    assert ICuotaRepository.buscar_por_id.__annotations__['return'] == Optional[Cuota]

def test_icuotarepository_has_actualizar_method():
    from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
    assert hasattr(ICuotaRepository, 'actualizar')
    assert ICuotaRepository.actualizar.__annotations__['cuota'] == Cuota
    assert ICuotaRepository.actualizar.__annotations__['return'] == Cuota