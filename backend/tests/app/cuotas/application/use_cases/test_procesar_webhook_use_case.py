import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import EstadoPago
from src.app.core.services.i_email_service import IEmailService
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol


def test_use_case_file_exists():
    try:
        from src.app.cuotas.application.use_cases import procesar_webhook_use_case
    except ImportError:
        pytest.fail("El fichero del caso de uso 'procesar_webhook_use_case.py' no existe.")

def test_use_case_class_exists():
    try:
        from src.app.cuotas.application.use_cases.procesar_webhook_use_case import ProcesarWebhookUseCase
    except ImportError:
        pytest.fail("La clase del caso de uso 'ProcesarWebhookUseCase' no existe.")

@pytest.mark.asyncio
async def test_use_case_initialization():
    mock_payment_gateway = AsyncMock(spec=IPaymentGateway)
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_email_service = AsyncMock(spec=IEmailService)
    mock_user_repository = AsyncMock(spec=IUserRepository)
    try:
        from src.app.cuotas.application.use_cases.procesar_webhook_use_case import ProcesarWebhookUseCase
        ProcesarWebhookUseCase(
            mock_payment_gateway,
            mock_cuota_repo,
            mock_email_service,
            mock_user_repository
        )
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'ProcesarWebhookUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    from src.app.cuotas.application.use_cases.procesar_webhook_use_case import ProcesarWebhookUseCase
    mock_payment_gateway = AsyncMock(spec=IPaymentGateway)
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_email_service = AsyncMock(spec=IEmailService)
    mock_user_repository = AsyncMock(spec=IUserRepository)
    use_case = ProcesarWebhookUseCase(
        mock_payment_gateway,
        mock_cuota_repo,
        mock_email_service,
        mock_user_repository
    )
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_procesar_webhook_success():
    from src.app.cuotas.application.use_cases.procesar_webhook_use_case import ProcesarWebhookUseCase
    mock_payment_gateway = AsyncMock(spec=IPaymentGateway)
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_email_service = AsyncMock(spec=IEmailService)
    mock_user_repository = AsyncMock(spec=IUserRepository)

    cuota_id = uuid4()
    user_id = uuid4()
    payload_str = f'{{"id": "evt_123", "object": "event", "type": "checkout.session.completed", "data": {{"object": {{"metadata": {{"cuota_id": "{cuota_id}"}}}}}}}}'
    payload = payload_str.encode('utf-8')
    sig_header = "some_signature"
    cuota_pendiente = Cuota(id=cuota_id, usuario_id=user_id, tipo_de_cuota_id=1, importe_pagado=50, estado_pago=EstadoPago.PENDIENTE)
    mock_user = User(id=user_id, email="test@example.com", contrasena_hasheada="hashed", nombre="Test", apellidos="User", numero_telefono="1234567890", rol=Rol.USUARIO, esta_activo=True, email_verificado=True)

    class MockEvent:
        def __init__(self, type, data):
            self.type = type
            self.data = data

    mock_event = MockEvent(type="checkout.session.completed", data={'object': {'metadata': {'cuota_id': str(cuota_id)}}})
    mock_payment_gateway.validar_webhook.return_value = mock_event
    mock_cuota_repo.buscar_por_id.return_value = cuota_pendiente
    mock_user_repository.buscar_por_id.return_value = mock_user
    mock_email_service.enviar_email_confirmacion_pago.return_value = AsyncMock()

    use_case = ProcesarWebhookUseCase(mock_payment_gateway, mock_cuota_repo, mock_email_service, mock_user_repository)
    await use_case.execute(payload, sig_header)

    mock_cuota_repo.actualizar.assert_called_once()
    mock_user_repository.buscar_por_id.assert_called_once_with(user_id)
    mock_email_service.enviar_email_confirmacion_pago.assert_called_once()
