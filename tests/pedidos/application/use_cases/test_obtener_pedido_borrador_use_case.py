import pytest
from unittest.mock import AsyncMock
from uuid import uuid4, UUID
from datetime import date, datetime
from decimal import Decimal

from src.app.pedidos.application.use_cases.obtener_pedido_borrador_use_case import ObtenerPedidoBorradorUseCase
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.pedidos.domain.entities import Pedido, TemporadaPedido
from src.app.pedidos.domain.value_objects import EstadoPedido
from src.app.pedidos.application.dtos import PedidoDTO
from src.app.pedidos.application.exceptions import TemporadaCerradaException, AccesoDenegadoException

@pytest.fixture
def mock_pedido_repository():
    return AsyncMock(spec=IPedidoRepository)

@pytest.fixture
def mock_temporada_pedido_repository():
    return AsyncMock(spec=ITemporadaPedidoRepository)

@pytest.fixture
def mock_pedido_policy():
    mock = AsyncMock(spec=PedidoPolicy)
    mock.ver_pedido.return_value = True
    return mock

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
def temporada_activa():
    return TemporadaPedido(
        id=1,
        nombre_temporada="2025-2026",
        fecha_inicio=date(2025, 8, 16),
        fecha_fin=date(2026, 5, 31),
        esta_activa=True,
        fecha_creacion=datetime.now()
    )

@pytest.fixture
def pedido_borrador(user_registrado, temporada_activa):
    return Pedido(
        id=uuid4(),
        usuario_id=user_registrado.id,
        temporada_id=temporada_activa.id,
        estado=EstadoPedido.BORRADOR,
        total_calculado=Decimal("0.00"),
        fecha_creacion=datetime.now(),
        lineas=[]
    )

@pytest.mark.asyncio
async def test_obtener_pedido_borrador_existente(mock_pedido_repository, mock_temporada_pedido_repository, mock_pedido_policy, user_registrado, temporada_activa, pedido_borrador):
    # Arrange
    mock_temporada_pedido_repository.get_temporada_activa.return_value = temporada_activa
    mock_pedido_repository.buscar_borrador_por_usuario_y_temporada.return_value = pedido_borrador

    use_case = ObtenerPedidoBorradorUseCase(mock_pedido_repository, mock_temporada_pedido_repository, mock_pedido_policy)

    # Act
    result = await use_case.execute(user_registrado)

    # Assert
    assert isinstance(result, PedidoDTO)
    assert result.id == pedido_borrador.id
    mock_pedido_repository.buscar_borrador_por_usuario_y_temporada.assert_called_once_with(user_registrado.id, temporada_activa.id)

@pytest.mark.asyncio
async def test_obtener_pedido_borrador_inexistente(mock_pedido_repository, mock_temporada_pedido_repository, mock_pedido_policy, user_registrado, temporada_activa):
    # Arrange
    mock_temporada_pedido_repository.get_temporada_activa.return_value = temporada_activa
    mock_pedido_repository.buscar_borrador_por_usuario_y_temporada.return_value = None

    use_case = ObtenerPedidoBorradorUseCase(mock_pedido_repository, mock_temporada_pedido_repository, mock_pedido_policy)

    # Act
    result = await use_case.execute(user_registrado)

    # Assert
    assert isinstance(result, PedidoDTO)
    assert result.id == UUID('00000000-0000-0000-0000-000000000000')
    assert result.usuario_id == user_registrado.id
    assert result.estado == EstadoPedido.BORRADOR

@pytest.mark.asyncio
async def test_obtener_pedido_borrador_temporada_cerrada(mock_pedido_repository, mock_temporada_pedido_repository, mock_pedido_policy, user_registrado):
    # Arrange
    mock_temporada_pedido_repository.get_temporada_activa.return_value = None

    use_case = ObtenerPedidoBorradorUseCase(mock_pedido_repository, mock_temporada_pedido_repository, mock_pedido_policy)

    # Act & Assert
    with pytest.raises(TemporadaCerradaException):
        await use_case.execute(user_registrado)

@pytest.mark.asyncio
async def test_obtener_pedido_borrador_acceso_denegado(mock_pedido_repository, mock_temporada_pedido_repository, mock_pedido_policy, user_registrado, temporada_activa, pedido_borrador):
    # Arrange
    mock_temporada_pedido_repository.get_temporada_activa.return_value = temporada_activa
    mock_pedido_repository.buscar_borrador_por_usuario_y_temporada.return_value = pedido_borrador
    mock_pedido_policy.ver_pedido.return_value = False

    use_case = ObtenerPedidoBorradorUseCase(mock_pedido_repository, mock_temporada_pedido_repository, mock_pedido_policy)

    # Act & Assert
    with pytest.raises(AccesoDenegadoException):
        await use_case.execute(user_registrado)