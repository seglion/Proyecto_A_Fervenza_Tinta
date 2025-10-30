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
from src.app.cuotas.application.dtos import ListaCuotasDTO, CuotaDTO, CrearTemporadaDTO, TemporadaCreadaDTO, ActualizarTemporadaDTO, TemporadaDTO, ListaTemporadasDTO, DetalleCuotaDTO, RegistrarCuotaManualDTO, CuotaCompletadaDTO, ActualizarCuotaManualDTO, InformePendientesDTO
from src.app.cuotas.application.use_cases.actualizar_temporada_use_case import ActualizarTemporadaUseCase
from src.app.cuotas.application.use_cases.listar_temporadas_use_case import ListarTemporadasUseCase
from src.app.cuotas.application.exceptions import UnauthorizedException, TemporadaNoEncontrada, TipoCuotaNoEncontrado, CuotaNoEncontrada, CuotaYaPagadaException
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

from src.app.cuotas.application.use_cases.ver_detalle_cuota_use_case import VerDetalleCuotaUseCase
from src.app.cuotas.application.use_cases.registrar_cuota_manual_use_case import RegistrarCuotaManualUseCase
from src.app.cuotas.application.use_cases.obtener_generar_mi_cuota_use_case import ObtenerGenerarMiCuotaUseCase
from src.app.cuotas.application.use_cases.generar_informe_pendientes_use_case import GenerarInformePendientesUseCase

from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.users.infrastructure.postgres_user_repository import PostgresUserRepository

def get_listar_temporadas_use_case(
    temporada_cuota_repository: ITemporadaCuotaRepository = Depends(get_temporada_cuota_repository),
    tipo_cuota_repository: ITipoCuotaRepository = Depends(get_tipo_cuota_repository),
) -> ListarTemporadasUseCase:
    cuota_policy = CuotaPolicy()
    return ListarTemporadasUseCase(temporada_cuota_repository, tipo_cuota_repository, cuota_policy)

def get_usuario_repository(db_connection: Any = Depends(get_db)) -> IUserRepository:
    return PostgresUserRepository(db_connection)

def get_ver_detalle_cuota_use_case(
    cuota_repository: ICuotaRepository = Depends(get_cuota_repository),
    tipo_cuota_repository: ITipoCuotaRepository = Depends(get_tipo_cuota_repository),
    temporada_cuota_repository: ITemporadaCuotaRepository = Depends(get_temporada_cuota_repository),
    usuario_repository: IUserRepository = Depends(get_usuario_repository),
) -> VerDetalleCuotaUseCase:
    cuota_policy = CuotaPolicy()
    return VerDetalleCuotaUseCase(cuota_repository, tipo_cuota_repository, temporada_cuota_repository, usuario_repository, cuota_policy)

def get_registrar_cuota_manual_use_case(
    cuota_repository: ICuotaRepository = Depends(get_cuota_repository),
) -> RegistrarCuotaManualUseCase:
    cuota_policy = CuotaPolicy()
    return RegistrarCuotaManualUseCase(cuota_repository, cuota_policy)

def get_obtener_generar_mi_cuota_use_case(
    cuota_repository: ICuotaRepository = Depends(get_cuota_repository),
    tipo_cuota_repository: ITipoCuotaRepository = Depends(get_tipo_cuota_repository),
    temporada_cuota_repository: ITemporadaCuotaRepository = Depends(get_temporada_cuota_repository),
) -> ObtenerGenerarMiCuotaUseCase:
    cuota_policy = CuotaPolicy()
    return ObtenerGenerarMiCuotaUseCase(cuota_repository, tipo_cuota_repository, temporada_cuota_repository, cuota_policy)

def get_generar_informe_pendientes_use_case(
    cuota_repository: ICuotaRepository = Depends(get_cuota_repository),
    temporada_cuota_repository: ITemporadaCuotaRepository = Depends(get_temporada_cuota_repository),
    tipo_cuota_repository: ITipoCuotaRepository = Depends(get_tipo_cuota_repository),
    usuario_repository: IUserRepository = Depends(get_usuario_repository),
) -> GenerarInformePendientesUseCase:
    cuota_policy = CuotaPolicy()
    return GenerarInformePendientesUseCase(cuota_repository, temporada_cuota_repository, tipo_cuota_repository, usuario_repository, cuota_policy)

@router.get("/informe-pendientes", response_model=InformePendientesDTO, status_code=status.HTTP_200_OK)
async def generar_informe_pendientes(
    admin_user: User = Depends(get_admin_user),
    use_case: GenerarInformePendientesUseCase = Depends(get_generar_informe_pendientes_use_case)
):
    return await use_case.execute(admin_user)

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

from uuid import UUID

@router.get("/temporadas", response_model=ListaTemporadasDTO, status_code=status.HTTP_200_OK)
async def listar_temporadas(
    admin_user: User = Depends(get_admin_user),
    use_case: ListarTemporadasUseCase = Depends(get_listar_temporadas_use_case)
):
    try:
        return await use_case.execute(admin_user)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.get("/mi-cuota-activa", response_model=CuotaDTO, status_code=status.HTTP_200_OK)
async def obtener_generar_mi_cuota_activa(
    current_user: User = Depends(get_current_user),
    use_case: ObtenerGenerarMiCuotaUseCase = Depends(get_obtener_generar_mi_cuota_use_case)
):
    try:
        return await use_case.execute(current_user)
    except TemporadaNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except TipoCuotaNoEncontrado as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/{cuota_id}", response_model=DetalleCuotaDTO, status_code=status.HTTP_200_OK)
async def ver_detalle_cuota(cuota_id: UUID, admin_user: User = Depends(get_admin_user), use_case: VerDetalleCuotaUseCase = Depends(get_ver_detalle_cuota_use_case)):
    return await use_case.execute(admin_user, cuota_id)

@router.put("/{cuota_id}/registrar-manual", response_model=CuotaCompletadaDTO, status_code=status.HTTP_200_OK) # Changed path and status code
async def registrar_cuota_manual(
    cuota_id: UUID, # New path parameter
    dto: ActualizarCuotaManualDTO, # Changed DTO
    admin_user: User = Depends(get_admin_user),
    use_case: RegistrarCuotaManualUseCase = Depends(get_registrar_cuota_manual_use_case)
):
    try:
        return await use_case.execute(admin_user, cuota_id, dto) # Updated execute call
    except CuotaNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CuotaYaPagadaException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
