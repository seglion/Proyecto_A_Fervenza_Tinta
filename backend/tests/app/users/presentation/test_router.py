import pytest
from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock

from app.users.application.dtos import (RegistrarUsuarioDTO, UsuarioCreadoDTO, IniciarSesionDTO, UsuarioResponseDTO, ActualizarMiPerfilDTO, CambiarContrasenaDTO)
from app.users.application.dtos.tokens_dto import TokensDTO
from app.users.domain.value_objects import Rol
from uuid import uuid4
import asyncpg

# Import the actual router and dependency functions
from app.users.presentation.router import router as users_router
from app.users.presentation.router import get_registrar_usuario_use_case
from app.core.database import get_db
from app.users.presentation.router import get_iniciar_sesion_use_case
from app.users.presentation.router import get_confirmar_email_use_case
from app.users.presentation.router import get_ver_mi_perfil_use_case
from app.users.presentation.router import get_actualizar_mi_perfil_use_case
from app.users.presentation.router import get_cambiar_contrasena_use_case
from app.users.presentation.router import get_solicitar_eliminacion_use_case
from app.users.presentation.router import get_reenviar_email_use_case
from app.users.presentation.router import get_solicitar_reseteo_contrasena_use_case
from app.users.presentation.router import get_confirmar_nueva_contrasena_use_case
from app.users.presentation.router import get_refrescar_sesion_use_case
from app.core.dependencies import get_current_user
from app.users.domain.entities import User

@pytest.fixture(scope="module")
def app_client():
    app = FastAPI()
    app.include_router(users_router)
    with TestClient(app) as client:
        yield client

def test_router_file_exists():
    try:
        from app.users.presentation.router import router
        assert isinstance(router, APIRouter)
    except ImportError:
        pytest.fail("El archivo 'router.py' o la instancia 'router' no existen en app.users.presentation")

@pytest.fixture
def mock_registrar_usuario_use_case():
    mock = AsyncMock()
    mock.execute.return_value = UsuarioCreadoDTO(
        id=uuid4(),
        email="test@example.com",
    )
    return mock

@pytest.fixture
async def mock_db_connection():
    mock_conn = AsyncMock(spec=asyncpg.Connection)
    yield mock_conn

@pytest.mark.asyncio
async def test_register_user_endpoint_success(app_client, mock_registrar_usuario_use_case, mock_db_connection):
    # Arrange
    app_client.app.dependency_overrides[get_registrar_usuario_use_case] = lambda: mock_registrar_usuario_use_case
    app_client.app.dependency_overrides[get_db] = lambda: mock_db_connection

    register_data = {
        "email": "test@example.com",
        "contrasena": "SecurePass123!@#",
        "nombre": "Test",
        "apellidos": "User",
        "numero_telefono": "123456789",
        "rol": "USUARIO",
    }

    # Act
    try:
        response = app_client.post("/users/register", json=register_data)
    except Exception as e:
        pytest.fail(f"Exception during client.post: {e}")
    finally:
        # Clear overrides after the test
        app_client.app.dependency_overrides = {}

    # Assert
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    mock_registrar_usuario_use_case.execute.assert_called_once()

@pytest.fixture
def mock_iniciar_sesion_use_case():
    mock = AsyncMock()
    mock.execute.return_value = TokensDTO(
        access_token="mock_access_token",
        refresh_token="mock_refresh_token",
        token_type="bearer"
    )
    return mock

@pytest.mark.asyncio
async def test_login_user_endpoint_success(app_client, mock_iniciar_sesion_use_case, mock_db_connection):
    # Arrange
    app_client.app.dependency_overrides[get_iniciar_sesion_use_case] = lambda: mock_iniciar_sesion_use_case
    app_client.app.dependency_overrides[get_db] = lambda: mock_db_connection

    login_data = {
        "username": "test@example.com",
        "password": "SecurePass123!@#",
    }

    # Act
    response = app_client.post("/users/auth/token", data=login_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["access_token"] == "mock_access_token"
    mock_iniciar_sesion_use_case.execute.assert_called_once()

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.fixture
def mock_confirmar_email_use_case():
    mock = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_confirm_email_endpoint_success(app_client, mock_confirmar_email_use_case, mock_db_connection):
    # Arrange
    app_client.app.dependency_overrides[get_confirmar_email_use_case] = lambda: mock_confirmar_email_use_case
    app_client.app.dependency_overrides[get_db] = lambda: mock_db_connection

    token = "some_verification_token"

    # Act
    response = app_client.get(f"/users/verificar-email?token={token}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Email verified successfully."}
    mock_confirmar_email_use_case.execute.assert_called_once_with(token)

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.fixture
def mock_ver_mi_perfil_use_case():
    mock = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_get_my_profile_endpoint_success(app_client, mock_ver_mi_perfil_use_case):
    # Arrange
    test_user_id = uuid4()
    mock_current_user = User(
        id=test_user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo="testuser",
        rol=Rol.USUARIO,
        esta_activo=True,
        email_verificado=True
    )
    mock_ver_mi_perfil_use_case.execute.return_value = UsuarioResponseDTO(
        id=test_user_id,
        email="test@example.com",
        nombre="Test",
        apellidos="User",
        apodo="testuser",
        numero_telefono="123456789",
        url_avatar=None,
        esta_activo=True,
        rol="USUARIO"
    )

    app_client.app.dependency_overrides[get_ver_mi_perfil_use_case] = lambda: mock_ver_mi_perfil_use_case
    app_client.app.dependency_overrides[get_current_user] = lambda: mock_current_user

    # Act
    response = app_client.get("/users/me")

    # Assert
    assert response.status_code == 200
    assert response.json()["id"] == str(test_user_id)
    mock_ver_mi_perfil_use_case.execute.assert_called_once_with(mock_current_user, test_user_id)

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.fixture
def mock_actualizar_mi_perfil_use_case():
    mock = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_update_my_profile_endpoint_success(app_client, mock_actualizar_mi_perfil_use_case):
    # Arrange
    test_user_id = uuid4()
    mock_current_user = User(
        id=test_user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo="testuser",
        rol=Rol.USUARIO,
        esta_activo=True,
        email_verificado=True
    )

    update_data = {"nombre": "Updated Name", "apodo": "updatednick"}

    mock_actualizar_mi_perfil_use_case.execute.return_value = UsuarioResponseDTO(
        id=test_user_id,
        email="test@example.com",
        nombre="Updated Name",
        apellidos="User",
        apodo="updatednick",
        numero_telefono="123456789",
        url_avatar=None,
        esta_activo=True,
        rol="USUARIO"
    )

    app_client.app.dependency_overrides[get_actualizar_mi_perfil_use_case] = lambda: mock_actualizar_mi_perfil_use_case
    app_client.app.dependency_overrides[get_current_user] = lambda: mock_current_user

    # Act
    response = app_client.put("/users/me", json=update_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["nombre"] == "Updated Name"
    assert response.json()["apodo"] == "updatednick"
    mock_actualizar_mi_perfil_use_case.execute.assert_called_once()

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.fixture
def mock_cambiar_contrasena_use_case():
    mock = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_change_password_endpoint_success(app_client, mock_cambiar_contrasena_use_case):
    # Arrange
    test_user_id = uuid4()
    mock_current_user = User(
        id=test_user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo="testuser",
        rol=Rol.USUARIO,
        esta_activo=True,
        email_verificado=True
    )

    password_data = {"contrasena_antigua": "old_password", "contrasena_nueva": "new_password"}

    app_client.app.dependency_overrides[get_cambiar_contrasena_use_case] = lambda: mock_cambiar_contrasena_use_case
    app_client.app.dependency_overrides[get_current_user] = lambda: mock_current_user

    # Act
    response = app_client.put("/users/me/password", json=password_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Password updated successfully."}
    mock_cambiar_contrasena_use_case.execute.assert_called_once()

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.fixture
def mock_solicitar_eliminacion_use_case():
    mock = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_request_deletion_endpoint_success(app_client, mock_solicitar_eliminacion_use_case):
    # Arrange
    test_user_id = uuid4()
    mock_current_user = User(
        id=test_user_id,
        email="test@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        apodo="testuser",
        rol=Rol.USUARIO,
        esta_activo=True,
        email_verificado=True
    )

    app_client.app.dependency_overrides[get_solicitar_eliminacion_use_case] = lambda: mock_solicitar_eliminacion_use_case
    app_client.app.dependency_overrides[get_current_user] = lambda: mock_current_user

    # Act
    response = app_client.delete("/users/me")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Deletion request sent successfully."}
    mock_solicitar_eliminacion_use_case.execute.assert_called_once_with(mock_current_user, test_user_id)

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.fixture
def mock_reenviar_email_use_case():
    mock = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_resend_verification_email_endpoint_success(app_client, mock_reenviar_email_use_case):
    # Arrange
    app_client.app.dependency_overrides[get_reenviar_email_use_case] = lambda: mock_reenviar_email_use_case

    email_data = {"email": "test@example.com"}

    # Act
    response = app_client.post("/users/reenviar-verificacion", json=email_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Verification email sent."}
    mock_reenviar_email_use_case.execute.assert_called_once_with(email_data["email"])

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.fixture
def mock_solicitar_reseteo_contrasena_use_case():
    mock = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_request_password_reset_endpoint_success(app_client, mock_solicitar_reseteo_contrasena_use_case):
    # Arrange
    app_client.app.dependency_overrides[get_solicitar_reseteo_contrasena_use_case] = lambda: mock_solicitar_reseteo_contrasena_use_case

    email_data = {"email": "test@example.com"}

    # Act
    response = app_client.post("/users/solicitar-reseteo", json=email_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Password reset email sent."}
    mock_solicitar_reseteo_contrasena_use_case.execute.assert_called_once_with(email_data["email"])

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.fixture
def mock_confirmar_nueva_contrasena_use_case():
    mock = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_confirm_password_reset_endpoint_success(app_client, mock_confirmar_nueva_contrasena_use_case):
    # Arrange
    app_client.app.dependency_overrides[get_confirmar_nueva_contrasena_use_case] = lambda: mock_confirmar_nueva_contrasena_use_case

    reset_data = {"token": "some_reset_token", "nueva_contrasena": "new_strong_password"}

    # Act
    response = app_client.post("/users/confirmar-reseteo", json=reset_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": "Password has been reset successfully."}
    mock_confirmar_nueva_contrasena_use_case.execute.assert_called_once()

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.fixture
def mock_refrescar_sesion_use_case():
    mock = AsyncMock()
    mock.execute.return_value = TokensDTO(
        access_token="new_mock_access_token",
        refresh_token="new_mock_refresh_token",
        token_type="bearer"
    )
    return mock

@pytest.mark.asyncio
async def test_refresh_session_endpoint_success(app_client, mock_refrescar_sesion_use_case):
    # Arrange
    app_client.app.dependency_overrides[get_refrescar_sesion_use_case] = lambda: mock_refrescar_sesion_use_case

    refresh_data = {"refresh_token": "some_refresh_token"}

    # Act
    response = app_client.post("/users/auth/refresh", json=refresh_data)

    # Assert
    assert response.status_code == 200
    assert response.json()["access_token"] == "new_mock_access_token"
    mock_refrescar_sesion_use_case.execute.assert_called_once_with(refresh_data["refresh_token"])

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}
