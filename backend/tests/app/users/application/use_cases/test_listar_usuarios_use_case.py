from app.users.application.exceptions import UnauthorizedException
import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.application.dtos import ListaUsuariosResponseDTO, UsuarioResponseDTO
from app.users.domain.entities import User
from app.users.application.use_cases.listar_usuarios_use_case import ListarUsuariosUseCase
from app.users.domain.value_objects import Rol

def test_listar_usuarios_use_case_file_exists():
    """
    Tests if the listar usuarios use case file exists.
    """
    try:
        from app.users.application.use_cases import listar_usuarios_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/listar_usuarios_use_case.py")

def test_listar_usuarios_use_case_class_exists():
    """
    Tests if the ListarUsuariosUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.listar_usuarios_use_case import ListarUsuariosUseCase
    except ImportError:
        pytest.fail("ListarUsuariosUseCase class does not exist in listar_usuarios_use_case.py")

@pytest.mark.asyncio
async def test_listar_usuarios_exitoso():
    """
    Tests the successful listing of users.
    """
    # Arrange
    mock_users = [
        User(id=uuid4(), email="test1@example.com", contrasena_hasheada="hashed_password", nombre="Test1", apellidos="User1", numero_telefono="111111111", apodo=None, rol=Rol.USUARIO),
        User(id=uuid4(), email="test2@example.com", contrasena_hasheada="hashed_password", nombre="Test2", apellidos="User2", numero_telefono="222222222", apodo=None, rol=Rol.ADMIN)
    ]

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_todos = AsyncMock(return_value=mock_users)

    user_policy = UserPolicy()

    use_case = ListarUsuariosUseCase(mock_user_repository, user_policy)

    # Act
    result = await use_case.execute(mock_users[1]) # Pass the admin user

    # Assert
    mock_user_repository.buscar_todos.assert_called_once()
    assert isinstance(result, ListaUsuariosResponseDTO)
    assert len(result.usuarios) == 2
    assert result.usuarios[0].email == mock_users[0].email
    assert result.usuarios[1].email == mock_users[1].email
    assert result.usuarios[0].rol == mock_users[0].rol.value
    assert result.usuarios[1].rol == mock_users[1].rol.value

@pytest.mark.asyncio
async def test_listar_usuarios_no_autorizado():
    """
    Tests that a ValueError is raised when the user is not authorized to list users.
    """
    # Arrange
    mock_user = User(id=uuid4(), email="test@example.com", contrasena_hasheada="hashed_password", nombre="Test", apellidos="User", numero_telefono="123456789", apodo=None, rol=Rol.USUARIO)

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_todos = AsyncMock()

    user_policy = UserPolicy()

    use_case = ListarUsuariosUseCase(mock_user_repository, user_policy)

    # Act & Assert
    with pytest.raises(UnauthorizedException):
        await use_case.execute(mock_user)

    mock_user_repository.buscar_todos.assert_not_called()