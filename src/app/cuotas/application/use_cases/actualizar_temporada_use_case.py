from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.application.dtos import ActualizarTemporadaDTO, TemporadaDTO, UsuarioPolicyDTO, TipoCuotaDTO
from src.app.users.domain.entities import User
from src.app.cuotas.domain.entities import TipoCuota
from src.app.cuotas.application.exceptions import UnauthorizedException, TemporadaNoEncontrada
from datetime import datetime

class ActualizarTemporadaUseCase:
    def __init__(
        self,
        temporada_cuota_repository: ITemporadaCuotaRepository,
        tipo_cuota_repository: ITipoCuotaRepository,
        cuota_policy: CuotaPolicy,
    ):
        self.temporada_cuota_repository = temporada_cuota_repository
        self.tipo_cuota_repository = tipo_cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User, temporada_id: int, dto: ActualizarTemporadaDTO) -> TemporadaDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("Not authorized to update a season.")

        temporada = await self.temporada_cuota_repository.buscar_por_id(temporada_id)
        if not temporada:
            raise TemporadaNoEncontrada("Season not found.")

        if dto.nombre_temporada:
            temporada.nombre_temporada = dto.nombre_temporada
        if dto.fecha_inicio:
            temporada.fecha_inicio = dto.fecha_inicio
        if dto.fecha_fin:
            temporada.fecha_fin = dto.fecha_fin
        
        temporada.fecha_actualizacion = datetime.now()

        temporada_actualizada = await self.temporada_cuota_repository.actualizar(temporada)

        if dto.tipos_cuota:
            tipos_cuota = [
                TipoCuota(
                    id=tc.id,
                    temporada_id=temporada_actualizada.id,
                    nombre=tc.nombre,
                    importe=tc.importe,
                    fecha_creacion=tc.fecha_creacion,
                )
                for tc in dto.tipos_cuota
            ]
            await self.tipo_cuota_repository.actualizar_varios(tipos_cuota)
            temporada_actualizada.tipos_cuota = tipos_cuota

        return TemporadaDTO.model_validate(temporada_actualizada)
