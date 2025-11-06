from app.users.application.exceptions import UnauthorizedException, UserNotFoundException
import pytest
from unittest.mock import Mock, AsyncMock
from app.users.domain.value_objects import Rol

def test_actualizar_mi_perfil_use_case_file_exists():
    """
    Tests if the actualizar mi perfil use case file exists.
    """
    try:
        from app.users.application.use_cases import actualizar_mi_perfil_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/actualizar_mi_perfil_use_case.py")

def test_actualizar_mi_perfil_use_case_class_exists():
    """
    Tests if the ActualizarMiPerfilUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.actualizar_mi_perfil_use_case import ActualizarMiPerfilUseCase
        from app.users.application.exceptions import UnauthorizedException, UserNotFoundException
    except ImportError:
        pytest.fail("ActualizarMiPerfilUseCase class does not exist in actualizar_mi_perfil_use_case.py")

@pytest.mark.asyncio
async def test_actualizar_mi_perfil_exitoso():
    """
    Tests the successful update of a user's profile.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.policies.user_policy import UserPolicy
    from app.users.application.dtos import ActualizarMiPerfilDTO, UsuarioResponseDTO
    from app.users.domain.entities import User
    from app.users.application.use_cases.actualizar_mi_perfil_use_case import ActualizarMiPerfilUseCase
    from uuid import uuid4

    user_id = uuid4()

    mock_user = User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo="testuser",
        email_verificado=True,
        esta_activo=True,
        rol=Rol.USUARIO
    )

    update_dto = ActualizarMiPerfilDTO(
        nombre="New Name",
        apellidos="New Lastname"
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=mock_user)
    mock_user_repository.actualizar = AsyncMock(return_value=mock_user) # Assume it returns the updated user

    user_policy = UserPolicy()

    use_case = ActualizarMiPerfilUseCase(mock_user_repository, user_policy)

    # Act
    result = await use_case.execute(mock_user, user_id, update_dto)

    # Assert
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_user_repository.actualizar.assert_called_once()
    updated_user = mock_user_repository.actualizar.call_args[0][0]
    assert updated_user.nombre == "New Name"
    assert updated_user.apellidos == "New Lastname"
    assert isinstance(result, UsuarioResponseDTO)
    assert result.nombre == "New Name"
    assert result.apellidos == "New Lastname"
    assert result.rol == updated_user.rol.value

@pytest.mark.asyncio
async def test_actualizar_mi_perfil_no_autorizado():
    """
    Tests that a ValueError is raised when the user is not authorized to update the profile.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.policies.user_policy import UserPolicy
    from app.users.domain.entities import User
    from app.users.application.dtos import ActualizarMiPerfilDTO
    from app.users.application.use_cases.actualizar_mi_perfil_use_case import ActualizarMiPerfilUseCase
    from uuid import uuid4

    current_user_id = uuid4()
    target_user_id = uuid4()

    mock_current_user = User(
        id=current_user_id,
        email="current@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Current",
        apellidos="User",
        numero_telefono="123456789",
        apodo="currentuser",
        email_verificado=True,
        esta_activo=True,
        rol=Rol.USUARIO
    )

    update_dto = ActualizarMiPerfilDTO(
        nombre="New Name"
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()
    mock_user_repository.actualizar = AsyncMock()

    user_policy = Mock(spec=UserPolicy)
    user_policy.actualizar_perfil.return_value = False # Not authorized

    use_case = ActualizarMiPerfilUseCase(mock_user_repository, user_policy)

    # Act & Assert
    with pytest.raises(UnauthorizedException, match="Not authorized to update this profile."):
        await use_case.execute(mock_current_user, target_user_id, update_dto)

    mock_user_repository.buscar_por_id.assert_not_called()
    mock_user_repository.actualizar.assert_not_called()

@pytest.mark.asyncio
async def test_actualizar_mi_perfil_usuario_no_encontrado():
    """
    Tests that a ValueError is raised when the user is not found.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.policies.user_policy import UserPolicy
    from app.users.domain.entities import User
    from app.users.application.dtos import ActualizarMiPerfilDTO
    from app.users.application.use_cases.actualizar_mi_perfil_use_case import ActualizarMiPerfilUseCase
    from uuid import uuid4

    user_id = uuid4()

    mock_user = User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo="testuser",
        email_verificado=True,
        esta_activo=True,
        rol=Rol.USUARIO
    )

    update_dto = ActualizarMiPerfilDTO(
        nombre="New Name"
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=None) # User not found
    mock_user_repository.actualizar = AsyncMock()

    user_policy = UserPolicy()

    use_case = ActualizarMiPerfilUseCase(mock_user_repository, user_policy)

    # Act & Assert
    with pytest.raises(UserNotFoundException, match="User not found."):
        await use_case.execute(mock_user, user_id, update_dto)

    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_user_repository.actualizar.assert_not_called()