from uuid import UUID
from app.users.domain.entities import User

class UserPolicy:
    def ver_perfil(self, current_user: User, target_user_id: UUID) -> bool:
        if current_user.id == target_user_id:
            return True
        # TODO: Add role check
        # if "admin" in current_user.roles:
        #     return True
        return False

    def actualizar_perfil(self, current_user: User, target_user_id: UUID) -> bool:
        return self.ver_perfil(current_user, target_user_id)
