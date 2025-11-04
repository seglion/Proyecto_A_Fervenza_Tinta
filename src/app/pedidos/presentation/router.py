from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List
from uuid import UUID

from src.app.core.database import get_db
from src.app.core.dependencies import get_current_user
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol

from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.infrastructure.postgres_pedido_repository import PostgresPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.infrastructure.postgres_temporada_pedido_repository import PostgresTemporadaPedidoRepository

# DTOs (se definirán en application/dtos.py)
# from src.app.pedidos.application.dtos import PedidoDTO, LineaDePedidoDTO, TemporadaPedidoDTO, CrearTemporadaPedidoDTO

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.rol.value != Rol.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

def get_pedido_repository(db_connection: Any = Depends(get_db)) -> IPedidoRepository:
    return PostgresPedidoRepository(db_connection)

def get_temporada_pedido_repository(db_connection: Any = Depends(get_db)) -> ITemporadaPedidoRepository:
    return PostgresTemporadaPedidoRepository(db_connection)

# TODO: Añadir funciones de dependencia para los casos de uso
# TODO: Implementar los endpoints según diagrama_pedidos.md
