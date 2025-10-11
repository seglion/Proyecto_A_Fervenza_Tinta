import pytest
from unittest.mock import Mock, AsyncMock


def test_solicitar_eliminacion_use_case_file_exists():
    """
    Tests if the solicitar eliminacion use case file exists.
    """
    try:
        from app.users.application.use_cases import solicitar_eliminacion_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/solicitar_eliminacion_use_case.py")

def test_solicitar_eliminacion_use_case_class_exists():
    """
    Tests if the SolicitarEliminacionUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.solicitar_eliminacion_use_case import SolicitarEliminacionUseCase
    except ImportError:
        pytest.fail("SolicitarEliminacionUseCase class does not exist in solicitar_eliminacion_use_case.py")

@pytest.mark.asyncio
async def test_solicitar_eliminacion_exitoso():
    """
    Tests the successful request for account deletion.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.policies.user_policy import UserPolicy
    from app.users.domain.entities import User
    from app.users.application.use_cases.solicitar_eliminacion_use_case import SolicitarEliminacionUseCase
    from uuid import uuid4

    user_id = uuid4()

    mock_user = User(
        id=user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo=None,
        email_verificado=True,
        esta_activo=True
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.desactivar_cuenta = AsyncMock()

    user_policy = UserPolicy()

    use_case = SolicitarEliminacionUseCase(mock_user_repository, user_policy)

    # Act
    await use_case.execute(mock_user, user_id)

    # Assert
    mock_user_repository.desactivar_cuenta.assert_called_once_with(user_id)

@pytest.mark.asyncio
async def test_solicitar_eliminacion_no_autorizado():
    """
    Tests that a ValueError is raised when the user is not authorized to delete the account.
    """
    # Arrange
    from app.users.application.repositories.i_user_repository import IUserRepository
    from app.users.application.policies.user_policy import UserPolicy
    from app.users.domain.entities import User
    from app.users.application.use_cases.solicitar_eliminacion_use_case import SolicitarEliminacionUseCase
    from uuid import uuid4

    current_user_id = uuid4()
    target_user_id = uuid4()

    mock_current_user = User(
        id=current_user_id,
        email="current@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Current",
        apellidos="User",
        numero_telefono="123456789",
        apodo="currentuser",
        email_verificado=True,
        esta_activo=True
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.desactivar_cuenta = AsyncMock()

    user_policy = UserPolicy()

    use_case = SolicitarEliminacionUseCase(mock_user_repository, user_policy)

    # Act & Assert
    with pytest.raises(ValueError, match="Not authorized to delete this account."):
        await use_case.execute(mock_current_user, target_user_id)

    mock_user_repository.desactivar_cuenta.assert_not_called()
