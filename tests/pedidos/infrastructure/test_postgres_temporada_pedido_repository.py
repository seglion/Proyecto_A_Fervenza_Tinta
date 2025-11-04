import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from datetime import date, datetime

from src.app.pedidos.infrastructure.postgres_temporada_pedido_repository import PostgresTemporadaPedidoRepository
from src.app.pedidos.domain.entities import TemporadaPedido

# Test para verificar la existencia del archivo postgres_temporada_pedido_repository.py
def test_postgres_temporada_pedido_repository_file_exists():
    path = Path("src/app/pedidos/infrastructure/postgres_temporada_pedido_repository.py")
    assert path.exists(), f"El archivo {path} no existe."

# Test para verificar la existencia de la clase PostgresTemporadaPedidoRepository
def test_postgres_temporada_pedido_repository_class_exists():
    assert hasattr(PostgresTemporadaPedidoRepository, "__init__")

# Test para verificar que PostgresTemporadaPedidoRepository implementa ITemporadaPedidoRepository
def test_postgres_temporada_pedido_repository_implements_interface():
    from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
    assert issubclass(PostgresTemporadaPedidoRepository, ITemporadaPedidoRepository)

# --- Tests para métodos individuales (usando mocks para la conexión a la DB) ---

@pytest.fixture
def mock_db_connection():
    return AsyncMock()

@pytest.fixture
def repository(mock_db_connection):
    return PostgresTemporadaPedidoRepository(mock_db_connection)

# Ejemplo de test para get_temporada_activa
@pytest.mark.asyncio
async def test_get_temporada_activa_found(repository, mock_db_connection):
    mock_row = {
        "id": 1,
        "nombre_temporada": "Temporada 2025-2026",
        "fecha_inicio": date(2025, 9, 1),
        "fecha_fin": date(2026, 7, 31),
        "esta_activa": True,
        "fecha_creacion": datetime.now(),
    }
    mock_db_connection.fetchrow.return_value = mock_row

    temporada = await repository.get_temporada_activa()

    assert temporada is not None
    assert temporada.id == mock_row["id"]
    assert temporada.esta_activa is True
    mock_db_connection.fetchrow.assert_called_once_with(
        "SELECT id, nombre_temporada, fecha_inicio, fecha_fin, esta_activa, fecha_creacion FROM temporadapedidos WHERE esta_activa = TRUE LIMIT 1"
    )

@pytest.mark.asyncio
async def test_get_temporada_activa_not_found(repository, mock_db_connection):
    mock_db_connection.fetchrow.return_value = None

    temporada = await repository.get_temporada_activa()

    assert temporada is None
    mock_db_connection.fetchrow.assert_called_once()

# TODO: Añadir más tests para los demás métodos de PostgresTemporadaPedidoRepository
# Estos tests deberían usar mocks para la conexión a la base de datos y verificar:
# - Que las consultas SQL son correctas.
# - Que los datos se mapean correctamente a las entidades de dominio.
# - Que los métodos manejan correctamente los casos de éxito y error.
# Para pruebas de integración completas, se necesitaría una base de datos de test real.