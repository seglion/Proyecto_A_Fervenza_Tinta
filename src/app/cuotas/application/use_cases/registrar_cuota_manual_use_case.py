from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import ActualizarCuotaManualDTO, CuotaCompletadaDTO, UsuarioPolicyDTO
from src.app.cuotas.application.exceptions import UnauthorizedException, CuotaNoEncontrada, CuotaYaPagadaException
from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import EstadoPago
from uuid import UUID
from datetime import datetime

class RegistrarCuotaManualUseCase:
    def __init__(
        self,
        cuota_repository: ICuotaRepository,
        cuota_policy: CuotaPolicy,
    ):
        self.cuota_repository = cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User, cuota_id: UUID, dto: ActualizarCuotaManualDTO) -> CuotaCompletadaDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para registrar una cuota manual.")

        cuota = await self.cuota_repository.buscar_por_id(cuota_id)
        if not cuota:
            raise CuotaNoEncontrada("La cuota no existe.")

        if cuota.estado_pago == EstadoPago.COMPLETADO:
            raise CuotaYaPagadaException("La cuota ya ha sido pagada.")

        # Actualizar cuota existente
        cuota.importe_pagado = dto.importe
        cuota.estado_pago = EstadoPago.COMPLETADO
        cuota.metodo_pago = dto.metodo
        cuota.notas_admin = dto.notas
        cuota.fecha_pago = datetime.now()
        cuota_final = await self.cuota_repository.actualizar(cuota)

        return CuotaCompletadaDTO(id=cuota_final.id)
