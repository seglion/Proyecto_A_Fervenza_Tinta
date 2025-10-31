import os
import pytest
import inspect
from abc import ABC, abstractmethod

import src.app.prendas.application.repositories.i_prenda_repository as i_prenda_repository_module
from src.app.prendas.domain.entities import Prenda

def test_i_prenda_repository_file_exists():
    file_path = "src/app/prendas/application/repositories/i_prenda_repository.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_i_prenda_repository_interface_exists():
    assert hasattr(i_prenda_repository_module, "IPrendaRepository"), "La interfaz IPrendaRepository no existe en i_prenda_repository.py"
    assert inspect.isclass(i_prenda_repository_module.IPrendaRepository), "IPrendaRepository no es una clase"
    assert issubclass(i_prenda_repository_module.IPrendaRepository, ABC), "IPrendaRepository no hereda de ABC"

def test_listar_todas_method_exists():
    assert hasattr(i_prenda_repository_module.IPrendaRepository, "listar_todas"), "El método listar_todas no existe en IPrendaRepository"
    assert inspect.isfunction(i_prenda_repository_module.IPrendaRepository.listar_todas), "listar_todas no es una función"
    assert "@abstractmethod" in inspect.getsource(i_prenda_repository_module.IPrendaRepository.listar_todas), "listar_todas no es un método abstracto"
