import pytest
from unittest.mock import Mock, AsyncMock
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.core.security.i_password_hasher import IPasswordHasher


def test_refrescar_sesion_use_case_file_exists():
    """
    Tests if the refrescar sesion use case file exists.
    """
    try:
        from app.users.application.use_cases import refrescar_sesion_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/refrescar_sesion_use_case.py")

def test_refrescar_sesion_use_case_class_exists():
    """
    Tests if the RefrescarSesionUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.refrescar_sesion_use_case import RefrescarSesionUseCase
    except ImportError:
        pytest.fail("RefrescarSesionUseCase class does not exist in refrescar_sesion_use_case.py")

@pytest.mark.asyncio
async def test_refrescar_sesion_exitoso():
    """
    Tests the successful session refresh.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.core.services.i_jwt_service import IJWTService
    from app.users.application.dtos import TokensDTO
    from app.users.domain.entities import User
    from app.users.application.use_cases.refrescar_sesion_use_case import RefrescarSesionUseCase
    from uuid import uuid4
    from app.users.domain.value_objects import Rol

    user_id = uuid4()
    refresh_token = "mock_refresh_token"
    new_access_token = "new_mock_access_token"
    hashed_refresh_token = "hashed_mock_refresh_token"

    mock_user = User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
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

    mock_jwt_service = Mock(spec=IJWTService)
    mock_jwt_service.validar_refresh_token.return_value = user_id
    mock_jwt_service.generar_tokens.return_value = (new_access_token, refresh_token) # We only care about the new access token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.invalidar_token = AsyncMock()
    mock_token_repository.crear = AsyncMock()

    mock_password_hasher = Mock(spec=IPasswordHasher)
    use_case = RefrescarSesionUseCase(mock_user_repository, mock_jwt_service, mock_token_repository, mock_password_hasher)

    # Act
    result = await use_case.execute(refresh_token)

    # Assert
    mock_jwt_service.validar_refresh_token.assert_called_once_with(refresh_token)
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_jwt_service.generar_tokens.assert_called_once_with(user_id, [mock_user.rol.value])
    assert isinstance(result, TokensDTO)
    assert result.access_token == new_access_token
    assert result.refresh_token == refresh_token
    assert result.token_type == "bearer"

@pytest.mark.asyncio
async def test_refrescar_sesion_token_invalido():
    """
    Tests that a ValueError is raised when the refresh token is invalid.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.core.services.i_jwt_service import IJWTService
    from app.users.application.use_cases.refrescar_sesion_use_case import RefrescarSesionUseCase
    from unittest.mock import AsyncMock

    refresh_token = "invalid_refresh_token"

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()

    mock_jwt_service = Mock(spec=IJWTService)
    mock_jwt_service.validar_refresh_token.side_effect = ValueError("Invalid token or inactive user.")
    mock_jwt_service.generar_tokens = Mock()

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_password_hasher = Mock(spec=IPasswordHasher)

    use_case = RefrescarSesionUseCase(mock_user_repository, mock_jwt_service, mock_token_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid token or inactive user."):
        await use_case.execute(refresh_token)

    mock_jwt_service.validar_refresh_token.assert_called_once_with(refresh_token)
    mock_user_repository.buscar_por_id.assert_not_called()
    mock_jwt_service.generar_tokens.assert_not_called()

@pytest.mark.asyncio
async def test_refrescar_sesion_usuario_no_encontrado():
    """
    Tests that a ValueError is raised when the user is not found.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.core.services.i_jwt_service import IJWTService
    from app.users.application.use_cases.refrescar_sesion_use_case import RefrescarSesionUseCase
    from uuid import uuid4
    from unittest.mock import AsyncMock
    from app.users.domain.value_objects import Rol

    user_id = uuid4()
    refresh_token = "mock_refresh_token"

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=None)
    mock_jwt_service = Mock(spec=IJWTService)
    mock_jwt_service.validar_refresh_token.return_value = user_id
    mock_jwt_service.generar_tokens.return_value = ("mock_access_token", "mock_new_refresh_token")



    mock_token_repository = Mock(spec=ITokenRepository)

    mock_password_hasher = Mock(spec=IPasswordHasher)



    use_case = RefrescarSesionUseCase(mock_user_repository, mock_jwt_service, mock_token_repository, mock_password_hasher)
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid token or inactive user."):
        await use_case.execute(refresh_token)

    mock_jwt_service.validar_refresh_token.assert_called_once_with(refresh_token)
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_jwt_service.generar_tokens.assert_not_called()

@pytest.mark.asyncio
async def test_refrescar_sesion_cuenta_inactiva():
    """
    Tests that a ValueError is raised when the user account is inactive.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.core.services.i_jwt_service import IJWTService
    from app.users.domain.entities import User
    from app.users.application.use_cases.refrescar_sesion_use_case import RefrescarSesionUseCase
    from uuid import uuid4
    from unittest.mock import AsyncMock
    from app.users.domain.value_objects import Rol

    user_id = uuid4()
    refresh_token = "mock_refresh_token"

    mock_user = User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        email_verificado=True,
        esta_activo=False, # Account is inactive
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=mock_user)

    mock_jwt_service = Mock(spec=IJWTService)
    mock_jwt_service.validar_refresh_token.return_value = user_id

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_password_hasher = Mock(spec=IPasswordHasher)

    use_case = RefrescarSesionUseCase(mock_user_repository, mock_jwt_service, mock_token_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid token or inactive user."):
        await use_case.execute(refresh_token)

    mock_jwt_service.validar_refresh_token.assert_called_once_with(refresh_token)
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_jwt_service.generar_tokens.assert_not_called()