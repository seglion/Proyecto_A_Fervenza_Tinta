from abc import ABC, abstractmethod

class IEmailService(ABC):
    @abstractmethod
    async def send_verification_email(self, email: str, token: str) -> None:
        pass
