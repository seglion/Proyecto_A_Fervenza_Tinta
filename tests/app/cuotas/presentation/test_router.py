import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import date, datetime

from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.core.dependencies import get_current_user
from src.app.cuotas.presentation.router import get_admin_user, get_ver_detalle_cuota_use_case
from src.app.cuotas.application.dtos import DetalleCuotaDTO, CuotaDTO, TemporadaDTO, TipoCuotaDTO

# ------------------ Fixtures ------------------
@pytest.fixture(scope="function")
def app_client():
    from src.app.cuotas.presentation.router import router as cuotas_router
    app = FastAPI()
    app.include_router(cuotas_router)
    with TestClient(app) as client:
        yield client

@pytest.fixture
def admin_user():
    return User(id=uuid4(), rol=Rol.ADMIN, email="admin@test.com", contrasena_hasheada="123", nombre="Admin", apellidos="Test", numero_telefono="123456789", esta_activo=True, email_verificado=True, aprobado_por_admin=True)

@pytest.fixture
def non_admin_user():
    return User(id=uuid4(), rol=Rol.USUARIO, email="user@test.com", contrasena_hasheada="123", nombre="User", apellidos="Test", numero_telefono="987654321", esta_activo=True, email_verificado=True, aprobado_por_admin=True)

@pytest.fixture
def mock_ver_detalle_cuota_use_case():
    mock = AsyncMock()
    cuota_id = uuid4()
    user_id = uuid4()
    mock.execute.return_value = DetalleCuotaDTO(
        cuota=CuotaDTO(
            id=cuota_id,
            usuario_id=user_id,
            tipo_de_cuota_id=1,
            importe_pagado=50.00,
            estado_pago="completado",
            fecha_pago=datetime.now(),
            metodo_pago="stripe"
        ),
        temporada=TemporadaDTO(
            id=1,
            nombre_temporada="2025-2026",
            fecha_inicio=date(2025, 10, 1),
            fecha_fin=date(2026, 7, 25),
            tipos_cuota=[
                TipoCuotaDTO(id=1, nombre="Cuota General", importe=50.00, fecha_creacion=datetime.now())
            ]
        )
    )
    return mock

# ------------------ Tests for VerDetalleCuota ------------------

@pytest.mark.asyncio
async def test_ver_detalle_cuota_success(app_client, admin_user, mock_ver_detalle_cuota_use_case):
    # Arrange
    cuota_id = uuid4()
    app_client.app.dependency_overrides[get_current_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_admin_user] = lambda: admin_user
    app_client.app.dependency_overrides[get_ver_detalle_cuota_use_case] = lambda: mock_ver_detalle_cuota_use_case

    # Act
    response = app_client.get(f"/cuotas/{cuota_id}")

    # Assert
    assert response.status_code == 200
    mock_ver_detalle_cuota_use_case.execute.assert_called_once_with(admin_user, cuota_id)
    # Assert body structure
    response_data = response.json()
    assert "cuota" in response_data
    assert "temporada" in response_data
    assert response_data["cuota"]["estado_pago"] == "completado"
    assert response_data["temporada"]["nombre_temporada"] == "2025-2026"


    # Cleanup
    app_client.app.dependency_overrides = {}

@pytest.mark.asyncio
async def test_ver_detalle_cuota_unauthorized_if_not_admin(app_client, non_admin_user):
    # Arrange
    cuota_id = uuid4()
    app_client.app.dependency_overrides[get_current_user] = lambda: non_admin_user
    
    # Act
    response = app_client.get(f"/cuotas/{cuota_id}")
    
    # Assert
    assert response.status_code == 403
    assert response.json() == {"detail": "The user doesn't have enough privileges"}
    
    # Cleanup
    app_client.app.dependency_overrides = {}
