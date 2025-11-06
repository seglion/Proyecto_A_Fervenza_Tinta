import pytest
from unittest.mock import AsyncMock
from uuid import uuid4, UUID
from datetime import datetime
from decimal import Decimal

from src.app.pedidos.application.use_cases.marcar_pago_manual_pedido_use_case import MarcarPagoManualPedidoUseCase
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.core.services.i_email_service import IEmailService
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.pedidos.domain.entities import Pedido
from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago
from src.app.pedidos.application.dtos import DatosPagoManualDTO, PedidoCompletadoDTO
from src.app.pedidos.application.exceptions import AccesoDenegadoException, PedidoNoEncontradoException, PedidoNoModificableException

@pytest.fixture
def mock_pedido_repository():
    return AsyncMock(spec=IPedidoRepository)

@pytest.fixture
def mock_user_repository():
    return AsyncMock(spec=IUserRepository)

@pytest.fixture
def mock_email_service():
    return AsyncMock(spec=IEmailService)

@pytest.fixture
def mock_pedido_policy():
    mock = AsyncMock(spec=PedidoPolicy)
    mock.marcar_pagado.return_value = True
    return mock

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
def pedido_encargado(admin_user):
    return Pedido(
        id=uuid4(),
        usuario_id=admin_user.id,
        temporada_id=1,
        estado=EstadoPedido.ENCARGADO,
        total_calculado=Decimal("20.00"),
        fecha_creacion=datetime.now()
    )

@pytest.fixture
def pedido_completado(admin_user):
    return Pedido(
        id=uuid4(),
        usuario_id=admin_user.id,
        temporada_id=1,
        estado=EstadoPedido.COMPLETADO,
        total_calculado=Decimal("20.00"),
        fecha_creacion=datetime.now()
    )

@pytest.fixture
def datos_pago_manual_dto():
    return DatosPagoManualDTO(metodo_pago="MANUAL", id_transaccion_externa="test-tx-123")

@pytest.mark.asyncio
async def test_marcar_pago_manual_pedido(mock_pedido_repository, mock_user_repository, mock_email_service, mock_pedido_policy, admin_user, pedido_encargado, datos_pago_manual_dto):
    # Arrange
    mock_pedido_repository.buscar_por_id_con_detalle.return_value = pedido_encargado
    mock_pedido_repository.guardar_pedido.return_value = pedido_encargado
    mock_user_repository.buscar_por_id.return_value = admin_user

    use_case = MarcarPagoManualPedidoUseCase(mock_pedido_repository, mock_user_repository, mock_email_service, mock_pedido_policy)

    # Act
    result = await use_case.execute(pedido_encargado.id, datos_pago_manual_dto, admin_user)

    # Assert
    assert isinstance(result, Pedido)
    assert result.estado == EstadoPedido.COMPLETADO
    mock_pedido_repository.guardar_pedido.assert_called_once()
    saved_pedido = mock_pedido_repository.guardar_pedido.call_args[0][0]
    assert saved_pedido.estado == EstadoPedido.COMPLETADO
    assert saved_pedido.metodo_pago == MetodoPago.MANUAL
    mock_email_service.enviar_confirmacion_pago_pedido.assert_called_once()

@pytest.mark.asyncio
async def test_marcar_pago_manual_pedido_no_modificable(mock_pedido_repository, mock_user_repository, mock_email_service, mock_pedido_policy, admin_user, pedido_completado, datos_pago_manual_dto):
    # Arrange
    mock_pedido_repository.buscar_por_id_con_detalle.return_value = pedido_completado

    use_case = MarcarPagoManualPedidoUseCase(mock_pedido_repository, mock_user_repository, mock_email_service, mock_pedido_policy)

    # Act & Assert
    with pytest.raises(PedidoNoModificableException):
        await use_case.execute(pedido_completado.id, datos_pago_manual_dto, admin_user)