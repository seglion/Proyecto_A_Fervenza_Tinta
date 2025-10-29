from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.application.dtos import ListaTemporadasDTO, TemporadaDTO, UsuarioPolicyDTO, TipoCuotaDTO
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.exceptions import UnauthorizedException

class ListarTemporadasUseCase:
    def __init__(
        self,
        temporada_cuota_repository: ITemporadaCuotaRepository,
        tipo_cuota_repository: ITipoCuotaRepository,
        cuota_policy: CuotaPolicy
    ):
        self.temporada_cuota_repository = temporada_cuota_repository
        self.tipo_cuota_repository = tipo_cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User) -> ListaTemporadasDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("Not authorized to list seasons.")

        temporadas = await self.temporada_cuota_repository.listar_todas()
        
        temporadas_con_tipos_cuota = []
        for temporada in temporadas:
            tipos_cuota_entities = await self.tipo_cuota_repository.buscar_por_temporada_id(temporada.id)
            temporada.tipos_cuota = tipos_cuota_entities # Assign entities to the domain object
            temporadas_con_tipos_cuota.append(temporada)

        return ListaTemporadasDTO(
            temporadas=[TemporadaDTO.model_validate(t) for t in temporadas_con_tipos_cuota]
        )
