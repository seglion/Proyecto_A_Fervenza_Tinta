import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, date
from uuid import UUID
from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import MetodoPago, EstadoPago # Import MetodoPago and EstadoPago from domain
from src.app.cuotas.application.dtos import CuotaDetalleResponseDTO

# Test para asegurar que la clase PostgresCuotaRepository existe
def test_postgres_cuota_repository_class_exists():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    assert PostgresCuotaRepository is not None

# Test para verificar que el constructor asigna correctamente la conexión a la base de datos
def test_postgres_cuota_repository_init():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)
    assert repository.db_connection is mock_db_connection

# Test para el método listar_todas
@pytest.mark.asyncio
async def test_listar_todas_cuotas():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    now = datetime.now()
    mock_rows = [
        {
            'id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
            'usuario_id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12'),
            'tipo_de_cuota_id': 1,
            'importe_pagado': 50.00,
            'estado_pago': "completado",
            'fecha_pago': now,
            'metodo_pago': "stripe",
            'id_transaccion_externa': "txn_123",
            'notas_admin': "Pago manual",
            'fecha_creacion': now
        },
        {
            'id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13'),
            'usuario_id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14'),
            'tipo_de_cuota_id': 2,
            'importe_pagado': 25.00,
            'estado_pago': "pendiente",
            'fecha_pago': None,
            'metodo_pago': None,
            'id_transaccion_externa': None,
            'notas_admin': None,
            'fecha_creacion': now
        }
    ]
    mock_db_connection.fetch.return_value = mock_rows

    cuotas = await repository.listar_todas()

    mock_db_connection.fetch.assert_called_once_with("SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas")

    assert len(cuotas) == 2
    assert isinstance(cuotas[0], Cuota)
    assert cuotas[0].id == UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
    assert cuotas[0].estado_pago == EstadoPago.COMPLETADO
    assert cuotas[1].estado_pago == EstadoPago.PENDIENTE

# Test para el método buscar_por_usuario_y_temporada
@pytest.mark.asyncio
async def test_buscar_por_usuario_y_temporada_found():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    now = datetime.now()
    usuario_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12')
    temporada_id = 1
    mock_row = {
        'id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
        'usuario_id': usuario_id,
        'tipo_de_cuota_id': temporada_id,
        'importe_pagado': 50.00,
        'estado_pago': "completado",
        'fecha_pago': now,
        'metodo_pago': "stripe",
        'id_transaccion_externa': "txn_123",
        'notas_admin': "Pago manual",
        'fecha_creacion': now
    }
    mock_db_connection.fetchrow.return_value = mock_row

    cuota = await repository.buscar_por_usuario_y_temporada(usuario_id, temporada_id)

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    assert "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE usuario_id = $1 AND tipo_de_cuota_id = $2" in args[0]
    assert args[1] == usuario_id
    assert args[2] == temporada_id

    assert cuota is not None
    assert isinstance(cuota, Cuota)
    assert cuota.id == UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')

@pytest.mark.asyncio
async def test_buscar_por_usuario_y_temporada_not_found():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    usuario_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12')
    temporada_id = 1
    mock_db_connection.fetchrow.return_value = None

    cuota = await repository.buscar_por_usuario_y_temporada(usuario_id, temporada_id)

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    assert "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE usuario_id = $1 AND tipo_de_cuota_id = $2" in args[0]
    assert args[1] == usuario_id
    assert args[2] == temporada_id

    assert cuota is None

# Test para el método guardar
@pytest.mark.asyncio
async def test_guardar_cuota():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    now = datetime.now()
    cuota_input = Cuota(
        id=UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
        usuario_id=UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12'),
        tipo_de_cuota_id=1,
        importe_pagado=50.00,
        estado_pago="pendiente",
        fecha_pago=None,
        metodo_pago=MetodoPago.STRIPE,
        id_transaccion_externa="txn_123",
        notas_admin="Notas de prueba",
        fecha_creacion=now
    )

    mock_db_connection.execute.return_value = None # execute no devuelve valor para INSERT

    cuota_guardada = await repository.guardar(cuota_input)

    mock_db_connection.execute.assert_called_once()
    args, kwargs = mock_db_connection.execute.call_args
    assert "INSERT INTO cuotas (id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion)" in args[0]
    assert "VALUES ($1, $2, $3, $4, $5, $6, $7::tipo_metodo_pago, $8, $9, $10)" in args[0]
    assert args[1] == cuota_input.id
    assert args[2] == cuota_input.usuario_id
    assert args[3] == cuota_input.tipo_de_cuota_id
    assert args[4] == cuota_input.importe_pagado
    assert args[5] == cuota_input.estado_pago
    assert args[6] == cuota_input.fecha_pago
    assert args[7] == cuota_input.metodo_pago.value
    assert args[8] == cuota_input.id_transaccion_externa
    assert args[9] == cuota_input.notas_admin
    assert args[10] == cuota_input.fecha_creacion

    assert cuota_guardada == cuota_input

@pytest.mark.asyncio
async def test_buscar_por_id_found():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    now = datetime.now()
    cuota_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
    mock_row = {
        'id': cuota_id,
        'usuario_id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12'),
        'tipo_de_cuota_id': 1,
        'importe_pagado': 50.00,
        'estado_pago': "completado",
        'fecha_pago': now,
        'metodo_pago': "stripe",
        'id_transaccion_externa': "txn_123",
        'notas_admin': "Pago manual",
        'fecha_creacion': now
    }
    mock_db_connection.fetchrow.return_value = mock_row

    cuota = await repository.buscar_por_id(cuota_id)

    mock_db_connection.fetchrow.assert_called_once_with(
        "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE id = $1",
        cuota_id
    )

    assert cuota is not None
    assert isinstance(cuota, Cuota)
    assert cuota.id == cuota_id

@pytest.mark.asyncio
async def test_buscar_por_id_not_found():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    cuota_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
    mock_db_connection.fetchrow.return_value = None

    cuota = await repository.buscar_por_id(cuota_id)

    mock_db_connection.fetchrow.assert_called_once_with(
        "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE id = $1",
        cuota_id
    )

    assert cuota is None

@pytest.mark.asyncio
async def test_actualizar_cuota_existente():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    from src.app.cuotas.domain.value_objects import EstadoPago
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    cuota_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
    usuario_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12')
    now = datetime.now()

    cuota_existente = Cuota(
        id=cuota_id,
        usuario_id=usuario_id,
        tipo_de_cuota_id=1,
        importe_pagado=50.00,
        estado_pago=EstadoPago.PENDIENTE,
        fecha_pago=None,
        metodo_pago=MetodoPago.STRIPE,
        id_transaccion_externa="txn_old",
        notas_admin="Notas antiguas",
        fecha_creacion=now
    )

    cuota_actualizada_input = Cuota(
        id=cuota_id,
        usuario_id=usuario_id,
        tipo_de_cuota_id=1,
        importe_pagado=60.00,
        estado_pago=EstadoPago.COMPLETADO,
        fecha_pago=now,
        metodo_pago=MetodoPago.EFECTIVO,
        id_transaccion_externa="txn_new",
        notas_admin="Notas nuevas",
        fecha_creacion=now # fecha_creacion no debería cambiar
    )

    mock_db_connection.execute.return_value = "UPDATE 1" # Indica que una fila fue actualizada

    cuota_result = await repository.actualizar(cuota_actualizada_input)

    mock_db_connection.execute.assert_called_once()
    args, kwargs = mock_db_connection.execute.call_args
    cleaned_actual_query = " ".join(args[0].split())
    expected_query = """
        UPDATE cuotas
        SET
            importe_pagado = $1,
            estado_pago = $2,
            fecha_pago = $3,
            metodo_pago = $4::tipo_metodo_pago,
            id_transaccion_externa = $5,
            notas_admin = $6
        WHERE id = $7
        """
    cleaned_expected_query = " ".join(expected_query.split())
    assert cleaned_actual_query == cleaned_expected_query
    assert args[1] == cuota_actualizada_input.importe_pagado
    assert args[2] == cuota_actualizada_input.estado_pago.value
    assert args[3] == cuota_actualizada_input.fecha_pago
    assert args[4] == cuota_actualizada_input.metodo_pago.value
    assert args[5] == cuota_actualizada_input.id_transaccion_externa
    assert args[6] == cuota_actualizada_input.notas_admin
    assert args[7] == cuota_id

    assert cuota_result == cuota_actualizada_input

@pytest.mark.asyncio
async def test_actualizar_cuota_no_existente():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    from src.app.cuotas.domain.value_objects import EstadoPago
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    cuota_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
    usuario_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12')
    now = datetime.now()

    cuota_actualizada_input = Cuota(
        id=cuota_id,
        usuario_id=usuario_id,
        tipo_de_cuota_id=1,
        importe_pagado=60.00,
        estado_pago=EstadoPago.COMPLETADO,
        fecha_pago=now,
        metodo_pago=MetodoPago.EFECTIVO,
        id_transaccion_externa="txn_new",
        notas_admin="Notas nuevas",
        fecha_creacion=now
    )

    mock_db_connection.execute.return_value = "UPDATE 0" # Indica que ninguna fila fue actualizada

    cuota_result = await repository.actualizar(cuota_actualizada_input)

    mock_db_connection.execute.assert_called_once()
    args, kwargs = mock_db_connection.execute.call_args
    cleaned_actual_query = " ".join(args[0].split())
    expected_query = """
        UPDATE cuotas
        SET
            importe_pagado = $1,
            estado_pago = $2,
            fecha_pago = $3,
            metodo_pago = $4::tipo_metodo_pago,
            id_transaccion_externa = $5,
            notas_admin = $6
        WHERE id = $7
        """
    cleaned_expected_query = " ".join(expected_query.split())
    assert cleaned_actual_query == cleaned_expected_query
    assert args[1] == cuota_actualizada_input.importe_pagado
    assert args[2] == cuota_actualizada_input.estado_pago.value
    assert args[3] == cuota_actualizada_input.fecha_pago
    assert args[4] == cuota_actualizada_input.metodo_pago.value
    assert args[5] == cuota_actualizada_input.id_transaccion_externa
    assert args[6] == cuota_actualizada_input.notas_admin
    assert args[7] == cuota_id

    assert cuota_result == cuota_actualizada_input # El repositorio devuelve la cuota que se intentó actualizar, incluso si no existía

@pytest.mark.asyncio
async def test_buscar_por_usuario_id_completadas_found():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    from src.app.cuotas.domain.value_objects import EstadoPago
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    usuario_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12')
    now = datetime.now()

    mock_rows = [
        {
            'id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
            'usuario_id': usuario_id,
            'tipo_de_cuota_id': 1,
            'importe_pagado': 50.00,
            'estado_pago': "completado",
            'fecha_pago': now,
            'metodo_pago': "stripe",
            'id_transaccion_externa': "txn_123",
            'notas_admin': "Pago manual",
            'fecha_creacion': now
        },
        {
            'id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13'),
            'usuario_id': usuario_id,
            'tipo_de_cuota_id': 2,
            'importe_pagado': 25.00,
            'estado_pago': "completado",
            'fecha_pago': now,
            'metodo_pago': "efectivo",
            'id_transaccion_externa': None,
            'notas_admin': None,
            'fecha_creacion': now
        }
    ]
    mock_db_connection.fetch.return_value = mock_rows

    cuotas = await repository.buscar_por_usuario_id_completadas(usuario_id)

    mock_db_connection.fetch.assert_called_once_with(
        "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE usuario_id = $1 AND estado_pago = $2",
        usuario_id, EstadoPago.COMPLETADO.value
    )

    assert len(cuotas) == 2
    assert isinstance(cuotas[0], Cuota)
    assert cuotas[0].usuario_id == usuario_id
    assert cuotas[0].estado_pago == EstadoPago.COMPLETADO

@pytest.mark.asyncio
async def test_buscar_por_usuario_id_completadas_not_found():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    from src.app.cuotas.domain.value_objects import EstadoPago
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    usuario_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12')
    mock_db_connection.fetch.return_value = []

    cuotas = await repository.buscar_por_usuario_id_completadas(usuario_id)

    mock_db_connection.fetch.assert_called_once_with(
        "SELECT id, usuario_id, tipo_de_cuota_id, importe_pagado, estado_pago, fecha_pago, metodo_pago, id_transaccion_externa, notas_admin, fecha_creacion FROM cuotas WHERE usuario_id = $1 AND estado_pago = $2",
        usuario_id, EstadoPago.COMPLETADO.value
    )

    assert len(cuotas) == 0

# Test para el método buscar_por_id_con_detalle
@pytest.mark.asyncio
async def test_buscar_por_id_con_detalle_found():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    now = datetime.now()
    cuota_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
    mock_row = {
        'id': cuota_id,
        'usuario_id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12'),
        'tipo_de_cuota_id': 1,
        'importe_pagado': 50.00,
        'estado_pago': "completado",
        'fecha_pago': now,
        'metodo_pago': "stripe",
        'id_transaccion_externa': "txn_123",
        'notas_admin': "Pago manual",
        'fecha_creacion': now,
        'usuario_nombre': "John",
        'usuario_apellidos': "Doe",
        'tipo_cuota_nombre': "General",
        'temporada_nombre': "2025-2026"
    }
    mock_db_connection.fetchrow.return_value = mock_row

    cuota = await repository.buscar_por_id_con_detalle(cuota_id)

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    cleaned_actual_query = " ".join(args[0].split())
    expected_query = """
        SELECT
            c.id, c.usuario_id, c.tipo_de_cuota_id, c.importe_pagado, c.estado_pago, c.fecha_pago, c.metodo_pago, c.id_transaccion_externa, c.notas_admin, c.fecha_creacion,
            u.nombre AS usuario_nombre, u.apellidos AS usuario_apellidos,
            tc.nombre AS tipo_cuota_nombre,
            ts.nombre_temporada AS temporada_nombre
        FROM cuotas c
        JOIN usuarios u ON c.usuario_id = u.id
        JOIN tipos_de_cuota tc ON c.tipo_de_cuota_id = tc.id
        JOIN temporadas_cuota ts ON tc.temporada_id = ts.id
        WHERE c.id = $1
        """
    cleaned_expected_query = " ".join(expected_query.split())
    assert cleaned_actual_query == cleaned_expected_query
    assert args[1] == cuota_id

    assert cuota is not None
    assert isinstance(cuota, CuotaDetalleResponseDTO)
    assert cuota.id == cuota_id
    assert cuota.usuario_nombre == "John"
    assert cuota.tipo_cuota_nombre == "General"
    assert cuota.temporada_nombre == "2025-2026"

@pytest.mark.asyncio
async def test_buscar_por_id_con_detalle_not_found():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    cuota_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
    mock_db_connection.fetchrow.return_value = None

    cuota = await repository.buscar_por_id_con_detalle(cuota_id)

    mock_db_connection.fetchrow.assert_called_once()
    args, kwargs = mock_db_connection.fetchrow.call_args
    cleaned_actual_query = " ".join(args[0].split())
    expected_query = """
        SELECT
            c.id, c.usuario_id, c.tipo_de_cuota_id, c.importe_pagado, c.estado_pago, c.fecha_pago, c.metodo_pago, c.id_transaccion_externa, c.notas_admin, c.fecha_creacion,
            u.nombre AS usuario_nombre, u.apellidos AS usuario_apellidos,
            tc.nombre AS tipo_cuota_nombre,
            ts.nombre_temporada AS temporada_nombre
        FROM cuotas c
        JOIN usuarios u ON c.usuario_id = u.id
        JOIN tipos_de_cuota tc ON c.tipo_de_cuota_id = tc.id
        JOIN temporadas_cuota ts ON tc.temporada_id = ts.id
        WHERE c.id = $1
        """
    cleaned_expected_query = " ".join(expected_query.split())
    assert cleaned_actual_query == cleaned_expected_query
    assert args[1] == cuota_id

    assert cuota is None