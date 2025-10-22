from abc import ABC, abstractmethod

class IEmailService(ABC):
    @abstractmethod
    async def send_verification_email(self, email_to: str, name: str, token: str) -> None:
        pass

    @abstractmethod
    async def enviar_email_bienvenida(self, email_to: str, name: str) -> None:
        pass

    @abstractmethod
    async def send_reset_password_email(self, email_to: str, token: str) -> None:
        pass

    @abstractmethod
    async def enviar_email_rechazo(self, email_to: str) -> None:
        pass
