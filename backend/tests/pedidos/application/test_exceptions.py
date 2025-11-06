import pytest

from src.app.pedidos.application.exceptions import PedidoNoEncontradoException, AccesoDenegadoException

def test_pedido_no_encontrado_exception_existe():
    """Verifica que la excepción PedidoNoEncontradoException existe y es una subclase de Exception."""
    assert issubclass(PedidoNoEncontradoException, Exception)

def test_acceso_denegado_exception_existe():
    """Verifica que la excepción AccesoDenegadoException existe y es una subclase de Exception."""
    assert issubclass(AccesoDenegadoException, Exception)
