import pytest
from unittest.mock import Mock, AsyncMock
from app.users.domain.value_objects import Rol

def test_cambiar_contrasena_use_case_file_exists():
    """
    Tests if the cambiar contrasena use case file exists.
    """
    try:
        from app.users.application.use_cases import cambiar_contrasena_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/cambiar_contrasena_use_case.py")

def test_cambiar_contrasena_use_case_class_exists():
    """
    Tests if the CambiarContrasenaUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.cambiar_contrasena_use_case import CambiarContrasenaUseCase
    except ImportError:
        pytest.fail("CambiarContrasenaUseCase class does not exist in cambiar_contrasena_use_case.py")

@pytest.mark.asyncio
async def test_cambiar_contrasena_exitoso():
    """
    Tests the successful password change.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.policies.user_policy import UserPolicy
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.users.application.dtos import CambiarContrasenaDTO
    from app.users.domain.entities import User
    from app.users.application.use_cases.cambiar_contrasena_use_case import CambiarContrasenaUseCase
    from uuid import uuid4

    user_id = uuid4()
    old_password = "old_password"
    new_password = "new_password"
    hashed_old_password = "hashed_old_password"
    hashed_new_password = "hashed_new_password"

    mock_user = User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada=hashed_old_password,
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        email_verificado=True,
        esta_activo=True,
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=mock_user)
    mock_user_repository.actualizar_contrasena = AsyncMock()

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.verify.return_value = True # Old password is correct
    mock_password_hasher.hash.return_value = hashed_new_password

    user_policy = UserPolicy()

    use_case = CambiarContrasenaUseCase(mock_user_repository, mock_password_hasher, user_policy)

    dto = CambiarContrasenaDTO(contrasena_antigua=old_password, contrasena_nueva=new_password)

    # Act
    await use_case.execute(mock_user, user_id, dto)

    # Assert
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_password_hasher.verify.assert_called_once_with(old_password, hashed_old_password)
    mock_password_hasher.hash.assert_called_once_with(new_password)
    mock_user_repository.actualizar_contrasena.assert_called_once_with(user_id, hashed_new_password)
