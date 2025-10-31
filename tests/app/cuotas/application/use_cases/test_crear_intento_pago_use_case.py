import pytest
from unittest.mock import AsyncMock, Mock
from uuid import uuid4
from datetime import datetime
from decimal import Decimal

from src.app.cuotas.application.use_cases.obtener_generar_mi_cuota_use_case import ObtenerGenerarMiCuotaUseCase
from src.app.cuotas.application.repositories.i_cuota_repository import ICuotaRepository
from src.app.cuotas.application.policies.cuota_policy import CuotaPolicy
from src.app.core.services.i_payment_gateway import IPaymentGateway
from src.app.users.domain.entities import User
from src.app.users.domain.value_objects import Rol
from src.app.cuotas.domain.value_objects import EstadoPago
from src.app.cuotas.application.dtos import CuotaDTO, IntentoPagoDTO


def test_use_case_file_exists():
    try:
        from src.app.cuotas.application.use_cases import crear_intento_pago_use_case
    except ImportError:
        pytest.fail("El fichero del caso de uso 'crear_intento_pago_use_case.py' no existe.")

def test_use_case_class_exists():
    try:
        from src.app.cuotas.application.use_cases.crear_intento_pago_use_case import CrearIntentoPagoUseCase
    except ImportError:
        pytest.fail("La clase del caso de uso 'CrearIntentoPagoUseCase' no existe.")

@pytest.mark.asyncio
async def test_use_case_initialization():
    mock_obtener_generar_mi_cuota_uc = Mock(spec=ObtenerGenerarMiCuotaUseCase)
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_payment_gateway = AsyncMock(spec=IPaymentGateway)
    mock_policy = Mock(spec=CuotaPolicy)
    try:
        from src.app.cuotas.application.use_cases.crear_intento_pago_use_case import CrearIntentoPagoUseCase
        CrearIntentoPagoUseCase(
            mock_obtener_generar_mi_cuota_uc,
            mock_cuota_repo,
            mock_payment_gateway,
            mock_policy
        )
    except (ImportError, TypeError) as e:
        pytest.fail(f"La inicialización de 'CrearIntentoPagoUseCase' falló: {e}")

@pytest.mark.asyncio
async def test_execute_method_exists():
    from src.app.cuotas.application.use_cases.crear_intento_pago_use_case import CrearIntentoPagoUseCase
    mock_obtener_generar_mi_cuota_uc = Mock(spec=ObtenerGenerarMiCuotaUseCase)
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_payment_gateway = AsyncMock(spec=IPaymentGateway)
    mock_policy = Mock(spec=CuotaPolicy)
    use_case = CrearIntentoPagoUseCase(
        mock_obtener_generar_mi_cuota_uc,
        mock_cuota_repo,
        mock_payment_gateway,
        mock_policy
    )
    assert hasattr(use_case, 'execute'), "El método 'execute' no existe en el caso de uso."

@pytest.mark.asyncio
async def test_crear_intento_pago_success():
    from src.app.cuotas.application.use_cases.crear_intento_pago_use_case import CrearIntentoPagoUseCase
    mock_obtener_generar_mi_cuota_uc = AsyncMock(spec=ObtenerGenerarMiCuotaUseCase)
    mock_cuota_repo = AsyncMock(spec=ICuotaRepository)
    mock_payment_gateway = AsyncMock(spec=IPaymentGateway)
    mock_policy = Mock(spec=CuotaPolicy)

    user = User(id=uuid4(), rol=Rol.USUARIO, email="user@example.com", contrasena_hasheada="", nombre="", apellidos="", numero_telefono="", esta_activo=True)
    cuota_a_pagar = CuotaDTO(id=uuid4(), usuario_id=user.id, tipo_de_cuota_id=1, importe_pagado=Decimal("50.00"), estado_pago=EstadoPago.PENDIENTE)
    payment_url = "https://stripe.com/pay/some_session_id"

    mock_policy.puede_crear_intento_pago.return_value = True
    mock_obtener_generar_mi_cuota_uc.execute.return_value = cuota_a_pagar
    mock_payment_gateway.crear_sesion_pago.return_value = payment_url

    use_case = CrearIntentoPagoUseCase(
        mock_obtener_generar_mi_cuota_uc,
        mock_cuota_repo,
        mock_payment_gateway,
        mock_policy
    )
    result = await use_case.execute(user)

    assert isinstance(result, IntentoPagoDTO)
    assert result.url_pago == payment_url
