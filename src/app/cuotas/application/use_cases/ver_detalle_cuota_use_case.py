from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import DetalleCuotaDTO, UsuarioPolicyDTO, CuotaDTO, TemporadaDTO
from src.app.cuotas.application.exceptions import UnauthorizedException, CuotaNoEncontrada
from uuid import UUID

class VerDetalleCuotaUseCase:
    def __init__(
        self,
        cuota_repository: ICuotaRepository,
        cuota_policy: CuotaPolicy,
    ):
        self.cuota_repository = cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User, cuota_id: UUID) -> DetalleCuotaDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para ver el detalle de la cuota.")

        cuota = await self.cuota_repository.buscar_por_id_con_detalle(cuota_id)

        if not cuota:
            raise CuotaNoEncontrada("La cuota no existe.")

        cuota_dto = CuotaDTO.model_validate(cuota)
        temporada_dto = TemporadaDTO.model_validate(cuota.temporada)

        return DetalleCuotaDTO(cuota=cuota_dto, temporada=temporada_dto)
