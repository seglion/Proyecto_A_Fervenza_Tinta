import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.application.use_cases.eliminar_usuario_use_case import EliminarUsuarioUseCase

def test_eliminar_usuario_use_case_file_exists():
    """
    Tests if the eliminar usuario use case file exists.
    """
    try:
        from app.users.application.use_cases import eliminar_usuario_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/eliminar_usuario_use_case.py")

def test_eliminar_usuario_use_case_class_exists():
    """
    Tests if the EliminarUsuarioUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.eliminar_usuario_use_case import EliminarUsuarioUseCase
    except ImportError:
        pytest.fail("EliminarUsuarioUseCase class does not exist in eliminar_usuario_use_case.py")

@pytest.mark.asyncio
async def test_eliminar_usuario_exitoso():
    """
    Tests the successful deletion of a user by an admin.
    """
    # Arrange
    admin_user = User(
        id=uuid4(),
        email="admin@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Admin",
        apellidos="User",
        numero_telefono="123456789",
        apodo="adminuser",
        rol=Rol.ADMIN
    )
    user_to_delete_id = uuid4()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.eliminar_por_id = AsyncMock()

    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = True

    use_case = EliminarUsuarioUseCase(mock_user_repository, user_policy)

    # Act
    await use_case.execute(admin_user, user_to_delete_id)

    # Assert
    mock_user_repository.eliminar_por_id.assert_called_once_with(user_to_delete_id)
