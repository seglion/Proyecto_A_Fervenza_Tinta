import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import datetime

from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import EstadoPago
from src.app.cuotas.application.dtos import HistorialCuotasDTO, CuotaDTO


def test_use_case_file_exists():
    try:
        from src.app.cuotas.application.use_cases import consultar_historial_cuotas_use_case
    except ImportError:
        pytest.fail("El fichero del caso de uso 'consultar_historial_cuotas_use_case.py' no existe.")

def test_use_case_class_exists():
    try:
        from src.app.cuotas.application.use_cases.consultar_historial_cuotas_use_case import ConsultarHistorialCuotasUseCase
    except ImportError:
        pytest.fail("La clase del caso de uso 'ConsultarHistorialCuotasUseCase' no existe.")

@pytest.mark.asyncio
async def test_use_case_initialization():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    try:
        from src.app.cuotas.application.use_cases.consultar_historial_cuotas_use_case import ConsultarHistorialCuotasUseCase
        ConsultarHistorialCuotasUseCase(
            mock_cuota_repo,
            mock_policy
        )
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'ConsultarHistorialCuotasUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    from src.app.cuotas.application.use_cases.consultar_historial_cuotas_use_case import ConsultarHistorialCuotasUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    use_case = ConsultarHistorialCuotasUseCase(
        mock_cuota_repo,
        mock_policy
    )
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_consultar_historial_cuotas_success():
    from src.app.cuotas.application.use_cases.consultar_historial_cuotas_use_case import ConsultarHistorialCuotasUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)

    user = User(id=uuid4(), rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    cuotas_completadas = [
        Cuota(id=uuid4(), usuario_id=user.id, tipo_de_cuota_id=1, importe_pagado=50, estado_pago=EstadoPago.COMPLETADO, fecha_creacion=datetime.now()),
        Cuota(id=uuid4(), usuario_id=user.id, tipo_de_cuota_id=2, importe_pagado=50, estado_pago=EstadoPago.COMPLETADO, fecha_creacion=datetime.now())
    ]

    mock_policy.puede_consultar_historial.return_value = True
    mock_cuota_repo.buscar_por_usuario_id_completadas.return_value = cuotas_completadas

    use_case = ConsultarHistorialCuotasUseCase(mock_cuota_repo, mock_policy)
    result = await use_case.execute(user)

    assert isinstance(result, HistorialCuotasDTO)
    assert len(result.historial) == 2
    assert isinstance(result.historial[0], CuotaDTO)
