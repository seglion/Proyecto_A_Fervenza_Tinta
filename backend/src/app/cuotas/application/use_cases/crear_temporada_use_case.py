from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.application.dtos import CrearTemporadaDTO, TemporadaCreadaDTO, UsuarioPolicyDTO
from src.app.users.domain.entities import User
from src.app.cuotas.domain.entities import TemporadaCuota, TipoCuota
from src.app.cuotas.application.exceptions import UnauthorizedException
from datetime import datetime

class CrearTemporadaUseCase:
    def __init__(
        self,
        temporada_cuota_repository: ITemporadaCuotaRepository,
        tipo_cuota_repository: ITipoCuotaRepository,
        cuota_policy: CuotaPolicy,
    ):
        self.temporada_cuota_repository = temporada_cuota_repository
        self.tipo_cuota_repository = tipo_cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User, dto: CrearTemporadaDTO) -> TemporadaCreadaDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("Not authorized to create a season.")

        temporada = TemporadaCuota(
            id=None,  
            nombre_temporada=dto.nombre_temporada,
            fecha_inicio=dto.fecha_inicio,
            fecha_fin=dto.fecha_fin,
            fecha_creacion=datetime.now(),
        )
        temporada_creada = await self.temporada_cuota_repository.guardar_temporada(temporada)

        tipos_cuota = [
            TipoCuota(
                id=None, 
                temporada_id=temporada_creada.id,
                nombre=tipo_dto.nombre,
                importe=tipo_dto.importe,
                fecha_creacion=datetime.now(),
            )
            for tipo_dto in dto.tipos_cuota
        ]
        await self.tipo_cuota_repository.guardar_varios(tipos_cuota)

        return TemporadaCreadaDTO(id=temporada_creada.id)
