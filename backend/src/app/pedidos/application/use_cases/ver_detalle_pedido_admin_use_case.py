from uuid import UUID

from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.users.application.exceptions import UserNotFoundException
from src.app.pedidos.application.dtos import PedidoDetalleAdminDTO, PedidoDetalleDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import AccesoDenegadoException, PedidoNoEncontradoException
from src.app.users.domain.entities import User
from src.app.users.application.dtos import UsuarioResponseDTO

class VerDetallePedidoAdminUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        pedido_policy: PedidoPolicy,
        user_repository: IUserRepository,
        
    ):
        self.pedido_repository = pedido_repository
        self.pedido_policy = pedido_policy
        self.user_repository = user_repository


    async def execute(self, id_pedido: UUID, current_user: User) -> PedidoDetalleAdminDTO:
        if not self.pedido_policy.es_administrador(current_user):
            raise AccesoDenegadoException("No tiene permiso para ver el detalle de este pedido.")

        # 1. Obtiene el pedido (con lineas)
        pedido = await self.pedido_repository.buscar_por_id_con_detalle(id_pedido)
        if not pedido:
            raise PedidoNoEncontradoException("Pedido no encontrado.")

        # 2. Obtiene el usuario
        user = await self.user_repository.buscar_por_id(pedido.usuario_id)
        if not user:
            raise UserNotFoundException()
        
        # --- ¡LA CORRECCIÓN ESTÁ AQUÍ! ---
        
        # 3. Convierte el pedido (Entidad) a un dict
        # (Usa .model_dump() si 'pedido' es un Pydantic Model, o vars(pedido) si es SQLAlchemy)
        try:
            pedido_data = pedido.model_dump()
        except AttributeError:
            pedido_data = vars(pedido) # Fallback para SQLAlchemy
            # (Asegúrate de manejar las 'lineas' si no se convierten bien)

        # 4. Convierte el usuario (Entidad) a su DTO
        usuario_dto = UsuarioResponseDTO.model_validate(user)
        
        # 5. Crea el DTO de respuesta final combinando ambos
        response_dto = PedidoDetalleAdminDTO(
            **pedido_data, # Pasa todos los campos del pedido (id, estado, lineas, etc.)
            usuario_detalle=usuario_dto # ¡Añade el usuario que faltaba!
        )

        return response_dto