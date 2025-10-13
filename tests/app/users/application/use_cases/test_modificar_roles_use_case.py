import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.application.use_cases.modificar_roles_use_case import ModificarRolesUseCase

def test_modificar_roles_use_case_file_exists():
    """
    Tests if the modificar roles use case file exists.
    """
    try:
        from app.users.application.use_cases import modificar_roles_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/modificar_roles_use_case.py")

def test_modificar_roles_use_case_class_exists():
    """
    Tests if the ModificarRolesUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.modificar_roles_use_case import ModificarRolesUseCase
    except ImportError:
        pytest.fail("ModificarRolesUseCase class does not exist in modificar_roles_use_case.py")

@pytest.mark.asyncio
async def test_modificar_rol_exitoso():
    """
    Tests the successful modification of a user's role by an admin.
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
    user_to_modify_id = uuid4()
    user_to_modify = User(
        id=user_to_modify_id,
        email="user@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Normal",
        apellidos="User",
        numero_telefono="987654321",
        apodo="normaluser",
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=user_to_modify)
    mock_user_repository.actualizar = AsyncMock(return_value=user_to_modify)

    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = True

    use_case = ModificarRolesUseCase(mock_user_repository, user_policy)

    # Act
    await use_case.execute(admin_user, user_to_modify_id, Rol.ADMIN)

    # Assert
    mock_user_repository.buscar_por_id.assert_called_once_with(user_to_modify_id)
    mock_user_repository.actualizar.assert_called_once()
    updated_user = mock_user_repository.actualizar.call_args[0][0]
    assert updated_user.rol == Rol.ADMIN
