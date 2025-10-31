from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.exceptions import CuotaNoEncontrada
from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago
from uuid import UUID
from datetime import datetime

class ProcesarWebhookUseCase:
    def __init__(
        self,
        payment_gateway: IPaymentGateway,
        cuota_repository: ICuotaRepository,
    ):
        self.payment_gateway = payment_gateway
        self.cuota_repository = cuota_repository

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
