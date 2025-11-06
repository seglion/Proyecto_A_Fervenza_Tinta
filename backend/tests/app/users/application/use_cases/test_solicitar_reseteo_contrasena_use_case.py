import pytest
from unittest.mock import Mock, AsyncMock
from app.users.domain.value_objects import Rol

def test_solicitar_reseteo_contrasena_use_case_file_exists():
    """
    Tests if the solicitar reseteo contrasena use case file exists.
    """
    try:
        from app.users.application.use_cases import solicitar_reseteo_contrasena_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/solicitar_reseteo_contrasena_use_case.py")

def test_solicitar_reseteo_contrasena_use_case_class_exists():
    """
    Tests if the SolicitarReseteoContrasenaUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.solicitar_reseteo_contrasena_use_case import SolicitarReseteoContrasenaUseCase
    except ImportError:
        pytest.fail("SolicitarReseteoContrasenaUseCase class does not exist in solicitar_reseteo_contrasena_use_case.py")

@pytest.mark.asyncio
async def test_solicitar_reseteo_contrasena_exitoso():
    """
    Tests the successful request for a password reset.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.core.services.i_email_service import IEmailService
    from app.users.domain.entities import User, Token
    from app.users.domain.value_objects import TipoToken
    from app.users.application.use_cases.solicitar_reseteo_contrasena_use_case import SolicitarReseteoContrasenaUseCase
    from uuid import uuid4
    from datetime import datetime, timedelta, timezone

    user_id = uuid4()
    user_email = "test@example.com"
    plain_token_value = "new_plain_token"
    hashed_token_value = "new_hashed_token"

    mock_user = User(
        id=user_id,
        email=user_email,
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
    mock_user_repository.buscar_por_email = AsyncMock(return_value=mock_user)

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.crear = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.RESETEO_CONTRASENA,
        hash_token=hashed_token_value,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1),
        es_valido=True
    ))

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token_value

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.send_reset_password_email = AsyncMock() # Assuming a new method for reset password email

    use_case = SolicitarReseteoContrasenaUseCase(mock_user_repository, mock_token_repository, mock_password_hasher, mock_email_service)

    # Act
    await use_case.execute(user_email)

    # Assert
    mock_user_repository.buscar_por_email.assert_called_once_with(user_email)
    assert mock_password_hasher.hash.call_count == 1
    generated_plain_token = mock_password_hasher.hash.call_args[0][0]
    assert isinstance(generated_plain_token, str)

    mock_token_repository.crear.assert_called_once()
    created_token_entity = mock_token_repository.crear.call_args[0][0]
    assert created_token_entity.usuario_id == user_id
    assert created_token_entity.tipo_token == TipoToken.RESETEO_CONTRASENA
    assert created_token_entity.hash_token == hashed_token_value

    mock_email_service.send_reset_password_email.assert_called_once_with(user_email, generated_plain_token)

@pytest.mark.asyncio
async def test_solicitar_reseteo_contrasena_usuario_no_encontrado():
    """
    Tests that the use case returns silently when the user is not found.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.core.services.i_email_service import IEmailService
    from app.users.application.use_cases.solicitar_reseteo_contrasena_use_case import SolicitarReseteoContrasenaUseCase
    from unittest.mock import AsyncMock

    user_email = "non_existent@example.com"

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=None) # User not found

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.crear = AsyncMock()

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash = Mock()

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.send_reset_password_email = AsyncMock()

    use_case = SolicitarReseteoContrasenaUseCase(mock_user_repository, mock_token_repository, mock_password_hasher, mock_email_service)

    # Act
    await use_case.execute(user_email)

    # Assert
    mock_user_repository.buscar_por_email.assert_called_once_with(user_email)
    mock_password_hasher.hash.assert_not_called()
    mock_token_repository.crear.assert_not_called()
    mock_email_service.send_reset_password_email.assert_not_called()
