import pytest

def test_crear_temporada_use_case_file_exists():
    """
    Tests if the crear temporada use case file exists.
    """
    try:
        from src.app.cuotas.application.use_cases import crear_temporada_use_case
    except ImportError:
        pytest.fail("Use case file does not exist: src/app/cuotas/application/use_cases/crear_temporada_use_case.py")