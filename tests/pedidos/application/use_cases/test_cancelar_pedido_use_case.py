import pytest
from unittest.mock import AsyncMock
from uuid import uuid4, UUID
from datetime import datetime
from decimal import Decimal

from src.app.pedidos.application.use_cases.cancelar_pedido_use_case import CancelarPedidoUseCase
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.pedidos.domain.entities import Pedido
from src.app.pedidos.domain.value_objects import EstadoPedido
from src.app.pedidos.application.dtos import PedidoDTO
from src.app.pedidos.application.exceptions import AccesoDenegadoException, PedidoNoEncontradoException, PedidoNoValidoException

@pytest.fixture
def mock_pedido_repository():
    return AsyncMock(spec=IPedidoRepository)

@pytest.fixture
def mock_pedido_policy():
    mock = AsyncMock(spec=PedidoPolicy)
    mock.cancelar_pedido.return_value = True
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
        fecha_creacion=datetime.now(),
        fecha_finalizacion=datetime.now()
    )

@pytest.mark.asyncio
async def test_cancelar_pedido(mock_pedido_repository, mock_pedido_policy, admin_user, pedido_encargado):
    # Arrange
    mock_pedido_repository.buscar_por_id.return_value = pedido_encargado
    mock_pedido_repository.guardar_pedido.return_value = pedido_encargado

    use_case = CancelarPedidoUseCase(mock_pedido_repository, mock_pedido_policy)

    # Act
    result = await use_case.execute(pedido_encargado.id, admin_user)

    # Assert
    assert isinstance(result, PedidoDTO)
    assert result.estado == EstadoPedido.CANCELADO
    mock_pedido_repository.guardar_pedido.assert_called_once()
    saved_pedido = mock_pedido_repository.guardar_pedido.call_args[0][0]
    assert saved_pedido.estado == EstadoPedido.CANCELADO

@pytest.mark.asyncio
async def test_cancelar_pedido_acceso_denegado(mock_pedido_repository, mock_pedido_policy, pedido_encargado):
    # Arrange
    mock_pedido_policy.cancelar_pedido.return_value = False
    non_admin_user = User(
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

    use_case = CancelarPedidoUseCase(mock_pedido_repository, mock_pedido_policy)

    # Act & Assert
    with pytest.raises(AccesoDenegadoException):
        await use_case.execute(pedido_encargado.id, non_admin_user)

@pytest.mark.asyncio
async def test_cancelar_pedido_no_encontrado(mock_pedido_repository, mock_pedido_policy, admin_user):
    # Arrange
    mock_pedido_repository.buscar_por_id.return_value = None

    use_case = CancelarPedidoUseCase(mock_pedido_repository, mock_pedido_policy)

    # Act & Assert
    with pytest.raises(PedidoNoEncontradoException):
        await use_case.execute(uuid4(), admin_user)

@pytest.mark.asyncio
async def test_cancelar_pedido_ya_completado(mock_pedido_repository, mock_pedido_policy, admin_user, pedido_completado):
    # Arrange
    mock_pedido_repository.buscar_por_id.return_value = pedido_completado

    use_case = CancelarPedidoUseCase(mock_pedido_repository, mock_pedido_policy)

    # Act & Assert
    with pytest.raises(PedidoNoValidoException, match="No se puede cancelar un pedido que ya está completado."):
        await use_case.execute(pedido_completado.id, admin_user)