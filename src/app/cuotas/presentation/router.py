from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List

from src.app.core.database import get_db
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.cuotas.application.use_cases.listar_cuotas_use_case import ListarCuotasUseCase
from src.app.cuotas.application.dtos import ListaCuotasDTO, CuotaDTO
from src.app.users.domain.entities import User
from src.app.core.dependencies import get_current_user
from src.app.users.domain.value_objects import Rol

router = APIRouter(prefix="/cuotas", tags=["cuotas"])

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.rol != Rol.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

def get_cuota_repository(db_connection: Any = Depends(get_db)) -> ICuotaRepository:
    return PostgresCuotaRepository(db_connection)

def get_listar_cuotas_use_case(
    cuota_repository: ICuotaRepository = Depends(get_cuota_repository),
) -> ListarCuotasUseCase:
    cuota_policy = CuotaPolicy()
    return ListarCuotasUseCase(cuota_repository, cuota_policy)

@router.get("/", response_model=ListaCuotasDTO, status_code=status.HTTP_200_OK)
async def listar_cuotas(
    admin_user: User = Depends(get_admin_user),
    use_case: ListarCuotasUseCase = Depends(get_listar_cuotas_use_case)
):
    return await use_case.execute(admin_user)