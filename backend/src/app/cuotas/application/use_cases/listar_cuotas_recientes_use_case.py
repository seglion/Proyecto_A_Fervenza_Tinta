from typing import List
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.dtos import ListaCuotasRecientesDTO, CuotaDetalleResponseDTO, UsuarioPolicyDTO
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.cuotas.application.exceptions import UnauthorizedException

class ListarCuotasRecientesUseCase:
    """
    Caso de uso para obtener las N últimas cuotas completadas.
    """
    def __init__(self, cuota_repository: ICuotaRepository, cuota_policy: CuotaPolicy):
        self.cuota_repository = cuota_repository
        self.cuota_policy = cuota_policy


    async def execute(self, user: User, limit: int = 5) -> ListaCuotasRecientesDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=user.rol.value, esta_activo=user.esta_activo)
        if not self.cuota_policy.es_administrador(user_policy_dto):
            raise UnauthorizedException("apiErrors.notAuthorized")
        cuotas_con_detalle = await self.cuota_repository.listar_recientes_completadas_con_detalle(limit=limit)
        cuotas_dto: List[CuotaDetalleResponseDTO] = []
        for c_record in cuotas_con_detalle:
            cuotas_dto.append(
                CuotaDetalleResponseDTO(
                    id=c_record['id'],
                    usuario_id=c_record['usuario_id'],
                    tipo_de_cuota_id=c_record['tipo_de_cuota_id'],
                    importe_pagado=c_record['importe_pagado'],
                    estado_pago=c_record['estado_pago'],
                    fecha_pago=c_record['fecha_pago'],
                    metodo_pago=c_record['metodo_pago'],
                    id_transaccion_externa=c_record['id_transaccion_externa'],
                    notas_admin=c_record['notas_admin'],
                    
                    # Datos del JOIN
                    usuario_nombre=c_record['usuario_nombre'],
                    usuario_apellidos=c_record['usuario_apellidos'],
                    tipo_cuota_nombre=c_record['tipo_cuota_nombre'],
                    temporada_nombre=c_record['temporada_nombre']
                )
            )
        
        return ListaCuotasRecientesDTO(cuotas=cuotas_dto)