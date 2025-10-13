import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.users.application.use_cases.forzar_reseteo_use_case import ForzarReseteoUseCase
from app.core.services.i_email_service import IEmailService
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.core.security.i_password_hasher import IPasswordHasher

def test_forzar_reseteo_use_case_file_exists():
    """
    Tests if the forzar reseteo use case file exists.
    """
    try:
        from app.users.application.use_cases import forzar_reseteo_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/forzar_reseteo_use_case.py")

def test_forzar_reseteo_use_case_class_exists():
    """
    Tests if the ForzarReseteoUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.forzar_reseteo_use_case import ForzarReseteoUseCase
    except ImportError:
        pytest.fail("ForzarReseteoUseCase class does not exist in forzar_reseteo_use_case.py")

@pytest.mark.asyncio
async def test_forzar_reseteo_exitoso():
    """
    Tests the successful forced password reset by an admin.
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
    user_to_reset_id = uuid4()
    user_to_reset = User(
        id=user_to_reset_id,
        email="user@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Normal",
        apellidos="User",
        numero_telefono="987654321",
        apodo="normaluser",
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=user_to_reset)

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.crear = AsyncMock()

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = "hashed_token"

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.send_reset_password_email = AsyncMock()

    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = True

    use_case = ForzarReseteoUseCase(mock_user_repository, mock_token_repository, mock_password_hasher, user_policy, mock_email_service)

    # Act
    await use_case.execute(admin_user, user_to_reset_id)

    # Assert
    mock_user_repository.buscar_por_id.assert_called_once_with(user_to_reset_id)
    mock_token_repository.crear.assert_called_once()
    mock_email_service.send_reset_password_email.assert_called_once()
