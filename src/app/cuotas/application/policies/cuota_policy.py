from src.app.cuotas.application.dtos import UsuarioPolicyDTO
from src.app.users.domain.value_objects import Rol

class CuotaPolicy:
    def es_administrador(self, current_user: UsuarioPolicyDTO) -> bool:
        return current_user.rol == Rol.ADMIN
