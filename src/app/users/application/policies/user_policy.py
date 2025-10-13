from uuid import UUID
from app.users.domain.entities import User
from app.users.domain.value_objects import Rol

class UserPolicy:
    def ver_perfil(self, current_user: User, target_user_id: UUID) -> bool:
        if self.es_administrador(current_user):
            return True
        return current_user.id == target_user_id

    def actualizar_perfil(self, current_user: User, target_user_id: UUID) -> bool:
        return self.ver_perfil(current_user, target_user_id)

    def solicitar_eliminacion(self, current_user: User, target_user_id: UUID) -> bool:
        return self.ver_perfil(current_user, target_user_id)

    def es_administrador(self, current_user: User) -> bool:
        return current_user.rol == Rol.ADMIN