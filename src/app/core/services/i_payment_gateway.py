from abc import ABC, abstractmethod

class IPaymentGateway(ABC):
    
    @abstractmethod
    async def crear_sesion_pago(self, user_id: int, amount: int, currency: str) -> str:
        pass
