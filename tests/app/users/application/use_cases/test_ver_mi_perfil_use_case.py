from app.users.application.exceptions import UnauthorizedException
import pytest
from unittest.mock import Mock, AsyncMock
from app.users.domain.value_objects import Rol

def test_ver_mi_perfil_use_case_file_exists():
    """
    Tests if the ver mi perfil use case file exists.
    """
    try:
        from app.users.application.use_cases import ver_mi_perfil_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/ver_mi_perfil_use_case.py")

def test_ver_mi_perfil_use_case_class_exists():
    """
    Tests if the VerMiPerfilUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.ver_mi_perfil_use_case import VerMiPerfilUseCase
    except ImportError:
        pytest.fail("VerMiPerfilUseCase class does not exist in ver_mi_perfil_use_case.py")

@pytest.mark.asyncio
async def test_ver_mi_perfil_exitoso():
    """
    Tests the successful retrieval of a user's profile.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.policies.user_policy import UserPolicy
    from app.users.application.dtos import UsuarioResponseDTO
    from app.users.domain.entities import User
    from app.users.application.use_cases.ver_mi_perfil_use_case import VerMiPerfilUseCase
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

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=mock_user)

    user_policy = UserPolicy()

    use_case = VerMiPerfilUseCase(mock_user_repository, user_policy)

    # Act
    result = await use_case.execute(mock_user, user_id)

    # Assert
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    assert isinstance(result, UsuarioResponseDTO)
    assert result.id == user_id
    assert result.email == mock_user.email
    assert result.nombre == mock_user.nombre
    assert result.apellidos == mock_user.apellidos
    assert result.apodo == mock_user.apodo
    assert result.numero_telefono == mock_user.numero_telefono
    assert result.esta_activo == mock_user.esta_activo
    assert result.rol == mock_user.rol.value

@pytest.mark.asyncio
async def test_ver_mi_perfil_no_autorizado():
    """
    Tests that a ValueError is raised when the user is not authorized to view the profile.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.policies.user_policy import UserPolicy
    from app.users.application.dtos import UsuarioResponseDTO
    from app.users.domain.entities import User
    from app.users.application.use_cases.ver_mi_perfil_use_case import VerMiPerfilUseCase
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

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()

    user_policy = Mock(spec=UserPolicy)
    user_policy.ver_perfil.return_value = False # Not authorized

    use_case = VerMiPerfilUseCase(mock_user_repository, user_policy)

    # Act & Assert
    with pytest.raises(UnauthorizedException):
        await use_case.execute(mock_current_user, target_user_id)

    mock_user_repository.buscar_por_id.assert_not_called()
