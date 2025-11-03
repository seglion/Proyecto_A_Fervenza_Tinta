from uuid import UUID
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.prendas.application.dtos import PrendaDetalleDTO, UsuarioPolicyDTO, VariantePrendaDTO
from src.app.prendas.application.policies.prenda_policy import PrendaPolicy
from src.app.users.domain.entities import User
from src.app.prendas.application.exceptions import UnauthorizedException, PrendaNotFoundError

class VerDetallePrendaUseCase:
    def __init__(self, prenda_repository: IPrendaRepository, prenda_policy: PrendaPolicy):
        self.prenda_repository = prenda_repository
        self.prenda_policy = prenda_policy

    async def execute(self, prenda_id: UUID, user: User) -> PrendaDetalleDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.prenda_policy.es_usuario_activo(user_policy_dto):
            raise UnauthorizedException("No está autorizado para ver el detalle de la prenda.")

        prenda = await self.prenda_repository.buscar_por_id_con_variantes(prenda_id)
        if not prenda:
            raise PrendaNotFoundError(f"No se encontró la prenda con el ID {prenda_id}")

        return PrendaDetalleDTO(
            id=prenda.id,
            nombre=prenda.nombre,
            descripcion=prenda.descripcion,
            precio=prenda.precio,
            imagen_url=prenda.imagen_url,
            fecha_creacion=prenda.fecha_creacion,
            variantes=[VariantePrendaDTO.model_validate(v) for v in prenda.variantes]
        )
