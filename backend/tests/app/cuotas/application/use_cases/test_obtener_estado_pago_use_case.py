import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import date, datetime
from decimal import Decimal

from src.app.cuotas.domain.entities import TemporadaCuota, Cuota, TipoCuota
from src.app.cuotas.domain.value_objects import EstadoPago
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.application.dtos import EstadoPagoDTO
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy


def test_use_case_file_exists():
    try:
        from src.app.cuotas.application.use_cases import obtener_estado_pago_use_case
    except ImportError:
        pytest.fail("El fichero del caso de uso 'obtener_estado_pago_use_case.py' no existe.")

def test_use_case_class_exists():
    try:
        from src.app.cuotas.application.use_cases.obtener_estado_pago_use_case import ObtenerEstadoPagoUseCase
    except ImportError:
        pytest.fail("La clase del caso de uso 'ObtenerEstadoPagoUseCase' no existe.")

@pytest.mark.asyncio
async def test_use_case_initialization():
    mock_temporada_repo = AsyncMock()
    mock_cuota_repo = AsyncMock()
    mock_tipo_cuota_repo = AsyncMock()
    mock_policy = Mock(spec=CuotaPolicy)
    try:
        from src.app.cuotas.application.use_cases.obtener_estado_pago_use_case import ObtenerEstadoPagoUseCase
        ObtenerEstadoPagoUseCase(mock_temporada_repo, mock_cuota_repo, mock_tipo_cuota_repo, mock_policy)
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'ObtenerEstadoPagoUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    from src.app.cuotas.application.use_cases.obtener_estado_pago_use_case import ObtenerEstadoPagoUseCase
    mock_temporada_repo = AsyncMock()
    mock_cuota_repo = AsyncMock()
    mock_tipo_cuota_repo = AsyncMock()
    mock_policy = Mock(spec=CuotaPolicy)
    use_case = ObtenerEstadoPagoUseCase(mock_temporada_repo, mock_cuota_repo, mock_tipo_cuota_repo, mock_policy)
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_obtener_estado_pago_cuota_existente_completada():
    from src.app.cuotas.application.use_cases.obtener_estado_pago_use_case import ObtenerEstadoPagoUseCase
    mock_temporada_repo = AsyncMock()
    mock_cuota_repo = AsyncMock()
    mock_tipo_cuota_repo = AsyncMock()
    mock_policy = Mock(spec=CuotaPolicy)

    user = User(id=uuid4(), rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    temporada_activa = TemporadaCuota(id=1, nombre_temporada="2025-2026", fecha_inicio=date(2025, 9, 1), fecha_fin=date(2026, 6, 30), fecha_creacion=datetime.now())
    cuota_existente = Cuota(id=uuid4(), usuario_id=user.id, tipo_de_cuota_id=1, importe_pagado=50, estado_pago=EstadoPago.COMPLETADO, fecha_creacion=datetime.now())

    mock_policy.puede_ver_estado_pago.return_value = True
    mock_temporada_repo.get_temporada_activa.return_value = temporada_activa
    mock_cuota_repo.buscar_por_usuario_y_temporada.return_value = cuota_existente

    use_case = ObtenerEstadoPagoUseCase(mock_temporada_repo, mock_cuota_repo, mock_tipo_cuota_repo, mock_policy)
    result = await use_case.execute(user)

    assert isinstance(result, EstadoPagoDTO)
    assert result.estado == EstadoPago.COMPLETADO
    assert result.cuota is not None
    assert result.cuota.id == cuota_existente.id

@pytest.mark.asyncio
async def test_obtener_estado_pago_cuota_existente_pendiente():
    from src.app.cuotas.application.use_cases.obtener_estado_pago_use_case import ObtenerEstadoPagoUseCase
    mock_temporada_repo = AsyncMock()
    mock_cuota_repo = AsyncMock()
    mock_tipo_cuota_repo = AsyncMock()
    mock_policy = Mock(spec=CuotaPolicy)

    user = User(id=uuid4(), rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    temporada_activa = TemporadaCuota(id=1, nombre_temporada="2025-2026", fecha_inicio=date(2025, 9, 1), fecha_fin=date(2026, 6, 30), fecha_creacion=datetime.now())
    cuota_existente = Cuota(id=uuid4(), usuario_id=user.id, tipo_de_cuota_id=1, importe_pagado=0, estado_pago=EstadoPago.PENDIENTE, fecha_creacion=datetime.now())

    mock_policy.puede_ver_estado_pago.return_value = True
    mock_temporada_repo.get_temporada_activa.return_value = temporada_activa
    mock_cuota_repo.buscar_por_usuario_y_temporada.return_value = cuota_existente

    use_case = ObtenerEstadoPagoUseCase(mock_temporada_repo, mock_cuota_repo, mock_tipo_cuota_repo, mock_policy)
    result = await use_case.execute(user)

    assert isinstance(result, EstadoPagoDTO)
    assert result.estado == EstadoPago.PENDIENTE
    assert result.cuota is not None
    assert result.cuota.id == cuota_existente.id

@pytest.mark.asyncio
async def test_obtener_estado_pago_sin_cuota_socio_antiguo():
    from src.app.cuotas.application.use_cases.obtener_estado_pago_use_case import ObtenerEstadoPagoUseCase
    mock_temporada_repo = AsyncMock()
    mock_cuota_repo = AsyncMock()
    mock_tipo_cuota_repo = AsyncMock()
    mock_policy = Mock(spec=CuotaPolicy)

    user = User(id=uuid4(), rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    temporada_activa = TemporadaCuota(id=1, nombre_temporada="2025-2026", fecha_inicio=date(2025, 9, 1), fecha_fin=date(2026, 6, 30), fecha_creacion=datetime.now())
    tipo_cuota_general = TipoCuota(id=1, temporada_id=1, nombre="General", importe=Decimal("50.00"), fecha_creacion=datetime.now())

    mock_policy.puede_ver_estado_pago.return_value = True
    mock_temporada_repo.get_temporada_activa.return_value = temporada_activa
    mock_cuota_repo.buscar_por_usuario_y_temporada.return_value = None
    mock_cuota_repo.ha_pagado_cuota_alta_antes.return_value = True
    mock_tipo_cuota_repo.get_tipo_cuota_general.return_value = tipo_cuota_general

    use_case = ObtenerEstadoPagoUseCase(mock_temporada_repo, mock_cuota_repo, mock_tipo_cuota_repo, mock_policy)
    result = await use_case.execute(user)

    assert isinstance(result, EstadoPagoDTO)
    assert result.estado == EstadoPago.PENDIENTE
    assert result.cuota is not None
    assert result.cuota.tipo_de_cuota_id == tipo_cuota_general.id
    assert result.cuota.importe_pagado == tipo_cuota_general.importe

@pytest.mark.asyncio
async def test_obtener_estado_pago_sin_cuota_socio_nuevo():
    from src.app.cuotas.application.use_cases.obtener_estado_pago_use_case import ObtenerEstadoPagoUseCase
    mock_temporada_repo = AsyncMock()
    mock_cuota_repo = AsyncMock()
    mock_tipo_cuota_repo = AsyncMock()
    mock_policy = Mock(spec=CuotaPolicy)

    user = User(id=uuid4(), rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    temporada_activa = TemporadaCuota(id=1, nombre_temporada="2025-2026", fecha_inicio=date(2025, 9, 1), fecha_fin=date(2026, 6, 30), fecha_creacion=datetime.now())
    tipo_cuota_nuevo = TipoCuota(id=2, temporada_id=1, nombre="Nuevo Socio", importe=Decimal("70.00"), fecha_creacion=datetime.now())

    mock_policy.puede_ver_estado_pago.return_value = True
    mock_temporada_repo.get_temporada_activa.return_value = temporada_activa
    mock_cuota_repo.buscar_por_usuario_y_temporada.return_value = None
    mock_cuota_repo.ha_pagado_cuota_alta_antes.return_value = False
    mock_tipo_cuota_repo.get_tipo_cuota_nuevo_socio.return_value = tipo_cuota_nuevo

    use_case = ObtenerEstadoPagoUseCase(mock_temporada_repo, mock_cuota_repo, mock_tipo_cuota_repo, mock_policy)
    result = await use_case.execute(user)

    assert isinstance(result, EstadoPagoDTO)
    assert result.estado == EstadoPago.PENDIENTE
    assert result.cuota is not None
    assert result.cuota.tipo_de_cuota_id == tipo_cuota_nuevo.id
    assert result.cuota.importe_pagado == tipo_cuota_nuevo.importe
