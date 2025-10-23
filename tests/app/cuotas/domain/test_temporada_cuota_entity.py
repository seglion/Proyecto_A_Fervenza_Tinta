import pytest
from datetime import date, datetime, timezone

from src.app.cuotas.domain.entities import TemporadaCuota

def test_temporada_cuota_creation():
    """
    Tests that a TemporadaCuota object can be created with all required fields.
    """
    temporada = TemporadaCuota(
        id=1,
        nombre_temporada="Temporada 2025-2026",
        fecha_inicio=date(2025, 10, 1),
        fecha_fin=date(2026, 7, 25),
        fecha_creacion=datetime.now(timezone.utc)
    )
    assert isinstance(temporada, TemporadaCuota)
    assert temporada.id == 1
    assert temporada.nombre_temporada == "Temporada 2025-2026"
    assert temporada.fecha_inicio == date(2025, 10, 1)
    assert temporada.fecha_fin == date(2026, 7, 25)
    assert isinstance(temporada.fecha_creacion, datetime)

def test_temporada_cuota_has_id_attribute():
    """
    Tests if the TemporadaCuota class has an 'id' attribute with the correct type.
    """
    assert 'id' in TemporadaCuota.__annotations__
    assert TemporadaCuota.__annotations__['id'] == int

def test_temporada_cuota_has_nombre_temporada_attribute():
    """
    Tests if the TemporadaCuota class has a 'nombre_temporada' attribute with the correct type.
    """
    assert 'nombre_temporada' in TemporadaCuota.__annotations__
    assert TemporadaCuota.__annotations__['nombre_temporada'] == str

def test_temporada_cuota_has_fecha_inicio_attribute():
    """
    Tests if the TemporadaCuota class has a 'fecha_inicio' attribute with the correct type.
    """
    assert 'fecha_inicio' in TemporadaCuota.__annotations__
    assert TemporadaCuota.__annotations__['fecha_inicio'] == date

def test_temporada_cuota_has_fecha_fin_attribute():
    """
    Tests if the TemporadaCuota class has a 'fecha_fin' attribute with the correct type.
    """
    assert 'fecha_fin' in TemporadaCuota.__annotations__
    assert TemporadaCuota.__annotations__['fecha_fin'] == date

def test_temporada_cuota_has_fecha_creacion_attribute():
    """
    Tests if the TemporadaCuota class has a 'fecha_creacion' attribute with the correct type.
    """
    assert 'fecha_creacion' in TemporadaCuota.__annotations__
    assert TemporadaCuota.__annotations__['fecha_creacion'] == datetime
