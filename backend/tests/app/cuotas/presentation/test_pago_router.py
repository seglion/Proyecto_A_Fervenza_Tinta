import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from uuid import uuid4

from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.core.dependencies import get_current_user
from src.app.cuotas.presentation.router import get_crear_intento_pago_use_case, get_obtener_generar_mi_cuota_use_case
from src.app.cuotas.application.dtos import IntentoPagoDTO, CuotaDTO
from src.app.core.services.i_payment_gateway import IPaymentGateway

@pytest.fixture(scope="function")
def app_client():
    from src.app.cuotas.presentation.router import router as cuotas_router
    app = FastAPI()
    app.include_router(cuotas_router)
    with TestClient(app) as client:
        yield client

@pytest.fixture
def normal_user():
    return User(id=uuid4(), rol=Rol.USUARIO, email="user@test.com", contrasena_hasheada="123", nombre="User", apellidos="Test", numero_telefono="987654321", esta_activo=True, email_verificado=True, aprobado_por_admin=True)

@pytest.fixture
def mock_crear_intento_pago_use_case():
    mock = AsyncMock()
    mock.execute.return_value = IntentoPagoDTO(url_pago="https://stripe.com/pay/test_url")
    return mock

@pytest.fixture
def mock_obtener_generar_mi_cuota_use_case():
    mock = AsyncMock()
    mock.execute.return_value = CuotaDTO(id=uuid4(), usuario_id=uuid4(), tipo_de_cuota_id=1, importe_pagado=50.0, estado_pago="pendiente")
    return mock

@pytest.fixture
def mock_payment_gateway():
    mock = AsyncMock()
    mock.crear_sesion_pago.return_value = "https://stripe.com/pay/test_url"
    return mock

@pytest.mark.asyncio
async def test_crear_intento_pago_success(app_client, normal_user, mock_crear_intento_pago_use_case, mock_obtener_generar_mi_cuota_use_case, mock_payment_gateway):
    # Arrange
    app_client.app.dependency_overrides[get_current_user] = lambda: normal_user
    app_client.app.dependency_overrides[get_crear_intento_pago_use_case] = lambda: mock_crear_intento_pago_use_case
    app_client.app.dependency_overrides[get_obtener_generar_mi_cuota_use_case] = lambda: mock_obtener_generar_mi_cuota_use_case
    app_client.app.dependency_overrides[IPaymentGateway] = lambda: mock_payment_gateway

    # Act
    response = app_client.post("/cuotas/crear-intento-pago")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"url_pago": "https://stripe.com/pay/test_url"}
    mock_crear_intento_pago_use_case.execute.assert_called_once_with(normal_user)

    # Cleanup
    app_client.app.dependency_overrides = {}
