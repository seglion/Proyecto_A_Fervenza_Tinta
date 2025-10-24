import pytest
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol

def test_cuota_policy_file_exists():
    """
    Tests if the cuota policy file exists.
    """
    try:
        from src.app.cuotas.application.policies import cuota_policy
    except ImportError:
        pytest.fail("Policy file does not exist: src/app/cuotas/application/policies/cuota_policy.py")

def test_es_administrador():
    policy = CuotaPolicy()
    admin_user = User(rol=Rol.ADMIN, email="admin@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="")
    regular_user = User(rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="")

    assert policy.es_administrador(admin_user) is True
    assert policy.es_administrador(regular_user) is False