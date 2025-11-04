import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4, UUID
from datetime import datetime
from decimal import Decimal

from src.app.pedidos.application.use_cases.procesar_webhook_pedido_use_case import ProcesarWebhookPedidoUseCase
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.core.services.i_email_service import IEmailService
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.pedidos.domain.entities import Pedido
from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago
from src.app.pedidos.application.exceptions import PedidoNoEncontradoException

@pytest.fixture
def mock_pedido_repository():
    return AsyncMock(spec=IPedidoRepository)

@pytest.fixture
def mock_user_repository():
    return AsyncMock(spec=IUserRepository)

@pytest.fixture
def mock_payment_gateway():
    return AsyncMock(spec=IPaymentGateway)

@pytest.fixture
def mock_email_service():
    return AsyncMock(spec=IEmailService)

@pytest.fixture
def user_registrado():
    return User(
        id=uuid4(),
        email="user@example.com",
        contrasena_hasheada="hashed_password",
        nombre="Test",
        apellidos="User",
        numero_telefono="123456789",
        rol=Rol.USUARIO,
        esta_activo=True,
        email_verificado=True,
        aprobado_por_admin=True
    )

@pytest.fixture
def pedido_pendiente_pago(user_registrado):
    return Pedido(
        id=uuid4(),
        usuario_id=user_registrado.id,
        temporada_id=1,
        estado=EstadoPedido.PENDIENTEPAGO,
        total_calculado=Decimal("20.00"),
        fecha_creacion=datetime.now()
    )

@pytest.mark.asyncio
async def test_procesar_webhook_pedido(mock_pedido_repository, mock_user_repository, mock_payment_gateway, mock_email_service, user_registrado, pedido_pendiente_pago):
    # Arrange
    event = MagicMock()
    event.type = "checkout.session.completed"
    event.data = {
        'object': {
            'metadata': {'pedido_id': str(pedido_pendiente_pago.id)},
            'payment_intent': 'pi_123'
        }
    }
    mock_payment_gateway.validar_webhook.return_value = event
    mock_pedido_repository.buscar_por_id.return_value = pedido_pendiente_pago
    mock_user_repository.buscar_por_id.return_value = user_registrado

    use_case = ProcesarWebhookPedidoUseCase(mock_payment_gateway, mock_pedido_repository, mock_user_repository, mock_email_service)

    # Act
    await use_case.execute(b'payload', 'sig_header')

    # Assert
    mock_pedido_repository.guardar_pedido.assert_called_once()
    saved_pedido = mock_pedido_repository.guardar_pedido.call_args[0][0]
    assert saved_pedido.estado == EstadoPedido.COMPLETADO
    assert saved_pedido.metodo_pago == MetodoPago.STRIPE
    assert saved_pedido.id_transaccion_externa == 'pi_123'
    mock_email_service.enviar_confirmacion_pago_pedido.assert_called_once()