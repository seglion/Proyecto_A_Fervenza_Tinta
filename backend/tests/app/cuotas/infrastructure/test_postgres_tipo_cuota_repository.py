import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, date
from src.app.cuotas.domain.entities import TipoCuota
from src.app.cuotas.domain.value_objects import NombreTipoCuota # Importar NombreTipoCuota

# Test para asegurar que la clase PostgresTipoCuotaRepository existe
def test_postgres_tipo_cuota_repository_class_exists():
    from src.app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
    assert PostgresTipoCuotaRepository is not None

# Test para verificar que el constructor asigna correctamente la conexión a la base de datos
def test_postgres_tipo_cuota_repository_init():
    from src.app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTipoCuotaRepository(mock_db_connection) # Corregido el typo
    assert repository.db_connection is mock_db_connection

# Test para el método guardar_varios
@pytest.mark.asyncio
async def test_guardar_varios_tipos_cuota():
    from src.app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTipoCuotaRepository(mock_db_connection)

    now = datetime.now()
    tipos_cuota_input = [
        TipoCuota(
            id=None,
            temporada_id=1,
            nombre=NombreTipoCuota.SOCIO, # Usar el enum
            importe=50.00,
            fecha_creacion=now
        ),
        TipoCuota(
            id=None,
            temporada_id=1,
            nombre=NombreTipoCuota.ALTA, # Usar el enum
            importe=25.00,
            fecha_creacion=now
        )
    ]

    # Mockear el comportamiento de fetch para simular la inserción y el retorno de IDs
    mock_db_connection.fetch.return_value = [
        {'id': 101, 'temporada_id': 1, 'nombre': "General", 'importe': 50.00, 'fecha_creacion': now},
        {'id': 102, 'temporada_id': 1, 'nombre': "Nuevo Socio", 'importe': 25.00, 'fecha_creacion': now}
    ]

    tipos_cuota_guardados = await repository.guardar_varios(tipos_cuota_input)

    # Verificar que fetch fue llamado con la query y los parámetros correctos
    mock_db_connection.fetch.assert_called_once()
    args, kwargs = mock_db_connection.fetch.call_args
    # Limpiar la query para una comparación más robusta
    cleaned_query = " ".join(args[0].split())

    expected_query = "INSERT INTO tipocuotas (temporada_id, nombre, importe, fecha_creacion) VALUES ($1, $2, $3, $4), ($5, $6, $7, $8) RETURNING id"
    assert cleaned_query == expected_query

    # Verificar los parámetros pasados (asyncpg.fetch recibe los parámetros desempaquetados)
    expected_params = (
        tipos_cuota_input[0].temporada_id,
        tipos_cuota_input[0].nombre.value, # Usar .value
        tipos_cuota_input[0].importe,
        tipos_cuota_input[0].fecha_creacion,
        tipos_cuota_input[1].temporada_id,
        tipos_cuota_input[1].nombre.value, # Usar .value
        tipos_cuota_input[1].importe,
        tipos_cuota_input[1].fecha_creacion
    )
    assert args[1:] == expected_params # Comparar los argumentos desempaquetados

    # Verificar que las entidades devueltas tienen los IDs asignados
    assert len(tipos_cuota_guardados) == 2
    assert tipos_cuota_guardados[0].id == 101
    assert tipos_cuota_guardados[1].id == 102
    assert tipos_cuota_guardados[0].nombre == tipos_cuota_input[0].nombre
    assert tipos_cuota_guardados[1].nombre == tipos_cuota_input[1].nombre

# Test para el método actualizar_varios
@pytest.mark.asyncio
async def test_actualizar_varios_tipos_cuota():
    from src.app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTipoCuotaRepository(mock_db_connection)

    now = datetime.now()
    tipos_cuota_input = [
        TipoCuota(
            id=101,
            temporada_id=1,
            nombre=NombreTipoCuota.SOCIO, # Usar el enum
            importe=55.00,
            fecha_creacion=now
        ),
        TipoCuota(
            id=102,
            temporada_id=1,
            nombre=NombreTipoCuota.ALTA, # Usar el enum
            importe=30.00,
            fecha_creacion=now
        )
    ]

    mock_db_connection.execute.return_value = None # execute no devuelve valor para UPDATE

    tipos_cuota_actualizados = await repository.actualizar_varios(tipos_cuota_input)

    assert mock_db_connection.execute.call_count == 2

    # Verificar la primera llamada
    args1, kwargs1 = mock_db_connection.execute.call_args_list[0]
    assert "UPDATE tipocuotas SET nombre = $1, importe = $2 WHERE id = $3" in args1[0]
    assert args1[1:] == (tipos_cuota_input[0].nombre.value, tipos_cuota_input[0].importe, tipos_cuota_input[0].id)

    # Verificar la segunda llamada
    args2, kwargs2 = mock_db_connection.execute.call_args_list[1]
    assert "UPDATE tipocuotas SET nombre = $1, importe = $2 WHERE id = $3" in args2[0]
    assert args2[1:] == (tipos_cuota_input[1].nombre.value, tipos_cuota_input[1].importe, tipos_cuota_input[1].id)

    assert tipos_cuota_actualizados == tipos_cuota_input

# Test para el método get_tipo_cuota_general
    now = datetime.now()
    mock_row = {
        'id': 101,
        'temporada_id': 1,
        'nombre': NombreTipoCuota.SOCIO.value, # Usar el valor del enum
        'importe': 50.00,
        'fecha_creacion': now
    }
    mock_db_connection.fetchrow.return_value = mock_row

    temporada_id = 1
    tipo_cuota = await repository.get_tipo_cuota_general(temporada_id)

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    assert "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipocuotas WHERE temporada_id = $1 AND nombre = $2" in args[0]
    assert args[1] == temporada_id
    assert args[2] == NombreTipoCuota.SOCIO.value # Verificar el valor del enum

    assert tipo_cuota is not None
    assert isinstance(tipo_cuota, TipoCuota)
    assert tipo_cuota.id == 101

@pytest.mark.asyncio
async def test_get_tipo_cuota_general_not_found():
    from src.app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTipoCuotaRepository(mock_db_connection)

    mock_db_connection.fetchrow.return_value = None

    temporada_id = 1
    tipo_cuota = await repository.get_tipo_cuota_general(temporada_id)

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    assert "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipocuotas WHERE temporada_id = $1 AND nombre = $2" in args[0]
    assert args[1] == temporada_id
    assert args[2] == NombreTipoCuota.SOCIO.value # Verificar el valor del enum

    assert tipo_cuota is None

# Test para el método get_tipo_cuota_nuevo_socio
@pytest.mark.asyncio
async def test_get_tipo_cuota_nuevo_socio_found():
    from src.app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTipoCuotaRepository(mock_db_connection)

    now = datetime.now()
    mock_row = {
        'id': 103,
        'temporada_id': 1,
        'nombre': NombreTipoCuota.ALTA.value, # Usar el valor del enum
        'importe': 25.00,
        'fecha_creacion': now
    }
    mock_db_connection.fetchrow.return_value = mock_row

    temporada_id = 1
    tipo_cuota = await repository.get_tipo_cuota_nuevo_socio(temporada_id)

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    assert "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipocuotas WHERE temporada_id = $1 AND nombre = $2" in args[0]
    assert args[1] == temporada_id
    assert args[2] == NombreTipoCuota.ALTA.value # Verificar el valor del enum

    assert tipo_cuota is not None
    assert isinstance(tipo_cuota, TipoCuota)
    assert tipo_cuota.id == 103

@pytest.mark.asyncio
async def test_get_tipo_cuota_nuevo_socio_not_found():
    from src.app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTipoCuotaRepository(mock_db_connection)

    mock_db_connection.fetchrow.return_value = None

    temporada_id = 1
    tipo_cuota = await repository.get_tipo_cuota_nuevo_socio(temporada_id)

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    assert "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipocuotas WHERE temporada_id = $1 AND nombre = $2" in args[0]
    assert args[1] == temporada_id
    assert args[2] == NombreTipoCuota.ALTA.value # Verificar el valor del enum

    assert tipo_cuota is None

# Test para el método get_tipo_cuota_general
@pytest.mark.asyncio
async def test_get_tipo_cuota_general_found():
    from src.app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTipoCuotaRepository(mock_db_connection)

    now = datetime.now()
    mock_row = {
        'id': 101,
        'temporada_id': 1,
        'nombre': NombreTipoCuota.SOCIO.value, # Usar el valor del enum
        'importe': 50.00,
        'fecha_creacion': now
    }
    mock_db_connection.fetchrow.return_value = mock_row

    temporada_id = 1
    tipo_cuota = await repository.get_tipo_cuota_general(temporada_id)

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    assert "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipocuotas WHERE temporada_id = $1 AND nombre = $2" in args[0]
    assert args[1] == temporada_id
    assert args[2] == NombreTipoCuota.SOCIO.value # Verificar el valor del enum

    assert tipo_cuota is not None
    assert isinstance(tipo_cuota, TipoCuota)
    assert tipo_cuota.id == 101

@pytest.mark.asyncio
async def test_get_tipo_cuota_general_not_found_again():
    from src.app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTipoCuotaRepository(mock_db_connection)

    mock_db_connection.fetchrow.return_value = None

    temporada_id = 1
    tipo_cuota = await repository.get_tipo_cuota_general(temporada_id)

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    assert "SELECT id, temporada_id, nombre, importe, fecha_creacion FROM tipocuotas WHERE temporada_id = $1 AND nombre = $2" in args[0]
    assert args[1] == temporada_id
    assert args[2] == NombreTipoCuota.SOCIO.value # Verificar el valor del enum

    assert tipo_cuota is None