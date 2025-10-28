import pytest
from unittest.mock import AsyncMock

# Test para asegurar que la clase StripePaymentGateway existe
def test_stripe_payment_gateway_class_exists():
    from src.app.infrastructure.payments.stripe_payment_gateway import StripePaymentGateway
    assert StripePaymentGateway is not None