import os
import pytest
import inspect
from unittest.mock import MagicMock, AsyncMock
from uuid import UUID
from datetime import datetime
import asyncpg

import src.app.prendas.infrastructure.postgres_prenda_repository as postgres_prenda_repository_module
from src.app.prendas.domain.entities import Prenda

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