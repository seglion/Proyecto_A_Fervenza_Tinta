import pytest
from unittest.mock import Mock, AsyncMock

from app.users.application.repositories.i_token_repository import ITokenRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.users.application.use_cases.cerrar_sesion_use_case import CerrarSesionUseCase

def test_cerrar_sesion_use_case_file_exists():
    """
    Tests if the cerrar sesion use case file exists.
    """
    try:
        from app.users.application.use_cases import cerrar_sesion_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/cerrar_sesion_use_case.py")

def test_cerrar_sesion_use_case_class_exists():
    """
    Tests if the CerrarSesionUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.cerrar_sesion_use_case import CerrarSesionUseCase
    except ImportError:
        pytest.fail("CerrarSesionUseCase class does not exist in cerrar_sesion_use_case.py")

@pytest.mark.asyncio
async def test_cerrar_sesion_exitoso():
    """
    Tests the successful session logout.
    """
    # Arrange
    refresh_token = "mock_refresh_token"
    hashed_refresh_token = "hashed_mock_refresh_token"

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.invalidar_token = AsyncMock()

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_refresh_token

    use_case = CerrarSesionUseCase(mock_token_repository, mock_password_hasher)

    # Act
    await use_case.execute(refresh_token)

    # Assert
    mock_password_hasher.hash.assert_called_once_with(refresh_token)
    mock_token_repository.invalidar_token.assert_called_once_with(hashed_refresh_token)
