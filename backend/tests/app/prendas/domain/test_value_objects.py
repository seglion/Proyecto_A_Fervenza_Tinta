import os
import pytest
import inspect
from enum import Enum

import src.app.prendas.domain.value_objects as value_objects_module

def test_value_objects_file_exists():
    file_path = "src/app/prendas/domain/value_objects.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_generoprenda_enum_exists():
    assert hasattr(value_objects_module, "GeneroPrenda"), "El Enum GeneroPrenda no existe en value_objects.py"
    assert inspect.isclass(value_objects_module.GeneroPrenda), "GeneroPrenda no es una clase"
    assert issubclass(value_objects_module.GeneroPrenda, Enum), "GeneroPrenda no es un Enum"

def test_tallaprenda_enum_exists():
    assert hasattr(value_objects_module, "TallaPrenda"), "El Enum TallaPrenda no existe en value_objects.py"
    assert inspect.isclass(value_objects_module.TallaPrenda), "TallaPrenda no es una clase"
    assert issubclass(value_objects_module.TallaPrenda, Enum), "TallaPrenda no es un Enum"
