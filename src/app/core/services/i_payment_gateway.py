from abc import ABC, abstractmethod
from uuid import UUID

class IPaymentGateway(ABC):
    
    @abstractmethod
    async def crear_sesion_pago(self, user_id: int, amount: int, currency: str, cuota_id: UUID) -> str:
        pass

    @abstractmethod
    async def validar_webhook(self, payload: bytes, sig_header: str) -> object:
        pass
