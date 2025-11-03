from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from uuid import UUID

from src.app.core.database import get_db
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.prendas.application.repositories.i_variante_prenda_repository import IVariantePrendaRepository # Añadido
from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository
from src.app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository # Añadido
from src.app.prendas.application.policies.prenda_policy import PrendaPolicy
from src.app.prendas.application.use_cases.listar_prendas_use_case import ListarPrendasUseCase
from src.app.prendas.application.use_cases.ver_detalle_prenda_use_case import VerDetallePrendaUseCase
from src.app.prendas.application.use_cases.crear_prenda_use_case import CrearPrendaUseCase
from src.app.prendas.application.use_cases.actualizar_prenda_use_case import ActualizarPrendaUseCase
from src.app.prendas.application.use_cases.eliminar_prenda_use_case import EliminarPrendaUseCase
from src.app.prendas.application.use_cases.anadir_variante_use_case import AnadirVarianteUseCase # Añadido
from src.app.prendas.application.use_cases.eliminar_variante_use_case import EliminarVarianteUseCase # Añadido
from src.app.prendas.application.dtos import ListaPrendasDTO, PrendaDetalleDTO, CrearPrendaDTO, PrendaCreadaDTO, ActualizarPrendaDTO, PrendaActualizadaDTO, AnadirVarianteDTO, VarianteCreadaDTO # Modificado
from src.app.users.domain.entities import User
from src.app.core.dependencies import get_current_user
from src.app.users.domain.value_objects import Rol # Añadido

router = APIRouter(prefix="/prendas", tags=["prendas"])

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    if current_user.rol.value != Rol.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

def get_prenda_repository(db_connection: Any = Depends(get_db)) -> IPrendaRepository:
    return PostgresPrendaRepository(db_connection)

def get_variante_prenda_repository(db_connection: Any = Depends(get_db)) -> IVariantePrendaRepository:
    return PostgresVariantePrendaRepository(db_connection)


def get_listar_prendas_use_case(
    prenda_repository: IPrendaRepository = Depends(get_prenda_repository),
) -> ListarPrendasUseCase:
    prenda_policy = PrendaPolicy()
    return ListarPrendasUseCase(prenda_repository, prenda_policy)

def get_ver_detalle_prenda_use_case(
    prenda_repository: IPrendaRepository = Depends(get_prenda_repository),
) -> VerDetallePrendaUseCase:
    prenda_policy = PrendaPolicy()
    return VerDetallePrendaUseCase(prenda_repository, prenda_policy)

def get_crear_prenda_use_case(
    prenda_repository: IPrendaRepository = Depends(get_prenda_repository),
) -> CrearPrendaUseCase:
    prenda_policy = PrendaPolicy()
    return CrearPrendaUseCase(prenda_repository, prenda_policy)

def get_actualizar_prenda_use_case(
    prenda_repository: IPrendaRepository = Depends(get_prenda_repository),
) -> ActualizarPrendaUseCase:
    prenda_policy = PrendaPolicy()
    return ActualizarPrendaUseCase(prenda_repository, prenda_policy)

def get_eliminar_prenda_use_case(
    prenda_repository: IPrendaRepository = Depends(get_prenda_repository),
) -> EliminarPrendaUseCase:
    prenda_policy = PrendaPolicy()
    return EliminarPrendaUseCase(prenda_repository, prenda_policy)

def get_anadir_variante_use_case(
    prenda_repository: IPrendaRepository = Depends(get_prenda_repository),
    variante_prenda_repository: IVariantePrendaRepository = Depends(get_variante_prenda_repository),
) -> AnadirVarianteUseCase:
    prenda_policy = PrendaPolicy()
    return AnadirVarianteUseCase(prenda_repository, variante_prenda_repository, prenda_policy) # Añadido

def get_eliminar_variante_use_case(
    prenda_repository: IPrendaRepository = Depends(get_prenda_repository),
    variante_prenda_repository: IVariantePrendaRepository = Depends(get_variante_prenda_repository),
) -> EliminarVarianteUseCase:
    prenda_policy = PrendaPolicy()
    return EliminarVarianteUseCase(prenda_repository, variante_prenda_repository, prenda_policy)


@router.get("/", response_model=ListaPrendasDTO, status_code=status.HTTP_200_OK)
async def listar_prendas(
    current_user: User = Depends(get_current_user),
    use_case: ListarPrendasUseCase = Depends(get_listar_prendas_use_case)
):
    return await use_case.execute(current_user)

@router.get("/{prenda_id}", response_model=PrendaDetalleDTO, status_code=status.HTTP_200_OK)
async def ver_detalle_prenda(
    prenda_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: VerDetallePrendaUseCase = Depends(get_ver_detalle_prenda_use_case)
):
    return await use_case.execute(prenda_id, current_user)

@router.post("/", response_model=PrendaCreadaDTO, status_code=status.HTTP_201_CREATED)
async def crear_prenda(
    data: CrearPrendaDTO,
    current_user: User = Depends(get_admin_user), # Solo administradores pueden crear prendas
    use_case: CrearPrendaUseCase = Depends(get_crear_prenda_use_case)
):
    return await use_case.execute(data, current_user)

@router.put("/{prenda_id}", response_model=PrendaActualizadaDTO, status_code=status.HTTP_200_OK)
async def actualizar_prenda(
    prenda_id: UUID,
    data: ActualizarPrendaDTO,
    current_user: User = Depends(get_admin_user),
    use_case: ActualizarPrendaUseCase = Depends(get_actualizar_prenda_use_case)
):
    return await use_case.execute(prenda_id, data, current_user)

@router.delete("/{prenda_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_prenda(
    prenda_id: UUID,
    current_user: User = Depends(get_admin_user),
    use_case: EliminarPrendaUseCase = Depends(get_eliminar_prenda_use_case)
):
    await use_case.execute(prenda_id, current_user)
    return

@router.post("/{prenda_id}/variantes", response_model=VarianteCreadaDTO, status_code=status.HTTP_201_CREATED)
async def anadir_variante(
    prenda_id: UUID,
    data: AnadirVarianteDTO,
    current_user: User = Depends(get_admin_user),
    use_case: AnadirVarianteUseCase = Depends(get_anadir_variante_use_case)
):
    return await use_case.execute(prenda_id, data, current_user)

@router.delete("/{prenda_id}/variantes/{variante_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_variante(
    prenda_id: UUID,
    variante_id: UUID,
    current_user: User = Depends(get_admin_user),
    use_case: EliminarVarianteUseCase = Depends(get_eliminar_variante_use_case)
):
    await use_case.execute(prenda_id, variante_id, current_user)
    return

