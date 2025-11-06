import stripe
from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.core.config import settings
from typing import  Optional
from uuid import UUID

class StripePaymentGateway(IPaymentGateway):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    async def crear_sesion_pago(self, user_id: int, amount: int, currency: str, cuota_id: UUID) -> str:
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
                metadata={'user_id': str(user_id), 'cuota_id': str(cuota_id)}
            )
            return checkout_session.url

        except Exception as e:
            # Manejo de otros errores inesperados
            print(f"Error inesperado al crear sesión de pago: {e}")
            raise

    async def crear_sesion_pago_pedido(self, amount: int, currency: str, line_items: list, pedido_id: UUID,user_id: UUID) -> str:
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode="payment",
                success_url="https://example.com/success", # Estas URLs deberían ser configurables
                cancel_url="https://example.com/cancel",   # Estas URLs deberían ser configurables
                metadata={'user_id': str(user_id), 'pedido_id': str(pedido_id)}
            )
            return checkout_session.url, checkout_session.id

        except Exception as e:
            # Manejo de otros errores inesperados
            print(f"Error inesperado al crear sesión de pago de pedido: {e}")
            raise

    async def validar_webhook(self, payload: bytes, sig_header: str, webhook_secret: Optional[str] = None) -> object:
        secret = webhook_secret if webhook_secret else settings.STRIPE_CUOTAS_WEBHOOK_SECRET
        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                secret
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