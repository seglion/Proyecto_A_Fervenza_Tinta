import pytest
from unittest.mock import Mock, AsyncMock


def test_confirmar_nueva_contrasena_use_case_file_exists():
    """
    Tests if the confirmar nueva contrasena use case file exists.
    """
    try:
        from app.users.application.use_cases import confirmar_nueva_contrasena_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/confirmar_nueva_contrasena_use_case.py")

def test_confirmar_nueva_contrasena_use_case_class_exists():
    """
    Tests if the ConfirmarNuevaContrasenaUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.confirmar_nueva_contrasena_use_case import ConfirmarNuevaContrasenaUseCase
    except ImportError:
        pytest.fail("ConfirmarNuevaContrasenaUseCase class does not exist in confirmar_nueva_contrasena_use_case.py")

@pytest.mark.asyncio
async def test_confirmar_nueva_contrasena_exitoso():
    """
    Tests the successful confirmation of a new password.
    """
    # Arrange
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.users.domain.entities import Token, User
    from app.users.domain.value_objects import TipoToken
    from app.users.application.use_cases.confirmar_nueva_contrasena_use_case import ConfirmarNuevaContrasenaUseCase
    from uuid import uuid4
    from datetime import datetime, timedelta, timezone

    user_id = uuid4()
    plain_token = "some_plain_token"
    hashed_token = "some_hashed_token"
    new_plain_password = "new_password123"
    new_hashed_password = "new_hashed_password"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token
    mock_password_hasher.hash.side_effect = [hashed_token, new_hashed_password] # First hash for token, second for new password

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.RESETEO_CONTRASENA,
        hash_token=hashed_token,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1),
        es_valido=True
    ))
    mock_token_repository.actualizar = AsyncMock()

    mock_user = User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada="old_hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        email_verificado=True,
        esta_activo=True
    )
    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=mock_user)
    mock_user_repository.actualizar_contrasena = AsyncMock()

    use_case = ConfirmarNuevaContrasenaUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act
    await use_case.execute(plain_token, new_plain_password)

    # Assert
    mock_password_hasher.hash.assert_any_call(plain_token)
    mock_password_hasher.hash.assert_any_call(new_plain_password)
    assert mock_password_hasher.hash.call_count == 2
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_user_repository.actualizar_contrasena.assert_called_once_with(user_id, new_hashed_password)
    mock_token_repository.actualizar.assert_called_once()
    updated_token = mock_token_repository.actualizar.call_args[0][0]
    assert updated_token.es_valido is False

@pytest.mark.asyncio
async def test_confirmar_nueva_contrasena_token_no_encontrado():
    """
    Tests that a ValueError is raised when the token is not found.
    """
    # Arrange
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.users.application.use_cases.confirmar_nueva_contrasena_use_case import ConfirmarNuevaContrasenaUseCase
    from unittest.mock import AsyncMock

    plain_token = "non_existent_token"
    hashed_token = "hashed_non_existent_token"
    new_plain_password = "new_password123"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=None) # Token not found
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()
    mock_user_repository.actualizar_contrasena = AsyncMock()

    use_case = ConfirmarNuevaContrasenaUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid or expired token."):
        await use_case.execute(plain_token, new_plain_password)

    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_not_called()
    mock_user_repository.actualizar_contrasena.assert_not_called()
    mock_token_repository.actualizar.assert_not_called()

@pytest.mark.asyncio
async def test_confirmar_nueva_contrasena_tipo_token_incorrecto():
    """
    Tests that a ValueError is raised when the token found is not of type RESEOTEO_CONTRASENA.
    """
    # Arrange
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.users.domain.entities import Token, User
    from app.users.domain.value_objects import TipoToken
    from app.users.application.use_cases.confirmar_nueva_contrasena_use_case import ConfirmarNuevaContrasenaUseCase
    from uuid import uuid4
    from datetime import datetime, timedelta, timezone

    user_id = uuid4()
    plain_token = "some_plain_token"
    hashed_token = "some_hashed_token"
    new_plain_password = "new_password123"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.VERIFICACION_EMAIL, # Incorrect token type
        hash_token=hashed_token,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1),
        es_valido=True
    ))
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()
    mock_user_repository.actualizar_contrasena = AsyncMock()

    use_case = ConfirmarNuevaContrasenaUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid or expired token."):
        await use_case.execute(plain_token, new_plain_password)

    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_not_called()
    mock_user_repository.actualizar_contrasena.assert_not_called()
    mock_token_repository.actualizar.assert_not_called()

@pytest.mark.asyncio
async def test_confirmar_nueva_contrasena_token_invalido():
    """
    Tests that a ValueError is raised when the token found is marked as invalid.
    """
    # Arrange
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.users.domain.entities import Token, User
    from app.users.domain.value_objects import TipoToken
    from app.users.application.use_cases.confirmar_nueva_contrasena_use_case import ConfirmarNuevaContrasenaUseCase
    from uuid import uuid4
    from datetime import datetime, timedelta, timezone

    user_id = uuid4()
    plain_token = "some_plain_token"
    hashed_token = "some_hashed_token"
    new_plain_password = "new_password123"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.RESETEO_CONTRASENA,
        hash_token=hashed_token,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1),
        es_valido=False # Token is invalid
    ))
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()
    mock_user_repository.actualizar_contrasena = AsyncMock()

    use_case = ConfirmarNuevaContrasenaUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid or expired token."):
        await use_case.execute(plain_token, new_plain_password)

    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_not_called()
    mock_user_repository.actualizar_contrasena.assert_not_called()
    mock_token_repository.actualizar.assert_not_called()

@pytest.mark.asyncio
async def test_confirmar_nueva_contrasena_token_expirado():
    """
    Tests that a ValueError is raised when the token found has expired.
    """
    # Arrange
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.users.domain.entities import Token, User
    from app.users.domain.value_objects import TipoToken
    from app.users.application.use_cases.confirmar_nueva_contrasena_use_case import ConfirmarNuevaContrasenaUseCase
    from uuid import uuid4
    from datetime import datetime, timedelta, timezone

    user_id = uuid4()
    plain_token = "some_plain_token"
    hashed_token = "some_hashed_token"
    new_plain_password = "new_password123"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.RESETEO_CONTRASENA,
        hash_token=hashed_token,
        fecha_expiracion=datetime.now(timezone.utc) - timedelta(hours=1), # Token has expired
        es_valido=True
    ))
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()
    mock_user_repository.actualizar_contrasena = AsyncMock()

    use_case = ConfirmarNuevaContrasenaUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="Invalid or expired token."):
        await use_case.execute(plain_token, new_plain_password)

    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_not_called()
    mock_user_repository.actualizar_contrasena.assert_not_called()
    mock_token_repository.actualizar.assert_not_called()

@pytest.mark.asyncio
async def test_confirmar_nueva_contrasena_usuario_no_encontrado():
    """
    Tests that a ValueError is raised when the user associated with the token is not found.
    """
    # Arrange
    from app.users.application.repositories.i_token_repository import ITokenRepository
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.core.security.i_password_hasher import IPasswordHasher
    from app.users.domain.entities import Token
    from app.users.domain.value_objects import TipoToken
    from app.users.application.use_cases.confirmar_nueva_contrasena_use_case import ConfirmarNuevaContrasenaUseCase
    from uuid import uuid4
    from datetime import datetime, timedelta, timezone

    user_id = uuid4()
    plain_token = "some_plain_token"
    hashed_token = "some_hashed_token"
    new_plain_password = "new_password123"

    mock_password_hasher = Mock(spec=IPasswordHasher)
    mock_password_hasher.hash.return_value = hashed_token

    mock_token_repository = Mock(spec=ITokenRepository)
    mock_token_repository.buscar_por_hash = AsyncMock(return_value=Token(
        id=uuid4(),
        usuario_id=user_id,
        tipo_token=TipoToken.RESETEO_CONTRASENA,
        hash_token=hashed_token,
        fecha_expiracion=datetime.now(timezone.utc) + timedelta(hours=1),
        es_valido=True
    ))
    mock_token_repository.actualizar = AsyncMock()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=None) # User not found
    mock_user_repository.actualizar_contrasena = AsyncMock()

    use_case = ConfirmarNuevaContrasenaUseCase(mock_token_repository, mock_user_repository, mock_password_hasher)

    # Act & Assert
    with pytest.raises(ValueError, match="User not found."):
        await use_case.execute(plain_token, new_plain_password)

    mock_password_hasher.hash.assert_called_once_with(plain_token)
    mock_token_repository.buscar_por_hash.assert_called_once_with(hashed_token)
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_user_repository.actualizar_contrasena.assert_not_called()
    mock_token_repository.actualizar.assert_not_called()
