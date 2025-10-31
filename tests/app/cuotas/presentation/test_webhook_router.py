import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from src.app.cuotas.presentation.router import get_procesar_webhook_use_case

@pytest.fixture(scope="function")
def app_client():
    from src.app.cuotas.presentation.router import router as cuotas_router
    app = FastAPI()
    app.include_router(cuotas_router)
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_procesar_webhook_use_case():
    mock = AsyncMock()
    return mock

@pytest.mark.asyncio
async def test_procesar_webhook_success(app_client, mock_procesar_webhook_use_case):
    # Arrange
    app_client.app.dependency_overrides[get_procesar_webhook_use_case] = lambda: mock_procesar_webhook_use_case
    payload = {"type": "payment_intent.succeeded"}
    headers = {"stripe-signature": "test_signature"}

    # Act
    response = app_client.post("/cuotas/webhooks/stripe", json=payload, headers=headers)

    # Assert
    assert response.status_code == 200
    mock_procesar_webhook_use_case.execute.assert_called_once()

    # Cleanup
    app_client.app.dependency_overrides = {}
