import os
import pytest
import inspect
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

import src.app.prendas.application.repositories.i_variante_prenda_repository as i_variante_prenda_repository_module
from src.app.prendas.domain.entities import VariantePrenda

def test_i_variante_prenda_repository_file_exists():
    file_path = "src/app/prendas/application/repositories/i_variante_prenda_repository.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_i_variante_prenda_repository_interface_exists():
    assert hasattr(i_variante_prenda_repository_module, "IVariantePrendaRepository"), "La interfaz IVariantePrendaRepository no existe en i_variante_prenda_repository.py"
    assert inspect.isclass(i_variante_prenda_repository_module.IVariantePrendaRepository), "IVariantePrendaRepository no es una clase"
    assert issubclass(i_variante_prenda_repository_module.IVariantePrendaRepository, ABC), "IVariantePrendaRepository no hereda de ABC"

def test_guardar_method_exists():
    assert hasattr(i_variante_prenda_repository_module.IVariantePrendaRepository, "guardar"), "El método guardar no existe en IVariantePrendaRepository"
    assert inspect.isfunction(i_variante_prenda_repository_module.IVariantePrendaRepository.guardar), "guardar no es una función"
    assert "@abstractmethod" in inspect.getsource(i_variante_prenda_repository_module.IVariantePrendaRepository.guardar), "guardar no es un método abstracto"

def test_eliminar_por_id_method_exists():
    assert hasattr(i_variante_prenda_repository_module.IVariantePrendaRepository, "eliminar_por_id"), "El método eliminar_por_id no existe en IVariantePrendaRepository"
    assert inspect.isfunction(i_variante_prenda_repository_module.IVariantePrendaRepository.eliminar_por_id), "eliminar_por_id no es una función"
    assert "@abstractmethod" in inspect.getsource(i_variante_prenda_repository_module.IVariantePrendaRepository.eliminar_por_id), "eliminar_por_id no es un método abstracto"

def test_buscar_por_id_method_exists():
    assert hasattr(i_variante_prenda_repository_module.IVariantePrendaRepository, "buscar_por_id"), "El método buscar_por_id no existe en IVariantePrendaRepository"
    assert inspect.isfunction(i_variante_prenda_repository_module.IVariantePrendaRepository.buscar_por_id), "buscar_por_id no es una función"
    assert "@abstractmethod" in inspect.getsource(i_variante_prenda_repository_module.IVariantePrendaRepository.buscar_por_id), "buscar_por_id no es un método abstracto"

def test_listar_por_prenda_id_method_exists():
    assert hasattr(i_variante_prenda_repository_module.IVariantePrendaRepository, "listar_por_prenda_id"), "El método listar_por_prenda_id no existe en IVariantePrendaRepository"
    assert inspect.isfunction(i_variante_prenda_repository_module.IVariantePrendaRepository.listar_por_prenda_id), "listar_por_prenda_id no es una función"
    assert "@abstractmethod" in inspect.getsource(i_variante_prenda_repository_module.IVariantePrendaRepository.listar_por_prenda_id), "listar_por_prenda_id no es un método abstracto"