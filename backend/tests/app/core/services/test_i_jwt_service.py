import pytest
from abc import ABC
from typing import Tuple
from uuid import UUID
from app.core.services.i_jwt_service import IJWTService

def test_jwt_service_interface_file_exists():
    """
    Tests if the JWT service interface file exists.
    """
    try:
        from app.core.services import i_jwt_service
    except ImportError:
        pytest.fail("JWT service interface file does not exist: src/app/core/services/i_jwt_service.py")

def test_jwt_service_interface_class_exists():
    """
    Tests if the IJWTService class exists in the interface file and is an ABC.
    """
    try:
        from app.core.services.i_jwt_service import IJWTService
        assert issubclass(IJWTService, ABC)
    except ImportError:
        pytest.fail("IJWTService class does not exist in i_jwt_service.py")

def test_ijwt_service_has_generar_tokens_method():
    """
    Tests if the IJWTService interface has a 'generar_tokens' abstract method.
    """
    assert hasattr(IJWTService, 'generar_tokens')
    assert 'user_id' in IJWTService.generar_tokens.__annotations__
    assert IJWTService.generar_tokens.__annotations__['user_id'] == UUID
    assert 'roles' in IJWTService.generar_tokens.__annotations__
    assert IJWTService.generar_tokens.__annotations__['roles'] == list[str]
    assert IJWTService.generar_tokens.__annotations__['return'] == Tuple[str, str]

def test_ijwt_service_has_validar_access_token_method():
    """
    Tests if the IJWTService interface has a 'validar_access_token' abstract method.
    """
    assert hasattr(IJWTService, 'validar_access_token')
    assert 'token' in IJWTService.validar_access_token.__annotations__
    assert IJWTService.validar_access_token.__annotations__['token'] == str
    assert IJWTService.validar_access_token.__annotations__['return'] == UUID

def test_ijwt_service_has_validar_refresh_token_method():
    """
    Tests if the IJWTService interface has a 'validar_refresh_token' abstract method.
    """
    assert hasattr(IJWTService, 'validar_refresh_token')
    assert 'token' in IJWTService.validar_refresh_token.__annotations__
    assert IJWTService.validar_refresh_token.__annotations__['token'] == str
    assert IJWTService.validar_refresh_token.__annotations__['return'] == UUID
