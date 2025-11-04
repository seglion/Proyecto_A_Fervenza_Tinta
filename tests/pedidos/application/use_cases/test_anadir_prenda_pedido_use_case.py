import pytest
from unittest.mock import AsyncMock
from uuid import uuid4, UUID
from datetime import date, datetime
from decimal import Decimal

from src.app.pedidos.application.use_cases.anadir_prenda_pedido_use_case import AnadirPrendaPedidoUseCase
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.prendas.application.repositories.i_variante_prenda_repository import IVariantePrendaRepository
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.pedidos.domain.entities import Pedido, TemporadaPedido, LineaDePedido
from src.app.prendas.domain.entities import Prenda, VariantePrenda
from src.app.pedidos.domain.value_objects import EstadoPedido
from src.app.pedidos.application.dtos import PedidoDTO, DatosLineaDTO
from src.app.pedidos.application.exceptions import TemporadaCerradaException, PedidoNoValidoException

@pytest.fixture
def mock_pedido_repository():
    return AsyncMock(spec=IPedidoRepository)

@pytest.fixture
def mock_temporada_pedido_repository():
    return AsyncMock(spec=ITemporadaPedidoRepository)

@pytest.fixture
def mock_variante_prenda_repository():
    return AsyncMock(spec=IVariantePrendaRepository)

@pytest.fixture
def mock_prenda_repository():
    return AsyncMock(spec=IPrendaRepository)

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

@pytest.fixture
def prenda():
    return Prenda(id=uuid4(), nombre="Camiseta", descripcion="", precio=Decimal("10.00"), imagen_url="", fecha_creacion=datetime.now())

@pytest.fixture
def variante_prenda(prenda):
    return VariantePrenda(id=uuid4(), prenda_id=prenda.id, genero="Unisex", talla="M", fecha_creacion=datetime.now())

@pytest.mark.asyncio
async def test_anadir_prenda_a_pedido(mock_pedido_repository, mock_temporada_pedido_repository, mock_variante_prenda_repository, mock_prenda_repository, user_registrado, temporada_activa, pedido_borrador, prenda, variante_prenda):
    # Arrange
    mock_temporada_pedido_repository.get_temporada_activa.return_value = temporada_activa
    mock_pedido_repository.obtener_o_crear_borrador.return_value = pedido_borrador
    mock_variante_prenda_repository.buscar_por_id.return_value = variante_prenda
    mock_prenda_repository.buscar_por_id_con_variantes.return_value = prenda
    mock_pedido_repository.anadir_o_actualizar_linea.return_value = pedido_borrador
    mock_pedido_repository.guardar_pedido.return_value = pedido_borrador

    use_case = AnadirPrendaPedidoUseCase(mock_pedido_repository, mock_temporada_pedido_repository, mock_variante_prenda_repository, mock_prenda_repository)
    datos_linea = DatosLineaDTO(variante_id=variante_prenda.id, cantidad=1)

    # Act
    result = await use_case.execute(user_registrado, datos_linea)

    # Assert
    assert isinstance(result, PedidoDTO)
    mock_pedido_repository.anadir_o_actualizar_linea.assert_called_once_with(pedido_borrador, variante_prenda, prenda, 1)
    mock_pedido_repository.guardar_pedido.assert_called_once_with(pedido_borrador)