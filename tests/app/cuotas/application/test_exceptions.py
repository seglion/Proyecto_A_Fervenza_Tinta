import pytest
from fastapi import status

def test_exceptions_file_exists():
    """
    Tests if the exceptions file exists.
    """
    try:
        from src.app.cuotas.application import exceptions
    except ImportError:
        pytest.fail("Exceptions file does not exist: src/app/cuotas/application/exceptions.py")

def test_base_exception_class_exists():
    """
    Tests if the CuotaException base class exists in the exceptions file.
    """
    try:
        from src.app.cuotas.application.exceptions import CuotaException
    except ImportError:
        pytest.fail("CuotaException class does not exist in exceptions.py")

def test_temporada_no_encontrada_exception():
    from src.app.cuotas.application.exceptions import TemporadaNoEncontrada
    with pytest.raises(TemporadaNoEncontrada) as exc_info:
        raise TemporadaNoEncontrada()
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Season not found."

def test_cuota_no_encontrada_exception():
    from src.app.cuotas.application.exceptions import CuotaNoEncontrada
    with pytest.raises(CuotaNoEncontrada) as exc_info:
        raise CuotaNoEncontrada()
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Fee not found."

def test_intento_de_pago_fallido_exception():
    from src.app.cuotas.application.exceptions import IntentoDePagoFallido
    with pytest.raises(IntentoDePagoFallido) as exc_info:
        raise IntentoDePagoFallido()
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Payment attempt failed."

import pytest
from src.app.cuotas.application.exceptions import TemporadaNoEncontrada, UnauthorizedException, CuotaYaPagadaException

def test_temporada_no_encontrada_exception():
    with pytest.raises(TemporadaNoEncontrada) as exc_info:
        raise TemporadaNoEncontrada("Temporada no encontrada")
    assert exc_info.value.detail == "Temporada no encontrada"

def test_unauthorized_exception():
    with pytest.raises(UnauthorizedException) as exc_info:
        raise UnauthorizedException("No autorizado")
    assert exc_info.value.detail == "No autorizado"

def test_cuota_ya_pagada_exception():
    with pytest.raises(CuotaYaPagadaException) as exc_info:
        raise CuotaYaPagadaException("La cuota ya ha sido pagada.")
    assert exc_info.value.detail == "La cuota ya ha sido pagada."

