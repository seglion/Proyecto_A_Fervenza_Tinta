import pytest
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.cuotas.application.dtos import UsuarioPolicyDTO
from src.app.users.domain.value_objects import Rol

@pytest.fixture
def cuota_policy():
    return CuotaPolicy()

def test_es_administrador_true(cuota_policy):
    user = UsuarioPolicyDTO(rol=Rol.ADMIN, esta_activo=True)
    assert cuota_policy.es_administrador(user) is True

def test_es_administrador_false(cuota_policy):
    user = UsuarioPolicyDTO(rol=Rol.USUARIO, esta_activo=True)
    assert cuota_policy.es_administrador(user) is False

def test_puede_ver_estado_pago_usuario_activo(cuota_policy):
    user = UsuarioPolicyDTO(rol=Rol.USUARIO, esta_activo=True)
    assert cuota_policy.puede_ver_estado_pago(user) is True

def test_puede_ver_estado_pago_usuario_inactivo(cuota_policy):
    user = UsuarioPolicyDTO(rol=Rol.USUARIO, esta_activo=False)
    assert cuota_policy.puede_ver_estado_pago(user) is False

