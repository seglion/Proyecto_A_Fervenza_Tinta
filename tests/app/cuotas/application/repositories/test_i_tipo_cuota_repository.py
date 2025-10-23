import pytest
from typing import List, Optional

from src.app.cuotas.domain.entities import TipoCuota

def test_tipo_cuota_repository_interface_file_exists():
    """
    Tests if the tipo cuota repository interface file exists.
    """
    try:
        from src.app.cuotas.application.repositories import i_tipo_cuota_repository
    except ImportError:
        pytest.fail("Tipo cuota repository interface file does not exist: src/app/cuotas/application/repositories/i_tipo_cuota_repository.py")

def test_tipo_cuota_repository_interface_class_exists():
    """
    Tests if the ITipoCuotaRepository class exists in the interface file.
    """
    try:
        from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
    except ImportError:
        pytest.fail("ITipoCuotaRepository class does not exist in i_tipo_cuota_repository.py")

def test_itipocuotarepository_has_guardar_varios_method():
    """
    Tests if the ITipoCuotaRepository interface has a 'guardar_varios' abstract method.
    """
    from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
    assert hasattr(ITipoCuotaRepository, 'guardar_varios')
    assert 'tipos_cuota' in ITipoCuotaRepository.guardar_varios.__annotations__
    assert ITipoCuotaRepository.guardar_varios.__annotations__['tipos_cuota'] == List[TipoCuota]
    assert ITipoCuotaRepository.guardar_varios.__annotations__['return'] == List[TipoCuota]

def test_itipocuotarepository_has_actualizar_varios_method():
    """
    Tests if the ITipoCuotaRepository interface has an 'actualizar_varios' abstract method.
    """
    from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
    assert hasattr(ITipoCuotaRepository, 'actualizar_varios')
    assert 'tipos_cuota' in ITipoCuotaRepository.actualizar_varios.__annotations__
    assert ITipoCuotaRepository.actualizar_varios.__annotations__['tipos_cuota'] == List[TipoCuota]
    assert ITipoCuotaRepository.actualizar_varios.__annotations__['return'] == List[TipoCuota]

def test_itipocuotarepository_has_get_tipo_cuota_general_method():
    """
    Tests if the ITipoCuotaRepository interface has a 'get_tipo_cuota_general' abstract method.
    """
    from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
    assert hasattr(ITipoCuotaRepository, 'get_tipo_cuota_general')
    assert 'temporada_id' in ITipoCuotaRepository.get_tipo_cuota_general.__annotations__
    assert ITipoCuotaRepository.get_tipo_cuota_general.__annotations__['temporada_id'] == int
    assert ITipoCuotaRepository.get_tipo_cuota_general.__annotations__['return'] == Optional[TipoCuota]

def test_itipocuotarepository_has_get_tipo_cuota_nuevo_socio_method():
    """
    Tests if the ITipoCuotaRepository interface has a 'get_tipo_cuota_nuevo_socio' abstract method.
    """
    from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
    assert hasattr(ITipoCuotaRepository, 'get_tipo_cuota_nuevo_socio')
    assert 'temporada_id' in ITipoCuotaRepository.get_tipo_cuota_nuevo_socio.__annotations__
    assert ITipoCuotaRepository.get_tipo_cuota_nuevo_socio.__annotations__['temporada_id'] == int
    assert ITipoCuotaRepository.get_tipo_cuota_nuevo_socio.__annotations__['return'] == Optional[TipoCuota]