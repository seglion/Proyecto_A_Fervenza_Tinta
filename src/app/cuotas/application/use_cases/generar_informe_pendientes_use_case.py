from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.repositories.i_temporada_cuota_repository import ITemporadaCuotaRepository
from src.app.cuotas.application.repositories.i_tipo_cuota_repository import ITipoCuotaRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.domain.entities import Cuota, TemporadaCuota, TipoCuota
from src.app.cuotas.domain.value_objects import EstadoPago
from src.app.cuotas.application.dtos import InformePendientesDTO, UsuarioPolicyDTO, UsuarioConCuotaPendienteDTO, CuotaDTO
from src.app.users.application.dtos import UsuarioResponseDTO
from src.app.cuotas.application.exceptions import UnauthorizedException, TemporadaNoEncontrada, TipoCuotaNoEncontrado
from uuid import uuid4
from datetime import datetime

class GenerarInformePendientesUseCase:
    def __init__(
        self,
        cuota_repository: ICuotaRepository,
        temporada_cuota_repository: ITemporadaCuotaRepository,
        tipo_cuota_repository: ITipoCuotaRepository,
        usuario_repository: IUserRepository,
        cuota_policy: CuotaPolicy,
    ):
        self.cuota_repository = cuota_repository
        self.temporada_cuota_repository = temporada_cuota_repository
        self.tipo_cuota_repository = tipo_cuota_repository
        self.usuario_repository = usuario_repository
        self.cuota_policy = cuota_policy

    async def execute(self, user: User) -> InformePendientesDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("No tienes permiso para generar informes.")

        temporada_activa = await self.temporada_cuota_repository.get_temporada_activa()
        if not temporada_activa:
            raise TemporadaNoEncontrada("No hay temporada activa en este momento.")

        tipo_cuota_general = await self.tipo_cuota_repository.get_tipo_cuota_general(temporada_activa.id)
        if not tipo_cuota_general:
            raise TipoCuotaNoEncontrado("No se encontró la cuota general para la temporada activa.")

        tipo_cuota_nuevo_socio = await self.tipo_cuota_repository.get_tipo_cuota_nuevo_socio(temporada_activa.id)
        if not tipo_cuota_nuevo_socio:
            raise TipoCuotaNoEncontrado("No se encontró la cuota de nuevo socio para la temporada activa.")

        all_users = await self.usuario_repository.buscar_todos()
        reporte_pendientes = []

        for current_user in all_users:
            cuota_del_usuario = await self.cuota_repository.buscar_cualquier_cuota_por_usuario_y_temporada(current_user.id, temporada_activa.id)

            if not cuota_del_usuario:
                # Si no tiene cuota para la temporada activa, se la creamos pendiente
                es_socio_antiguo = await self.cuota_repository.ha_pagado_cuota_alta_antes(current_user.id)
                
                if es_socio_antiguo:
                    tipo_cuota_a_crear = tipo_cuota_general
                else:
                    tipo_cuota_a_crear = tipo_cuota_nuevo_socio
                
                nueva_cuota = Cuota(
                    id=uuid4(),
                    usuario_id=current_user.id,
                    tipo_de_cuota_id=tipo_cuota_a_crear.id,
                    importe_pagado=tipo_cuota_a_crear.importe, # Importe inicial de la cuota
                    estado_pago=EstadoPago.PENDIENTE,
                    fecha_pago=None,
                    metodo_pago=None,
                    id_transaccion_externa=None,
                    notas_admin=None,
                    fecha_creacion=datetime.now()
                )
                cuota_generada = await self.cuota_repository.guardar(nueva_cuota)
                cuota_para_reporte = cuota_generada
            else:
                cuota_para_reporte = cuota_del_usuario

            if cuota_para_reporte.estado_pago == EstadoPago.PENDIENTE:
                reporte_pendientes.append(
                    UsuarioConCuotaPendienteDTO(
                        usuario=UsuarioResponseDTO.model_validate(current_user),
                        cuota=CuotaDTO.model_validate(cuota_para_reporte)
                    )
                )
        
        return InformePendientesDTO(pendientes=reporte_pendientes)
