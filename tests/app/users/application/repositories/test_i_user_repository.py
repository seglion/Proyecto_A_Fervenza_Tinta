import pytest
from app.users.domain.entities import User, Role
from typing import Optional, List
from uuid import UUID

def test_user_repository_interface_file_exists():
    """
    Tests if the user repository interface file exists.
    """
    try:
        from app.users.application.repositories import i_user_repository
    except ImportError:
        pytest.fail("User repository interface file does not exist: src/app/users/application/repositories/i_user_repository.py")

def test_user_repository_interface_class_exists():
    """
    Tests if the IUserRepository class exists in the interface file.
    """
    try:
        from app.users.application.repositories.i_user_repository import IUserRepository
    except ImportError:
        pytest.fail("IUserRepository class does not exist in i_user_repository.py")

def test_iuserrepository_has_buscar_por_email_method():
    """
    Tests if the IUserRepository interface has a 'buscar_por_email' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'buscar_por_email')
    assert 'email' in IUserRepository.buscar_por_email.__annotations__
    assert IUserRepository.buscar_por_email.__annotations__['email'] == str
    assert IUserRepository.buscar_por_email.__annotations__['return'] == Optional[User]

def test_iuserrepository_has_crear_method():
    """
    Tests if the IUserRepository interface has a 'crear' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'crear')
    assert 'user' in IUserRepository.crear.__annotations__
    assert IUserRepository.crear.__annotations__['user'] == User
    assert IUserRepository.crear.__annotations__['return'] == User

def test_iuserrepository_has_actualizar_method():
    """
    Tests if the IUserRepository interface has an 'actualizar' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'actualizar')
    assert 'user' in IUserRepository.actualizar.__annotations__
    assert IUserRepository.actualizar.__annotations__['user'] == User
    assert IUserRepository.actualizar.__annotations__['return'] == User

def test_iuserrepository_has_buscar_por_id_method():
    """
    Tests if the IUserRepository interface has a 'buscar_por_id' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'buscar_por_id')
    assert 'user_id' in IUserRepository.buscar_por_id.__annotations__
    assert IUserRepository.buscar_por_id.__annotations__['user_id'] == UUID
    assert IUserRepository.buscar_por_id.__annotations__['return'] == Optional[User]

def test_iuserrepository_has_eliminar_por_id_method():
    """
    Tests if the IUserRepository interface has an 'eliminar_por_id' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'eliminar_por_id')
    assert 'user_id' in IUserRepository.eliminar_por_id.__annotations__
    assert IUserRepository.eliminar_por_id.__annotations__['user_id'] == UUID
    assert IUserRepository.eliminar_por_id.__annotations__['return'] == None

def test_iuserrepository_has_desactivar_cuenta_method():
    """
    Tests if the IUserRepository interface has a 'desactivar_cuenta' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'desactivar_cuenta')
    assert 'user_id' in IUserRepository.desactivar_cuenta.__annotations__
    assert IUserRepository.desactivar_cuenta.__annotations__['user_id'] == UUID
    assert IUserRepository.desactivar_cuenta.__annotations__['return'] == None

def test_iuserrepository_has_actualizar_contrasena_method():
    """
    Tests if the IUserRepository interface has an 'actualizar_contrasena' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'actualizar_contrasena')
    assert 'user_id' in IUserRepository.actualizar_contrasena.__annotations__
    assert IUserRepository.actualizar_contrasena.__annotations__['user_id'] == UUID
    assert 'nueva_contrasena_hasheada' in IUserRepository.actualizar_contrasena.__annotations__
    assert IUserRepository.actualizar_contrasena.__annotations__['nueva_contrasena_hasheada'] == str
    assert IUserRepository.actualizar_contrasena.__annotations__['return'] == None

def test_iuserrepository_has_actualizar_roles_method():
    """
    Tests if the IUserRepository interface has an 'actualizar_roles' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'actualizar_roles')
    assert 'user_id' in IUserRepository.actualizar_roles.__annotations__
    assert IUserRepository.actualizar_roles.__annotations__['user_id'] == UUID
    assert 'roles' in IUserRepository.actualizar_roles.__annotations__
    assert IUserRepository.actualizar_roles.__annotations__['roles'] == List[Role]
    assert IUserRepository.actualizar_roles.__annotations__['return'] == None

def test_iuserrepository_has_buscar_todos_method():
    """
    Tests if the IUserRepository interface has a 'buscar_todos' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'buscar_todos')
    assert IUserRepository.buscar_todos.__annotations__['return'] == List[User]
