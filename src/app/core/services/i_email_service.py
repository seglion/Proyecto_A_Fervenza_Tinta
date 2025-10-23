from abc import ABC, abstractmethod

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
