from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import EstadoPagoDTO, UsuarioPolicyDTO, CuotaDTO
from src.app.cuotas.application.exceptions import UnauthorizedException
from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import EstadoPago
from uuid import uuid4
from datetime import datetime

class ObtenerEstadoPagoUseCase:
    def __init__(
        self,
        temporada_cuota_repository: ITemporadaCuotaRepository,
        cuota_repository: ICuotaRepository,
        tipo_cuota_repository: ITipoCuotaRepository,
        cuota_policy: CuotaPolicy,
    ):
        self.temporada_cuota_repository = temporada_cuota_repository
        self.cuota_repository = cuota_repository
        self.tipo_cuota_repository = tipo_cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User) -> EstadoPagoDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol, esta_activo=user.esta_activo)
        if not self.cuota_policy.puede_ver_estado_pago(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para ver el estado de pago.")

        temporada_activa = await self.temporada_cuota_repository.get_temporada_activa()
        if not temporada_activa:
            # TODO: Handle case where there is no active season
            pass

        cuota = await self.cuota_repository.buscar_por_usuario_y_temporada(user.id, temporada_activa.id)

        if cuota:
            cuota_dto = CuotaDTO.model_validate(cuota)
            return EstadoPagoDTO(estado=cuota.estado_pago, cuota=cuota_dto)
        else:
            ha_pagado_antes = await self.cuota_repository.ha_pagado_cuota_alta_antes(user.id)
            if ha_pagado_antes:
                tipo_cuota = await self.tipo_cuota_repository.get_tipo_cuota_general(temporada_activa.id)
            else:
                tipo_cuota = await self.tipo_cuota_repository.get_tipo_cuota_nuevo_socio(temporada_activa.id)
            
            nueva_cuota = Cuota(
                id=uuid4(),
                usuario_id=user.id,
                tipo_de_cuota_id=tipo_cuota.id,
                importe_pagado=tipo_cuota.importe,
                estado_pago=EstadoPago.PENDIENTE,
                fecha_creacion=datetime.now(),
            )
            cuota_dto = CuotaDTO.model_validate(nueva_cuota)
            return EstadoPagoDTO(estado=EstadoPago.PENDIENTE, cuota=cuota_dto)
