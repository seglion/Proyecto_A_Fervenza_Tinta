from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import RegistrarCuotaManualDTO, CuotaDTO, UsuarioPolicyDTO
from src.app.cuotas.application.exceptions import UnauthorizedException
from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import EstadoPago
from uuid import uuid4
from datetime import datetime

class RegistrarCuotaManualUseCase:
    def __init__(
        self,
        cuota_repository: ICuotaRepository,
        cuota_policy: CuotaPolicy,
    ):
        self.cuota_repository = cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User, dto: RegistrarCuotaManualDTO) -> CuotaDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para registrar una cuota manual.")

        nueva_cuota = Cuota(
            id=uuid4(),
            usuario_id=dto.usuario_id,
            tipo_de_cuota_id=dto.tipo_cuota_id,
            importe_pagado=dto.importe,
            estado_pago=EstadoPago.COMPLETADO,
            metodo_pago=dto.metodo,
            notas_admin=dto.notas,
            fecha_pago=datetime.now(),
            fecha_creacion=datetime.now(),
        )

        cuota_guardada = await self.cuota_repository.guardar(nueva_cuota)

        return CuotaDTO.model_validate(cuota_guardada)
