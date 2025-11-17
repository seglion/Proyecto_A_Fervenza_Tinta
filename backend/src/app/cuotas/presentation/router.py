from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Any
from uuid import UUID
from src.app.cuotas.application.use_cases.listar_cuotas_recientes_use_case import ListarCuotasRecientesUseCase
from src.app.cuotas.application.dtos import ListaCuotasRecientesDTO
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
from src.app.cuotas.application.dtos import ListaCuotasDTO, CuotaDTO, CrearTemporadaDTO, TemporadaCreadaDTO, ActualizarTemporadaDTO, TemporadaDTO, ListaTemporadasDTO, DetalleCuotaDTO,  CuotaCompletadaDTO, ActualizarCuotaManualDTO, InformePendientesDTO, HistorialCuotasDTO, IntentoPagoDTO
from src.app.cuotas.application.use_cases.actualizar_temporada_use_case import ActualizarTemporadaUseCase
from src.app.cuotas.application.use_cases.listar_temporadas_use_case import ListarTemporadasUseCase
from src.app.cuotas.application.exceptions import UnauthorizedException, TemporadaNoEncontrada, TipoCuotaNoEncontrado, CuotaNoEncontrada, CuotaYaPagadaException
from src.app.users.domain.entities import User
from src.app.core.dependencies import get_current_user, get_email_service
from src.app.users.domain.value_objects import Rol
from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.infrastructure.payments.stripe_payment_gateway import StripePaymentGateway
from src.app.cuotas.application.use_cases.ver_detalle_cuota_use_case import VerDetalleCuotaUseCase
from src.app.cuotas.application.use_cases.registrar_cuota_manual_use_case import RegistrarCuotaManualUseCase
from src.app.cuotas.application.use_cases.obtener_generar_mi_cuota_use_case import ObtenerGenerarMiCuotaUseCase
from src.app.cuotas.application.use_cases.generar_informe_pendientes_use_case import GenerarInformePendientesUseCase
from src.app.cuotas.application.use_cases.consultar_historial_cuotas_use_case import ConsultarHistorialCuotasUseCase
from src.app.cuotas.application.use_cases.crear_intento_pago_use_case import CrearIntentoPagoUseCase
from src.app.cuotas.application.use_cases.procesar_webhook_use_case import ProcesarWebhookUseCase
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.users.infrastructure.postgres_user_repository import PostgresUserRepository
from src.app.core.services.i_email_service import IEmailService

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

def get_payment_gateway() -> IPaymentGateway:
    return StripePaymentGateway()

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

def get_consultar_historial_cuotas_use_case(
    cuota_repository: ICuotaRepository = Depends(get_cuota_repository),
    tipo_cuota_repository: ITipoCuotaRepository = Depends(get_tipo_cuota_repository),
    temporada_cuota_repository: ITemporadaCuotaRepository = Depends(get_temporada_cuota_repository),
) -> ConsultarHistorialCuotasUseCase:
    cuota_policy = CuotaPolicy()
    return ConsultarHistorialCuotasUseCase(
        cuota_repository=cuota_repository,
        tipo_cuota_repository=tipo_cuota_repository,
        temporada_cuota_repository=temporada_cuota_repository,
        cuota_policy=cuota_policy
    )

def get_crear_intento_pago_use_case(
    obtener_generar_mi_cuota_uc: ObtenerGenerarMiCuotaUseCase = Depends(get_obtener_generar_mi_cuota_use_case),
    cuota_repository: ICuotaRepository = Depends(get_cuota_repository),
    payment_gateway: IPaymentGateway = Depends(get_payment_gateway),
) -> CrearIntentoPagoUseCase:
    cuota_policy = CuotaPolicy()
    return CrearIntentoPagoUseCase(obtener_generar_mi_cuota_uc, cuota_repository, payment_gateway, cuota_policy)

def get_procesar_webhook_use_case(
    payment_gateway: IPaymentGateway = Depends(get_payment_gateway),
    cuota_repository: ICuotaRepository = Depends(get_cuota_repository),
    email_service: IEmailService = Depends(get_email_service),
    user_repository: IUserRepository = Depends(get_usuario_repository),
) -> ProcesarWebhookUseCase:
    return ProcesarWebhookUseCase(payment_gateway=payment_gateway, cuota_repository=cuota_repository, email_service=email_service, user_repository=user_repository)

def get_listar_cuotas_recientes_use_case(
    cuota_repository: ICuotaRepository = Depends(get_cuota_repository),
) -> ListarCuotasRecientesUseCase:
    cuota_policy = CuotaPolicy()
    return ListarCuotasRecientesUseCase(cuota_repository, cuota_policy)





@router.post("/crear-intento-pago", response_model=IntentoPagoDTO, status_code=status.HTTP_200_OK)
async def crear_intento_pago(
    current_user: User = Depends(get_current_user),
    use_case: CrearIntentoPagoUseCase = Depends(get_crear_intento_pago_use_case)
):
    return await use_case.execute(current_user)

@router.get("/informe-pendientes", response_model=InformePendientesDTO, status_code=status.HTTP_200_OK)
async def generar_informe_pendientes(
    admin_user: User = Depends(get_admin_user),
    use_case: GenerarInformePendientesUseCase = Depends(get_generar_informe_pendientes_use_case)
):
    return await use_case.execute(admin_user)

@router.get("/historial", response_model=HistorialCuotasDTO, status_code=status.HTTP_200_OK)
async def consultar_historial_cuotas(
    current_user: User = Depends(get_current_user),
    use_case: ConsultarHistorialCuotasUseCase = Depends(get_consultar_historial_cuotas_use_case)
):
    return await use_case.execute(current_user)

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
@router.post("/webhooks/stripe", status_code=status.HTTP_200_OK)
async def procesar_webhook(
    request: Request,
    use_case: ProcesarWebhookUseCase = Depends(get_procesar_webhook_use_case)
):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    await use_case.execute(payload, sig_header)
    return {"status": "ok"}

@router.get("/recientes", response_model=ListaCuotasRecientesDTO, status_code=status.HTTP_200_OK)
async def listar_cuotas_recientes(
    admin_user: User = Depends(get_admin_user),
    use_case: ListarCuotasRecientesUseCase = Depends(get_listar_cuotas_recientes_use_case)
):
    """
    Obtiene las últimas 5 cuotas completadas (pagadas) para el dashboard.
    """
    try:
        return await use_case.execute(admin_user, limit=5)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@router.get("/{cuota_id}", response_model=DetalleCuotaDTO, status_code=status.HTTP_200_OK)
async def ver_detalle_cuota(cuota_id: UUID, admin_user: User = Depends(get_admin_user), use_case: VerDetalleCuotaUseCase = Depends(get_ver_detalle_cuota_use_case)):
    return await use_case.execute(admin_user, cuota_id)

@router.put("/{cuota_id}/registrar-manual", response_model=CuotaCompletadaDTO, status_code=status.HTTP_200_OK)
async def registrar_cuota_manual(
    cuota_id: UUID, 
    dto: ActualizarCuotaManualDTO, 
    admin_user: User = Depends(get_admin_user),
    use_case: RegistrarCuotaManualUseCase = Depends(get_registrar_cuota_manual_use_case)
):
    try:
        return await use_case.execute(admin_user, cuota_id, dto) 
    except CuotaNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CuotaYaPagadaException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

