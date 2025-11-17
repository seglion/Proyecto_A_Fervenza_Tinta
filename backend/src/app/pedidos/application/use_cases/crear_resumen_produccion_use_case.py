from typing import List
from uuid import UUID

# Importaciones de tu slice de Pedidos
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.policies.pedido_policy import PedidoPolicy
from src.app.pedidos.application.exceptions import AccesoDenegadoException
from src.app.pedidos.application.dtos import (
    ResumenProduccionDTO, 
    ResumenVarianteDTO
)

# Importaciones de tu slice de Usuarios
from src.app.users.domain.entities import User


class CrearResumenProduccionUseCase:
    """
    Caso de uso para obtener el informe de producción (resumen de variantes pedidas)
    para una temporada específica.
    """
    def __init__(
        self, 
        pedido_repository: IPedidoRepository, 
        pedido_policy: PedidoPolicy
    ):
        self.pedido_repository = pedido_repository
        self.pedido_policy = pedido_policy

    async def execute(self, admin_user: User, temporada_id: int) -> ResumenProduccionDTO:
        
        # 1. Comprobar permisos de administrador
        if not self.pedido_policy.es_administrador(admin_user):
            raise AccesoDenegadoException("apiErrors.notAuthorized")

        # 2. Llamar al repositorio (que hace el JOIN y GROUP BY)
        records = await self.pedido_repository.obtener_resumen_produccion(temporada_id)

        # 3. Mapear los records de la BBDD (asyncpg.Record) a DTOs
        # (Usamos dict(record) para convertir el record a un dict que Pydantic entiende)
        resumen_list: List[ResumenVarianteDTO] = []
        for record in records:
            resumen_list.append(ResumenVarianteDTO.model_validate(dict(record)))
        
        # 4. Devolver el DTO contenedor
        return ResumenProduccionDTO(resumen=resumen_list)