import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, date
from uuid import UUID
from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import MetodoPago, EstadoPago, NombreTipoCuota
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
        estado_pago=EstadoPago.PENDIENTE,
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
    assert args[5] == cuota_input.estado_pago.value
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
async def test_ha_pagado_cuota_alta_antes_true():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    from src.app.cuotas.domain.value_objects import EstadoPago, NombreTipoCuota
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    usuario_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12')
    mock_db_connection.fetchval.return_value = 1 # Indica que se encontró al menos una cuota de alta

    result = await repository.ha_pagado_cuota_alta_antes(usuario_id)

    mock_db_connection.fetchval.assert_called_once_with(
        "SELECT COUNT(*) FROM cuotas c JOIN tipocuotas tc ON c.tipo_de_cuota_id = tc.id WHERE c.usuario_id = $1 AND tc.nombre = $2 AND c.estado_pago = $3",
        usuario_id, NombreTipoCuota.ALTA.value, EstadoPago.COMPLETADO.value
    )

    assert result is True

@pytest.mark.asyncio
async def test_ha_pagado_cuota_alta_antes_false():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    from src.app.cuotas.domain.value_objects import EstadoPago, NombreTipoCuota
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    usuario_id = UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12')
    mock_db_connection.fetchval.return_value = 0 # Indica que no se encontró ninguna cuota de alta

    result = await repository.ha_pagado_cuota_alta_antes(usuario_id)

    mock_db_connection.fetchval.assert_called_once_with(
        "SELECT COUNT(*) FROM cuotas c JOIN tipocuotas tc ON c.tipo_de_cuota_id = tc.id WHERE c.usuario_id = $1 AND tc.nombre = $2 AND c.estado_pago = $3",
        usuario_id, NombreTipoCuota.ALTA.value, EstadoPago.COMPLETADO.value
    )

    assert result is False

@pytest.mark.asyncio
async def test_get_usuarios_pendientes_por_temporada_found():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    from src.app.cuotas.domain.value_objects import EstadoPago
    from src.app.users.domain.entities import User
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    temporada_id = 1
    now = datetime.now()

    mock_rows = [
        {
            'id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
            'email': "user1@example.com",
            'contrasena_hasheada': "hashed_password",
            'nombre': "Usuario 1",
            'apellidos': "Apellido 1",
            'numero_telefono': "123456789",
            'rol': "socio",
            'apodo': "U1",
            'url_avatar': "http://example.com/avatar1.png",
            'esta_activo': True,
            'email_verificado': True,
            'aprobado_por_admin': True,
            'fecha_creacion': now,
            'fecha_actualizacion': now
        },
        {
            'id': UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13'),
            'email': "user2@example.com",
            'contrasena_hasheada': "hashed_password",
            'nombre': "Usuario 2",
            'apellidos': "Apellido 2",
            'numero_telefono': "987654321",
            'rol': "socio",
            'apodo': "U2",
            'url_avatar': "http://example.com/avatar2.png",
            'esta_activo': True,
            'email_verificado': True,
            'aprobado_por_admin': True,
            'fecha_creacion': now,
            'fecha_actualizacion': now
        }
    ]
    mock_db_connection.fetch.return_value = mock_rows

    users = await repository.get_usuarios_pendientes_por_temporada(temporada_id)

    mock_db_connection.fetch.assert_called_once()
    args, kwargs = mock_db_connection.fetch.call_args
    cleaned_actual_query = " ".join(args[0].split())
    expected_query = """
        SELECT u.id, u.email, u.contrasena_hasheada, u.nombre, u.apellidos, u.numero_telefono, u.rol, u.apodo, u.url_avatar, u.esta_activo, u.email_verificado, u.aprobado_por_admin, u.fecha_creacion, u.fecha_actualizacion
        FROM usuarios u
        WHERE u.id IN (
            SELECT c.usuario_id
            FROM cuotas c
            JOIN tipocuotas tc ON c.tipo_de_cuota_id = tc.id
            WHERE tc.temporada_id = $1
            GROUP BY c.usuario_id
            HAVING COUNT(CASE WHEN c.estado_pago = $2 THEN 1 ELSE NULL END) = 0
        )
        """
    cleaned_expected_query = " ".join(expected_query.split())
    assert cleaned_actual_query == cleaned_expected_query
    assert args[1] == temporada_id
    assert args[2] == EstadoPago.COMPLETADO.value

    assert len(users) == 2
    assert isinstance(users[0], User)
    assert users[0].id == UUID('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
    assert users[0].nombre == "Usuario 1"
    assert users[0].email == "user1@example.com"
    assert users[0].contrasena_hasheada == "hashed_password"

@pytest.mark.asyncio
async def test_get_usuarios_pendientes_por_temporada_not_found():
    from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
    from src.app.cuotas.domain.value_objects import EstadoPago
    from src.app.users.domain.entities import User
    mock_db_connection = AsyncMock()
    repository = PostgresCuotaRepository(mock_db_connection)

    temporada_id = 1
    mock_db_connection.fetch.return_value = []

    users = await repository.get_usuarios_pendientes_por_temporada(temporada_id)

    mock_db_connection.fetch.assert_called_once()
    args, kwargs = mock_db_connection.fetch.call_args
    cleaned_actual_query = " ".join(args[0].split())
    expected_query = """
        SELECT u.id, u.email, u.contrasena_hasheada, u.nombre, u.apellidos, u.numero_telefono, u.rol, u.apodo, u.url_avatar, u.esta_activo, u.email_verificado, u.aprobado_por_admin, u.fecha_creacion, u.fecha_actualizacion
        FROM usuarios u
        WHERE u.id IN (
            SELECT c.usuario_id
            FROM cuotas c
            JOIN tipocuotas tc ON c.tipo_de_cuota_id = tc.id
            WHERE tc.temporada_id = $1
            GROUP BY c.usuario_id
            HAVING COUNT(CASE WHEN c.estado_pago = $2 THEN 1 ELSE NULL END) = 0
        )
        """
    cleaned_expected_query = " ".join(expected_query.split())
    assert cleaned_actual_query == cleaned_expected_query
    assert args[1] == temporada_id
    assert args[2] == EstadoPago.COMPLETADO.value

    assert len(users) == 0

