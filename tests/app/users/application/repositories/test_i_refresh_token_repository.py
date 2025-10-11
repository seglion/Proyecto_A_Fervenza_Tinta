import pytest
from abc import ABC

def test_refresh_token_repository_interface_file_exists():
    """
    Tests if the refresh token repository interface file exists.
    """
    try:
        from app.users.application.repositories import i_refresh_token_repository
    except ImportError:
        pytest.fail("Refresh token repository interface file does not exist: src/app/users/application/repositories/i_refresh_token_repository.py")

def test_refresh_token_repository_interface_class_exists():
    """
    Tests if the IRefreshTokenRepository class exists in the interface file.
    """
    try:
        from app.users.application.repositories.i_refresh_token_repository import IRefreshTokenRepository
        assert issubclass(IRefreshTokenRepository, ABC)
    except ImportError:
        pytest.fail("IRefreshTokenRepository class does not exist in i_refresh_token_repository.py")

def test_irefreshtokenrepository_has_invalidar_token_method():
    """
    Tests if the IRefreshTokenRepository interface has an 'invalidar_token' abstract method.
    """
    from app.users.application.repositories.i_refresh_token_repository import IRefreshTokenRepository
    assert hasattr(IRefreshTokenRepository, 'invalidar_token')
    assert 'refresh_token' in IRefreshTokenRepository.invalidar_token.__annotations__
    assert IRefreshTokenRepository.invalidar_token.__annotations__['refresh_token'] == str
    assert IRefreshTokenRepository.invalidar_token.__annotations__['return'] == None
