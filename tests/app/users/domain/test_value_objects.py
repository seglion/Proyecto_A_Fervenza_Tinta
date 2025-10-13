import pytest
from app.users.domain.value_objects import Rol, TipoToken

def test_rol_enum_exists_and_has_correct_values():
    """
    Tests if the Rol enum exists and has the correct values.
    """
    assert Rol.ADMIN.value == "admin"
    assert Rol.USUARIO.value == "usuario"

def test_tipo_token_enum_exists_and_has_correct_values():
    """
    Tests if the TipoToken enum exists and has the correct values.
    """
    assert TipoToken.VERIFICACION_EMAIL.value == "verificacion_email"
    assert TipoToken.RESETEO_CONTRASENA.value == "reseteo_contrasena"
