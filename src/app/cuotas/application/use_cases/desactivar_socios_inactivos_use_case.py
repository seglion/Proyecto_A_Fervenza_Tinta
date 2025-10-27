from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.users.application.repositories.i_user_repository import IUserRepository
from datetime import date

class DesactivarSociosInactivosUseCase:
    def __init__(
        self,
        cuota_repository: ICuotaRepository,
        user_repository: IUserRepository,
    ):
        self.cuota_repository = cuota_repository
        self.user_repository = user_repository

    async def execute(self, fecha_limite: date) -> None:
        usuarios_a_desactivar_ids = await self.cuota_repository.get_usuarios_inactivos_desde(fecha_limite)

        if usuarios_a_desactivar_ids:
            await self.user_repository.desactivar_usuarios(usuarios_a_desactivar_ids)
