import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import date, datetime

from src.app.pedidos.application.use_cases.crear_temporada_pedido_use_case import CrearTemporadaPedidoUseCase
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.pedidos.domain.entities import TemporadaPedido
from src.app.pedidos.application.dtos import DatosTemporadaPedidoDTO, TemporadaPedidoDTO
from src.app.pedidos.application.exceptions import AccesoDenegadoException

@pytest.fixture
def mock_temporada_pedido_repository():
    return AsyncMock(spec=ITemporadaPedidoRepository)

@pytest.fixture
def mock_pedido_policy():
    mock = AsyncMock(spec=PedidoPolicy)
    mock.gestionar_temporadas.return_value = True
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
def datos_temporada_dto():
    return DatosTemporadaPedidoDTO(
        nombre_temporada="2026-2027",
        fecha_inicio=date(2026, 8, 16),
        fecha_fin=date(2027, 5, 31)
    )

@pytest.mark.asyncio
async def test_crear_temporada_pedido(mock_temporada_pedido_repository, mock_pedido_policy, admin_user, datos_temporada_dto):
    # Arrange
    mock_temporada_pedido_repository.guardar.return_value = TemporadaPedido(
        id=2,
        nombre_temporada=datos_temporada_dto.nombre_temporada,
        fecha_inicio=datos_temporada_dto.fecha_inicio,
        fecha_fin=datos_temporada_dto.fecha_fin,
        esta_activa=False,
        fecha_creacion=datetime.now()
    )

    use_case = CrearTemporadaPedidoUseCase(mock_temporada_pedido_repository, mock_pedido_policy)

    # Act
    result = await use_case.execute(datos_temporada_dto, admin_user)

    # Assert
    assert isinstance(result, TemporadaPedidoDTO)
    assert result.nombre_temporada == datos_temporada_dto.nombre_temporada
    mock_temporada_pedido_repository.guardar.assert_called_once()

@pytest.mark.asyncio
async def test_crear_temporada_pedido_acceso_denegado(mock_temporada_pedido_repository, mock_pedido_policy, datos_temporada_dto):
    # Arrange
    mock_pedido_policy.gestionar_temporadas.return_value = False
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

    use_case = CrearTemporadaPedidoUseCase(mock_temporada_pedido_repository, mock_pedido_policy)

    # Act & Assert
    with pytest.raises(AccesoDenegadoException):
        await use_case.execute(datos_temporada_dto, non_admin_user)