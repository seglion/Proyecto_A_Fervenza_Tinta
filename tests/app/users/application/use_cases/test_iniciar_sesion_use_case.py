import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.users.application.repositories.i_user_repository import IUserRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.core.services.i_jwt_service import IJWTService
from app.users.application.dtos import IniciarSesionDTO, TokensDTO
from app.users.domain.entities import User
from app.users.application.use_cases.iniciar_sesion_use_case import IniciarSesionUseCase
from app.users.domain.value_objects import Rol

def test_iniciar_sesion_use_case_file_exists():
    """
    Tests if the iniciar sesion use case file exists.
    """
    try:
        from app.users.application.use_cases import iniciar_sesion_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/iniciar_sesion_use_case.py")

def test_iniciar_sesion_use_case_class_exists():
    """
    Tests if the IniciarSesionUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.iniciar_sesion_use_case import IniciarSesionUseCase
    except ImportError:
        pytest.fail("IniciarSesionUseCase class does not exist in iniciar_sesion_use_case.py")

@pytest.mark.asyncio
async def test_iniciar_sesion_exitoso():
    """
    Tests the successful user login.
    """
    # Arrange
    user_id = uuid4()
    user_email = "test@example.com"
    plain_password = "password123"
    hashed_password = "hashed_password"
    access_token = "mock_access_token"
    refresh_token = "mock_refresh_token"

    mock_user = User(
        id=user_id,
        email=user_email,
        contrasena_hasheada=hashed_password,
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        email_verificado=True, # User must be verified
        esta_activo=True, # User must be active
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=mock_user)

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.verify.return_value = True

    mock_jwt_service = Mock(spec=IJWTService)
    mock_jwt_service.generar_tokens.return_value = (access_token, refresh_token)

    use_case = IniciarSesionUseCase(mock_user_repository, mock_password_hasher, mock_jwt_service)

    dto = IniciarSesionDTO(email=user_email, contrasena=plain_password)

    # Act
    result = await use_case.execute(dto)

    # Assert
    mock_user_repository.buscar_por_email.assert_called_once_with(user_email)
    mock_password_hasher.verify.assert_called_once_with(plain_password, hashed_password)
    mock_jwt_service.generar_tokens.assert_called_once_with(user_id, [mock_user.rol.value])
    assert isinstance(result, TokensDTO)
    assert result.access_token == access_token
    assert result.refresh_token == refresh_token
    assert result.token_type == "bearer"

@pytest.mark.asyncio
async def test_iniciar_sesion_usuario_no_encontrado():
    """
    Tests that a ValueError is raised when the user is not found.
    """
    # Arrange
    user_email = "nonexistent@example.com"
    plain_password = "password123"

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=None)

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_jwt_service = Mock(spec=IJWTService)

    use_case = IniciarSesionUseCase(mock_user_repository, mock_password_hasher, mock_jwt_service)

    dto = IniciarSesionDTO(email=user_email, contrasena=plain_password)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid credentials."):
        await use_case.execute(dto)

    mock_user_repository.buscar_por_email.assert_called_once_with(user_email)
    mock_password_hasher.verify.assert_not_called()
    mock_jwt_service.generar_tokens.assert_not_called()

@pytest.mark.asyncio
async def test_iniciar_sesion_contrasena_incorrecta():
    """
    Tests that a ValueError is raised when the password is incorrect.
    """
    # Arrange
    user_id = uuid4()
    user_email = "test@example.com"
    plain_password = "wrong_password"
    hashed_password = "correct_hashed_password"

    mock_user = User(
        id=user_id,
        email=user_email,
        contrasena_hasheada=hashed_password,
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        email_verificado=True,
        esta_activo=True,
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=mock_user)

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.verify.return_value = False # Incorrect password

    mock_jwt_service = Mock(spec=IJWTService)

    use_case = IniciarSesionUseCase(mock_user_repository, mock_password_hasher, mock_jwt_service)

    dto = IniciarSesionDTO(email=user_email, contrasena=plain_password)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid credentials."):
        await use_case.execute(dto)

    mock_user_repository.buscar_por_email.assert_called_once_with(user_email)
    mock_password_hasher.verify.assert_called_once_with(plain_password, hashed_password)
    mock_jwt_service.generar_tokens.assert_not_called()

@pytest.mark.asyncio
async def test_iniciar_sesion_email_no_verificado():
    """
    Tests that a ValueError is raised when the user's email is not verified.
    """
    # Arrange
    user_id = uuid4()
    user_email = "test@example.com"
    plain_password = "password123"
    hashed_password = "hashed_password"

    mock_user = User(
        id=user_id,
        email=user_email,
        contrasena_hasheada=hashed_password,
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        email_verificado=False, # Email not verified
        esta_activo=True,
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=mock_user)

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.verify.return_value = True

    mock_jwt_service = Mock(spec=IJWTService)

    use_case = IniciarSesionUseCase(mock_user_repository, mock_password_hasher, mock_jwt_service)

    dto = IniciarSesionDTO(email=user_email, contrasena=plain_password)

    # Act & Assert
    with pytest.raises(ValueError, match="Email not verified."):
        await use_case.execute(dto)

    mock_user_repository.buscar_por_email.assert_called_once_with(user_email)
    mock_password_hasher.verify.assert_called_once_with(plain_password, hashed_password)
    mock_jwt_service.generar_tokens.assert_not_called()

@pytest.mark.asyncio
async def test_iniciar_sesion_cuenta_inactiva():
    """
    Tests that a ValueError is raised when the user account is inactive.
    """
    # Arrange
    user_id = uuid4()
    user_email = "test@example.com"
    plain_password = "password123"
    hashed_password = "hashed_password"

    mock_user = User(
        id=user_id,
        email=user_email,
        contrasena_hasheada=hashed_password,
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        email_verificado=True,
        esta_activo=False, # Account is inactive
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=mock_user)

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.verify.return_value = True

    mock_jwt_service = Mock(spec=IJWTService)

    use_case = IniciarSesionUseCase(mock_user_repository, mock_password_hasher, mock_jwt_service)

    dto = IniciarSesionDTO(email=user_email, contrasena=plain_password)

    # Act & Assert
    with pytest.raises(ValueError, match="Account is inactive."):
        await use_case.execute(dto)

    mock_user_repository.buscar_por_email.assert_called_once_with(user_email)
    mock_password_hasher.verify.assert_called_once_with(plain_password, hashed_password)
    mock_jwt_service.generar_tokens.assert_not_called()
