import pytest
from datetime import datetime, timezone
from decimal import Decimal

from src.app.cuotas.domain.entities import TipoCuota
from src.app.cuotas.domain.value_objects import NombreTipoCuota

def test_tipo_cuota_creation():
    """
    Tests that a TipoCuota object can be created with all required fields.
    """
    tipo_cuota = TipoCuota(
        id=1,
        temporada_id=1,
        nombre=NombreTipoCuota.SOCIO,
        importe=Decimal("25.00"),
        fecha_creacion=datetime.now(timezone.utc)
    )
    assert isinstance(tipo_cuota, TipoCuota)
    assert tipo_cuota.id == 1
    assert tipo_cuota.temporada_id == 1
    assert tipo_cuota.nombre == NombreTipoCuota.SOCIO
    assert tipo_cuota.importe == Decimal("25.00")
    assert isinstance(tipo_cuota.fecha_creacion, datetime)

def test_tipo_cuota_has_id_attribute():
    """
    Tests if the TipoCuota class has an 'id' attribute with the correct type.
    """
    assert 'id' in TipoCuota.__annotations__
    assert TipoCuota.__annotations__['id'] == int

def test_tipo_cuota_has_temporada_id_attribute():
    """
    Tests if the TipoCuota class has a 'temporada_id' attribute with the correct type.
    """
    assert 'temporada_id' in TipoCuota.__annotations__
    assert TipoCuota.__annotations__['temporada_id'] == int

def test_tipo_cuota_has_nombre_attribute():
    """
    Tests if the TipoCuota class has a 'nombre' attribute with the correct type.
    """
    assert 'nombre' in TipoCuota.__annotations__
    assert TipoCuota.__annotations__['nombre'] == NombreTipoCuota

def test_tipo_cuota_has_importe_attribute():
    """
    Tests if the TipoCuota class has an 'importe' attribute with the correct type.
    """
    assert 'importe' in TipoCuota.__annotations__
    assert TipoCuota.__annotations__['importe'] == Decimal

def test_tipo_cuota_has_fecha_creacion_attribute():
    """
    Tests if the TipoCuota class has a 'fecha_creacion' attribute with the correct type.
    """
    assert 'fecha_creacion' in TipoCuota.__annotations__
    assert TipoCuota.__annotations__['fecha_creacion'] == datetime
