

from src.app.pedidos.application.dtos import PedidoDTO, CrearLineaDePedidoDTO
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.prendas.application.repositories.i_variante_prenda_repository import IVariantePrendaRepository
from src.app.prendas.application.repositories.i_prenda_repository import IPrendaRepository
from src.app.pedidos.application.exceptions import TemporadaPedidoNoActivaException, VariantePrendaNoEncontradaException, PedidoNoEncontradoException
from src.app.users.domain.entities import User


class AnadirPrendaPedidoUseCase:
    def __init__(
        self,
        pedido_repository: IPedidoRepository,
        temporada_pedido_repository: ITemporadaPedidoRepository,
        variante_prenda_repository: IVariantePrendaRepository,
        prenda_repository: IPrendaRepository,
    ):
        self.pedido_repository = pedido_repository
        self.temporada_pedido_repository = temporada_pedido_repository
        self.variante_prenda_repository = variante_prenda_repository
        self.prenda_repository = prenda_repository

    async def execute(self, current_user: User, datos_linea: CrearLineaDePedidoDTO) -> PedidoDTO:

        temporada_activa = await self.temporada_pedido_repository.get_temporada_activa()
        if not temporada_activa or not temporada_activa.esta_activa:
            raise TemporadaPedidoNoActivaException("No hay temporada de pedidos activa o está cerrada.")


        pedido_borrador = await self.pedido_repository.obtener_o_crear_borrador(
            current_user.id,
            temporada_activa.id
        )


        variante = await self.variante_prenda_repository.buscar_por_id(datos_linea.variante_prenda_id)
        if not variante:
            raise VariantePrendaNoEncontradaException("Variante de prenda no encontrada.")

        prenda = await self.prenda_repository.buscar_por_id_con_variantes(variante.prenda_id) 
        if not prenda:
            raise PedidoNoEncontradoException("Prenda no encontrada.") 


        if datos_linea.cantidad <= 0:
            # Si la cantidad es 0 o menos, se elimina la línea si existe
            linea_a_eliminar = next((linea for linea in pedido_borrador.lineas if linea.variante_prenda_id == datos_linea.variante_prenda_id), None)
            if linea_a_eliminar:
                pedido_actualizado = await self.pedido_repository.eliminar_linea_y_recalcular(
                    pedido_borrador,
                    linea_a_eliminar.id
                )
            else:
                pedido_actualizado = pedido_borrador # No hay nada que eliminar
        else:
            pedido_actualizado = await self.pedido_repository.anadir_o_actualizar_linea(
                pedido_borrador,
                variante,
                prenda,
                datos_linea.cantidad
            )

        # 5. Guardar el pedido actualizado (el repositorio ya recalcula el total)
        pedido_final = await self.pedido_repository.guardar_pedido(pedido_actualizado)

        return PedidoDTO.model_validate(pedido_final)
