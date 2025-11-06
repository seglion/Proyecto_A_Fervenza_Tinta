from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.dtos import ListaCuotasDTO, CuotaDTO, UsuarioPolicyDTO
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.exceptions import UnauthorizedException

class ListarCuotasUseCase:
    def __init__(self, cuota_repository: ICuotaRepository, cuota_policy: CuotaPolicy):
        self.cuota_repository = cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User) -> ListaCuotasDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("Not authorized to list fees.")

        cuotas = await self.cuota_repository.listar_todas()
        return ListaCuotasDTO(
            cuotas=[CuotaDTO.model_validate(c) for c in cuotas]
        )
