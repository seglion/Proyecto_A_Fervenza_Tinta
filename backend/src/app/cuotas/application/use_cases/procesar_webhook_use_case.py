from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.exceptions import CuotaNoEncontrada
from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago
from uuid import UUID
from datetime import datetime
from src.app.core.services.i_email_service import IEmailService
from src.app.users.application.repositories.i_user_repository import IUserRepository

class ProcesarWebhookUseCase:
    def __init__(
        self,
        payment_gateway: IPaymentGateway,
        cuota_repository: ICuotaRepository,
        email_service: IEmailService,
        user_repository: IUserRepository,
    ):
        self.payment_gateway = payment_gateway
        self.cuota_repository = cuota_repository
        self.email_service = email_service
        self.user_repository = user_repository

    async def execute(self, payload: bytes, sig_header: str) -> None:
        event = await self.payment_gateway.validar_webhook(payload, sig_header)

        if event.type == "checkout.session.completed":
            session = event.data['object']
            cuota_id = session['metadata']['cuota_id']
            payment_intent_id = session.get('payment_intent')

            cuota = await self.cuota_repository.buscar_por_id(UUID(cuota_id))

            if not cuota:
                raise CuotaNoEncontrada("La cuota no existe.")

            cuota.estado_pago = EstadoPago.COMPLETADO
            cuota.fecha_pago = datetime.now()
            cuota.id_transaccion_externa = payment_intent_id
            cuota.metodo_pago = MetodoPago.STRIPE

            await self.cuota_repository.actualizar(cuota)

            # Obtener el usuario para enviar el correo de confirmación
            user = await self.user_repository.buscar_por_id(cuota.usuario_id)
            if user:
                cuota_info = {
                    "id": str(cuota.id),
                    "monto": cuota.importe_pagado,
                    "estado": cuota.estado_pago.value,
                    "fecha_pago": cuota.fecha_pago.isoformat() if cuota.fecha_pago else None,
                    "metodo_pago": cuota.metodo_pago.value,
                }
                self.email_service.enviar_email_confirmacion_pago(
                    email_to=user.email,
                    name=user.nombre,
                    cuota_info=cuota_info
                )
