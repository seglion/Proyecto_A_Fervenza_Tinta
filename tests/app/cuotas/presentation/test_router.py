from fastapi import FastAPI, APIRouter, Depends
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from uuid import uuid4
import pytest


from src.app.cuotas.application.dtos import CuotaDTO, ListaCuotasDTO
from src.app.cuotas.presentation.router import router as cuotas_router
from src.app.cuotas.presentation.router import get_listar_cuotas_use_case
from src.app.cuotas.presentation.router import get_admin_user
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.core.dependencies import get_current_user

@pytest.fixture(scope="module")
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

def test_router_file_exists():
    try:
        from src.app.cuotas.presentation.router import router
        assert isinstance(router, APIRouter)
    except ImportError:
        pytest.fail("El archivo 'router.py' o la instancia 'router' no existen en app.cuotas.presentation")

@pytest.fixture
def mock_listar_cuotas_use_case():
    mock = AsyncMock()
    mock.execute.return_value = ListaCuotasDTO(
        cuotas=[
            CuotaDTO(
                id=uuid4(),
                usuario_id=uuid4(),
                tipo_de_cuota_id=1,
                importe_pagado=50.00,
                estado_pago="completado",
                fecha_pago="2025-01-01T10:00:00Z",
                metodo_pago="stripe",
                id_transaccion_externa="txn_123",
                notas_admin="Notas de prueba"
            )
        ]
    )
    return mock

@pytest.mark.asyncio
async def test_listar_cuotas_endpoint_success(app_client, mock_listar_cuotas_use_case, admin_user):
    # Arrange
    app_client.app.dependency_overrides[get_listar_cuotas_use_case] = lambda: mock_listar_cuotas_use_case
    app_client.app.dependency_overrides[get_current_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user

    # Act
    response = app_client.get("/cuotas")

    # Assert
    assert response.status_code == 200
    assert len(response.json()["cuotas"]) == 1
    mock_listar_cuotas_use_case.execute.assert_called_once_with(admin_user)

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_listar_cuotas_endpoint_unauthorized(app_client, mock_listar_cuotas_use_case, non_admin_user):
    # Arrange
    app_client.app.dependency_overrides[get_listar_cuotas_use_case] = lambda: mock_listar_cuotas_use_case
    app_client.app.dependency_overrides[get_current_user] = lambda: non_admin_user
    app_client.app.dependency_overrides[get_admin_user] = lambda: non_admin_user

    # Act
    response = app_client.get("/cuotas")

    # Assert
    assert response.status_code == 403
    assert response.json() == {"detail": "The user doesn't have enough privileges"}
    mock_listar_cuotas_use_case.execute.assert_not_called()

    # Clear overrides after the test
    app_client.app.dependency_overrides = {}