import pytest
from unittest.mock import AsyncMock
from datetime import date, datetime

from src.app.pedidos.application.use_cases.cerrar_pedidos_borrador_use_case import CerrarPedidosBorradorUseCase
from src.app.pedidos.application.repositories.i_pedido_repository import IPedidoRepository
from src.app.pedidos.application.repositories.i_temporada_pedido_repository import ITemporadaPedidoRepository
from src.app.pedidos.domain.entities import TemporadaPedido

@pytest.fixture
def mock_pedido_repository():
    return AsyncMock(spec=IPedidoRepository)

@pytest.fixture
def mock_temporada_pedido_repository():
    return AsyncMock(spec=ITemporadaPedidoRepository)

@pytest.fixture
def temporadas_finalizadas():
    return [
        TemporadaPedido(
            id=1,
            nombre_temporada="2024-2025",
            fecha_inicio=date(2024, 8, 16),
            fecha_fin=date(2025, 5, 31),
            esta_activa=False,
            fecha_creacion=datetime.now()
        )
    ]

@pytest.mark.asyncio
async def test_cerrar_pedidos_borrador(mock_pedido_repository, mock_temporada_pedido_repository, temporadas_finalizadas):
    # Arrange
    mock_temporada_pedido_repository.get_temporadas_finalizadas_pendientes_cierre.return_value = temporadas_finalizadas

    use_case = CerrarPedidosBorradorUseCase(mock_pedido_repository, mock_temporada_pedido_repository)

    # Act
    await use_case.execute()

    # Assert
    mock_pedido_repository.cancelar_pedidos_borrador.assert_called_once_with(temporadas_finalizadas[0].id)
    mock_temporada_pedido_repository.marcar_temporadas_como_cerradas.assert_called_once_with([temporadas_finalizadas[0].id])

@pytest.mark.asyncio
async def test_cerrar_pedidos_borrador_no_temporadas(mock_pedido_repository, mock_temporada_pedido_repository):
    # Arrange
    mock_temporada_pedido_repository.get_temporadas_finalizadas_pendientes_cierre.return_value = []

    use_case = CerrarPedidosBorradorUseCase(mock_pedido_repository, mock_temporada_pedido_repository)

    # Act
    await use_case.execute()

    # Assert
    mock_pedido_repository.cancelar_pedidos_borrador.assert_not_called()
    mock_temporada_pedido_repository.marcar_temporadas_como_cerradas.assert_not_called()