from abc import ABC, abstractmethod
from typing import Optional, List
from app.users.domain.entities import Role

class IRoleRepository(ABC):
    @abstractmethod
    async def crear(self, role: Role) -> Role:
        pass

    @abstractmethod
    async def buscar_por_id(self, role_id: int) -> Optional[Role]:
        pass

    @abstractmethod
    async def buscar_por_nombre(self, nombre: str) -> Optional[Role]:
        pass

    @abstractmethod
    async def buscar_todos(self) -> List[Role]:
        pass
