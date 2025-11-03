import pytest
from unittest.mock import AsyncMock
from uuid import UUID, uuid4
from datetime import datetime

from src.app.prendas.domain.entities import VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda

import src.app.prendas.infrastructure.postgres_variante_prenda_repository as postgres_variante_prenda_repository_module

# --- Test de Estructura ---

def test_postgres_variante_prenda_repository_class_exists():
    from src.app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository
    assert PostgresVariantePrendaRepository is not None

def test_postgres_variante_prenda_repository_init():
    from src.app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresVariantePrendaRepository(mock_db_connection)
    assert repository.db_connection is mock_db_connection

# --- Test de guardar ---

@pytest.mark.asyncio
async def test_guardar_variante_prenda():
    from src.app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresVariantePrendaRepository(mock_db_connection)
    variante = VariantePrenda(
        id=uuid4(),
        prenda_id=uuid4(),
        genero=GeneroPrenda.HOMBRE,
        talla=TallaPrenda.M,
        fecha_creacion=datetime.now()
    )

    result = await repository.guardar(variante)

    mock_db_connection.execute.assert_called_once()
    args = mock_db_connection.execute.call_args[0]
    
    expected_query = "INSERT INTO variantes_prenda (id, prenda_id, genero, talla, fecha_creacion) VALUES ($1, $2, $3::genero_prenda_enum, $4::talla_prenda_enum, $5)"
    assert " ".join(args[0].split()) == expected_query

    assert args[1] == variante.id
    assert args[2] == variante.prenda_id
    assert args[3] == variante.genero.value
    assert args[4] == variante.talla.value
    assert args[5] == variante.fecha_creacion
    assert result == variante

# --- Test de eliminar_por_id ---

@pytest.mark.asyncio
async def test_eliminar_por_id_variante_prenda():
    from src.app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresVariantePrendaRepository(mock_db_connection)
    variante_id = uuid4()

    await repository.eliminar_por_id(variante_id)

    mock_db_connection.execute.assert_called_once_with("DELETE FROM variantes_prenda WHERE id = $1", variante_id)

# --- Test de buscar_por_id ---

@pytest.mark.asyncio
async def test_buscar_por_id_variante_prenda_not_found():
    from src.app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository
    mock_db_connection = AsyncMock()
    mock_db_connection.fetchrow.return_value = None
    repository = PostgresVariantePrendaRepository(mock_db_connection)
    variante_id = uuid4()

    result = await repository.buscar_por_id(variante_id)

    mock_db_connection.fetchrow.assert_called_once_with("SELECT id, prenda_id, genero, talla, fecha_creacion FROM variantes_prenda WHERE id = $1", variante_id)
    assert result is None

@pytest.mark.asyncio
async def test_buscar_por_id_variante_prenda_found():
    from src.app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository
    mock_db_connection = AsyncMock()
    now = datetime.now()
    variante_id = uuid4()
    prenda_id = uuid4()
    mock_row = {
        'id': variante_id,
        'prenda_id': prenda_id,
        'genero': GeneroPrenda.MUJER.value,
        'talla': TallaPrenda.S.value,
        'fecha_creacion': now
    }
    mock_db_connection.fetchrow.return_value = mock_row
    repository = PostgresVariantePrendaRepository(mock_db_connection)

    result = await repository.buscar_por_id(variante_id)

    mock_db_connection.fetchrow.assert_called_once_with("SELECT id, prenda_id, genero, talla, fecha_creacion FROM variantes_prenda WHERE id = $1", variante_id)
    assert result is not None
    assert isinstance(result, VariantePrenda)
    assert result.id == variante_id
    assert result.genero == GeneroPrenda.MUJER

# --- Test de listar_por_prenda_id ---

@pytest.mark.asyncio
async def test_listar_por_prenda_id_returns_empty_list():
    from src.app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository
    mock_db_connection = AsyncMock()
    mock_db_connection.fetch.return_value = []
    repository = PostgresVariantePrendaRepository(mock_db_connection)
    prenda_id = uuid4()

    result = await repository.listar_por_prenda_id(prenda_id)

    mock_db_connection.fetch.assert_called_once_with("SELECT id, prenda_id, genero, talla, fecha_creacion FROM variantes_prenda WHERE prenda_id = $1", prenda_id)
    assert result == []

@pytest.mark.asyncio
async def test_listar_por_prenda_id_returns_list_of_variantes():
    from src.app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository
    mock_db_connection = AsyncMock()
    now = datetime.now()
    prenda_id = uuid4()
    variante1_id = uuid4()
    variante2_id = uuid4()

    mock_rows = [
        {'id': variante1_id, 'prenda_id': prenda_id, 'genero': GeneroPrenda.HOMBRE.value, 'talla': TallaPrenda.M.value, 'fecha_creacion': now},
        {'id': variante2_id, 'prenda_id': prenda_id, 'genero': GeneroPrenda.MUJER.value, 'talla': TallaPrenda.S.value, 'fecha_creacion': now}
    ]
    mock_db_connection.fetch.return_value = mock_rows
    repository = PostgresVariantePrendaRepository(mock_db_connection)

    result = await repository.listar_por_prenda_id(prenda_id)

    mock_db_connection.fetch.assert_called_once_with("SELECT id, prenda_id, genero, talla, fecha_creacion FROM variantes_prenda WHERE prenda_id = $1", prenda_id)
    assert len(result) == 2
    assert isinstance(result[0], VariantePrenda)
    assert result[0].id == variante1_id
    assert result[0].genero == GeneroPrenda.HOMBRE
    assert result[1].talla == TallaPrenda.S