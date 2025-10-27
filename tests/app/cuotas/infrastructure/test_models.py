import pytest
from sqlalchemy import String, Date, DateTime, func, Integer, ForeignKey, Numeric, UUID, Enum, Text # Import Text for type checking
from src.app.cuotas.infrastructure.models import TemporadaCuotaModel, TipoCuotaModel, CuotaModel # Import CuotaModel

# 1. Test para asegurar que el módulo de modelos existe
def test_models_module_exists():
    import src.app.cuotas.infrastructure.models as models_module # Use an alias for the module object
    assert models_module is not None

# 2. Test para asegurar que la clase TemporadaCuotaModel existe
def test_temporada_cuota_model_class_exists():
    assert TemporadaCuotaModel is not None

# 3. Test para verificar que el tablename se genera correctamente
def test_temporada_cuota_model_has_correct_tablename():
    assert TemporadaCuotaModel.__tablename__ == "temporadacuotas"

# 4. Test para verificar que la columna 'id' es la clave primaria
def test_temporada_cuota_model_has_id_primary_key():
    assert 'id' in TemporadaCuotaModel.__table__.c
    assert TemporadaCuotaModel.__table__.c.id.primary_key is True

# 5. Test para verificar las propiedades de la columna 'nombre_temporada'
def test_temporada_cuota_model_has_nombre_temporada_column():
    nombre_temporada_col = TemporadaCuotaModel.__table__.c.nombre_temporada
    assert isinstance(nombre_temporada_col.type, String)
    assert nombre_temporada_col.type.length == 100
    assert nombre_temporada_col.unique is True
    assert nombre_temporada_col.nullable is False

# 6. Test para verificar las propiedades de la columna 'fecha_inicio'
def test_temporada_cuota_model_has_fecha_inicio_column():
    fecha_inicio_col = TemporadaCuotaModel.__table__.c.fecha_inicio
    assert isinstance(fecha_inicio_col.type, Date)
    assert fecha_inicio_col.nullable is False

# 7. Test para verificar las propiedades de la columna 'fecha_fin'
def test_temporada_cuota_model_has_fecha_fin_column():
    fecha_fin_col = TemporadaCuotaModel.__table__.c.fecha_fin
    assert isinstance(fecha_fin_col.type, Date)
    assert fecha_fin_col.nullable is False

# 8. Test para verificar las propiedades de la columna 'fecha_creacion'
def test_temporada_cuota_model_has_fecha_creacion_column():
    fecha_creacion_col = TemporadaCuotaModel.__table__.c.fecha_creacion
    assert isinstance(fecha_creacion_col.type, DateTime)
    assert fecha_creacion_col.nullable is False
    # Check for default value func.now()
    assert str(fecha_creacion_col.default.arg) == "now()"

# 9. Test para asegurar que la clase TipoCuotaModel existe
def test_tipo_cuota_model_class_exists():
    assert TipoCuotaModel is not None

# 10. Test para verificar que el tablename de TipoCuotaModel se genera correctamente
def test_tipo_cuota_model_has_correct_tablename():
    assert TipoCuotaModel.__tablename__ == "tipocuotas"

# 11. Test para verificar las propiedades de la columna 'temporada_id'
def test_tipo_cuota_model_has_temporada_id_column():
    assert 'temporada_id' in TipoCuotaModel.__table__.c
    temporada_id_col = TipoCuotaModel.__table__.c.temporada_id
    assert isinstance(temporada_id_col.type, Integer)
    assert temporada_id_col.nullable is False
    assert len(temporada_id_col.foreign_keys) == 1
    fk = list(temporada_id_col.foreign_keys)[0]
    assert str(fk.column) == 'temporadacuotas.id'

# 12. Test para verificar las propiedades de la columna 'nombre'
def test_tipo_cuota_model_has_nombre_column():
    assert 'nombre' in TipoCuotaModel.__table__.c
    nombre_col = TipoCuotaModel.__table__.c.nombre
    assert isinstance(nombre_col.type, String)
    assert nombre_col.type.length == 100
    assert nombre_col.nullable is False

# 13. Test para verificar las propiedades de la columna 'importe'
def test_tipo_cuota_model_has_importe_column():
    assert 'importe' in TipoCuotaModel.__table__.c
    importe_col = TipoCuotaModel.__table__.c.importe
    assert isinstance(importe_col.type, Numeric)
    assert importe_col.type.precision == 10
    assert importe_col.type.scale == 2
    assert importe_col.nullable is False

# 14. Test para verificar las propiedades de la columna 'fecha_creacion'
def test_tipo_cuota_model_has_fecha_creacion_column():
    assert 'fecha_creacion' in TipoCuotaModel.__table__.c
    fecha_creacion_col = TipoCuotaModel.__table__.c.fecha_creacion
    assert isinstance(fecha_creacion_col.type, DateTime)
    assert fecha_creacion_col.nullable is False
    # Check for default value func.now()
    assert str(fecha_creacion_col.default.arg) == "now()"

# 15. Test para asegurar que la clase CuotaModel existe
def test_cuota_model_class_exists():
    assert CuotaModel is not None

# 16. Test para verificar que el tablename de CuotaModel se genera correctamente
def test_cuota_model_has_correct_tablename():
    assert CuotaModel.__tablename__ == "cuotas"

# 17. Test para verificar las propiedades de la columna 'usuario_id'
def test_cuota_model_has_usuario_id_column():
    assert 'usuario_id' in CuotaModel.__table__.c
    usuario_id_col = CuotaModel.__table__.c.usuario_id
    assert isinstance(usuario_id_col.type, UUID)
    assert usuario_id_col.nullable is False
    assert len(usuario_id_col.foreign_keys) == 1
    fk = list(usuario_id_col.foreign_keys)[0]
    assert str(fk.column) == 'usuarios.id'

# 18. Test para verificar las propiedades de la columna 'tipo_de_cuota_id'
def test_cuota_model_has_tipo_de_cuota_id_column():
    assert 'tipo_de_cuota_id' in CuotaModel.__table__.c
    tipo_de_cuota_id_col = CuotaModel.__table__.c.tipo_de_cuota_id
    assert isinstance(tipo_de_cuota_id_col.type, Integer)
    assert tipo_de_cuota_id_col.nullable is False
    assert len(tipo_de_cuota_id_col.foreign_keys) == 1
    fk = list(tipo_de_cuota_id_col.foreign_keys)[0]
    assert str(fk.column) == 'tipocuotas.id'

# 19. Test para verificar las propiedades de la columna 'importe_pagado'
def test_cuota_model_has_importe_pagado_column():
    assert 'importe_pagado' in CuotaModel.__table__.c
    importe_pagado_col = CuotaModel.__table__.c.importe_pagado
    assert isinstance(importe_pagado_col.type, Numeric)
    assert importe_pagado_col.type.precision == 10
    assert importe_pagado_col.type.scale == 2
    assert importe_pagado_col.nullable is False

# 20. Test para verificar las propiedades de la columna 'estado_pago'
def test_cuota_model_has_estado_pago_column():
    assert 'estado_pago' in CuotaModel.__table__.c
    estado_pago_col = CuotaModel.__table__.c.estado_pago
    assert isinstance(estado_pago_col.type, String)
    assert estado_pago_col.type.length == 50
    assert estado_pago_col.nullable is False

# 21. Test para verificar las propiedades de la columna 'fecha_pago'
def test_cuota_model_has_fecha_pago_column():
    assert 'fecha_pago' in CuotaModel.__table__.c
    fecha_pago_col = CuotaModel.__table__.c.fecha_pago
    assert isinstance(fecha_pago_col.type, DateTime)
    assert fecha_pago_col.nullable is True

# 22. Test para verificar las propiedades de la columna 'metodo_pago'
def test_cuota_model_has_metodo_pago_column():
    assert 'metodo_pago' in CuotaModel.__table__.c
    metodo_pago_col = CuotaModel.__table__.c.metodo_pago
    assert isinstance(metodo_pago_col.type, Enum)
    assert metodo_pago_col.nullable is True

# 23. Test para verificar las propiedades de la columna 'id_transaccion_externa'
def test_cuota_model_has_id_transaccion_externa_column():
    assert 'id_transaccion_externa' in CuotaModel.__table__.c
    id_transaccion_externa_col = CuotaModel.__table__.c.id_transaccion_externa
    assert isinstance(id_transaccion_externa_col.type, String)
    assert id_transaccion_externa_col.type.length == 255
    assert id_transaccion_externa_col.unique is True
    assert id_transaccion_externa_col.nullable is True

# 24. Test para verificar las propiedades de la columna 'notas_admin'
def test_cuota_model_has_notas_admin_column():
    assert 'notas_admin' in CuotaModel.__table__.c
    notas_admin_col = CuotaModel.__table__.c.notas_admin
    assert isinstance(notas_admin_col.type, Text)
    assert notas_admin_col.nullable is True

# 25. Test para verificar las propiedades de la columna 'fecha_creacion'
def test_cuota_model_has_fecha_creacion_column():
    assert 'fecha_creacion' in CuotaModel.__table__.c
    fecha_creacion_col = CuotaModel.__table__.c.fecha_creacion
    assert isinstance(fecha_creacion_col.type, DateTime)
    assert fecha_creacion_col.nullable is False
    # Check for default value func.now()
    assert str(fecha_creacion_col.default.arg) == "now()"



