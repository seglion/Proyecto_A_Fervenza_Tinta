import pytest
from unittest.mock import Mock, AsyncMock
from abc import ABC
from app.users.application.repositories.i_token_repository import ITokenRepository
from app.users.application.repositories.i_user_repository import IUserRepository
from app.core.security.i_password_hasher import IPasswordHasher
from app.users.domain.entities import Token, User
from app.users.domain.value_objects import TipoToken
from app.users.application.use_cases.confirmar_email_use_case import ConfirmarEmailUseCase
from uuid import uuid4
from datetime import datetime, timedelta, timezone

def test_confirmar_email_use_case_file_exists():
    """
    Tests if the confirmar email use case file exists.
    """
    try:
        from app.users.application.use_cases import confirmar_email_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/confirmar_email_use_case.py")

def test_confirmar_email_use_case_class_exists():
    """
    Tests if the ConfirmarEmailUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.confirmar_email_use_case import ConfirmarEmailUseCase
    except ImportError:
        pytest.fail("ConfirmarEmailUseCase class does not exist in confirmar_email_use_case.py")

@pytest.mark.asyncio
async def test_confirmar_email_exitoso():
    """
    Tests the successful confirmation of a user's email.
    """
    # Arrange
    user_id = uuid4()
    plain_token = "some_plain_token"
    hashed_token = "some_hashed_token"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.VERIFICACION_EMAIL,
        hash_token=hashed_token,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1),
        es_valido=True
    ))
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        email_verificado=False
    ))
    mock_user_repository.actualizar = AsyncMock()

    use_case = ConfirmarEmailUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act
    await use_case.execute(plain_token)

    # Assert
    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_user_repository.actualizar.assert_called_once()
    updated_user = mock_user_repository.actualizar.call_args[0][0]
    assert updated_user.email_verificado is True
    mock_token_repository.actualizar.assert_called_once()
    updated_token = mock_token_repository.actualizar.call_args[0][0]
    assert updated_token.es_valido is False

@pytest.mark.asyncio
async def test_confirmar_email_token_no_encontrado():
    """
    Tests that a ValueError is raised when the token is not found.
    """
    # Arrange
    plain_token = "non_existent_token"
    hashed_token = "hashed_non_existent_token"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=None) # Token not found
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()
    mock_user_repository.actualizar = AsyncMock()

    use_case = ConfirmarEmailUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid or expired token."):
        await use_case.execute(plain_token)

    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_not_called()
    mock_user_repository.actualizar.assert_not_called()
    mock_token_repository.actualizar.assert_not_called()

@pytest.mark.asyncio
async def test_confirmar_email_tipo_token_incorrecto():
    """
    Tests that a ValueError is raised when the token found is not of type VERIFICACION_EMAIL.
    """
    # Arrange
    user_id = uuid4()
    plain_token = "some_plain_token"
    hashed_token = "some_hashed_token"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.RESETEO_CONTRASENA, # Incorrect token type
        hash_token=hashed_token,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1),
        es_valido=True
    ))
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()
    mock_user_repository.actualizar = AsyncMock()

    use_case = ConfirmarEmailUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid or expired token."):
        await use_case.execute(plain_token)

    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_not_called()
    mock_user_repository.actualizar.assert_not_called()
    mock_token_repository.actualizar.assert_not_called()

@pytest.mark.asyncio
async def test_confirmar_email_token_invalido():
    """
    Tests that a ValueError is raised when the token found is marked as invalid.
    """
    # Arrange
    user_id = uuid4()
    plain_token = "some_plain_token"
    hashed_token = "some_hashed_token"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.VERIFICACION_EMAIL,
        hash_token=hashed_token,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1),
        es_valido=False # Token is invalid
    ))
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()
    mock_user_repository.actualizar = AsyncMock()

    use_case = ConfirmarEmailUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid or expired token."):
        await use_case.execute(plain_token)

    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_not_called()
    mock_user_repository.actualizar.assert_not_called()
    mock_token_repository.actualizar.assert_not_called()

@pytest.mark.asyncio
async def test_confirmar_email_token_expirado():
    """
    Tests that a ValueError is raised when the token found has expired.
    """
    # Arrange
    user_id = uuid4()
    plain_token = "some_plain_token"
    hashed_token = "some_hashed_token"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.VERIFICACION_EMAIL,
        hash_token=hashed_token,
        fecha_expiracion=datetime.now(timezone.utc) - timedelta(hours=1), # Token has expired
        es_valido=True
    ))
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()
    mock_user_repository.actualizar = AsyncMock()

    use_case = ConfirmarEmailUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid or expired token."):
        await use_case.execute(plain_token)

    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_not_called()
    mock_user_repository.actualizar.assert_not_called()
    mock_token_repository.actualizar.assert_not_called()

@pytest.mark.asyncio
async def test_confirmar_email_usuario_no_encontrado():
    """
    Tests that a ValueError is raised when the user associated with the token is not found.
    """
    # Arrange
    user_id = uuid4()
    plain_token = "some_plain_token"
    hashed_token = "some_hashed_token"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.VERIFICACION_EMAIL,
        hash_token=hashed_token,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1),
        es_valido=True
    ))
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=None) # User not found
    mock_user_repository.actualizar = AsyncMock()

    use_case = ConfirmarEmailUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="User not found."):
        await use_case.execute(plain_token)

    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_user_repository.actualizar.assert_not_called()
    mock_token_repository.actualizar.assert_not_called()
