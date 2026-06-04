from abc import ABC, abstractmethod


class IStorageService(ABC):
    @abstractmethod
    async def upload_image(self, data: bytes, filename: str, content_type: str) -> str:
        """Sube una imagen y devuelve su URL pública."""