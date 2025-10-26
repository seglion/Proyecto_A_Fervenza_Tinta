import pytest
from app.users.domain.value_objects import Rol, TipoToken

def test_rol_enum_exists_and_has_correct_values():
    """
    Tests if the Rol enum exists and has the correct values.
    """
    assert hasattr(Rol, 'ADMIN')
    assert hasattr(Rol, 'USUARIO')
    assert Rol.ADMIN.value == "ADMIN"
    assert Rol.USUARIO.value == "USUARIO"


def test_tipo_token_enum_exists_and_has_correct_values():
    """
    Tests if the TipoToken enum exists and has the correct values.
    """
    try:
        from app.users.domain.value_objects import TipoToken
    except ImportError:
        pytest.fail("TipoToken enum does not exist in value_objects.py")

    assert hasattr(TipoToken, 'VERIFICACION_EMAIL')
    assert hasattr(TipoToken, 'RESETEO_CONTRASENA')
    assert TipoToken.VERIFICACION_EMAIL.value == "VERIFICACION_EMAIL"
    assert TipoToken.RESETEO_CONTRASENA.value == "RESETEO_CONTRASENA"
