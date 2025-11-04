import pytest
from unittest.mock import AsyncMock
from uuid import uuid4, UUID
from datetime import date, datetime
from decimal import Decimal

from src.app.pedidos.application.use_cases.confirmar_encargo_use_case import ConfirmarEncargoUseCase
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.pedidos.domain.entities import Pedido, TemporadaPedido, LineaDePedido
from src.app.pedidos.domain.value_objects import EstadoPedido
from src.app.pedidos.application.dtos import PedidoDTO
from src.app.pedidos.application.exceptions import TemporadaCerradaException, PedidoNoEncontradoException, PedidoNoValidoException, AccesoDenegadoException

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
def pedido_borrador_con_linea(user_registrado, temporada_activa):
    pedido = Pedido(
        id=uuid4(),
        usuario_id=user_registrado.id,
        temporada_id=temporada_activa.id,
        estado=EstadoPedido.BORRADOR,
        total_calculado=Decimal("10.00"),
        fecha_creacion=datetime.now(),
        lineas=[]
    )
    linea = LineaDePedido(
        id=uuid4(),
        pedido_id=pedido.id,
        variante_prenda_id=uuid4(),
        cantidad=1,
        precio_unitario_conxelado=Decimal("10.00"),
        desc_variante_conxelada="Camiseta M"
    )
    pedido.lineas.append(linea)
    return pedido

@pytest.mark.asyncio
async def test_confirmar_encargo(mock_pedido_repository, mock_temporada_pedido_repository, mock_pedido_policy, user_registrado, temporada_activa, pedido_borrador_con_linea):
    # Arrange
    mock_temporada_pedido_repository.get_temporada_activa.return_value = temporada_activa
    mock_pedido_repository.buscar_borrador_por_usuario.return_value = pedido_borrador_con_linea
    mock_pedido_repository.guardar_pedido.return_value = pedido_borrador_con_linea

    use_case = ConfirmarEncargoUseCase(mock_pedido_repository, mock_temporada_pedido_repository, mock_pedido_policy)

    # Act
    result = await use_case.execute(user_registrado)

    # Assert
    assert isinstance(result, PedidoDTO)
    mock_pedido_repository.guardar_pedido.assert_called_once()
    saved_pedido = mock_pedido_repository.guardar_pedido.call_args[0][0]
    assert saved_pedido.estado == EstadoPedido.ENCARGADO