import pytest
from fastapi import APIRouter, FastAPI, Depends
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from uuid import uuid4

from app.users.application.dtos import ListaUsuariosResponseDTO, UsuarioResponseDTO
from app.users.domain.entities import User
from app.users.domain.value_objects import Rol
from app.core.dependencies import get_current_user
from app.users.presentation.admin_router import get_ver_perfil_otro_usuario_use_case, router as admin_router, get_admin_user
from app.users.presentation.admin_router import get_listar_usuarios_use_case
from app.users.presentation.admin_router import get_ver_perfil_usuario_use_case
from app.users.presentation.admin_router import get_ver_perfil_otro_usuario_use_case
from app.users.presentation.admin_router import get_aprobar_usuario_use_case
from app.users.presentation.admin_router import get_rechazar_usuario_use_case
from app.users.presentation.admin_router import get_activar_desactivar_usuario_use_case
from app.users.presentation.admin_router import get_modificar_roles_use_case
from app.users.presentation.admin_router import get_eliminar_usuario_use_case
from app.users.presentation.admin_router import get_forzar_reseteo_use_case # Will be created
from app.core.config import settings

@pytest.fixture(scope="module")
def app_client():
    app = FastAPI()
    app.include_router(admin_router)
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_listar_usuarios_use_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def mock_ver_perfil_usuario_use_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def mock_ver_perfil_otro_usuario_use_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def mock_aprobar_usuario_use_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def mock_rechazar_usuario_use_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def mock_activar_desactivar_usuario_use_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def mock_modificar_roles_use_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def mock_eliminar_usuario_use_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def mock_forzar_reseteo_use_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def admin_user():
    return User(
        id=uuid4(),
        email="admin@example.com",
        rol=Rol.ADMIN,
        # ... other fields
        contrasena_hasheada="hashed",
        nombre="Admin",
        apellidos="User",
        numero_telefono="1234567890",
        esta_activo=True,
        email_verificado=True
    )

@pytest.mark.asyncio
async def test_list_users_as_admin(app_client, mock_listar_usuarios_use_case, admin_user):
    # Arrange
    mock_listar_usuarios_use_case.execute.return_value = ListaUsuariosResponseDTO(
                usuarios=[
                    UsuarioResponseDTO(id=uuid4(), email="test1@example.com", nombre="Test", apellidos="One", numero_telefono="111", rol="USUARIO", esta_activo=True),
                    UsuarioResponseDTO(id=uuid4(), email="test2@example.com", nombre="Test", apellidos="Two", numero_telefono="222", rol="USUARIO", esta_activo=True),
                ]
            )
        
    app_client.app.dependency_overrides[get_listar_usuarios_use_case] = lambda: mock_listar_usuarios_use_case
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    # Act
    response = app_client.get("/admin/users")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_listar_usuarios_use_case.execute.assert_called_once()

    # Clean up
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_get_user_profile_as_admin(app_client, mock_ver_perfil_otro_usuario_use_case, admin_user):
    # Arrange
    target_user_id = uuid4()
    mock_ver_perfil_otro_usuario_use_case.execute.return_value = UsuarioResponseDTO(
        id=target_user_id, email="target@example.com", nombre="Target", apellidos="User", 
        numero_telefono="333", rol="USUARIO", esta_activo=True
    )
    app_client.app.dependency_overrides[get_ver_perfil_otro_usuario_use_case] = lambda: mock_ver_perfil_otro_usuario_use_case
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    # Act
    response = app_client.get(f"/admin/users/{target_user_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == str(target_user_id)
    mock_ver_perfil_otro_usuario_use_case.execute.assert_called_once_with(admin_user, target_user_id)

    # Clean up
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_approve_user_as_admin(app_client, mock_aprobar_usuario_use_case, admin_user):
    # Arrange
    target_user_id = uuid4()
    app_client.app.dependency_overrides[get_aprobar_usuario_use_case] = lambda: mock_aprobar_usuario_use_case
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    # Act
    response = app_client.post(f"/admin/users/{target_user_id}/aprobar")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "User approved successfully."}
    mock_aprobar_usuario_use_case.execute.assert_called_once_with(admin_user, target_user_id)

    # Clean up
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_reject_user_as_admin(app_client, mock_rechazar_usuario_use_case, admin_user):
    # Arrange
    target_user_id = uuid4()
    app_client.app.dependency_overrides[get_rechazar_usuario_use_case] = lambda: mock_rechazar_usuario_use_case
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    # Act
    response = app_client.post(f"/admin/users/{target_user_id}/rechazar")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "User rejected successfully."}
    mock_rechazar_usuario_use_case.execute.assert_called_once_with(admin_user, target_user_id)

    # Clean up
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_set_user_status_as_admin(app_client, mock_activar_desactivar_usuario_use_case, admin_user):
    # Arrange
    target_user_id = uuid4()
    status_data = {"esta_activo": False}
    app_client.app.dependency_overrides[get_activar_desactivar_usuario_use_case] = lambda: mock_activar_desactivar_usuario_use_case
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    # Act
    response = app_client.put(f"/admin/users/{target_user_id}/estado", json=status_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "User status updated successfully."}
    mock_activar_desactivar_usuario_use_case.execute.assert_called_once_with(admin_user, target_user_id, False)

    # Clean up
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_modify_roles_as_admin(app_client, mock_modificar_roles_use_case, admin_user):
    # Arrange
    target_user_id = uuid4()
    roles_data = {"rol": "USUARIO"}
    app_client.app.dependency_overrides[get_modificar_roles_use_case] = lambda: mock_modificar_roles_use_case
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    # Act
    response = app_client.put(f"/admin/users/{target_user_id}/roles", json=roles_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "User roles updated successfully."}
    mock_modificar_roles_use_case.execute.assert_called_once()

    # Clean up
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_delete_user_as_admin(app_client, mock_eliminar_usuario_use_case, admin_user):
    # Arrange
    target_user_id = uuid4()
    app_client.app.dependency_overrides[get_eliminar_usuario_use_case] = lambda: mock_eliminar_usuario_use_case
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    # Act
    response = app_client.delete(f"/admin/users/{target_user_id}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully."}
    mock_eliminar_usuario_use_case.execute.assert_called_once_with(admin_user, target_user_id)

    # Clean up
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_force_password_reset_as_admin(app_client, mock_forzar_reseteo_use_case, admin_user):
    # Arrange
    target_user_id = uuid4()
    app_client.app.dependency_overrides[get_forzar_reseteo_use_case] = lambda: mock_forzar_reseteo_use_case
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    # Act
    response = app_client.post(f"/admin/users/{target_user_id}/forzar-reseteo")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset forced successfully."}
    mock_forzar_reseteo_use_case.execute.assert_called_once_with(admin_user, target_user_id)

    # Clean up
    app_client.app.dependency_overrides = {}
