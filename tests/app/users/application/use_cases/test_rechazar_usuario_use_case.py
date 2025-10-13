import pytest
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from app.users.application.repositories.i_user_repository import IUserRepository
from app.users.application.policies.user_policy import UserPolicy
from app.core.services.i_email_service import IEmailService

def test_rechazar_usuario_use_case_file_exists():
    """
    Tests if the rechazar usuario use case file exists.
    """
    try:
        from app.users.application.use_cases import rechazar_usuario_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/users/application/use_cases/rechazar_usuario_use_case.py")

def test_rechazar_usuario_use_case_class_exists():
    """
    Tests if the RechazarUsuarioUseCase class exists in the use case file.
    """
    try:
        from app.users.application.use_cases.rechazar_usuario_use_case import RechazarUsuarioUseCase
    except ImportError:
        pytest.fail("RechazarUsuarioUseCase class does not exist in rechazar_usuario_use_case.py")

@pytest.mark.asyncio
async def test_rechazar_usuario_exitoso():
    """
    Tests the successful rejection of a user by an admin.
    """
    # Arrange
    admin_user = User(
        id=uuid4(),
        email="admin@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Admin",
        apellidos="User",
        numero_telefono="123456789",
        apodo="adminuser",
        email_verificado=True,
        esta_activo=True,
        aprobado_por_admin=True,
        rol=Rol.ADMIN
    )
    user_to_reject_id = uuid4()
    user_to_reject = User(
        id=user_to_reject_id,
        email="pending@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Pending",
        apellidos="User",
        numero_telefono="987654321",
        apodo="pendinguser",
        email_verificado=True,
        esta_activo=True,
        aprobado_por_admin=False,
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=user_to_reject)
    mock_user_repository.eliminar_por_id = AsyncMock()

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.enviar_email_rechazo = AsyncMock()

    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = True

    from app.users.application.use_cases.rechazar_usuario_use_case import RechazarUsuarioUseCase
    use_case = RechazarUsuarioUseCase(mock_user_repository, user_policy, mock_email_service)

    # Act
    await use_case.execute(admin_user, user_to_reject_id)

    # Assert
    mock_user_repository.buscar_por_id.assert_called_once_with(user_to_reject_id)
    mock_user_repository.eliminar_por_id.assert_called_once_with(user_to_reject_id)
    mock_email_service.enviar_email_rechazo.assert_called_once_with(user_to_reject.email)

@pytest.mark.asyncio
async def test_rechazar_usuario_no_autorizado():
    """
    Tests that a ValueError is raised when a non-admin user tries to reject another user.
    """
    # Arrange
    non_admin_user = User(
        id=uuid4(),
        email="user@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Normal",
        apellidos="User",
        numero_telefono="111111111",
        apodo="normaluser",
        email_verificado=True,
        esta_activo=True,
        aprobado_por_admin=True,
        rol=Rol.USUARIO
    )
    user_to_reject_id = uuid4()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock()
    mock_user_repository.eliminar_por_id = AsyncMock()

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.enviar_email_rechazo = AsyncMock()

    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = False

    from app.users.application.use_cases.rechazar_usuario_use_case import RechazarUsuarioUseCase
    use_case = RechazarUsuarioUseCase(mock_user_repository, user_policy, mock_email_service)

    # Act & Assert
    with pytest.raises(ValueError, match="Not authorized to reject users."):
        await use_case.execute(non_admin_user, user_to_reject_id)

    mock_user_repository.buscar_por_id.assert_not_called()
    mock_user_repository.eliminar_por_id.assert_not_called()
    mock_email_service.enviar_email_rechazo.assert_not_called()

@pytest.mark.asyncio
async def test_rechazar_usuario_no_encontrado():
    """
    Tests that a ValueError is raised when the user to reject is not found.
    """
    # Arrange
    admin_user = User(
        id=uuid4(),
        email="admin@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Admin",
        apellidos="User",
        numero_telefono="123456789",
        apodo="adminuser",
        email_verificado=True,
        esta_activo=True,
        aprobado_por_admin=True,
        rol=Rol.ADMIN
    )
    non_existent_user_id = uuid4()

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=None)
    mock_user_repository.eliminar_por_id = AsyncMock()

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.enviar_email_rechazo = AsyncMock()

    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = True

    from app.users.application.use_cases.rechazar_usuario_use_case import RechazarUsuarioUseCase
    use_case = RechazarUsuarioUseCase(mock_user_repository, user_policy, mock_email_service)

    # Act & Assert
    with pytest.raises(ValueError, match="User not found."):
        await use_case.execute(admin_user, non_existent_user_id)

    mock_user_repository.buscar_por_id.assert_called_once_with(non_existent_user_id)
    mock_user_repository.eliminar_por_id.assert_not_called()
    mock_email_service.enviar_email_rechazo.assert_not_called()

@pytest.mark.asyncio
async def test_rechazar_usuario_ya_aprobado():
    """
    Tests that a ValueError is raised when the user is already approved.
    """
    # Arrange
    admin_user = User(
        id=uuid4(),
        email="admin@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Admin",
        apellidos="User",
        numero_telefono="123456789",
        apodo="adminuser",
        email_verificado=True,
        esta_activo=True,
        aprobado_por_admin=True,
        rol=Rol.ADMIN
    )
    already_approved_user_id = uuid4()
    already_approved_user = User(
        id=already_approved_user_id,
        email="approved@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Approved",
        apellidos="User",
        numero_telefono="999999999",
        apodo="approveduser",
        email_verificado=True,
        esta_activo=True,
        aprobado_por_admin=True, # Already approved
        rol=Rol.USUARIO
    )

    mock_user_repository = Mock(spec=IUserRepository)
    mock_user_repository.buscar_por_id = AsyncMock(return_value=already_approved_user)
    mock_user_repository.eliminar_por_id = AsyncMock()

    mock_email_service = Mock(spec=IEmailService)
    mock_email_service.enviar_email_rechazo = AsyncMock()

    user_policy = Mock(spec=UserPolicy)
    user_policy.es_administrador.return_value = True

    from app.users.application.use_cases.rechazar_usuario_use_case import RechazarUsuarioUseCase
    use_case = RechazarUsuarioUseCase(mock_user_repository, user_policy, mock_email_service)

    # Act & Assert
    with pytest.raises(ValueError, match="User is already approved."):
        await use_case.execute(admin_user, already_approved_user_id)

    mock_user_repository.buscar_por_id.assert_called_once_with(already_approved_user_id)
    mock_user_repository.eliminar_por_id.assert_not_called()
    mock_email_service.enviar_email_rechazo.assert_not_called()
