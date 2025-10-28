import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, date
from src.app.cuotas.domain.entities import TemporadaCuota

# Test para asegurar que la clase PostgresTemporadaCuotaRepository existe
def test_postgres_temporada_cuota_repository_class_exists():
    from src.app.cuotas.infrastructure.postgres_temporada_cuota_repository import PostgresTemporadaCuotaRepository
    assert PostgresTemporadaCuotaRepository is not None

# Test para verificar que el constructor asigna correctamente la conexión a la base de datos
def test_postgres_temporada_cuota_repository_init():
    from src.app.cuotas.infrastructure.postgres_temporada_cuota_repository import PostgresTemporadaCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTemporadaCuotaRepository(mock_db_connection)
    assert repository.db_connection is mock_db_connection

# Test para el método guardar_temporada
@pytest.mark.asyncio
async def test_guardar_temporada():
    from src.app.cuotas.infrastructure.postgres_temporada_cuota_repository import PostgresTemporadaCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTemporadaCuotaRepository(mock_db_connection)

    now = datetime.now()
    temporada_input = TemporadaCuota(
        id=None,
        nombre_temporada="Test 2025-2026",
        fecha_inicio=now.date(),
        fecha_fin=now.date(),
        fecha_creacion=now
    )

    # Mockear el comportamiento de fetchval para simular el retorno del ID generado
    mock_db_connection.fetchval.return_value = 1 # Simula que la DB devuelve el ID 1

    temporada_guardada = await repository.guardar_temporada(temporada_input)

    # Verificar que fetchval fue llamado con la query y los parámetros correctos
    mock_db_connection.fetchval.assert_called_once()
    args, kwargs = mock_db_connection.fetchval.call_args
    assert "INSERT INTO temporadas_cuota" in args[0]
    assert temporada_input.nombre_temporada == args[1]
    assert temporada_input.fecha_inicio == args[2]
    assert temporada_input.fecha_fin == args[3]
    assert temporada_input.fecha_creacion == args[4]

    # Verificar que la entidad devuelta tiene el ID asignado
    assert temporada_guardada.id == 1
    assert temporada_guardada.nombre_temporada == temporada_input.nombre_temporada
    assert temporada_guardada.fecha_inicio == temporada_input.fecha_inicio
    assert temporada_guardada.fecha_fin == temporada_input.fecha_fin
    assert temporada_guardada.fecha_creacion == temporada_input.fecha_creacion

# Test para el método listar_todas
@pytest.mark.asyncio
async def test_listar_todas_temporadas():
    from src.app.cuotas.infrastructure.postgres_temporada_cuota_repository import PostgresTemporadaCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTemporadaCuotaRepository(mock_db_connection)

    # Datos de ejemplo que fetch devolvería
    now = datetime.now()
    mock_rows = [
        {'id': 1, 'nombre_temporada': "T1", 'fecha_inicio': date(2025, 1, 1), 'fecha_fin': date(2025, 12, 31), 'fecha_creacion': now},
        {'id': 2, 'nombre_temporada': "T2", 'fecha_inicio': date(2026, 1, 1), 'fecha_fin': date(2026, 12, 31), 'fecha_creacion': now}
    ]
    mock_db_connection.fetch.return_value = mock_rows

    temporadas = await repository.listar_todas()

    # Verificar que fetch fue llamado con la query correcta
    mock_db_connection.fetch.assert_called_once_with("SELECT id, nombre_temporada, fecha_inicio, fecha_fin, fecha_creacion FROM temporadas_cuota ORDER BY fecha_inicio DESC")

    # Verificar que se mapearon correctamente a entidades TemporadaCuota
    assert len(temporadas) == 2
    assert isinstance(temporadas[0], TemporadaCuota)
    assert temporadas[0].id == 1
    assert temporadas[0].nombre_temporada == "T1"
    assert temporadas[1].id == 2
    assert temporadas[1].nombre_temporada == "T2"

# Test para el método actualizar
@pytest.mark.asyncio
async def test_actualizar_temporada():
    from src.app.cuotas.infrastructure.postgres_temporada_cuota_repository import PostgresTemporadaCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTemporadaCuotaRepository(mock_db_connection)

    now = datetime.now()
    temporada_existente = TemporadaCuota(
        id=1,
        nombre_temporada="Original 2025-2026",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 12, 31),
        fecha_creacion=now
    )
    temporada_actualizada_input = TemporadaCuota(
        id=1,
        nombre_temporada="Actualizada 2025-2026",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2026, 1, 1),
        fecha_creacion=now # fecha_creacion no cambia en la actualización
    )

    mock_db_connection.execute.return_value = None # execute no devuelve valor para UPDATE

    temporada_result = await repository.actualizar(temporada_actualizada_input)

    mock_db_connection.execute.assert_called_once()
    args, kwargs = mock_db_connection.execute.call_args
    assert "UPDATE temporadas_cuota" in args[0]
    assert temporada_actualizada_input.nombre_temporada == args[1]
    assert temporada_actualizada_input.fecha_inicio == args[2]
    assert temporada_actualizada_input.fecha_fin == args[3]
    assert temporada_actualizada_input.id == args[4]

    assert temporada_result == temporada_actualizada_input

# Test para el método get_temporada_activa
@pytest.mark.asyncio
async def test_get_temporada_activa_found():
    from src.app.cuotas.infrastructure.postgres_temporada_cuota_repository import PostgresTemporadaCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTemporadaCuotaRepository(mock_db_connection)

    now = datetime.now()
    mock_row = {
        'id': 1,
        'nombre_temporada': "Activa 2025-2026",
        'fecha_inicio': date(2025, 1, 1),
        'fecha_fin': date(2026, 12, 31),
        'fecha_creacion': now
    }
    mock_db_connection.fetchrow.return_value = mock_row

    temporada_activa = await repository.get_temporada_activa()

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    assert "SELECT id, nombre_temporada, fecha_inicio, fecha_fin, fecha_creacion FROM temporadas_cuota WHERE fecha_inicio <= CURRENT_DATE AND fecha_fin >= CURRENT_DATE" in args[0]

    assert temporada_activa is not None
    assert isinstance(temporada_activa, TemporadaCuota)
    assert temporada_activa.id == 1

@pytest.mark.asyncio
async def test_get_temporada_activa_not_found():
    from src.app.cuotas.infrastructure.postgres_temporada_cuota_repository import PostgresTemporadaCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTemporadaCuotaRepository(mock_db_connection)

    mock_db_connection.fetchrow.return_value = None

    temporada_activa = await repository.get_temporada_activa()

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    assert "SELECT id, nombre_temporada, fecha_inicio, fecha_fin, fecha_creacion FROM temporadas_cuota WHERE fecha_inicio <= CURRENT_DATE AND fecha_fin >= CURRENT_DATE" in args[0]

    assert temporada_activa is None

# Test para el método actualizar
@pytest.mark.asyncio
async def test_actualizar_temporada():
    from src.app.cuotas.infrastructure.postgres_temporada_cuota_repository import PostgresTemporadaCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresTemporadaCuotaRepository(mock_db_connection)

    now = datetime.now()
    temporada_existente = TemporadaCuota(
        id=1,
        nombre_temporada="Original 2025-2026",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2025, 12, 31),
        fecha_creacion=now
    )
    temporada_actualizada_input = TemporadaCuota(
        id=1,
        nombre_temporada="Actualizada 2025-2026",
        fecha_inicio=date(2025, 1, 1),
        fecha_fin=date(2026, 1, 1),
        fecha_creacion=now # fecha_creacion no cambia en la actualización
    )

    mock_db_connection.execute.return_value = None # execute no devuelve valor para UPDATE

    temporada_result = await repository.actualizar(temporada_actualizada_input)

    mock_db_connection.execute.assert_called_once()
    args, kwargs = mock_db_connection.execute.call_args
    assert "UPDATE temporadas_cuota" in args[0]
    assert temporada_actualizada_input.nombre_temporada == args[1]
    assert temporada_actualizada_input.fecha_inicio == args[2]
    assert temporada_actualizada_input.fecha_fin == args[3]
    assert temporada_actualizada_input.id == args[4]

    assert temporada_result == temporada_actualizada_input