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
