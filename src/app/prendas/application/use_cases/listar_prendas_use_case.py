from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.prendas.application.dtos import ListaPrendasDTO, PrendaDTO, UsuarioPolicyDTO, VariantePrendaDTO
from src.app.prendas.application.policies.prenda_policy import PrendaPolicy
from src.app.users.domain.entities import User
from src.app.prendas.application.exceptions import UnauthorizedException

class ListarPrendasUseCase:
    def __init__(self, prenda_repository: IPrendaRepository, prenda_policy: PrendaPolicy):
        self.prenda_repository = prenda_repository
        self.prenda_policy = prenda_policy

    async def execute(self, user: User) -> ListaPrendasDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.prenda_policy.es_usuario_activo(user_policy_dto):
            raise UnauthorizedException("No está autorizado para listar prendas.")

        prendas = await self.prenda_repository.listar_todas()
        return ListaPrendasDTO(
            prendas=[
                PrendaDTO(
                    id=p.id,
                    nombre=p.nombre,
                    descripcion=p.descripcion,
                    precio=p.precio,
                    imagen_url=p.imagen_url,
                    fecha_creacion=p.fecha_creacion,
                    variantes=[VariantePrendaDTO.model_validate(v) for v in p.variantes]
                )
                for p in prendas
            ]
        )
