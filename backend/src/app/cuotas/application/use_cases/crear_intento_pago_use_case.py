from src.app.cuotas.application.use_cases.obtener_generar_mi_cuota_use_case import ObtenerGenerarMiCuotaUseCase
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
        obtener_generar_mi_cuota_uc: ObtenerGenerarMiCuotaUseCase,
        cuota_repository: ICuotaRepository,
        payment_gateway: IPaymentGateway,
        cuota_policy: CuotaPolicy,
    ):
        self.obtener_generar_mi_cuota_uc = obtener_generar_mi_cuota_uc
        self.cuota_repository = cuota_repository
        self.payment_gateway = payment_gateway
        self.cuota_policy = cuota_policy

    async def execute(self, user: User) -> IntentoPagoDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.cuota_policy.puede_crear_intento_pago(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para crear un intento de pago.")

        cuota_a_pagar_dto = await self.obtener_generar_mi_cuota_uc.execute(user)

        if cuota_a_pagar_dto.estado_pago == EstadoPago.COMPLETADO:
            raise CuotaYaPagadaException("La cuota para la temporada actual ya ha sido pagada.")

        url_pago = await self.payment_gateway.crear_sesion_pago(
            user_id=user.id,
            amount=int(cuota_a_pagar_dto.importe_pagado*100),
            currency="eur",
            cuota_id=cuota_a_pagar_dto.id
        )

        return IntentoPagoDTO(url_pago=url_pago)
