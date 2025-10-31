from dataclasses import asdict
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import HistorialCuotasDTO, UsuarioPolicyDTO, CuotaDetalleResponseDTO
from src.app.cuotas.application.exceptions import UnauthorizedException

class ConsultarHistorialCuotasUseCase:
    def __init__(
        self,
        cuota_repository: ICuotaRepository,
        tipo_cuota_repository: ITipoCuotaRepository,
        temporada_cuota_repository: ITemporadaCuotaRepository,
        cuota_policy: CuotaPolicy,
    ):
        self._cuota_repository = cuota_repository
        self._tipo_cuota_repository = tipo_cuota_repository
        self._temporada_cuota_repository = temporada_cuota_repository
        self._cuota_policy = cuota_policy

    async def execute(self, user: User) -> HistorialCuotasDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self._cuota_policy.puede_consultar_historial(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para consultar el historial de cuotas.")

        cuotas = await self._cuota_repository.buscar_por_usuario_id(user.id)
        
        historial_detallado = []
        for cuota in cuotas:
            tipo_cuota = await self._tipo_cuota_repository.buscar_por_id(cuota.tipo_de_cuota_id)
            if not tipo_cuota:
                continue

            temporada = await self._temporada_cuota_repository.buscar_por_id(tipo_cuota.temporada_id)
            if not temporada:
                continue
            
            detalle_dto = CuotaDetalleResponseDTO(
                **asdict(cuota),
                usuario_nombre=user.nombre,
                usuario_apellidos=user.apellidos,
                tipo_cuota_nombre=tipo_cuota.nombre,
                temporada_nombre=temporada.nombre_temporada
            )
            historial_detallado.append(detalle_dto)

        return HistorialCuotasDTO(historial=historial_detallado)
