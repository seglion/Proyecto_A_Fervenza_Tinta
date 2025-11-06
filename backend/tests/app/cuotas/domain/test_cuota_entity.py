import pytest
from uuid import UUID, uuid4
from datetime import datetime, timezone
from decimal import Decimal

from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago

def test_cuota_creation():
    """
    Tests that a Cuota object can be created with all required fields.
    """
    cuota = Cuota(
        usuario_id=uuid4(),
        tipo_de_cuota_id=1,
        importe_pagado=Decimal("25.00"),
        estado_pago=EstadoPago.PENDIENTE,
    )
    assert isinstance(cuota, Cuota)
    assert isinstance(cuota.id, UUID)
    assert isinstance(cuota.usuario_id, UUID)
    assert cuota.tipo_de_cuota_id == 1
    assert cuota.importe_pagado == Decimal("25.00")
    assert cuota.estado_pago == EstadoPago.PENDIENTE
    assert cuota.fecha_pago is None
    assert cuota.metodo_pago is None
    assert cuota.id_transaccion_externa is None
    assert cuota.notas_admin is None
    assert isinstance(cuota.fecha_creacion, datetime)

def test_cuota_has_id_attribute():
    """
    Tests if the Cuota class has an 'id' attribute with the correct type.
    """
    assert 'id' in Cuota.__annotations__
    assert Cuota.__annotations__['id'] == UUID

def test_cuota_has_usuario_id_attribute():
    """
    Tests if the Cuota class has a 'usuario_id' attribute with the correct type.
    """
    assert 'usuario_id' in Cuota.__annotations__
    assert Cuota.__annotations__['usuario_id'] == UUID

def test_cuota_has_tipo_de_cuota_id_attribute():
    """
    Tests if the Cuota class has a 'tipo_de_cuota_id' attribute with the correct type.
    """
    assert 'tipo_de_cuota_id' in Cuota.__annotations__
    assert Cuota.__annotations__['tipo_de_cuota_id'] == int

def test_cuota_has_importe_pagado_attribute():
    """
    Tests if the Cuota class has an 'importe_pagado' attribute with the correct type.
    """
    assert 'importe_pagado' in Cuota.__annotations__
    assert Cuota.__annotations__['importe_pagado'] == Decimal

def test_cuota_has_estado_pago_attribute():
    """
    Tests if the Cuota class has an 'estado_pago' attribute with the correct type.
    """
    assert 'estado_pago' in Cuota.__annotations__
    assert Cuota.__annotations__['estado_pago'] == EstadoPago

def test_cuota_has_fecha_pago_attribute():
    """
    Tests if the Cuota class has a 'fecha_pago' attribute with the correct type.
    """
    assert 'fecha_pago' in Cuota.__annotations__
    assert Cuota.__annotations__['fecha_pago'] == (datetime | None)

def test_cuota_has_metodo_pago_attribute():
    """
    Tests if the Cuota class has a 'metodo_pago' attribute with the correct type.
    """
    assert 'metodo_pago' in Cuota.__annotations__
    assert Cuota.__annotations__['metodo_pago'] == (MetodoPago | None)

def test_cuota_has_id_transaccion_externa_attribute():
    """
    Tests if the Cuota class has an 'id_transaccion_externa' attribute with the correct type.
    """
    assert 'id_transaccion_externa' in Cuota.__annotations__
    assert Cuota.__annotations__['id_transaccion_externa'] == (str | None)

def test_cuota_has_notas_admin_attribute():
    """
    Tests if the Cuota class has a 'notas_admin' attribute with the correct type.
    """
    assert 'notas_admin' in Cuota.__annotations__
    assert Cuota.__annotations__['notas_admin'] == (str | None)

def test_cuota_has_fecha_creacion_attribute():
    """
    Tests if the Cuota class has a 'fecha_creacion' attribute with the correct type.
    """
    assert 'fecha_creacion' in Cuota.__annotations__
    assert Cuota.__annotations__['fecha_creacion'] == datetime
