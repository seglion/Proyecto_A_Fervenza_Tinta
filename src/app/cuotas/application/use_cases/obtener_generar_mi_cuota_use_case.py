from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.dtos import CuotaDTO
from uuid import uuid4
from datetime import datetime

from src.app.cuotas.domain.value_objects import EstadoPago
from src.app.cuotas.application.exceptions import TemporadaNoEncontrada, TipoCuotaNoEncontrado
from src.app.cuotas.domain.entities import Cuota

class ObtenerGenerarMiCuotaUseCase:
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

    async def execute(self, user: User) -> CuotaDTO:
        temporada_activa = await self.temporada_cuota_repository.get_temporada_activa()
        if not temporada_activa:
            raise TemporadaNoEncontrada("No hay temporada activa en este momento.")

        cuota_existente = await self.cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada(user.id, temporada_activa.id)

        if cuota_existente:
            return CuotaDTO(
                id=cuota_existente.id,
                usuario_id=cuota_existente.usuario_id,
                tipo_de_cuota_id=cuota_existente.tipo_de_cuota_id,
                importe_pagado=cuota_existente.importe_pagado,
                estado_pago=cuota_existente.estado_pago,
                fecha_pago=cuota_existente.fecha_pago,
                metodo_pago=cuota_existente.metodo_pago,
                id_transaccion_externa=cuota_existente.id_transaccion_externa,
                notas_admin=cuota_existente.notas_admin,
                fecha_creacion=cuota_existente.fecha_creacion
            )

        # Si no hay cuota existente, generarla
        es_socio_antiguo = await self.cuota_repository.ha_pagado_cuota_alta_antes(user.id)

        if es_socio_antiguo:
            tipo_cuota = await self.tipo_cuota_repository.get_tipo_cuota_general(temporada_activa.id)
            if not tipo_cuota:
                raise TipoCuotaNoEncontrado("No se encontró la cuota general para la temporada activa.")
        else:
            tipo_cuota = await self.tipo_cuota_repository.get_tipo_cuota_nuevo_socio(temporada_activa.id)
            if not tipo_cuota:
                raise TipoCuotaNoEncontrado("No se encontró la cuota de nuevo socio para la temporada activa.")

        nueva_cuota = Cuota(
            id=uuid4(),
            usuario_id=user.id,
            tipo_de_cuota_id=tipo_cuota.id,
            importe_pagado=tipo_cuota.importe,
            estado_pago=EstadoPago.PENDIENTE,
            fecha_pago=None,
            metodo_pago=None,
            id_transaccion_externa=None,
            notas_admin=None,
            fecha_creacion=datetime.now()
        )

        cuota_generada = await self.cuota_repository.guardar(nueva_cuota)
        return CuotaDTO(
            id=cuota_generada.id,
            usuario_id=cuota_generada.usuario_id,
            tipo_de_cuota_id=cuota_generada.tipo_de_cuota_id,
            importe_pagado=cuota_generada.importe_pagado,
            estado_pago=cuota_generada.estado_pago,
            fecha_pago=cuota_generada.fecha_pago,
            metodo_pago=cuota_generada.metodo_pago,
            id_transaccion_externa=cuota_generada.id_transaccion_externa,
            notas_admin=cuota_generada.notas_admin,
            fecha_creacion=cuota_generada.fecha_creacion
        )
