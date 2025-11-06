import pytest
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.domain.entities import Pedido, TemporadaPedido, LineaDePedido
from src.app.prendas.domain.entities import Prenda, VariantePrenda


# Test para verificar la existencia del archivo i_pedido_repository.py
def test_i_pedido_repository_file_exists():
    path = Path("src/app/pedidos/application/repositories/i_pedido_repository.py")
    assert path.exists(), f"El archivo {path} no existe."

# Test para verificar que IPedidoRepository es una clase abstracta
def test_i_pedido_repository_is_abstract():
    assert issubclass(IPedidoRepository, ABC)

# Test para verificar los métodos abstractos de IPedidoRepository
def test_i_pedido_repository_abstract_methods():
    expected_methods = [
        "buscar_borrador_por_usuario_y_temporada",
        "obtener_o_crear_borrador",
        "anadir_o_actualizar_linea",
        "guardar_pedido",
        "buscar_borrador_por_usuario",
        "buscar_historial_por_usuario",
        "buscar_pedidos_finalizados_por_temporada",
        "buscar_por_id_con_detalle",
        "buscar_por_id",
        "cancelar_pedidos_borrador",
        "eliminar_linea_y_recalcular",
    ]
    for method_name in expected_methods:
        assert hasattr(IPedidoRepository, method_name), f"El método {method_name} no existe en IPedidoRepository."
        assert getattr(IPedidoRepository, method_name).__isabstractmethod__, f"El método {method_name} no es abstracto."
