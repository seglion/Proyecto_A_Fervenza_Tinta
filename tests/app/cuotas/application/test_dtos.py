import pytest
from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from src.app.cuotas.domain.value_objects import EstadoPago, MetodoPago
from src.app.users.application.dtos import UsuarioResponseDTO
from src.app.users.domain.value_objects import Rol

def test_dtos_file_exists():
    """
    Tests if the dtos file exists.
    """
    try:
        from src.app.cuotas.application import dtos
    except ImportError:
        pytest.fail("DTOs file does not exist: src/app/cuotas/application/dtos.py")

def test_tipo_cuota_dto():
    from src.app.cuotas.application.dtos import TipoCuotaDTO
    assert issubclass(TipoCuotaDTO, BaseModel)
    fields = TipoCuotaDTO.__annotations__
    assert fields['nombre'] == str
    assert fields['importe'] == Decimal

def test_crear_temporada_dto():
    from src.app.cuotas.application.dtos import CrearTemporadaDTO, TipoCuotaDTO
    assert issubclass(CrearTemporadaDTO, BaseModel)
    fields = CrearTemporadaDTO.__annotations__
    assert fields['nombre_temporada'] == str
    assert fields['fecha_inicio'] == date
    assert fields['fecha_fin'] == date
    assert fields['tipos_cuota'] == List[TipoCuotaDTO]

def test_temporada_creada_dto():
    from src.app.cuotas.application.dtos import TemporadaCreadaDTO
    assert issubclass(TemporadaCreadaDTO, BaseModel)
    fields = TemporadaCreadaDTO.__annotations__
    assert fields['id'] == int

def test_temporada_dto():
    from src.app.cuotas.application.dtos import TemporadaDTO, TipoCuotaDTO
    assert issubclass(TemporadaDTO, BaseModel)
    fields = TemporadaDTO.__annotations__
    assert fields['id'] == int
    assert fields['nombre_temporada'] == str
    assert fields['fecha_inicio'] == date
    assert fields['fecha_fin'] == date
    assert fields['tipos_cuota'] == List[TipoCuotaDTO]

def test_lista_temporadas_dto():
    from src.app.cuotas.application.dtos import ListaTemporadasDTO, TemporadaDTO
    assert issubclass(ListaTemporadasDTO, BaseModel)
    fields = ListaTemporadasDTO.__annotations__
    assert fields['temporadas'] == List[TemporadaDTO]

def test_actualizar_temporada_dto():
    from src.app.cuotas.application.dtos import ActualizarTemporadaDTO, TipoCuotaDTO
    assert issubclass(ActualizarTemporadaDTO, BaseModel)
    fields = ActualizarTemporadaDTO.__annotations__
    assert fields['nombre_temporada'] == Optional[str]
    assert fields['fecha_inicio'] == Optional[date]
    assert fields['fecha_fin'] == Optional[date]
    assert fields['tipos_cuota'] == Optional[List[TipoCuotaDTO]]

def test_cuota_dto():
    from src.app.cuotas.application.dtos import CuotaDTO
    assert issubclass(CuotaDTO, BaseModel)
    fields = CuotaDTO.__annotations__
    assert fields['id'] == UUID
    assert fields['usuario_id'] == UUID
    assert fields['tipo_de_cuota_id'] == int
    assert fields['importe_pagado'] == Decimal
    assert fields['estado_pago'] == EstadoPago
    assert fields['fecha_pago'] == Optional[datetime]
    assert fields['metodo_pago'] == Optional[MetodoPago]
    assert fields['id_transaccion_externa'] == Optional[str]
    assert fields['notas_admin'] == Optional[str]

def test_lista_cuotas_dto():
    from src.app.cuotas.application.dtos import ListaCuotasDTO, CuotaDTO
    assert issubclass(ListaCuotasDTO, BaseModel)
    fields = ListaCuotasDTO.__annotations__
    assert fields['cuotas'] == List[CuotaDTO]

def test_estado_pago_dto():
    from src.app.cuotas.application.dtos import EstadoPagoDTO, CuotaDTO
    assert issubclass(EstadoPagoDTO, BaseModel)
    fields = EstadoPagoDTO.__annotations__
    assert fields['estado'] == EstadoPago
    assert fields['cuota'] == Optional[CuotaDTO]

def test_intento_pago_dto():
    from src.app.cuotas.application.dtos import IntentoPagoDTO
    assert issubclass(IntentoPagoDTO, BaseModel)
    fields = IntentoPagoDTO.__annotations__
    assert fields['url_pago'] == str

def test_historial_cuotas_dto():
    from src.app.cuotas.application.dtos import HistorialCuotasDTO, CuotaDTO
    assert issubclass(HistorialCuotasDTO, BaseModel)
    fields = HistorialCuotasDTO.__annotations__
    assert fields['historial'] == List[CuotaDTO]

def test_detalle_cuota_dto():
    from src.app.cuotas.application.dtos import DetalleCuotaDTO, CuotaDTO, TemporadaDTO
    assert issubclass(DetalleCuotaDTO, BaseModel)
    fields = DetalleCuotaDTO.__annotations__
    assert fields['cuota'] == CuotaDTO
    assert fields['temporada'] == TemporadaDTO

def test_registrar_cuota_manual_dto():
    from src.app.cuotas.application.dtos import RegistrarCuotaManualDTO
    assert issubclass(RegistrarCuotaManualDTO, BaseModel)
    fields = RegistrarCuotaManualDTO.__annotations__
    assert fields['usuario_id'] == UUID
    assert fields['tipo_cuota_id'] == int
    assert fields['importe'] == Decimal
    assert fields['metodo'] == MetodoPago
    assert fields['notas'] == Optional[str]

def test_informe_pendientes_dto():
    from src.app.cuotas.application.dtos import InformePendientesDTO
    assert issubclass(InformePendientesDTO, BaseModel)
    fields = InformePendientesDTO.__annotations__
    assert fields['pendientes'] == List[UsuarioResponseDTO]

def test_usuario_policy_dto():
    from src.app.cuotas.application.dtos import UsuarioPolicyDTO
    assert issubclass(UsuarioPolicyDTO, BaseModel)
    fields = UsuarioPolicyDTO.__annotations__
    assert fields['rol'] == Rol
    assert fields['esta_activo'] == bool