from uuid import UUID
from datetime import datetime

from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.core.services.i_email_service import IEmailService
from src.app.pedidos.application.exceptions import PedidoNoEncontradoException
from src.app.pedidos.domain.value_objects import EstadoPedido

# Asumiendo que MetodoPago está en el mismo fichero de value_objects
from src.app.pedidos.domain.value_objects import MetodoPago


class ProcesarWebhookPedidoUseCase:
    def __init__(
        self,
        payment_gateway: IPaymentGateway,
        pedido_repository: IPedidoRepository,
        user_repository: IUserRepository,
        email_service: IEmailService,
    ):
        self.payment_gateway = payment_gateway
        self.pedido_repository = pedido_repository
        self.user_repository = user_repository
        self.email_service = email_service

    async def execute(self, payload: bytes, sig_header: str) -> None:
        # La seguridad en los webhooks se basa en la validación de la firma,
        # que se hace dentro de payment_gateway.validar_webhook.
        # No se aplica una política de usuario porque la acción es iniciada
        # por un sistema externo (Stripe), no por un usuario logueado.
        event = await self.payment_gateway.validar_webhook(payload, sig_header)

        if event.type == "checkout.session.completed":
            session = event.data['object']
            pedido_id = session['metadata']['pedido_id']
            payment_intent_id = session.get('payment_intent')

            pedido = await self.pedido_repository.buscar_por_id(UUID(pedido_id))

            if not pedido:
                raise PedidoNoEncontradoException("El pedido no existe.")

            pedido.estado = EstadoPedido.COMPLETADO
            pedido.fecha_finalizacion = datetime.now()
            pedido.id_transaccion_externa = payment_intent_id
            pedido.metodo_pago = MetodoPago.STRIPE

            await self.pedido_repository.guardar_pedido(pedido)

            # Obtener el usuario para enviar el correo de confirmación
            user = await self.user_repository.buscar_por_id(pedido.usuario_id)
            if user:
                # Asumiendo que el servicio de email tiene un método para esto
                await self.email_service.enviar_confirmacion_pago_pedido(user.email, pedido)
