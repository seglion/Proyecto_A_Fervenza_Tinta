import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal

from src.app.pedidos.infrastructure.postgres_pedido_repository import PostgresPedidoRepository
from src.app.pedidos.domain.entities import Pedido, LineaDePedido
from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago
from src.app.prendas.domain.entities import Prenda, VariantePrenda

# Test para verificar la existencia del archivo postgres_pedido_repository.py
def test_postgres_pedido_repository_file_exists():
    path = Path("src/app/pedidos/infrastructure/postgres_pedido_repository.py")
    assert path.exists(), f"El archivo {path} no existe."

# Test para verificar la existencia de la clase PostgresPedidoRepository
def test_postgres_pedido_repository_class_exists():
    assert hasattr(PostgresPedidoRepository, "__init__")

# Test para verificar que PostgresPedidoRepository implementa IPedidoRepository
def test_postgres_pedido_repository_implements_interface():
    from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
    assert issubclass(PostgresPedidoRepository, IPedidoRepository)

# --- Tests para métodos individuales (usando mocks para la conexión a la DB) ---

@pytest.fixture
def mock_db_connection():
    return AsyncMock()

@pytest.fixture
def repository(mock_db_connection):
    return PostgresPedidoRepository(mock_db_connection)

# Ejemplo de test para buscar_borrador_por_usuario_y_temporada
@pytest.mark.asyncio
async def test_buscar_borrador_por_usuario_y_temporada_found(repository, mock_db_connection):
    user_id = uuid4()
    temporada_id = 1
    mock_row = {
        "id": uuid4(),
        "usuario_id": user_id,
        "temporada_id": temporada_id,
        "estado": EstadoPedido.BORRADOR.value,
        "total_calculado": Decimal("10.00"),
        "metodo_pago": None,
        "id_transaccion_externa": None,
        "fecha_creacion": datetime.now(),
        "fecha_finalizacion": None,
    }
    mock_db_connection.fetchrow.return_value = mock_row

    pedido = await repository.buscar_borrador_por_usuario_y_temporada(user_id, temporada_id)

    assert pedido is not None
    assert pedido.id == mock_row["id"]
    assert pedido.usuario_id == user_id
    assert pedido.estado == EstadoPedido.BORRADOR
    mock_db_connection.fetchrow.assert_called_once_with(
        "SELECT id, usuario_id, temporada_id, estado, total_calculado, metodo_pago, id_transaccion_externa, fecha_creacion, fecha_finalizacion FROM pedidos WHERE usuario_id = $1 AND temporada_id = $2 AND estado = $3::estado_pedido_enum",
        user_id, temporada_id, EstadoPedido.BORRADOR.value
    )

@pytest.mark.asyncio
async def test_buscar_borrador_por_usuario_y_temporada_not_found(repository, mock_db_connection):
    user_id = uuid4()
    temporada_id = 1
    mock_db_connection.fetchrow.return_value = None

    pedido = await repository.buscar_borrador_por_usuario_y_temporada(user_id, temporada_id)

    assert pedido is None
    mock_db_connection.fetchrow.assert_called_once()

# TODO: Añadir más tests para los demás métodos de PostgresPedidoRepository
# Estos tests deberían usar mocks para la conexión a la base de datos y verificar:
# - Que las consultas SQL son correctas.
# - Que los datos se mapean correctamente a las entidades de dominio.
# - Que los métodos manejan correctamente los casos de éxito y error.
# Para pruebas de integración completas, se necesitaría una base de datos de test real.