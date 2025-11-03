import pytest
from unittest.mock import AsyncMock
from uuid import UUID, uuid4
from datetime import datetime

from src.app.prendas.domain.entities import Prenda, VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda

# --- Test de Estructura ---

def test_postgres_prenda_repository_class_exists():
    from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
    assert PostgresPrendaRepository is not None

def test_postgres_prenda_repository_init():
    from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresPrendaRepository(mock_db_connection)
    assert repository.db_connection is mock_db_connection

# --- Test de listar_todas ---

@pytest.mark.asyncio
async def test_listar_todas_returns_empty_list():
    from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
    mock_db_connection = AsyncMock()
    mock_db_connection.fetch.return_value = []
    repository = PostgresPrendaRepository(mock_db_connection)

    result = await repository.listar_todas()

    mock_db_connection.fetch.assert_called_once_with("SELECT id, nombre, descripcion, precio, imagen_url, fecha_creacion FROM prendas")
    assert result == []

@pytest.mark.asyncio
async def test_listar_todas_returns_list_of_prendas():
    from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
    mock_db_connection = AsyncMock()
    now = datetime.now()
    mock_rows = [
        {'id': UUID('a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'), 'nombre': 'Camiseta', 'descripcion': 'Camiseta de algodón', 'precio': 19.99, 'imagen_url': 'http://example.com/camiseta.jpg', 'fecha_creacion': now},
        {'id': UUID('b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2'), 'nombre': 'Pantalón', 'descripcion': 'Pantalón vaquero', 'precio': 39.99, 'imagen_url': 'http://example.com/pantalon.jpg', 'fecha_creacion': now}
    ]
    mock_db_connection.fetch.return_value = mock_rows
    repository = PostgresPrendaRepository(mock_db_connection)

    result = await repository.listar_todas()

    assert len(result) == 2
    assert isinstance(result[0], Prenda)
    assert result[0].id == UUID('a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1')
    assert result[0].nombre == 'Camiseta'

# --- Test de buscar_por_id_con_variantes ---

@pytest.mark.asyncio
async def test_buscar_por_id_con_variantes_not_found():
    from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
    mock_db_connection = AsyncMock()
    mock_db_connection.fetch.return_value = []
    repository = PostgresPrendaRepository(mock_db_connection)
    prenda_id = uuid4()

    result = await repository.buscar_por_id_con_variantes(prenda_id)

    assert result is None
    mock_db_connection.fetch.assert_called_once()
    query = mock_db_connection.fetch.call_args[0][0]
    assert "WHERE p.id = $1" in query

@pytest.mark.asyncio
async def test_buscar_por_id_con_variantes_found():
    from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
    mock_db_connection = AsyncMock()
    now = datetime.now()
    prenda_id = uuid4()
    variante1_id = uuid4()
    variante2_id = uuid4()

    mock_rows = [
        {'prenda_id': prenda_id, 'nombre': 'Camiseta', 'descripcion': 'Algodón', 'precio': 25.0, 'imagen_url': 'url', 'fecha_creacion': now, 'variante_id': variante1_id, 'genero': 'HOMBRE', 'talla': 'M', 'variante_fecha_creacion': now},
        {'prenda_id': prenda_id, 'nombre': 'Camiseta', 'descripcion': 'Algodón', 'precio': 25.0, 'imagen_url': 'url', 'fecha_creacion': now, 'variante_id': variante2_id, 'genero': 'MUJER', 'talla': 'S', 'variante_fecha_creacion': now}
    ]
    mock_db_connection.fetch.return_value = mock_rows
    repository = PostgresPrendaRepository(mock_db_connection)

    result = await repository.buscar_por_id_con_variantes(prenda_id)

    assert result is not None
    assert isinstance(result, Prenda)
    assert result.id == prenda_id
    assert len(result.variantes) == 2
    assert isinstance(result.variantes[0], VariantePrenda)
    assert result.variantes[0].id == variante1_id
    assert result.variantes[0].genero == GeneroPrenda.HOMBRE
    assert result.variantes[1].talla == TallaPrenda.S

# --- Test de guardar ---

@pytest.mark.asyncio
async def test_guardar_prenda():
    from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresPrendaRepository(mock_db_connection)
    prenda = Prenda(id=uuid4(), nombre='Gorra', descripcion='Gorra de lana', precio=15.0, imagen_url='url', fecha_creacion=datetime.now())

    result = await repository.guardar(prenda)

    mock_db_connection.execute.assert_called_once()
    args = mock_db_connection.execute.call_args[0]
    
    expected_query = "INSERT INTO prendas (id, nombre, descripcion, precio, imagen_url, fecha_creacion) VALUES ($1, $2, $3, $4, $5, $6)"
    assert " ".join(args[0].split()) == expected_query

    assert args[1] == prenda.id
    assert args[2] == prenda.nombre
    assert args[3] == prenda.descripcion
    assert args[4] == prenda.precio
    assert args[5] == prenda.imagen_url
    assert args[6] == prenda.fecha_creacion
    assert result == prenda

# --- Test de actualizar ---

@pytest.mark.asyncio
async def test_actualizar_prenda():
    from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresPrendaRepository(mock_db_connection)
    prenda = Prenda(id=uuid4(), nombre='Gorra', descripcion='Gorra de lana', precio=15.0, imagen_url='url', fecha_creacion=datetime.now())

    result = await repository.actualizar(prenda)

    mock_db_connection.execute.assert_called_once()
    args = mock_db_connection.execute.call_args[0]

    expected_query = "UPDATE prendas SET nombre = $1, descripcion = $2, precio = $3, imagen_url = $4 WHERE id = $5"
    assert " ".join(args[0].split()) == expected_query

    assert args[1] == prenda.nombre
    assert args[2] == prenda.descripcion
    assert args[3] == prenda.precio
    assert args[4] == prenda.imagen_url
    assert args[5] == prenda.id
    assert result == prenda

# --- Test de eliminar_por_id ---

@pytest.mark.asyncio
async def test_eliminar_por_id():
    from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresPrendaRepository(mock_db_connection)
    prenda_id = uuid4()

    await repository.eliminar_por_id(prenda_id)

    mock_db_connection.execute.assert_called_once_with("DELETE FROM prendas WHERE id = $1", prenda_id)