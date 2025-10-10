import pytest
from app.users.domain.entities import Token
from typing import Optional
from uuid import UUID

def test_token_repository_interface_file_exists():
    """
    Tests if the token repository interface file exists.
    """
    try:
        from app.users.application.repositories import i_token_repository
    except ImportError:
        pytest.fail("Token repository interface file does not exist: src/app/users/application/repositories/i_token_repository.py")

def test_token_repository_interface_class_exists():
    """
    Tests if the ITokenRepository class exists in the interface file.
    """
    try:
        from app.users.application.repositories.i_token_repository import ITokenRepository
    except ImportError:
        pytest.fail("ITokenRepository class does not exist in i_token_repository.py")

def test_itokenrepository_has_crear_method():
    """
    Tests if the ITokenRepository interface has a 'crear' abstract method.
    """
    from app.users.application.repositories.i_token_repository import ITokenRepository
    assert hasattr(ITokenRepository, 'crear')
    assert 'token' in ITokenRepository.crear.__annotations__
    assert ITokenRepository.crear.__annotations__['token'] == Token
    assert ITokenRepository.crear.__annotations__['return'] == Token

def test_itokenrepository_has_buscar_por_hash_method():
    """
    Tests if the ITokenRepository interface has a 'buscar_por_hash' abstract method.
    """
    from app.users.application.repositories.i_token_repository import ITokenRepository
    assert hasattr(ITokenRepository, 'buscar_por_hash')
    assert 'hash_token' in ITokenRepository.buscar_por_hash.__annotations__
    assert ITokenRepository.buscar_por_hash.__annotations__['hash_token'] == str
    assert ITokenRepository.buscar_por_hash.__annotations__['return'] == Optional[Token]

def test_itokenrepository_has_actualizar_method():
    """
    Tests if the ITokenRepository interface has an 'actualizar' abstract method.
    """
    from app.users.application.repositories.i_token_repository import ITokenRepository
    assert hasattr(ITokenRepository, 'actualizar')
    assert 'token' in ITokenRepository.actualizar.__annotations__
    assert ITokenRepository.actualizar.__annotations__['token'] == Token
    assert ITokenRepository.actualizar.__annotations__['return'] == Token
