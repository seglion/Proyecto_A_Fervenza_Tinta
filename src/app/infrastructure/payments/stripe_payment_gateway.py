import stripe
from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.core.config import settings
from typing import List, Optional

class StripePaymentGateway(IPaymentGateway):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    async def crear_sesion_pago(self, user_id: int, amount: int, currency: str) -> str:
        try:
            checkout_session = stripe.checkout.Session.create(
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
                success_url="https://example.com/success", # Estas URLs deberían ser configurables
                cancel_url="https://example.com/cancel",   # Estas URLs deberían ser configurables
                metadata={'user_id': str(user_id)}
            )
            return checkout_session.url
        except stripe.error.StripeError as e:
            # Manejo de errores específicos de Stripe
            print(f"Error de Stripe al crear sesión de pago: {e}")
            raise
        except Exception as e:
            # Manejo de otros errores inesperados
            print(f"Error inesperado al crear sesión de pago: {e}")
            raise

    async def validar_webhook(self, payload: bytes, sig_header: str) -> object:
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError as e:
            # Invalid payload
            print(f"Error de valor en el payload del webhook: {e}")
            raise
        except stripe.SignatureVerificationError as e:
            # Invalid signature
            print(f"Error de verificación de firma del webhook: {e}")
            raise
        except Exception as e:
            # Otros errores inesperados
            print(f"Error inesperado al validar webhook: {e}")
            raise