import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import datetime, date

from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.domain.entities import Cuota, TemporadaCuota
from src.app.cuotas.domain.value_objects import EstadoPago
from src.app.cuotas.application.dtos import DetalleCuotaDTO, CuotaDTO, TemporadaDTO


def test_use_case_file_exists():
    try:
        from src.app.cuotas.application.use_cases import ver_detalle_cuota_use_case
    except ImportError:
        pytest.fail("El fichero del caso de uso 'ver_detalle_cuota_use_case.py' no existe.")

def test_use_case_class_exists():
    try:
        from src.app.cuotas.application.use_cases.ver_detalle_cuota_use_case import VerDetalleCuotaUseCase
    except ImportError:
        pytest.fail("La clase del caso de uso 'VerDetalleCuotaUseCase' no existe.")

@pytest.mark.asyncio
async def test_use_case_initialization():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    try:
        from src.app.cuotas.application.use_cases.ver_detalle_cuota_use_case import VerDetalleCuotaUseCase
        VerDetalleCuotaUseCase(
            mock_cuota_repo,
            mock_policy
        )
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'VerDetalleCuotaUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    from src.app.cuotas.application.use_cases.ver_detalle_cuota_use_case import VerDetalleCuotaUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    use_case = VerDetalleCuotaUseCase(
        mock_cuota_repo,
        mock_policy
    )
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_ver_detalle_cuota_success():
    from src.app.cuotas.application.use_cases.ver_detalle_cuota_use_case import VerDetalleCuotaUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)

    admin_user = User(id=uuid4(), rol=Rol.ADMIN, email="admin@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    cuota_id = uuid4()
    cuota_con_detalle = Cuota(id=cuota_id, usuario_id=uuid4(), tipo_de_cuota_id=1, importe_pagado=50, estado_pago=EstadoPago.COMPLETADO, fecha_creacion=datetime.now())
    cuota_con_detalle.temporada = TemporadaCuota(id=1, nombre_temporada="2025-2026", fecha_inicio=date.today(), fecha_fin=date.today(), fecha_creacion=datetime.now())

    mock_policy.es_administrador.return_value = True
    mock_cuota_repo.buscar_por_id_con_detalle.return_value = cuota_con_detalle

    use_case = VerDetalleCuotaUseCase(mock_cuota_repo, mock_policy)
    result = await use_case.execute(admin_user, cuota_id)

    assert isinstance(result, DetalleCuotaDTO)
    assert isinstance(result.cuota, CuotaDTO)
    assert isinstance(result.temporada, TemporadaDTO)
    assert result.cuota.id == cuota_id
