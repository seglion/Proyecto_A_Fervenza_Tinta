import pytest
from fastapi import FastAPI, APIRouter, Depends
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import date, datetime

from src.app.cuotas.application.dtos import CrearTemporadaDTO, TemporadaCreadaDTO, TipoCuotaCrearDTO, ActualizarTemporadaDTO, TemporadaDTO, ListaTemporadasDTO
from src.app.cuotas.presentation.router import router as cuotas_router
from src.app.cuotas.presentation.router import get_crear_temporada_use_case
from src.app.cuotas.presentation.router import get_actualizar_temporada_use_case
from src.app.cuotas.presentation.router import get_listar_temporadas_use_case
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.core.dependencies import get_current_user
from src.app.cuotas.presentation.router import get_admin_user

# ------------------ Fixtures ------------------
@pytest.fixture(scope="function")
def app_client():
    app = FastAPI()
    app.include_router(cuotas_router)
    with TestClient(app) as client:
        yield client

@pytest.fixture
def admin_user():
    return User(
        id=uuid4(),
        email="admin@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Admin",
        apellidos="User",
        numero_telefono="123456789",
        rol=Rol.ADMIN,
        esta_activo=True,
        email_verificado=True,
        aprobado_por_admin=True
    )

@pytest.fixture
def non_admin_user():
    return User(
        id=uuid4(),
        email="user@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Normal",
        apellidos="User",
        numero_telefono="987654321",
        rol=Rol.USUARIO,
        esta_activo=True,
        email_verificado=True,
        aprobado_por_admin=True
    )

@pytest.fixture
def mock_crear_temporada_use_case():
    mock = AsyncMock()
    mock.execute.return_value = TemporadaCreadaDTO(id=1)
    return mock

@pytest.fixture
def mock_actualizar_temporada_use_case():
    mock = AsyncMock()
    mock.execute.return_value = TemporadaDTO(
        id=1,
        nombre_temporada="Temporada Actualizada",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 12, 31),
        tipos_cuota=[]
    )
    return mock

@pytest.fixture
def mock_listar_temporadas_use_case():
    mock = AsyncMock()
    mock.execute.return_value = ListaTemporadasDTO(
        temporadas=[
            TemporadaDTO(
                id=1,
                nombre_temporada="Temporada 2025-2026",
                fecha_inicio=date(2025, 10, 1),
                fecha_fin=date(2026, 7, 25),
                tipos_cuota=[]
            )
        ]
    )
    return mock

# ------------------ Tests for CrearTemporada ------------------
@pytest.mark.asyncio
async def test_crear_temporada_endpoint_success(app_client, mock_crear_temporada_use_case, admin_user):
    # Arrange
    app_client.app.dependency_overrides[get_crear_temporada_use_case] = lambda: mock_crear_temporada_use_case
    app_client.app.dependency_overrides[get_current_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    temporada_data = {
        "nombre_temporada": "Temporada 2025-2026",
        "fecha_inicio": "2025-10-01",
        "fecha_fin": "2026-07-25",
        "tipos_cuota": [
            {"nombre": "Cuota General", "importe": 50.00},
            {"nombre": "Cuota Nuevo Socio", "importe": 25.00}
        ]
    }

    # Act
    response = app_client.post("/cuotas/temporadas", json=temporada_data)

    # Assert
    assert response.status_code == 201
    assert response.json() == {"id": 1}
    mock_crear_temporada_use_case.execute.assert_called_once()

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_crear_temporada_endpoint_unauthorized(app_client, mock_crear_temporada_use_case, non_admin_user):
    # Arrange
    app_client.app.dependency_overrides[get_crear_temporada_use_case] = lambda: mock_crear_temporada_use_case
    app_client.app.dependency_overrides[get_current_user] = lambda: non_admin_user

    temporada_data = {
        "nombre_temporada": "Temporada 2025-2026",
        "fecha_inicio": "2025-10-01",
        "fecha_fin": "2026-07-25",
        "tipos_cuota": [
            {"nombre": "Cuota General", "importe": 50.00},
            {"nombre": "Cuota Nuevo Socio", "importe": 25.00}
        ]
    }

    # Act
    response = app_client.post("/cuotas/temporadas", json=temporada_data)

    # Assert
    assert response.status_code == 403
    assert response.json() == {"detail": "The user doesn't have enough privileges"}
    mock_crear_temporada_use_case.execute.assert_not_called()

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

# ------------------ Tests for ActualizarTemporada ------------------

@pytest.mark.asyncio
async def test_actualizar_temporada_endpoint_success(app_client, mock_actualizar_temporada_use_case, admin_user):
    # Arrange
    app_client.app.dependency_overrides[get_actualizar_temporada_use_case] = lambda: mock_actualizar_temporada_use_case
    app_client.app.dependency_overrides[get_current_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    temporada_id = 1
    update_data = {
        "nombre_temporada": "Temporada Actualizada",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-12-31",
        "tipos_cuota": []
    }

    # Act
    response = app_client.put(f"/cuotas/temporadas/{temporada_id}", json=update_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "nombre_temporada": "Temporada Actualizada",
        "fecha_inicio": "2025-01-01",
        "fecha_fin": "2025-12-31",
        "tipos_cuota": []
    }
    mock_actualizar_temporada_use_case.execute.assert_called_once_with(admin_user, temporada_id, ActualizarTemporadaDTO(**update_data))

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

# ------------------ Tests for ListarTemporadas ------------------
@pytest.mark.asyncio
async def test_listar_temporadas_endpoint_exists(app_client, admin_user):
    # Arrange
    app_client.app.dependency_overrides[get_current_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    # Act
    response = app_client.get("/cuotas/temporadas")

    # Assert
    # Expecting 200 OK because the endpoint is now implemented
    assert response.status_code == 200

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}