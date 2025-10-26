import os
import pytest
from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago

def test_value_objects_file_exists():
    assert os.path.exists("src/app/cuotas/domain/value_objects.py")

def test_estado_pago_enum_exists():
    assert hasattr(EstadoPago, 'PENDIENTE')
    assert hasattr(EstadoPago, 'COMPLETADO')
    assert hasattr(EstadoPago, 'FALLIDO')

def test_metodo_pago_enum_exists():
    assert hasattr(MetodoPago, 'STRIPE')
    assert hasattr(MetodoPago, 'EFECTIVO')
