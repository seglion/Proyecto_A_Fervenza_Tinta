import os
import pytest
import inspect

import src.app.prendas.domain.entities as entities_module
from src.app.prendas.domain.entities import Prenda

def test_entities_file_exists():
    file_path = "src/app/prendas/domain/entities.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_prenda_class_exists():
    assert hasattr(entities_module, "Prenda"), "La clase Prenda no existe en entities.py"
    assert inspect.isclass(entities_module.Prenda), "Prenda no es una clase"

def test_varianteprenda_class_exists():
    assert hasattr(entities_module, "VariantePrenda"), "La clase VariantePrenda no existe en entities.py"
    assert inspect.isclass(entities_module.VariantePrenda), "VariantePrenda no es una clase"