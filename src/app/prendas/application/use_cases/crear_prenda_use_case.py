from datetime import datetime
from uuid import uuid4

from src.app.prendas.application.dtos import CrearPrendaDTO, PrendaCreadaDTO, UsuarioPolicyDTO
from src.app.prendas.application.policies.prenda_policy import PrendaPolicy
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.prendas.domain.entities import Prenda
from src.app.users.domain.entities import User # Añadido
from src.app.prendas.application.exceptions import NotAuthorizedError


class CrearPrendaUseCase:
    def __init__(self, prenda_repository: IPrendaRepository, prenda_policy: PrendaPolicy):
        self.prenda_repository = prenda_repository
        self.prenda_policy = prenda_policy

    async def execute(self, data: CrearPrendaDTO, current_user: User) -> PrendaCreadaDTO:
        user_policy_dto = UsuarioPolicyDTO(rol=current_user.rol.value, esta_activo=current_user.esta_activo)
        if not self.prenda_policy.es_administrador(user_policy_dto):
            raise NotAuthorizedError("No tienes permiso para crear una prenda.")

        prenda = Prenda(
            id=uuid4(),
            nombre=data.nombre,
            descripcion=data.descripcion,
            precio=data.precio,
            imagen_url=data.imagen_url,
            fecha_creacion=datetime.now()
        )

        prenda_creada = await self.prenda_repository.guardar(prenda)
        return PrendaCreadaDTO(id=prenda_creada.id)