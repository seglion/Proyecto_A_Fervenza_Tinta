import pytest
from typing import Optional
from app.users.domain.entities import Role

def test_role_class_exists():
    """
    Tests if the Role class exists in the entities file.
    """
    try:
        from app.users.domain.entities import Role
    except ImportError:
        pytest.fail("Role class does not exist in entities.py")

def test_role_has_id_attribute():
    """
    Tests if the Role class has an 'id' attribute with the correct type.
    """
    assert 'id' in Role.__annotations__
    assert Role.__annotations__['id'] == Optional[int]

def test_role_has_nombre_attribute():
    """
    Tests if the Role class has a 'nombre' attribute with the correct type.
    """
    assert 'nombre' in Role.__annotations__
    assert Role.__annotations__['nombre'] == str

def test_role_has_descripcion_attribute():
    """
    Tests if the Role class has a 'descripcion' attribute with the correct type.
    """
    assert 'descripcion' in Role.__annotations__
    assert Role.__annotations__['descripcion'] == Optional[str]
