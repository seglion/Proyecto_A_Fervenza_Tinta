import pytest
from app.users.domain.entities import Role
from typing import Optional, List

def test_role_repository_interface_file_exists():
    """
    Tests if the role repository interface file exists.
    """
    try:
        from app.users.application.repositories import i_role_repository
    except ImportError:
        pytest.fail("Role repository interface file does not exist: src/app/users/application/repositories/i_role_repository.py")

def test_role_repository_interface_class_exists():
    """
    Tests if the IRoleRepository class exists in the interface file.
    """
    try:
        from app.users.application.repositories.i_role_repository import IRoleRepository
    except ImportError:
        pytest.fail("IRoleRepository class does not exist in i_role_repository.py")

def test_irolepository_has_crear_method():
    """
    Tests if the IRoleRepository interface has a 'crear' abstract method.
    """
    from app.users.application.repositories.i_role_repository import IRoleRepository
    assert hasattr(IRoleRepository, 'crear')
    assert 'role' in IRoleRepository.crear.__annotations__
    assert IRoleRepository.crear.__annotations__['role'] == Role
    assert IRoleRepository.crear.__annotations__['return'] == Role

def test_irolepository_has_buscar_por_id_method():
    """
    Tests if the IRoleRepository interface has a 'buscar_por_id' abstract method.
    """
    from app.users.application.repositories.i_role_repository import IRoleRepository
    assert hasattr(IRoleRepository, 'buscar_por_id')
    assert 'role_id' in IRoleRepository.buscar_por_id.__annotations__
    assert IRoleRepository.buscar_por_id.__annotations__['role_id'] == int
    assert IRoleRepository.buscar_por_id.__annotations__['return'] == Optional[Role]

def test_irolepository_has_buscar_por_nombre_method():
    """
    Tests if the IRoleRepository interface has a 'buscar_por_nombre' abstract method.
    """
    from app.users.application.repositories.i_role_repository import IRoleRepository
    assert hasattr(IRoleRepository, 'buscar_por_nombre')
    assert 'nombre' in IRoleRepository.buscar_por_nombre.__annotations__
    assert IRoleRepository.buscar_por_nombre.__annotations__['nombre'] == str
    assert IRoleRepository.buscar_por_nombre.__annotations__['return'] == Optional[Role]

def test_irolepository_has_buscar_todos_method():
    """
    Tests if the IRoleRepository interface has a 'buscar_todos' abstract method.
    """
    from app.users.application.repositories.i_role_repository import IRoleRepository
    assert hasattr(IRoleRepository, 'buscar_todos')
    assert IRoleRepository.buscar_todos.__annotations__['return'] == List[Role]
