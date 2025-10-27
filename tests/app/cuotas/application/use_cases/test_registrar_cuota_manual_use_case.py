import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from decimal import Decimal

from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.domain.entities import Cuota
from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago
from src.app.cuotas.application.dtos import RegistrarCuotaManualDTO, CuotaDTO


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
            mock_cuota_repo,
            mock_policy
        )
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'RegistrarCuotaManualUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    from src.app.cuotas.application.use_cases.registrar_cuota_manual_use_case import RegistrarCuotaManualUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)
    use_case = RegistrarCuotaManualUseCase(
        mock_cuota_repo,
        mock_policy
    )
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_registrar_cuota_manual_success():
    from src.app.cuotas.application.use_cases.registrar_cuota_manual_use_case import RegistrarCuotaManualUseCase
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_policy = Mock(spec=CuotaPolicy)

    admin_user = User(id=uuid4(), rol=Rol.ADMIN, email="admin@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    dto = RegistrarCuotaManualDTO(usuario_id=uuid4(), tipo_cuota_id=1, importe=Decimal("50.00"), metodo=MetodoPago.EFECTIVO, notas="Pago en efectivo")
    
    mock_policy.es_administrador.return_value = True
    mock_cuota_repo.guardar.return_value = Cuota(id=uuid4(), usuario_id=dto.usuario_id, tipo_de_cuota_id=dto.tipo_cuota_id, importe_pagado=dto.importe, estado_pago=EstadoPago.COMPLETADO, metodo_pago=dto.metodo, notas_admin=dto.notas)

    use_case = RegistrarCuotaManualUseCase(mock_cuota_repo, mock_policy)
    result = await use_case.execute(admin_user, dto)

    assert isinstance(result, CuotaDTO)
    assert result.usuario_id == dto.usuario_id
    assert result.estado_pago == EstadoPago.COMPLETADO
