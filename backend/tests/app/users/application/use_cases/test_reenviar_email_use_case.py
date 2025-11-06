from app.users.domain.value_objects import Rol
import pytest
from unittest.mock import Mock, AsyncMock, ANY


def test_reenviar_email_use_case_file_exists():
    """
    Tests if the reenviar email use case file exists.
    """
    try:
        from app.users.application.use_cases import reenviar_email_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/reenviar_email_use_case.py")

def test_reenviar_email_use_case_class_exists():
    """
    Tests if the ReenviarEmailUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.reenviar_email_use_case import ReenviarEmailUseCase
    except ImportError:
        pytest.fail("ReenviarEmailUseCase class does not exist in reenviar_email_use_case.py")

@pytest.mark.asyncio
async def test_reenviar_email_exitoso():
    """
    Tests the successful re-sending of a verification email.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.core.services.i_email_service import IEmailService
    from app.users.domain.entities import User, Token
    from app.users.domain.value_objects import TipoToken,Rol
    from app.users.application.use_cases.reenviar_email_use_case import ReenviarEmailUseCase
    from uuid import uuid4
    from datetime import datetime, timedelta, timezone

    user_id = uuid4()
    user_email = "test@example.com"
    # plain_token_value = "new_plain_token" # No longer needed as we capture the actual generated one
    hashed_token_value = "new_hashed_token"

    mock_user = User(
        id=user_id,
        email=user_email,
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        rol=Rol.USUARIO,
        numero_telefono="123456789",
        apodo=None,
        email_verificado=False
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=mock_user)
    mock_user_repository.actualizar = AsyncMock()

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.crear = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        hash_token=hashed_token_value,
        tipo_token=TipoToken.VERIFICACION_EMAIL,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=24),
        es_valido=True
    ))

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token_value

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.send_verification_email = AsyncMock()

    use_case = ReenviarEmailUseCase(mock_user_repository, mock_token_repository, mock_password_hasher, mock_email_service)

    # Act
    await use_case.execute(user_email)

    # Assert
    mock_user_repository.buscar_por_email.assert_called_once_with(user_email)
    # The hash method is called with the newly generated plain token

    mock_email_service.send_verification_email.assert_called_once_with(user_email, mock_user.nombre, ANY)

@pytest.mark.asyncio
async def test_reenviar_email_usuario_no_encontrado():
    """
    Tests that the use case returns silently when the user is not found.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.core.services.i_email_service import IEmailService
    from app.users.application.use_cases.reenviar_email_use_case import ReenviarEmailUseCase
    from unittest.mock import AsyncMock

    user_email = "non_existent@example.com"

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=None) # User not found

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.crear = AsyncMock()

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash = Mock()

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.send_verification_email = AsyncMock()

    use_case = ReenviarEmailUseCase(mock_user_repository, mock_token_repository, mock_password_hasher, mock_email_service)

    # Act
    await use_case.execute(user_email)

    # Assert
    mock_user_repository.buscar_por_email.assert_called_once_with(user_email)
    mock_password_hasher.hash.assert_not_called()
    mock_token_repository.crear.assert_not_called()
    mock_email_service.send_verification_email.assert_not_called()

@pytest.mark.asyncio
async def test_reenviar_email_usuario_ya_verificado():
    """
    Tests that the use case returns silently when the user's email is already verified.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.core.services.i_email_service import IEmailService
    from app.users.domain.entities import User
    from app.users.application.use_cases.reenviar_email_use_case import ReenviarEmailUseCase
    from uuid import uuid4
    from unittest.mock import AsyncMock

    user_id = uuid4()
    user_email = "verified@example.com"

    mock_user = User(
        id=user_id,
        email=user_email,
        contrasena_hasheada="hashed_password",
        nombre="Verified",
        apellidos="User",
        rol=Rol.USUARIO,
        numero_telefono="123456789",
        apodo=None,
        email_verificado=True # User is already verified
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_email = AsyncMock(return_value=mock_user)

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.crear = AsyncMock()

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash = Mock()

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.send_verification_email = AsyncMock()

    use_case = ReenviarEmailUseCase(mock_user_repository, mock_token_repository, mock_password_hasher, mock_email_service)

    # Act
    await use_case.execute(user_email)

    # Assert
    mock_user_repository.buscar_por_email.assert_called_once_with(user_email)
    mock_password_hasher.hash.assert_not_called()
    mock_token_repository.crear.assert_not_called()
    mock_email_service.send_verification_email.assert_not_called()
