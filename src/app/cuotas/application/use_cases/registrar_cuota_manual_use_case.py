from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import RegistrarCuotaManualDTO, CuotaCompletadaDTO, UsuarioPolicyDTO
from src.app.cuotas.application.exceptions import UnauthorizedException, TipoCuotaNoEncontrado, TemporadaNoEncontrada
from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import EstadoPago
from uuid import uuid4
from datetime import datetime

class RegistrarCuotaManualUseCase:
    def __init__(
        self,
        cuota_repository: ICuotaRepository,
        tipo_cuota_repository: ITipoCuotaRepository,
        temporada_cuota_repository: ITemporadaCuotaRepository,
        cuota_policy: CuotaPolicy,
    ):
        self.cuota_repository = cuota_repository
        self.tipo_cuota_repository = tipo_cuota_repository
        self.temporada_cuota_repository = temporada_cuota_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User, dto: RegistrarCuotaManualDTO) -> CuotaCompletadaDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para registrar una cuota manual.")

        # 1. Validar que el tipo_cuota_id existe y pertenece a la temporada activa
        tipo_cuota = await self.tipo_cuota_repository.buscar_por_id(dto.tipo_cuota_id)
        if not tipo_cuota:
            raise TipoCuotaNoEncontrado("El tipo de cuota especificado no existe.")

        temporada_activa = await self.temporada_cuota_repository.get_temporada_activa()
        if not temporada_activa or tipo_cuota.temporada_id != temporada_activa.id:
            raise TemporadaNoEncontrada("El tipo de cuota no pertenece a la temporada activa.")

        # 2. Buscar cuota pendiente existente
        cuota_existente = await self.cuota_repository.buscar_cuota_pendiente_por_usuario_y_tipo_cuota(
            dto.usuario_id, dto.tipo_cuota_id
        )

        if cuota_existente:
            # Actualizar cuota existente
            cuota_existente.importe_pagado = dto.importe
            cuota_existente.estado_pago = EstadoPago.COMPLETADO
            cuota_existente.metodo_pago = dto.metodo
            cuota_existente.notas_admin = dto.notas
            cuota_existente.fecha_pago = datetime.now()
            cuota_final = await self.cuota_repository.actualizar(cuota_existente)
        else:
            # Crear nueva cuota
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
            cuota_final = await self.cuota_repository.guardar(nueva_cuota)

        return CuotaCompletadaDTO(id=cuota_final.id)
