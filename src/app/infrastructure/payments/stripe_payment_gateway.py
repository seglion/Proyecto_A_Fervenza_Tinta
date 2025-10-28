import asyncpg
from src.app.core.services.i_payment_gateway import IPaymentGateway
from typing import List, Optional

class StripePaymentGateway(IPaymentGateway):
    def __init__(self):
        pass

    async def crear_sesion_pago(self, user_id: int, amount: int, currency: str) -> str:
        pass

    async def validar_webhook(self, payload: bytes, sig_header: str) -> object:
        pass