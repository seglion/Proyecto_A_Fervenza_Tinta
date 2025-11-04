from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.pedidos.domain.entities import Pedido
from uuid import UUID


class PedidoPolicy:
    def es_administrador(self, current_user: User) -> bool:
        return current_user.rol == Rol.ADMIN

    def ver_pedido(self, current_user: User, pedido: Pedido) -> bool:
        if self.es_administrador(current_user):
            return True
        return current_user.id == pedido.usuario_id

    def gestionar_temporadas(self, current_user: User) -> bool:
        return self.es_administrador(current_user)

    def listar_todos_pedidos(self, current_user: User) -> bool:
        return self.es_administrador(current_user)

    def marcar_pagado(self, current_user: User) -> bool:
        return self.es_administrador(current_user)

    def cancelar_pedido(self, current_user: User) -> bool:
        return self.es_administrador(current_user)

    def puede_listar_historial(self, current_user: User) -> bool:
        return current_user.esta_activo
