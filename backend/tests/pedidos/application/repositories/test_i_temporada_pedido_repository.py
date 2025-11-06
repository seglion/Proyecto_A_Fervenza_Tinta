import pytest
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional, List

from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.domain.entities import TemporadaPedido


# Test para verificar la existencia del archivo i_temporada_pedido_repository.py
def test_i_temporada_pedido_repository_file_exists():
    path = Path("src/app/pedidos/application/repositories/i_temporada_pedido_repository.py")
    assert path.exists(), f"El archivo {path} no existe."

# Test para verificar que ITemporadaPedidoRepository es una clase abstracta
def test_i_temporada_pedido_repository_is_abstract():
    assert issubclass(ITemporadaPedidoRepository, ABC)

# Test para verificar los métodos abstractos de ITemporadaPedidoRepository
def test_i_temporada_pedido_repository_abstract_methods():
    expected_methods = [
        "get_temporada_activa",
        "guardar",
        "marcar_temporadas_como_cerradas",
        "get_temporadas_finalizadas_pendientes_cierre",
    ]
    for method_name in expected_methods:
        assert hasattr(ITemporadaPedidoRepository, method_name), f"El método {method_name} no existe en ITemporadaPedidoRepository."
        assert getattr(ITemporadaPedidoRepository, method_name).__isabstractmethod__, f"El método {method_name} no es abstracto."
