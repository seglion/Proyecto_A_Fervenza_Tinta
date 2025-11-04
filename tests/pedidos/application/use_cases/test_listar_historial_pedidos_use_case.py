import pytest
from unittest.mock import AsyncMock
from uuid import uuid4, UUID
from datetime import date, datetime
from decimal import Decimal

from src.app.pedidos.application.use_cases.listar_historial_pedidos_use_case import ListarHistorialPedidosUseCase
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.pedidos.domain.entities import Pedido, TemporadaPedido
from src.app.pedidos.domain.value_objects import EstadoPedido
from src.app.pedidos.application.dtos import ListaPedidosDTO
from src.app.pedidos.application.exceptions import AccesoDenegadoException

@pytest.fixture
def mock_pedido_repository():
    return AsyncMock(spec=IPedidoRepository)

@pytest.fixture
def mock_pedido_policy():
    mock = AsyncMock(spec=PedidoPolicy)
    mock.puede_listar_historial.return_value = True
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
def historial_pedidos(user_registrado, temporada_activa):
    return [
        Pedido(
            id=uuid4(),
            usuario_id=user_registrado.id,
            temporada_id=temporada_activa.id,
            estado=EstadoPedido.COMPLETADO,
            total_calculado=Decimal("20.00"),
            fecha_creacion=datetime.now(),
            fecha_finalizacion=datetime.now()
        ),
        Pedido(
            id=uuid4(),
            usuario_id=user_registrado.id,
            temporada_id=temporada_activa.id,
            estado=EstadoPedido.ENCARGADO,
            total_calculado=Decimal("30.00"),
            fecha_creacion=datetime.now(),
            fecha_finalizacion=datetime.now()
        )
    ]

@pytest.mark.asyncio
async def test_listar_historial_pedidos(mock_pedido_repository, mock_pedido_policy, user_registrado, historial_pedidos):
    # Arrange
    mock_pedido_repository.buscar_historial_por_usuario.return_value = historial_pedidos

    use_case = ListarHistorialPedidosUseCase(mock_pedido_repository, mock_pedido_policy)

    # Act
    result = await use_case.execute(user_registrado)

    # Assert
    assert isinstance(result, ListaPedidosDTO)
    assert len(result.pedidos) == 2
    mock_pedido_repository.buscar_historial_por_usuario.assert_called_once_with(user_registrado.id)

@pytest.mark.asyncio
async def test_listar_historial_pedidos_acceso_denegado(mock_pedido_repository, mock_pedido_policy, user_registrado):
    # Arrange
    mock_pedido_policy.puede_listar_historial.return_value = False

    use_case = ListarHistorialPedidosUseCase(mock_pedido_repository, mock_pedido_policy)

    # Act & Assert
    with pytest.raises(AccesoDenegadoException):
        await use_case.execute(user_registrado)