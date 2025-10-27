import pytest
from abc import ABC, abstractmethod


def test_gateway_interface_file_exists():
    try:
        from src.app.core.services import i_payment_gateway
    except ImportError:
        pytest.fail("El fichero de la interfaz del gateway de pago 'i_payment_gateway.py' no existe.")

def test_interface_class_exists():
    try:
        from src.app.core.services.i_payment_gateway import IPaymentGateway
    except ImportError:
        pytest.fail("La clase de la interfaz 'IPaymentGateway' no existe.")

def test_crear_sesion_pago_is_abstract_method():
    from src.app.core.services.i_payment_gateway import IPaymentGateway

    with pytest.raises(TypeError):
        class ConcretePaymentGateway(IPaymentGateway):
            async def validar_webhook(self, payload: bytes, sig_header: str) -> object:
                pass
        ConcretePaymentGateway()

def test_validar_webhook_is_abstract_method():
    from src.app.core.services.i_payment_gateway import IPaymentGateway

    with pytest.raises(TypeError):
        class ConcretePaymentGateway(IPaymentGateway):
            async def crear_sesion_pago(self, user_id: int, amount: int, currency: str) -> str:
                pass
        ConcretePaymentGateway()
