import pytest
from unittest.mock import AsyncMock, patch
from uuid import UUID
from src.app.core.config import settings
import stripe


@pytest.fixture(autouse=True)
def mock_stripe_secret_key(monkeypatch):
    monkeypatch.setattr(settings, "STRIPE_SECRET_KEY", "sk_test_mock_key")
    monkeypatch.setattr(settings, "STRIPE_WEBHOOK_SECRET", "whsec_mock_key")

# Test para asegurar que la clase StripePaymentGateway existe
def test_stripe_payment_gateway_class_exists():
    from src.app.infrastructure.payments.stripe_payment_gateway import StripePaymentGateway
    assert StripePaymentGateway is not None

@pytest.mark.asyncio
@patch('stripe.checkout.Session.create')
async def test_crear_sesion_pago_success(mock_stripe_session_create):
    from src.app.infrastructure.payments.stripe_payment_gateway import StripePaymentGateway
    gateway = StripePaymentGateway()

    user_id = 123
    amount = 1000 # 10.00 EUR
    currency = "eur"
    cuota_id = UUID('a1b2c3d4-e5f6-7890-1234-567890abcdef') # Dummy UUID for testing
    expected_url = "https://checkout.stripe.com/pay/session_id"

    mock_stripe_session_create.return_value = AsyncMock(url=expected_url)

    session_url = await gateway.crear_sesion_pago(user_id, amount, currency, cuota_id)

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
        metadata={'user_id': str(user_id), 'cuota_id': str(cuota_id)}
    )
    assert session_url == expected_url

@pytest.mark.asyncio
@patch('stripe.Webhook.construct_event')
async def test_validar_webhook_success(mock_stripe_construct_event):
    from src.app.infrastructure.payments.stripe_payment_gateway import StripePaymentGateway
    gateway = StripePaymentGateway()

    payload = b'{}'
    sig_header = "t=123,v1=abc"
    expected_event = {"id": "evt_123", "type": "checkout.session.completed"}

    mock_stripe_construct_event.return_value = expected_event

    event = await gateway.validar_webhook(payload, sig_header)

    mock_stripe_construct_event.assert_called_once_with(
        payload,
        sig_header,
        settings.STRIPE_WEBHOOK_SECRET
    )
    assert event == expected_event

@pytest.mark.asyncio
@patch('stripe.Webhook.construct_event')
async def test_validar_webhook_failure(mock_stripe_construct_event):
    from src.app.infrastructure.payments.stripe_payment_gateway import StripePaymentGateway
    gateway = StripePaymentGateway()

    payload = b'{}'
    sig_header = "t=123,v1=invalid"

    mock_stripe_construct_event.side_effect = stripe.SignatureVerificationError("Invalid signature", sig_header, payload)

    with pytest.raises(stripe.SignatureVerificationError):
        await gateway.validar_webhook(payload, sig_header)

    mock_stripe_construct_event.assert_called_once_with(
        payload,
        sig_header,
        settings.STRIPE_WEBHOOK_SECRET
    )