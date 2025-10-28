import pytest
from unittest.mock import AsyncMock, patch

# Test para asegurar que la clase StripePaymentGateway existe
def test_stripe_payment_gateway_class_exists():
    from src.app.infrastructure.payments.stripe_payment_gateway import StripePaymentGateway
    assert StripePaymentGateway is not None

@pytest.mark.asyncio
@patch('stripe.checkout.Session.create')
@patch('src.app.infrastructure.payments.stripe_payment_gateway.settings')
async def test_crear_sesion_pago_success(mock_settings, mock_stripe_session_create):
    from src.app.infrastructure.payments.stripe_payment_gateway import StripePaymentGateway
    mock_settings.STRIPE_SECRET_KEY = "sk_test_mock_key"
    gateway = StripePaymentGateway()

    user_id = 123
    amount = 1000 # 10.00 EUR
    currency = "eur"
    expected_url = "https://checkout.stripe.com/pay/session_id"

    mock_stripe_session_create.return_value = AsyncMock(url=expected_url)

    session_url = await gateway.crear_sesion_pago(user_id, amount, currency)

    mock_stripe_session_create.assert_called_once_with(
        line_items=[
            {
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Cuota de Socio',
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }
        ],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        metadata={'user_id': str(user_id)}
    )
    assert session_url == expected_url