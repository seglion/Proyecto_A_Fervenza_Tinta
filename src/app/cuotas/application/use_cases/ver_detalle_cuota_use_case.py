from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository # Nuevo
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import DetalleCuotaDTO, UsuarioPolicyDTO, CuotaDTO, TemporadaDTO, TipoCuotaDTO # TipoCuotaDTO añadido
from src.app.users.application.dtos import UsuarioResponseDTO # Nuevo
from src.app.cuotas.application.exceptions import UnauthorizedException, CuotaNoEncontrada, TipoCuotaNoEncontrado, TemporadaNoEncontrada
from uuid import UUID

class VerDetalleCuotaUseCase:
    def __init__(
        self,
        cuota_repository: ICuotaRepository,
        tipo_cuota_repository: ITipoCuotaRepository,
        temporada_cuota_repository: ITemporadaCuotaRepository,
        usuario_repository: IUserRepository, # Nuevo
        cuota_policy: CuotaPolicy,
    ):
        self.cuota_repository = cuota_repository
        self.tipo_cuota_repository = tipo_cuota_repository
        self.temporada_cuota_repository = temporada_cuota_repository
        self.usuario_repository = usuario_repository # Nuevo
        self.cuota_policy = cuota_policy

    async def execute(self, user: User, cuota_id: UUID) -> DetalleCuotaDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para ver el detalle de la cuota.")

        cuota = await self.cuota_repository.buscar_por_id(cuota_id)
        if not cuota:
            raise CuotaNoEncontrada("La cuota no existe.")

        # Fetch user details
        usuario = await self.usuario_repository.buscar_por_id(cuota.usuario_id) # Nuevo
        if not usuario:
            # This should ideally not happen if referential integrity is maintained
            raise Exception("Usuario asociado a la cuota no encontrado.") # Or a more specific exception

        tipo_cuota = await self.tipo_cuota_repository.buscar_por_id(cuota.tipo_de_cuota_id)
        if not tipo_cuota:
            raise TipoCuotaNoEncontrado("El tipo de cuota asociado no existe.")

        temporada = await self.temporada_cuota_repository.buscar_por_id(tipo_cuota.temporada_id)
        if not temporada:
            raise TemporadaNoEncontrada("La temporada asociada no existe.")

        # Ahora que tenemos las entidades, creamos los DTOs
        cuota_dto = CuotaDTO.model_validate(cuota)
        temporada_dto = TemporadaDTO.model_validate(temporada)
        tipo_cuota_detalle_dto = TipoCuotaDTO.model_validate(tipo_cuota) # Nuevo
        usuario_detalle_dto = UsuarioResponseDTO.model_validate(usuario) # Nuevo

        return DetalleCuotaDTO(
            cuota=cuota_dto,
            temporada=temporada_dto,
            tipo_cuota_detalle=tipo_cuota_detalle_dto, # Nuevo
            usuario_detalle=usuario_detalle_dto # Nuevo
        )
