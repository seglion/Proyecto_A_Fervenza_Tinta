from src.app.prendas.application.dtos import UsuarioPolicyDTO
from src.app.users.domain.value_objects import Rol

class PrendaPolicy:
    def es_administrador(self, current_user: UsuarioPolicyDTO) -> bool:
        return current_user.rol == Rol.ADMIN

    def es_usuario_activo(self, current_user: UsuarioPolicyDTO) -> bool:
        return current_user.esta_activo