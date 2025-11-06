from abc import ABC, abstractmethod
from typing import Dict, Any

class IEmailService(ABC):
    @abstractmethod
    def send_verification_email(self, email_to: str, name: str, token: str) -> None:
        pass

    @abstractmethod
    def enviar_email_bienvenida(self, email_to: str, name: str) -> None:
        pass

    @abstractmethod
    def send_reset_password_email(self, email_to: str, token: str) -> None:
        pass

    @abstractmethod
    def enviar_email_rechazo(self, email_to: str) -> None:
        pass

    @abstractmethod
    def enviar_email_confirmacion_pago(self, email_to: str, name: str, cuota_info: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def enviar_confirmacion_pago_pedido(self, email_to: str, pedido_info: Dict[str, Any]) -> None:
        pass
