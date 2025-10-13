import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.application.use_cases.activar_desactivar_usuario_use_case import ActivarDesactivarUsuarioUseCase

def test_activar_desactivar_usuario_use_case_file_exists():
    """
    Tests if the activar/desactivar usuario use case file exists.
    """
    try:
        from app.users.application.use_cases import activar_desactivar_usuario_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/activar_desactivar_usuario_use_case.py")

def test_activar_desactivar_usuario_use_case_class_exists():
    """
    Tests if the ActivarDesactivarUsuarioUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.activar_desactivar_usuario_use_case import ActivarDesactivarUsuarioUseCase
    except ImportError:
        pytest.fail("ActivarDesactivarUsuarioUseCase class does not exist in activar_desactivar_usuario_use_case.py")

@pytest.mark.asyncio
async def test_desactivar_usuario_exitoso():
    """
    Tests the successful deactivation of a user by an admin.
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
    user_to_deactivate_id = uuid4()
    user_to_deactivate = User(
        id=user_to_deactivate_id,
        email="active@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Active",
        apellidos="User",
        numero_telefono="987654321",
        apodo="activeuser",
        esta_activo=True,
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=user_to_deactivate)
    mock_user_repository.actualizar = AsyncMock(return_value=user_to_deactivate)

    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = True

    use_case = ActivarDesactivarUsuarioUseCase(mock_user_repository, user_policy)

    # Act
    await use_case.execute(admin_user, user_to_deactivate_id, False)

    # Assert
    mock_user_repository.buscar_por_id.assert_called_once_with(user_to_deactivate_id)
    mock_user_repository.actualizar.assert_called_once()
    updated_user = mock_user_repository.actualizar.call_args[0][0]
    assert updated_user.esta_activo is False

@pytest.mark.asyncio
async def test_activar_usuario_exitoso():
    """
    Tests the successful activation of a user by an admin.
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
    user_to_activate_id = uuid4()
    user_to_activate = User(
        id=user_to_activate_id,
        email="inactive@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Inactive",
        apellidos="User",
        numero_telefono="987654321",
        apodo="inactiveuser",
        esta_activo=False,
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=user_to_activate)
    mock_user_repository.actualizar = AsyncMock(return_value=user_to_activate)

    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = True

    use_case = ActivarDesactivarUsuarioUseCase(mock_user_repository, user_policy)

    # Act
    await use_case.execute(admin_user, user_to_activate_id, True)

    # Assert
    mock_user_repository.buscar_por_id.assert_called_once_with(user_to_activate_id)
    mock_user_repository.actualizar.assert_called_once()
    updated_user = mock_user_repository.actualizar.call_args[0][0]
    assert updated_user.esta_activo is True

@pytest.mark.asyncio
async def test_activar_desactivar_usuario_no_autorizado():
    """
    Tests that a ValueError is raised when a non-admin user tries to change user status.
    """
    # Arrange
    non_admin_user = User(
        id=uuid4(),
        email="user@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Normal",
        apellidos="User",
        numero_telefono="111111111",
        apodo="normaluser",
        rol=Rol.USUARIO
    )
    target_user_id = uuid4()

    mock_user_repository = Mock(spec=IUserRepository)
    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = False

    use_case = ActivarDesactivarUsuarioUseCase(mock_user_repository, user_policy)

    # Act & Assert
    with pytest.raises(ValueError, match="Not authorized to change user status."):
        await use_case.execute(non_admin_user, target_user_id, False)

@pytest.mark.asyncio
async def test_activar_desactivar_usuario_no_encontrado():
    """
    Tests that a ValueError is raised when the user to modify is not found.
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
    non_existent_user_id = uuid4()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=None)

    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = True

    use_case = ActivarDesactivarUsuarioUseCase(mock_user_repository, user_policy)

    # Act & Assert
    with pytest.raises(ValueError, match="User not found."):
        await use_case.execute(admin_user, non_existent_user_id, True)