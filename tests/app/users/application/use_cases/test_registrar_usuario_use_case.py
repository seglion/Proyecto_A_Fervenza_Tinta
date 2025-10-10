import pytest
from unittest.mock import Mock, AsyncMock, call
from app.users.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase

def test_registrar_usuario_use_case_file_exists():
    """
    Tests if the registrar usuario use case file exists.
    """
    try:
        from app.users.application.use_cases import registrar_usuario_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/registrar_usuario_use_case.py")

def test_registrar_usuario_use_case_class_exists():
    """
    Tests if the RegistrarUsuarioUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase
    except ImportError:
        pytest.fail("RegistrarUsuarioUseCase class does not exist in registrar_usuario_use_case.py")

async def test_registrar_usuario_exitoso():
    """
    Tests the successful registration of a user.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.users.application.dtos import RegistrarUsuarioDTO, UsuarioCreadoDTO
    from app.users.domain.entities import User, Token
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.core.services.i_email_service import IEmailService
    from app.users.domain.value_objects import TipoToken
    from uuid import uuid4
    from datetime import datetime, timedelta, timezone

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=None)
    
    created_user_id = uuid4()
    mock_user_repository.crear = AsyncMock(return_value=User(
        id=created_user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password", # Placeholder
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None
    ))

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.side_effect = ["hashed_password", "hashed_verification_token"]

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.send_verification_email = AsyncMock()

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.crear = AsyncMock(return_value=Token(
        usuario_id=created_user_id,
        tipo_token=TipoToken.VERIFICACION_EMAIL,
        hash_token="hashed_verification_token",
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=24)
    ))

    dto = RegistrarUsuarioDTO(
        email="test@example.com",
        contrasena="password123",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789"
    )

    use_case = RegistrarUsuarioUseCase(mock_user_repository, mock_password_hasher, mock_email_service, mock_token_repository)

    # Act
    result = await use_case.execute(dto)

    # Assert
    mock_user_repository.buscar_por_email.assert_called_once_with(dto.email)
    mock_password_hasher.hash.assert_has_calls([
        call(dto.contrasena),
        call(str(mock_email_service.send_verification_email.call_args[0][1])) # The plain token passed to email service
    ])
    assert mock_password_hasher.hash.call_count == 2
    mock_user_repository.crear.assert_called_once()
    mock_token_repository.crear.assert_called_once()
    # The actual token value passed to email service is the plain text one, not the hashed one
    assert mock_email_service.send_verification_email.call_args[0][0] == dto.email
    assert isinstance(mock_email_service.send_verification_email.call_args[0][1], str) # Check if it's a string (the plain token)
    assert isinstance(result, UsuarioCreadoDTO)
    assert result.id == created_user_id
    assert result.email == dto.email

async def test_registrar_usuario_email_existente():
    """
    Tests that a ValueError is raised when a user with the given email already exists.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.users.application.dtos import RegistrarUsuarioDTO
    from app.users.domain.entities import User
    from app.users.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.core.services.i_email_service import IEmailService
    from uuid import uuid4

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=User(
        id=uuid4(),
        email="existing@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Existing",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None
    ))

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = "hashed_password"

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.send_verification_email = AsyncMock()

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.crear = AsyncMock()

    dto = RegistrarUsuarioDTO(
        email="existing@example.com",
        contrasena="password123",
        nombre="Existing",
        apellidos="User",
        numero_telefono="123456789"
    )

    use_case = RegistrarUsuarioUseCase(mock_user_repository, mock_password_hasher, mock_email_service, mock_token_repository)

    # Act & Assert
    with pytest.raises(ValueError, match="User with this email already exists."):
        await use_case.execute(dto)

    mock_user_repository.buscar_por_email.assert_called_once_with(dto.email)
    mock_password_hasher.hash.assert_not_called()
    mock_user_repository.crear.assert_not_called()
    mock_token_repository.crear.assert_not_called()
    mock_email_service.send_verification_email.assert_not_called()
