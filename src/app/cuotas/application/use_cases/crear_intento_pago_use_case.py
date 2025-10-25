from src.app.cuotas.application.use_cases.obtener_estado_pago_use_case import ObtenerEstadoPagoUseCase
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import IntentoPagoDTO, UsuarioPolicyDTO
from src.app.cuotas.application.exceptions import UnauthorizedException, CuotaYaPagadaException
from src.app.cuotas.domain.value_objects import EstadoPago

class CrearIntentoPagoUseCase:
    def __init__(
        self,
        obtener_estado_pago_uc: ObtenerEstadoPagoUseCase,
        cuota_repository: ICuotaRepository,
        payment_gateway: IPaymentGateway,
        cuota_policy: CuotaPolicy,
    ):
        self.obtener_estado_pago_uc = obtener_estado_pago_uc
        self.cuota_repository = cuota_repository
        self.payment_gateway = payment_gateway
        self.cuota_policy = cuota_policy

    async def execute(self, user: User) -> IntentoPagoDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol, esta_activo=user.esta_activo)
        if not self.cuota_policy.puede_crear_intento_pago(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para crear un intento de pago.")

        estado_pago = await self.obtener_estado_pago_uc.execute(user)

        if estado_pago.estado == EstadoPago.COMPLETADO:
            raise CuotaYaPagadaException("La cuota para la temporada actual ya ha sido pagada.")

        cuota_guardada = await self.cuota_repository.guardar(estado_pago.cuota)

        url_pago = await self.payment_gateway.crear_sesion_pago(
            user_id=user.id,
            amount=cuota_guardada.importe_pagado,
            currency="eur",
        )

        return IntentoPagoDTO(url_pago=url_pago)
