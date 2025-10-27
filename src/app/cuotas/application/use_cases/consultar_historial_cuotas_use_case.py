from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import HistorialCuotasDTO, UsuarioPolicyDTO, CuotaDTO
from src.app.cuotas.application.exceptions import UnauthorizedException

class ConsultarHistorialCuotasUseCase:
    def __init__(
        self,
        cuota_repository: ICuotaRepository,
        cuota_policy: CuotaPolicy,
    ):
        self.cuota_repository = cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User) -> HistorialCuotasDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol, esta_activo=user.esta_activo)
        if not self.cuota_policy.puede_consultar_historial(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para consultar el historial de cuotas.")

        cuotas = await self.cuota_repository.buscar_por_usuario_id_completadas(user.id)

        cuotas_dto = [CuotaDTO.model_validate(c) for c in cuotas]

        return HistorialCuotasDTO(historial=cuotas_dto)
