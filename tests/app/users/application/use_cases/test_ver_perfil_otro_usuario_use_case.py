import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.users.application.use_cases.ver_perfil_otro_usuario_use_case import VerPerfilOtroUsuarioUseCase
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from app.users.application.dtos import UsuarioResponseDTO

@pytest.mark.asyncio
async def test_ver_perfil_otro_usuario_use_case_file_exists():
    """
    Tests if the ver perfil otro usuario use case file exists.
    """
    try:
        from app.users.application.use_cases import ver_perfil_otro_usuario_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/ver_perfil_otro_usuario_use_case.py")

@pytest.mark.asyncio
async def test_ver_perfil_otro_usuario_use_case_class_exists():
    """
    Tests if the VerPerfilOtroUsuarioUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.ver_perfil_otro_usuario_use_case import VerPerfilOtroUsuarioUseCase
    except ImportError:
        pytest.fail("VerPerfilOtroUsuarioUseCase class does not exist in ver_perfil_otro_usuario_use_case.py")

@pytest.mark.asyncio
async def test_admin_puede_ver_perfil_de_otro_usuario_exitosamente():
    """
    Un administrador puede ver el perfil de otro usuario exitosamente.
    """
    # Arrange
    admin_user = User(id=uuid4(), email="admin@example.com", contrasena_hasheada="hashed_admin_pass", nombre="Admin", apellidos="User", numero_telefono="123456789", rol=Rol.ADMIN)
    target_user_id = uuid4()
    target_user = User(id=target_user_id, email="user@example.com", contrasena_hasheada="hashed_user_pass", nombre="Test", apellidos="User", numero_telefono="987654321", rol=Rol.USUARIO)

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=target_user)

    mock_user_policy = Mock(spec=UserPolicy)
    mock_user_policy.es_administrador.return_value = True

    use_case = VerPerfilOtroUsuarioUseCase(mock_user_repository, mock_user_policy)

    # Act
    result = await use_case.execute(admin_user, target_user_id)

    # Assert
    mock_user_policy.es_administrador.assert_called_once_with(admin_user)
    mock_user_repository.buscar_por_id.assert_called_once_with(target_user_id)
    assert isinstance(result, UsuarioResponseDTO)
    assert result.id == target_user.id
    assert result.email == target_user.email

@pytest.mark.asyncio
async def test_no_admin_no_puede_ver_perfil_de_otro_usuario():
    """
    Un usuario no administrador no puede ver el perfil de otro usuario.
    """
    # Arrange
    non_admin_user = User(id=uuid4(), email="user@example.com", contrasena_hasheada="hashed_user_pass", nombre="Test", apellidos="User", numero_telefono="987654321", rol=Rol.USUARIO)
    target_user_id = uuid4()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()

    mock_user_policy = Mock(spec=UserPolicy)
    mock_user_policy.es_administrador.return_value = False

    use_case = VerPerfilOtroUsuarioUseCase(mock_user_repository, mock_user_policy)

    # Act & Assert
    with pytest.raises(ValueError, match="Not authorized to view other user's profile."):
        await use_case.execute(non_admin_user, target_user_id)

    mock_user_policy.es_administrador.assert_called_once_with(non_admin_user)
    mock_user_repository.buscar_por_id.assert_not_called()

@pytest.mark.asyncio
async def test_admin_intenta_ver_perfil_de_usuario_no_existente():
    """
    Un administrador intenta ver el perfil de un usuario que no existe.
    """
    # Arrange
    admin_user = User(id=uuid4(), email="admin@example.com", contrasena_hasheada="hashed_admin_pass", nombre="Admin", apellidos="User", numero_telefono="123456789", rol=Rol.ADMIN)
    non_existent_user_id = uuid4()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=None)

    mock_user_policy = Mock(spec=UserPolicy)
    mock_user_policy.es_administrador.return_value = True

    use_case = VerPerfilOtroUsuarioUseCase(mock_user_repository, mock_user_policy)

    # Act & Assert
    with pytest.raises(ValueError, match="User not found."):
        await use_case.execute(admin_user, non_existent_user_id)

    mock_user_policy.es_administrador.assert_called_once_with(admin_user)
    mock_user_repository.buscar_por_id.assert_called_once_with(non_existent_user_id)
