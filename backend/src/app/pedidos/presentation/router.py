from app.pedidos.application.use_cases.actualizar_temporada_pedido_use_case import ActualizarTemporadaPedidoUseCase
from app.pedidos.application.use_cases.listar_temporadas_pedido_use_case import ListarTemporadasPedidoUseCase
from app.pedidos.application.use_cases.obtener_temporada_activa_use_case import ObtenerTemporadaActivaUseCase
from src.app.pedidos.application.use_cases.crear_resumen_produccion_use_case import CrearResumenProduccionUseCase
from fastapi import APIRouter, Depends, HTTPException, status, Request,Query
from typing import Any,  Optional
from uuid import UUID
from dataclasses import asdict # Add this import

from src.app.core.database import get_db
from src.app.core.dependencies import get_current_user
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.users.infrastructure.postgres_user_repository import PostgresUserRepository

from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.infrastructure.postgres_pedido_repository import PostgresPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.infrastructure.postgres_temporada_pedido_repository import PostgresTemporadaPedidoRepository
from src.app.prendas.application.repositories.i_variante_prenda_repository import IVariantePrendaRepository
from src.app.prendas.infrastructure.postgres_variante_prenda_repository import PostgresVariantePrendaRepository
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.prendas.infrastructure.postgres_prenda_repository import PostgresPrendaRepository

from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.infrastructure.payments.stripe_payment_gateway import StripePaymentGateway
from src.app.core.dependencies import get_email_service
from src.app.core.services.i_email_service import IEmailService

from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.use_cases.listar_historial_pedidos_use_case import ListarHistorialPedidosUseCase
from src.app.pedidos.application.use_cases.obtener_pedido_borrador_use_case import ObtenerPedidoBorradorUseCase 
from src.app.pedidos.application.use_cases.ver_detalle_mi_pedido_use_case import VerDetalleMiPedidoUseCase
from src.app.pedidos.application.use_cases.anadir_prenda_pedido_use_case import AnadirPrendaPedidoUseCase
from src.app.pedidos.application.use_cases.eliminar_prenda_pedido_use_case import EliminarPrendaPedidoUseCase
from src.app.pedidos.application.use_cases.confirmar_pago_pedido_use_case import ConfirmarPagoPedidoUseCase
from src.app.pedidos.application.dtos import ActualizarTemporadaPedidoDTO, ListaPedidosAdminDTO, ListaPedidosDTO, ListaTemporadasPedidoDTO, PedidoDTO, PedidoDetalleDTO, CrearLineaDePedidoDTO, IntentoPagoPedidoDTO, ResumenProduccionDTO # Import PedidoDTO for conversion
from src.app.pedidos.application.exceptions import AccesoDenegadoException, PedidoException, PedidoNoEncontradoException, TemporadaCerradaException, LineaDePedidoNoEncontradaException, PedidoVacioException, TemporadaPedidoNoEncontradaException # Import specific exceptions
from src.app.pedidos.application.use_cases.confirmar_encargo_use_case import ConfirmarEncargoUseCase 
from src.app.pedidos.application.use_cases.listar_todos_pedidos_use_case import ListarTodosPedidosUseCase 
from src.app.pedidos.application.use_cases.ver_detalle_pedido_admin_use_case import VerDetallePedidoAdminUseCase 
from src.app.pedidos.application.use_cases.marcar_pago_manual_pedido_use_case import MarcarPagoManualPedidoUseCase 
from src.app.pedidos.application.use_cases.cancelar_pedido_use_case import CancelarPedidoUseCase 
from src.app.pedidos.application.use_cases.procesar_webhook_pedido_use_case import ProcesarWebhookPedidoUseCase 

from src.app.pedidos.application.use_cases.crear_temporada_pedido_use_case import CrearTemporadaPedidoUseCase
from src.app.pedidos.application.dtos import DatosTemporadaPedidoDTO, TemporadaPedidoDTO, PedidoDetalleAdminDTO, DatosPagoManualDTO 

router = APIRouter(prefix="/pedidos", tags=["pedidos"])
router_admin = APIRouter(prefix="/admin/pedidos", tags=["admin-pedidos"])
router_webhooks = APIRouter(prefix="/webhooks", tags=["webhooks"])

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

def get_user_repository(db_connection: Any = Depends(get_db)) -> IUserRepository:
    return PostgresUserRepository(db_connection)

def get_variante_prenda_repository(db_connection: Any = Depends(get_db)) -> IVariantePrendaRepository:
    return PostgresVariantePrendaRepository(db_connection)

def get_prenda_repository(db_connection: Any = Depends(get_db)) -> IPrendaRepository:
    return PostgresPrendaRepository(db_connection)

def get_payment_gateway() -> IPaymentGateway:
    return StripePaymentGateway()

def get_pedido_policy() -> PedidoPolicy:
    return PedidoPolicy()

def get_listar_historial_pedidos_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
) -> ListarHistorialPedidosUseCase:
    return ListarHistorialPedidosUseCase(pedido_repository, pedido_policy)

def get_obtener_pedido_borrador_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    temporada_pedido_repository: ITemporadaPedidoRepository = Depends(get_temporada_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
) -> ObtenerPedidoBorradorUseCase:
    return ObtenerPedidoBorradorUseCase(pedido_repository, temporada_pedido_repository, pedido_policy)

def get_ver_detalle_mi_pedido_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
    user_repository: IUserRepository = Depends(get_user_repository),
) -> VerDetalleMiPedidoUseCase:
    return VerDetalleMiPedidoUseCase(pedido_repository, pedido_policy, user_repository)

def get_anadir_prenda_pedido_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    temporada_pedido_repository: ITemporadaPedidoRepository = Depends(get_temporada_pedido_repository),
    variante_prenda_repository: IVariantePrendaRepository = Depends(get_variante_prenda_repository),
    prenda_repository: IPrendaRepository = Depends(get_prenda_repository),
) -> AnadirPrendaPedidoUseCase:
    return AnadirPrendaPedidoUseCase(pedido_repository, temporada_pedido_repository, variante_prenda_repository, prenda_repository)

def get_eliminar_prenda_pedido_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    temporada_pedido_repository: ITemporadaPedidoRepository = Depends(get_temporada_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
) -> EliminarPrendaPedidoUseCase:
    return EliminarPrendaPedidoUseCase(pedido_repository, temporada_pedido_repository, pedido_policy)

def get_confirmar_pago_pedido_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    temporada_pedido_repository: ITemporadaPedidoRepository = Depends(get_temporada_pedido_repository),
    payment_gateway: IPaymentGateway = Depends(get_payment_gateway),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
) -> ConfirmarPagoPedidoUseCase:
    return ConfirmarPagoPedidoUseCase(pedido_repository, temporada_pedido_repository, payment_gateway, pedido_policy)


def get_confirmar_encargo_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    temporada_pedido_repository: ITemporadaPedidoRepository = Depends(get_temporada_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
) -> ConfirmarEncargoUseCase:
    return ConfirmarEncargoUseCase(pedido_repository, temporada_pedido_repository, pedido_policy)

def get_crear_temporada_pedido_use_case(
    temporada_pedido_repository: ITemporadaPedidoRepository = Depends(get_temporada_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
) -> CrearTemporadaPedidoUseCase:
    return CrearTemporadaPedidoUseCase(temporada_pedido_repository, pedido_policy)

def get_listar_todos_pedidos_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
) -> ListarTodosPedidosUseCase:
    return ListarTodosPedidosUseCase(pedido_repository, pedido_policy)

def get_ver_detalle_pedido_admin_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
    user_repository: IUserRepository = Depends(get_user_repository),
) -> VerDetallePedidoAdminUseCase:
    return VerDetallePedidoAdminUseCase(pedido_repository, pedido_policy,user_repository)

def get_marcar_pago_manual_pedido_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    user_repository: IUserRepository = Depends(get_user_repository),
    email_service: IEmailService = Depends(get_email_service),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
) -> MarcarPagoManualPedidoUseCase:
    return MarcarPagoManualPedidoUseCase(pedido_repository, user_repository, email_service, pedido_policy)

def get_cancelar_pedido_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
) -> CancelarPedidoUseCase:
    return CancelarPedidoUseCase(pedido_repository, pedido_policy)

def get_listar_temporadas_pedido_use_case(
    temporada_pedido_repository: ITemporadaPedidoRepository = Depends(get_temporada_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
    ) -> ListarTemporadasPedidoUseCase:
    return ListarTemporadasPedidoUseCase(temporada_pedido_repository, pedido_policy)

def get_obtener_temporada_activa_use_case(
    temporada_pedido_repository: ITemporadaPedidoRepository = Depends(get_temporada_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
) -> ObtenerTemporadaActivaUseCase:
    return ObtenerTemporadaActivaUseCase(temporada_pedido_repository, pedido_policy)

def get_actualizar_temporada_pedido_use_case(
    temporada_pedido_repository: ITemporadaPedidoRepository = Depends(get_temporada_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy),
    ) -> ActualizarTemporadaPedidoUseCase:
    return ActualizarTemporadaPedidoUseCase(temporada_pedido_repository, pedido_policy)

def get_crear_resumen_produccion_use_case(
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    pedido_policy: PedidoPolicy = Depends(get_pedido_policy)
) -> CrearResumenProduccionUseCase:
    """
    Crea una instancia del caso de uso para generar el resumen de producción.
    """
    return CrearResumenProduccionUseCase(
        pedido_repository=pedido_repository,
        pedido_policy=pedido_policy
    )

@router_admin.get("/", response_model=ListaPedidosAdminDTO, status_code=status.HTTP_200_OK)
async def listar_todos_pedidos(
    admin_user: User = Depends(get_admin_user),
    temporada_id: Optional[int] = None,
    use_case: ListarTodosPedidosUseCase = Depends(get_listar_todos_pedidos_use_case)
):
    try:
        pedidos_admin_dto = await use_case.execute(admin_user, temporada_id)
        return pedidos_admin_dto
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router_admin.get("/resumen-produccion/{temporada_id}", response_model=ResumenProduccionDTO)
async def get_resumen_produccion(
    temporada_id: int,
    admin_user: User = Depends(get_admin_user),
    use_case: CrearResumenProduccionUseCase = Depends(get_crear_resumen_produccion_use_case),

):
    """
    Obtiene el resumen de producción (total de variantes pedidas) 
    para una temporada específica.
    """
    try:
        return await use_case.execute(admin_user, temporada_id)
    except AccesoDenegadoException  as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # (Es buena idea loggear el error 'e' aquí)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    return await use_case.execute(admin_user, temporada_id)    




@router_admin.post("/temporadas", response_model=TemporadaPedidoDTO, status_code=status.HTTP_201_CREATED)
async def crear_temporada_pedido(
    datos_temporada: DatosTemporadaPedidoDTO,
    admin_user: User = Depends(get_admin_user),
    use_case: CrearTemporadaPedidoUseCase = Depends(get_crear_temporada_pedido_use_case)
):
    try:
        temporada_creada = await use_case.execute(datos_temporada, admin_user)
        return temporada_creada
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router_admin.get("/temporadas", response_model=ListaTemporadasPedidoDTO, status_code=status.HTTP_200_OK) 
async def listar_temporadas_pedido(
    admin_user: User = Depends(get_admin_user),
    use_case: ListarTemporadasPedidoUseCase = Depends(get_listar_temporadas_pedido_use_case)
    ):
    try:
        temporadas = await use_case.execute(admin_user)
        return ListaTemporadasPedidoDTO(temporadas=temporadas)
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router_admin.get("/temporadas/activa", response_model=TemporadaPedidoDTO, status_code=status.HTTP_200_OK)
async def obtener_temporada_activa_pedido(
    admin_user: User = Depends(get_admin_user),
    use_case: ObtenerTemporadaActivaUseCase = Depends(get_obtener_temporada_activa_use_case)
    ):
    try:
        temporada_activa = await use_case.execute(admin_user)
        return temporada_activa
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except TemporadaPedidoNoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router_admin.put("/temporadas/{temporada_id}", response_model=TemporadaPedidoDTO, status_code=status.HTTP_200_OK)
async def actualizar_temporada_pedido(
    temporada_id: int,
    datos_actualizacion: ActualizarTemporadaPedidoDTO,
    admin_user: User = Depends(get_admin_user),
    use_case: ActualizarTemporadaPedidoUseCase = Depends(get_actualizar_temporada_pedido_use_case)
    ):
    try:
        temporada_actualizada = await use_case.execute(temporada_id, datos_actualizacion, admin_user)
        return temporada_actualizada
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except TemporadaPedidoNoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.get("/borrador", response_model=PedidoDTO, status_code=status.HTTP_200_OK)
async def obtener_pedido_borrador(
    current_user: User = Depends(get_current_user),
    use_case: ObtenerPedidoBorradorUseCase = Depends(get_obtener_pedido_borrador_use_case)
):
    try:
        pedido_borrador_domain = await use_case.execute(current_user)
        return PedidoDTO.model_validate(pedido_borrador_domain)
    except PedidoNoEncontradoException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
    
    


@router.get("/", response_model=ListaPedidosDTO, status_code=status.HTTP_200_OK)
async def listar_pedidos(
    current_user: User = Depends(get_current_user),
    use_case: ListarHistorialPedidosUseCase = Depends(get_listar_historial_pedidos_use_case)
):
    try:
        pedidos_domain_entities = await use_case.execute(current_user)
        pedidos_dtos = []
        for pedido in pedidos_domain_entities:
            # Convert dataclass to dictionary
            pedido_dict = asdict(pedido)
            # Ensure enums are converted to their values
            pedido_dict["estado"] = pedido_dict["estado"].value
            if pedido_dict["metodo_pago"]:
                pedido_dict["metodo_pago"] = pedido_dict["metodo_pago"].value
            
            # Recursively convert nested LineaDePedido dataclasses to dictionaries
            pedido_dict["lineas"] = [asdict(linea) for linea in pedido_dict["lineas"]]
            # No enums in LineaDePedido, so no further conversion needed here

            pedidos_dtos.append(PedidoDTO(**pedido_dict))
        return {"pedidos": pedidos_dtos}
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")



@router.get("/{pedido_id}", response_model=PedidoDetalleDTO, status_code=status.HTTP_200_OK)
async def ver_detalle_mi_pedido(
    pedido_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: VerDetalleMiPedidoUseCase = Depends(get_ver_detalle_mi_pedido_use_case)
):
    try:
        pedido_detalle_domain = await use_case.execute(pedido_id, current_user.id)
        return PedidoDetalleDTO.model_validate(pedido_detalle_domain)
    except PedidoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router_admin.get("/{pedido_id}", response_model=PedidoDetalleAdminDTO, status_code=status.HTTP_200_OK)
async def ver_detalle_pedido_admin(
    pedido_id: UUID,
    admin_user: User = Depends(get_admin_user),
    use_case: VerDetallePedidoAdminUseCase = Depends(get_ver_detalle_pedido_admin_use_case)
):
    try:
        pedido_detalle_admin_domain = await use_case.execute(pedido_id, admin_user)
        return PedidoDetalleAdminDTO.model_validate(pedido_detalle_admin_domain)
    except PedidoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.post("/borrador/lineas", response_model=PedidoDTO, status_code=status.HTTP_200_OK)
async def anadir_prenda_pedido(
    crear_linea_dto: CrearLineaDePedidoDTO,
    current_user: User = Depends(get_current_user),
    use_case: AnadirPrendaPedidoUseCase = Depends(get_anadir_prenda_pedido_use_case)
):
    try:
        pedido_actualizado_domain = await use_case.execute(current_user, crear_linea_dto)
        return PedidoDTO.model_validate(pedido_actualizado_domain)
    except TemporadaCerradaException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except PedidoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/borrador/lineas/{linea_id}", response_model=PedidoDTO, status_code=status.HTTP_200_OK)
async def eliminar_prenda_pedido(
    linea_id: UUID,
    current_user: User = Depends(get_current_user),
    use_case: EliminarPrendaPedidoUseCase = Depends(get_eliminar_prenda_pedido_use_case)
):
    try:
        pedido_actualizado_domain = await use_case.execute(current_user, linea_id)
        return PedidoDTO.model_validate(pedido_actualizado_domain)
    except LineaDePedidoNoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/borrador/confirmar-pago", response_model=IntentoPagoPedidoDTO, status_code=status.HTTP_200_OK)
async def confirmar_pedido_e_iniciar_pago(
    current_user: User = Depends(get_current_user),
    use_case: ConfirmarPagoPedidoUseCase = Depends(get_confirmar_pago_pedido_use_case)
):
    try:
        intento_pago_dto = await use_case.execute(current_user)
        return intento_pago_dto
    except PedidoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PedidoVacioException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/borrador/confirmar-encargo", response_model=PedidoDTO, status_code=status.HTTP_201_CREATED)
async def confirmar_pedido_como_encargo(
    current_user: User = Depends(get_current_user),
    use_case: ConfirmarEncargoUseCase = Depends(get_confirmar_encargo_use_case)
):
    try:
        pedido_encargado_domain = await use_case.execute(current_user)
        return PedidoDTO.model_validate(pedido_encargado_domain)
    except PedidoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (PedidoVacioException, TemporadaCerradaException) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router_admin.post("/{pedido_id}/marcar-pagado", response_model=PedidoDTO, status_code=status.HTTP_200_OK)
async def marcar_pedido_como_pagado_manualmente(
    pedido_id: UUID,
    datos_pago_manual: DatosPagoManualDTO,
    admin_user: User = Depends(get_admin_user),
    use_case: MarcarPagoManualPedidoUseCase = Depends(get_marcar_pago_manual_pedido_use_case)
    ):
    try:
        pedido_actualizado_domain = await use_case.execute(pedido_id, datos_pago_manual, admin_user)
        return PedidoDTO.model_validate(pedido_actualizado_domain)
    except PedidoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except PedidoException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router_admin.delete("/{pedido_id}/cancelar", response_model=PedidoDTO, status_code=status.HTTP_200_OK)
async def cancelar_pedido(
    pedido_id: UUID,
    admin_user: User = Depends(get_admin_user),
    use_case: CancelarPedidoUseCase = Depends(get_cancelar_pedido_use_case)
    ):
    try:
        pedido_cancelado_domain = await use_case.execute(pedido_id, admin_user)
        return PedidoDTO.model_validate(pedido_cancelado_domain)
    except PedidoNoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AccesoDenegadoException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_procesar_webhook_pedido_use_case(
    payment_gateway: IPaymentGateway = Depends(get_payment_gateway),
    pedido_repository: IPedidoRepository = Depends(get_pedido_repository),
    user_repository: IUserRepository = Depends(get_user_repository),
    email_service: IEmailService = Depends(get_email_service),
) -> ProcesarWebhookPedidoUseCase:
    return ProcesarWebhookPedidoUseCase(
        payment_gateway=payment_gateway,
        pedido_repository=pedido_repository,
        user_repository=user_repository,
        email_service=email_service,
    )

@router.post("/webhooks/stripe", status_code=status.HTTP_200_OK)
async def procesar_webhook_pedido(
    request: Request,
    use_case: ProcesarWebhookPedidoUseCase = Depends(get_procesar_webhook_pedido_use_case),
):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        await use_case.execute(payload, sig_header)
        return {"status": "success"}
    except PedidoException as e:
        # Log the exception for monitoring purposes
        # For example: logging.error(f"Stripe webhook failed: {e.detail}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # General exception for unexpected errors
        # logging.error(f"Unexpected error in Stripe webhook: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")