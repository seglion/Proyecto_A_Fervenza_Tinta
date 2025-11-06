

from src.app.pedidos.application.dtos import IntentoPagoPedidoDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import TemporadaCerradaException, PedidoNoEncontradoException, PedidoVacioException, AccesoDenegadoException
from src.app.users.domain.entities import User
from src.app.pedidos.domain.value_objects import EstadoPedido


class ConfirmarPagoPedidoUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        temporada_pedido_repository: ITemporadaPedidoRepository,
        payment_gateway: IPaymentGateway,
        pedido_policy: PedidoPolicy,
    ):
        self.pedido_repository = pedido_repository
        self.temporada_pedido_repository = temporada_pedido_repository
        self.payment_gateway = payment_gateway
        self.pedido_policy = pedido_policy

    async def execute(self, current_user: User) -> IntentoPagoPedidoDTO:
        # 1. Comprobar temporada activa
        temporada_activa = await self.temporada_pedido_repository.get_temporada_activa()
        if not temporada_activa or not temporada_activa.esta_activa:
            raise TemporadaCerradaException("No hay temporada de pedidos activa o está cerrada.")

        # 2. Buscar pedido 'borrador'
        pedido_borrador = await self.pedido_repository.buscar_borrador_por_usuario(
            current_user.id
        )
        if not pedido_borrador:
            raise PedidoNoEncontradoException("No se encontró un pedido en borrador para el usuario.")

        # 3. Verificar política de acceso
        if not self.pedido_policy.ver_pedido(current_user, pedido_borrador):
            raise AccesoDenegadoException()

        if not pedido_borrador.lineas:
            raise PedidoVacioException("El pedido no tiene líneas para confirmar.")

        # 4. Crear sesión de Stripe
        line_items = [
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": linea.desc_variante_conxelada,
                    },
                    "unit_amount": int(linea.precio_unitario_conxelado * 100),
                },
                "quantity": linea.cantidad,
            }
            for linea in pedido_borrador.lineas
        ]

        url_pago, id_transaccion = await self.payment_gateway.crear_sesion_pago_pedido(
            amount=int(pedido_borrador.total_calculado * 100),
            currency="eur",
            line_items=line_items,
            pedido_id=pedido_borrador.id,
            user_id=current_user.id
        )

        # 5. Actualizar pedido a 'pendiente_pago'
        pedido_borrador.estado = EstadoPedido.PENDIENTEPAGO
        pedido_borrador.id_transaccion_externa = id_transaccion
        # metodo_pago se establecerá en el webhook de Stripe

        await self.pedido_repository.guardar_pedido(pedido_borrador)

        return IntentoPagoPedidoDTO(url_pago=url_pago)
