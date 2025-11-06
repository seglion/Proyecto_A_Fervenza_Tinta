from uuid import UUID
from datetime import datetime

from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.core.services.i_email_service import IEmailService
from src.app.pedidos.application.exceptions import PedidoNoEncontradoException
from src.app.pedidos.domain.value_objects import EstadoPedido, MetodoPago
from src.app.core.config import settings


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

        event = await self.payment_gateway.validar_webhook(
            payload, sig_header, settings.STRIPE_PEDIDOS_WEBHOOK_SECRET
        )
        session = event.data['object']
        pedido_id_str = session['metadata']['pedido_id']
        pedido_id = UUID(pedido_id_str)

        if event.type == "checkout.session.completed":
            payment_intent_id = session.get('payment_intent')
            pedido = await self.pedido_repository.buscar_por_id(pedido_id)

            if not pedido:
                raise PedidoNoEncontradoException("El pedido no existe.")

            pedido.estado = EstadoPedido.COMPLETADO
            pedido.fecha_finalizacion = datetime.now()
            pedido.id_transaccion_externa = payment_intent_id
            pedido.metodo_pago = MetodoPago.STRIPE

            await self.pedido_repository.guardar_pedido(pedido)

            user = await self.user_repository.buscar_por_id(pedido.usuario_id)
            if user:
                pedido_info = {
                    "name": user.nombre,
                    "pedido_id": str(pedido.id),
                    "total": str(pedido.total_calculado),
                    "estado": pedido.estado.value,
                    "fecha_finalizacion": pedido.fecha_finalizacion.isoformat() if pedido.fecha_finalizacion else None,
                }
                self.email_service.enviar_confirmacion_pago_pedido(user.email, pedido_info)

        elif event.type == "checkout.session.expired":
            pedido = await self.pedido_repository.buscar_por_id(pedido_id)

            if not pedido:
                raise PedidoNoEncontradoException("El pedido no existe.")

            if pedido.estado == EstadoPedido.PENDIENTE_PAGO:
                pedido.estado = EstadoPedido.CANCELADO
                pedido.fecha_finalizacion = datetime.now()
                await self.pedido_repository.guardar_pedido(pedido)