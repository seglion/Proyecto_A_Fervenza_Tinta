import os
import pytest
import inspect
from unittest.mock import MagicMock, AsyncMock
from uuid import UUID
from datetime import datetime
import asyncpg

import src.app.prendas.infrastructure.postgres_prenda_repository as postgres_prenda_repository_module
from src.app.prendas.domain.entities import Prenda, VariantePrenda
from src.app.prendas.domain.value_objects import GeneroPrenda, TallaPrenda

class MockRecord:
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

def test_postgres_prenda_repository_file_exists():
    file_path = "src/app/prendas/infrastructure/postgres_prenda_repository.py"
    assert os.path.exists(file_path)
    assert os.path.isfile(file_path)

def test_postgres_prenda_repository_class_exists():
    assert hasattr(postgres_prenda_repository_module, "PostgresPrendaRepository"), "La clase PostgresPrendaRepository no existe en el módulo"
    assert inspect.isclass(postgres_prenda_repository_module.PostgresPrendaRepository), "PostgresPrendaRepository no es una clase"

def test_postgres_prenda_repository_constructor():
    mock_db_connection = AsyncMock(spec=asyncpg.Connection)
    repository = postgres_prenda_repository_module.PostgresPrendaRepository(db_connection=mock_db_connection)
    assert repository.db_connection is mock_db_connection

@pytest.mark.asyncio
async def test_listar_todas_returns_empty_list():
    mock_db_connection = AsyncMock(spec=asyncpg.Connection)
    mock_db_connection.fetch.return_value = []

    repository = postgres_prenda_repository_module.PostgresPrendaRepository(db_connection=mock_db_connection)
    prendas = await repository.listar_todas()

    mock_db_connection.fetch.assert_called_once_with("SELECT id, nombre, descripcion, precio, imagen_url, fecha_creacion FROM prendas")
    assert prendas == []

@pytest.mark.asyncio
async def test_listar_todas_returns_list_of_prendas():
    mock_db_connection = AsyncMock(spec=asyncpg.Connection)
    
    # Mock data for two prendas using MockRecord
    mock_rows = [
        MockRecord({'id': UUID('a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1'), 'nombre': 'Camiseta', 'descripcion': 'Camiseta de algodón', 'precio': 19.99, 'imagen_url': 'http://example.com/camiseta.jpg', 'fecha_creacion': datetime(2023, 1, 1, 10, 0, 0)}),
        MockRecord({'id': UUID('b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2'), 'nombre': 'Pantalón', 'descripcion': 'Pantalón vaquero', 'precio': 39.99, 'imagen_url': 'http://example.com/pantalon.jpg', 'fecha_creacion': datetime(2023, 1, 2, 11, 0, 0)})
    ]
    mock_db_connection.fetch.return_value = mock_rows

    repository = postgres_prenda_repository_module.PostgresPrendaRepository(db_connection=mock_db_connection)
    prendas = await repository.listar_todas()

    mock_db_connection.fetch.assert_called_once_with("SELECT id, nombre, descripcion, precio, imagen_url, fecha_creacion FROM prendas")
    assert len(prendas) == 2
    assert isinstance(prendas[0], Prenda)
    assert prendas[0].id == UUID('a1a1a1a1-a1a1-a1a1-a1a1-a1a1a1a1a1a1')
    assert prendas[0].nombre == 'Camiseta'
    assert prendas[1].id == UUID('b2b2b2b2-b2b2-b2b2-b2b2-b2b2b2b2b2b2')
    assert prendas[1].nombre == 'Pantalón'

@pytest.mark.asyncio
async def test_buscar_por_id_con_variantes_returns_none_if_not_found():
    mock_db_connection = AsyncMock(spec=asyncpg.Connection)
    mock_db_connection.fetch.return_value = [] # fetch returns an empty list if no rows
    
    repository = postgres_prenda_repository_module.PostgresPrendaRepository(db_connection=mock_db_connection)
    prenda_id = UUID('c3c3c3c3-c3c3-c3c3-c3c3-c3c3c3c3c3c3')
    prenda = await repository.buscar_por_id_con_variantes(prenda_id)

    query = """
        SELECT
            p.id AS prenda_id,
            p.nombre,
            p.descripcion,
            p.precio,
            p.imagen_url,
            p.fecha_creacion,
            vp.id AS variante_id,
            vp.genero,
            vp.talla,
            vp.fecha_creacion AS variante_fecha_creacion
        FROM prendas p
        LEFT JOIN variantes_prenda vp ON p.id = vp.prenda_id
        WHERE p.id = $1
    """
    mock_db_connection.fetch.assert_called_once_with(inspect.cleandoc(query), prenda_id)
    assert prenda is None

@pytest.mark.asyncio
async def test_guardar_prenda_inserts_into_db():
    mock_db_connection = AsyncMock(spec=asyncpg.Connection)
    mock_db_connection.execute.return_value = "INSERT 0 1"

    repository = postgres_prenda_repository_module.PostgresPrendaRepository(db_connection=mock_db_connection)
    new_prenda = Prenda(
        id=UUID('d4d4d4d4-d4d4-d4d4-d4d4-d4d4d4d4d4d4'),
        nombre='Gorra',
        descripcion='Gorra de béisbol',
        precio=15.00,
        imagen_url='http://example.com/gorra.jpg',
        fecha_creacion=datetime(2023, 3, 15, 12, 0, 0),
        variantes=[]
    )

    saved_prenda = await repository.guardar(new_prenda)

    query = """
        INSERT INTO prendas (id, nombre, descripcion, precio, imagen_url, fecha_creacion)
        VALUES ($1, $2, $3, $4, $5, $6)
    """
    mock_db_connection.execute.assert_called_once_with(
        inspect.cleandoc(query),
        new_prenda.id,
        new_prenda.nombre,
        new_prenda.descripcion,
        new_prenda.precio,
        new_prenda.imagen_url,
        new_prenda.fecha_creacion
    )
    assert saved_prenda == new_prenda