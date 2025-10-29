from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List

from src.app.core.database import get_db
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.infrastructure.postgres_cuota_repository import PostgresCuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.cuotas.application.use_cases.listar_cuotas_use_case import ListarCuotasUseCase
from src.app.cuotas.application.use_cases.crear_temporada_use_case import CrearTemporadaUseCase
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.infrastructure.postgres_temporada_cuota_repository import PostgresTemporadaCuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.infrastructure.postgres_tipo_cuota_repository import PostgresTipoCuotaRepository
from src.app.cuotas.application.dtos import ListaCuotasDTO, CuotaDTO, CrearTemporadaDTO, TemporadaCreadaDTO, ActualizarTemporadaDTO, TemporadaDTO, ListaTemporadasDTO
from src.app.cuotas.application.use_cases.actualizar_temporada_use_case import ActualizarTemporadaUseCase
from src.app.cuotas.application.use_cases.listar_temporadas_use_case import ListarTemporadasUseCase
from src.app.cuotas.application.exceptions import UnauthorizedException, TemporadaNoEncontrada
from src.app.users.domain.entities import User
from src.app.core.dependencies import get_current_user
from src.app.users.domain.value_objects import Rol

router = APIRouter(prefix="/cuotas", tags=["cuotas"])

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:

    if current_user.rol.value != Rol.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

def get_cuota_repository(db_connection: Any = Depends(get_db)) -> ICuotaRepository:
    return PostgresCuotaRepository(db_connection)

def get_temporada_cuota_repository(db_connection: Any = Depends(get_db)) -> ITemporadaCuotaRepository:
    return PostgresTemporadaCuotaRepository(db_connection)

def get_tipo_cuota_repository(db_connection: Any = Depends(get_db)) -> ITipoCuotaRepository:
    return PostgresTipoCuotaRepository(db_connection)

def get_listar_cuotas_use_case(
    cuota_repository: ICuotaRepository = Depends(get_cuota_repository),
) -> ListarCuotasUseCase:
    cuota_policy = CuotaPolicy()
    return ListarCuotasUseCase(cuota_repository, cuota_policy)

def get_crear_temporada_use_case(
    temporada_cuota_repository: ITemporadaCuotaRepository = Depends(get_temporada_cuota_repository),
    tipo_cuota_repository: ITipoCuotaRepository = Depends(get_tipo_cuota_repository),
) -> CrearTemporadaUseCase:
    cuota_policy = CuotaPolicy()
    return CrearTemporadaUseCase(temporada_cuota_repository, tipo_cuota_repository, cuota_policy)

def get_actualizar_temporada_use_case(
    temporada_cuota_repository: ITemporadaCuotaRepository = Depends(get_temporada_cuota_repository),
    tipo_cuota_repository: ITipoCuotaRepository = Depends(get_tipo_cuota_repository),
) -> ActualizarTemporadaUseCase:
    cuota_policy = CuotaPolicy()
    return ActualizarTemporadaUseCase(temporada_cuota_repository, tipo_cuota_repository, cuota_policy)

def get_listar_temporadas_use_case(
    temporada_cuota_repository: ITemporadaCuotaRepository = Depends(get_temporada_cuota_repository),
    tipo_cuota_repository: ITipoCuotaRepository = Depends(get_tipo_cuota_repository),
) -> ListarTemporadasUseCase:
    cuota_policy = CuotaPolicy()
    return ListarTemporadasUseCase(temporada_cuota_repository, tipo_cuota_repository, cuota_policy)

@router.get("/", response_model=ListaCuotasDTO, status_code=status.HTTP_200_OK)
async def listar_cuotas(
    admin_user: User = Depends(get_admin_user),
    use_case: ListarCuotasUseCase = Depends(get_listar_cuotas_use_case)
):
    return await use_case.execute(admin_user)

@router.post("/temporadas", response_model=TemporadaCreadaDTO, status_code=status.HTTP_201_CREATED)
async def crear_temporada(
    dto: CrearTemporadaDTO,
    admin_user: User = Depends(get_admin_user),
    use_case: CrearTemporadaUseCase = Depends(get_crear_temporada_use_case)
):
    return await use_case.execute(admin_user, dto)

@router.put("/temporadas/{temporada_id}", response_model=TemporadaDTO, status_code=status.HTTP_200_OK)
async def actualizar_temporada(
    temporada_id: int,
    dto: ActualizarTemporadaDTO,
    admin_user: User = Depends(get_admin_user),
    use_case: ActualizarTemporadaUseCase = Depends(get_actualizar_temporada_use_case)
):
    try:
        return await use_case.execute(admin_user, temporada_id, dto)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except TemporadaNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/temporadas", response_model=ListaTemporadasDTO, status_code=status.HTTP_200_OK)
async def listar_temporadas(
    admin_user: User = Depends(get_admin_user),
    use_case: ListarTemporadasUseCase = Depends(get_listar_temporadas_use_case)
):
    try:
        return await use_case.execute(admin_user)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))