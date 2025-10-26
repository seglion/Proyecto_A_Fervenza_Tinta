import pytest
from typing import List, Optional
from uuid import UUID

from app.users.domain.entities import User

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

def test_iuserrepository_has_crear_method():
    """
    Tests if the IUserRepository interface has a 'crear' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'crear')
    assert 'user' in IUserRepository.crear.__annotations__
    assert IUserRepository.crear.__annotations__['user'] == User
    assert IUserRepository.crear.__annotations__['return'] == User

def test_iuserrepository_has_buscar_por_email_method():
    """
    Tests if the IUserRepository interface has a 'buscar_por_email' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'buscar_por_email')
    assert 'email' in IUserRepository.buscar_por_email.__annotations__
    assert IUserRepository.buscar_por_email.__annotations__['email'] == str
    assert IUserRepository.buscar_por_email.__annotations__['return'] == Optional[User]

def test_iuserrepository_has_buscar_por_id_method():
    """
    Tests if the IUserRepository interface has a 'buscar_por_id' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'buscar_por_id')
    assert 'user_id' in IUserRepository.buscar_por_id.__annotations__
    assert IUserRepository.buscar_por_id.__annotations__['user_id'] == UUID
    assert IUserRepository.buscar_por_id.__annotations__['return'] == Optional[User]

def test_iuserrepository_has_actualizar_method():
    """
    Tests if the IUserRepository interface has an 'actualizar' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'actualizar')
    assert 'user' in IUserRepository.actualizar.__annotations__
    assert IUserRepository.actualizar.__annotations__['user'] == User
    assert IUserRepository.actualizar.__annotations__['return'] == User

def test_iuserrepository_has_actualizar_contrasena_method():
    """
    Tests if the IUserRepository interface has an 'actualizar_contrasena' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'actualizar_contrasena')
    assert 'user_id' in IUserRepository.actualizar_contrasena.__annotations__
    assert IUserRepository.actualizar_contrasena.__annotations__['user_id'] == UUID
    assert 'contrasena_hasheada' in IUserRepository.actualizar_contrasena.__annotations__
    assert IUserRepository.actualizar_contrasena.__annotations__['contrasena_hasheada'] == str
    assert IUserRepository.actualizar_contrasena.__annotations__['return'] == None

def test_iuserrepository_has_desactivar_cuenta_method():
    """
    Tests if the IUserRepository interface has a 'desactivar_cuenta' abstract method.
    """
    from app.users.application.repositories.i_user_repository import IUserRepository
    assert hasattr(IUserRepository, 'desactivar_cuenta')
    assert 'user_id' in IUserRepository.desactivar_cuenta.__annotations__
    assert IUserRepository.desactivar_cuenta.__annotations__['user_id'] == UUID
    assert IUserRepository.desactivar_cuenta.__annotations__['return'] == None

def test_iuserrepository_has_buscar_todos_method():

    """

    Tests if the IUserRepository interface has a 'buscar_todos' abstract method.

    """

    from app.users.application.repositories.i_user_repository import IUserRepository

    assert hasattr(IUserRepository, 'buscar_todos')

    assert IUserRepository.buscar_todos.__annotations__['return'] == List[User]



def test_desactivar_usuarios_is_abstract_method():

        from src.app.users.application.repositories.i_user_repository import IUserRepository

        with pytest.raises(TypeError):

            class ConcreteUserRepository(IUserRepository):

                async def crear(self, user):

                    pass

                async def buscar_por_email(self, email):

                    pass

                async def buscar_por_id(self, user_id):

                    pass

                async def actualizar(self, user):

                    pass

                async def actualizar_contrasena(self, user_id, contrasena_hasheada):

                    pass

                async def desactivar_cuenta(self, user_id):

                    pass

                async def buscar_todos(self):

                    pass

                async def eliminar_por_id(self, user_id):

                    pass

            ConcreteUserRepository()

    


