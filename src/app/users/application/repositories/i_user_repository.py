from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.users.domain.entities import User


class IUserRepository(ABC):
    @abstractmethod
    async def crear(self, user: User) -> User:
        pass

    @abstractmethod
    async def buscar_por_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def buscar_por_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def actualizar(self, user: User) -> User:
        pass

    @abstractmethod
    async def actualizar_contrasena(self, user_id: UUID, contrasena_hasheada: str) -> None:
        pass

    @abstractmethod
    async def desactivar_cuenta(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def buscar_todos(self) -> List[User]:
        pass

    @abstractmethod
    async def eliminar_por_id(self, user_id: UUID) -> None:
        pass

