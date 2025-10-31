import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from decimal import Decimal
from datetime import datetime

from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago
from src.app.cuotas.application.dtos import ActualizarCuotaManualDTO, CuotaCompletadaDTO


def test_use_case_file_exists():
    try:
        from src.app.cuotas.application.use_cases import registrar_cuota_manual_use_case
    except ImportError:
        pytest.fail("El fichero del caso de uso 'registrar_cuota_manual_use_case.py' no existe.")

def test_use_case_class_exists():
    try:
        from src.app.cuotas.application.use_cases.registrar_cuota_manual_use_case import RegistrarCuotaManualUseCase
    except ImportError:
        pytest.fail("La clase del caso de uso 'RegistrarCuotaManualUseCase' no existe.")

@pytest.mark.asyncio
async def test_use_case_initialization():
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    try:
        from src.app.cuotas.application.use_cases.registrar_cuota_manual_use_case import RegistrarCuotaManualUseCase
        RegistrarCuotaManualUseCase(
            cuota_repository=mock_cuota_repo,
            cuota_policy=mock_policy
        )
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'RegistrarCuotaManualUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    from src.app.cuotas.application.use_cases.registrar_cuota_manual_use_case import RegistrarCuotaManualUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    use_case = RegistrarCuotaManualUseCase(
        cuota_repository=mock_cuota_repo,
        cuota_policy=mock_policy
    )
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_registrar_cuota_manual_success():
    from src.app.cuotas.application.use_cases.registrar_cuota_manual_use_case import RegistrarCuotaManualUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)

    admin_user = User(id=uuid4(), rol=Rol.ADMIN, email="admin@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    cuota_id = uuid4()
    dto = ActualizarCuotaManualDTO(importe=Decimal("50.00"), metodo=MetodoPago.EFECTIVO, notas="Pago en efectivo")
    
    cuota_existente = Cuota(
        id=cuota_id, 
        usuario_id=uuid4(), 
        tipo_de_cuota_id=1, 
        importe_pagado=Decimal("0.00"), 
        estado_pago=EstadoPago.PENDIENTE, 
        fecha_creacion=datetime.now()
    )

    mock_policy.es_administrador.return_value = True
    mock_cuota_repo.buscar_por_id.return_value = cuota_existente
    mock_cuota_repo.actualizar.return_value = cuota_existente

    use_case = RegistrarCuotaManualUseCase(mock_cuota_repo, mock_policy)
    result = await use_case.execute(admin_user, cuota_id, dto)

    assert isinstance(result, CuotaCompletadaDTO)
    assert result.id == cuota_id
    mock_cuota_repo.buscar_por_id.assert_called_once_with(cuota_id)
    mock_cuota_repo.actualizar.assert_called_once()
