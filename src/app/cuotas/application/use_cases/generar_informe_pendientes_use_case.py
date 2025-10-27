from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import InformePendientesDTO, UsuarioPolicyDTO
from src.app.users.application.dtos import UsuarioResponseDTO
from src.app.cuotas.application.exceptions import UnauthorizedException

class GenerarInformePendientesUseCase:
    def __init__(
        self,
        cuota_repository: ICuotaRepository,
        cuota_policy: CuotaPolicy,
    ):
        self.cuota_repository = cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User, temporada_id: int) -> InformePendientesDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para generar informes.")

        usuarios_pendientes = await self.cuota_repository.get_usuarios_pendientes_por_temporada(temporada_id)

        pendientes_dto = [UsuarioResponseDTO.model_validate(u) for u in usuarios_pendientes]

        return InformePendientesDTO(pendientes=pendientes_dto)
