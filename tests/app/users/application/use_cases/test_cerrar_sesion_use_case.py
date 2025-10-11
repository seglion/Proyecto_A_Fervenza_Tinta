import pytest
from unittest.mock import Mock, AsyncMock

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
    from app.users.application.repositories.i_refresh_token_repository import IRefreshTokenRepository
    from app.users.application.use_cases.cerrar_sesion_use_case import CerrarSesionUseCase

    refresh_token = "mock_refresh_token"

    mock_refresh_token_repository = Mock(spec=IRefreshTokenRepository)
    mock_refresh_token_repository.invalidar_token = AsyncMock()

    use_case = CerrarSesionUseCase(mock_refresh_token_repository)

    # Act
    await use_case.execute(refresh_token)

    # Assert
    mock_refresh_token_repository.invalidar_token.assert_called_once_with(refresh_token)
