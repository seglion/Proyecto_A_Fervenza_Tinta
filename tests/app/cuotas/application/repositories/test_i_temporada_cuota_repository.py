import pytest
from typing import List, Optional

from src.app.cuotas.domain.entities import TemporadaCuota

def test_temporada_cuota_repository_interface_file_exists():
    """
    Tests if the temporada cuota repository interface file exists.
    """
    try:
        from src.app.cuotas.application.repositories import i_temporada_cuota_repository
    except ImportError:
        pytest.fail("Temporada cuota repository interface file does not exist: src/app/cuotas/application/repositories/i_temporada_cuota_repository.py")

def test_temporada_cuota_repository_interface_class_exists():
    """
    Tests if the ITemporadaCuotaRepository class exists in the interface file.
    """
    try:
        from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
    except ImportError:
        pytest.fail("ITemporadaCuotaRepository class does not exist in i_temporada_cuota_repository.py")

def test_itemporadacuotarepository_has_guardar_temporada_method():
    """
    Tests if the ITemporadaCuotaRepository interface has a 'guardar_temporada' abstract method.
    """
    from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
    assert hasattr(ITemporadaCuotaRepository, 'guardar_temporada')
    assert 'temporada' in ITemporadaCuotaRepository.guardar_temporada.__annotations__
    assert ITemporadaCuotaRepository.guardar_temporada.__annotations__['temporada'] == TemporadaCuota
    assert ITemporadaCuotaRepository.guardar_temporada.__annotations__['return'] == TemporadaCuota

def test_itemporadacuotarepository_has_listar_todas_method():
    """
    Tests if the ITemporadaCuotaRepository interface has a 'listar_todas' abstract method.
    """
    from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
    assert hasattr(ITemporadaCuotaRepository, 'listar_todas')
    assert ITemporadaCuotaRepository.listar_todas.__annotations__['return'] == List[TemporadaCuota]

def test_itemporadacuotarepository_has_actualizar_method():
    """
    Tests if the ITemporadaCuotaRepository interface has an 'actualizar' abstract method.
    """
    from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
    assert hasattr(ITemporadaCuotaRepository, 'actualizar')
    assert 'temporada' in ITemporadaCuotaRepository.actualizar.__annotations__
    assert ITemporadaCuotaRepository.actualizar.__annotations__['temporada'] == TemporadaCuota
    assert ITemporadaCuotaRepository.actualizar.__annotations__['return'] == TemporadaCuota

def test_itemporadacuotarepository_has_get_temporada_activa_method():
    """
    Tests if the ITemporadaCuotaRepository interface has a 'get_temporada_activa' abstract method.
    """
    from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
    assert hasattr(ITemporadaCuotaRepository, 'get_temporada_activa')
    assert ITemporadaCuotaRepository.get_temporada_activa.__annotations__['return'] == Optional[TemporadaCuota]