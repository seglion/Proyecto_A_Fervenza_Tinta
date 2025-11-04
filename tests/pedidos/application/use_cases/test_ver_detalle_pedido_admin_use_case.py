import pytest
from unittest.mock import AsyncMock
from uuid import uuid4, UUID
from datetime import date, datetime
from decimal import Decimal

from src.app.pedidos.application.use_cases.ver_detalle_pedido_admin_use_case import VerDetallePedidoAdminUseCase
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.pedidos.domain.entities import Pedido, TemporadaPedido
from src.app.pedidos.domain.value_objects import EstadoPedido
from src.app.pedidos.application.dtos import PedidoDetalleAdminDTO
from src.app.pedidos.application.exceptions import AccesoDenegadoException, PedidoNoEncontradoException

@pytest.fixture
def mock_pedido_repository():
    return AsyncMock(spec=IPedidoRepository)

@pytest.fixture
def mock_pedido_policy():
    mock = AsyncMock(spec=PedidoPolicy)
    mock.es_administrador.return_value = True
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
async def test_ver_detalle_pedido_admin(mock_pedido_repository, mock_pedido_policy, admin_user, pedido_completado):
    # Arrange
    mock_pedido_repository.buscar_por_id_con_detalle.return_value = pedido_completado

    use_case = VerDetallePedidoAdminUseCase(mock_pedido_repository, mock_pedido_policy)

    # Act
    result = await use_case.execute(pedido_completado.id, admin_user)

    # Assert
    assert isinstance(result, PedidoDetalleAdminDTO)
    assert result.id == pedido_completado.id
    mock_pedido_repository.buscar_por_id_con_detalle.assert_called_once_with(pedido_completado.id)

@pytest.mark.asyncio
async def test_ver_detalle_pedido_admin_acceso_denegado(mock_pedido_repository, mock_pedido_policy, pedido_completado):
    # Arrange
    mock_pedido_policy.es_administrador.return_value = False
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

    use_case = VerDetallePedidoAdminUseCase(mock_pedido_repository, mock_pedido_policy)

    # Act & Assert
    with pytest.raises(AccesoDenegadoException):
        await use_case.execute(pedido_completado.id, non_admin_user)

@pytest.mark.asyncio
async def test_ver_detalle_pedido_admin_no_encontrado(mock_pedido_repository, mock_pedido_policy, admin_user):
    # Arrange
    mock_pedido_repository.buscar_por_id_con_detalle.return_value = None

    use_case = VerDetallePedidoAdminUseCase(mock_pedido_repository, mock_pedido_policy)

    # Act & Assert
    with pytest.raises(PedidoNoEncontradoException):
        await use_case.execute(uuid4(), admin_user)