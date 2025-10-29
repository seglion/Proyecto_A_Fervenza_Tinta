

# SLICE CUOTAS

## Índice

  - [DIAGRAMA ER](#diagrama-er)
  - [Tablas de la Base de Datos](#tablas-de-la-base-de-datos)
      - [Tabla: temporadas\_cuota](#tabla-temporadas_cuota)
      - [Tabla: tipos\_de\_cuota](#tabla-tipos_de_cuota-nueva)
      - [Tabla: cuotas](#tabla-cuotas-actualizada)
  - [Casos De Uso](#casos-de-uso)
  - [Diagramas de Secuencia](#diagramas-de-secuencia)

-----

## DIAGRAMA ER

-----

```mermaid
erDiagram
    usuarios {
        UUID id PK "Clave Primaria"
        VARCHAR(255) email "Único, No Nulo"
        VARCHAR(255) contrasena_hasheada "No Nulo"
        VARCHAR(100) nombre "Nulo"
        VARCHAR(100) apellidos "Nulo"
        VARCHAR(50) apodo "Único, No Nulo"
        VARCHAR(50) rol "No Nulo (ej: 'admin', 'usuario')"
        VARCHAR(20) numero_telefono "Único, No Nulo"
        VARCHAR(255) url_avatar "Nulo"
        BOOLEAN esta_activo "Default: true"
        BOOLEAN email_verificado "Default: false"
        BOOLEAN aprobado_por_admin "Default: false"
        TIMESTAMPZ fecha_creacion "No Nulo"
        TIMESTAMPZ fecha_actualizacion "No Nulo"
    }

    tokens {
        UUID id PK "Clave Primaria"
        UUID usuario_id FK "Clave Externa a usuarios.id"
        VARCHAR(255) hash_token "Único, No Nulo"
        VARCHAR(50) tipo_token "No Nulo (ej: 'verificacion_email')"
        TIMESTAMPZ fecha_expiracion "No Nulo"
        BOOLEAN es_valido "Default: true"
        TIMESTAMPZ fecha_creacion "No Nulo"
    }

    temporadas_cuota {
        INTEGER id PK "Clave Primaria"
        VARCHAR(100) nombre_temporada "Único, No Nulo (ej: 2025-2026)"
        DATE fecha_inicio "No Nulo (ej: 2025-10-01)"
        DATE fecha_fin "No Nulo (ej: 2026-07-25)"
        TIMESTAMPZ fecha_creacion "No Nulo"
    }

    tipos_de_cuota {
        INTEGER id PK "Clave Primaria"
        INTEGER temporada_id FK "Clave Externa a temporadas_cuota.id"
        VARCHAR(100) nombre "No Nulo (ej: 'Cuota General', 'Cuota Nuevo Socio')"
        NUMERIC(10-2) importe "No Nulo (ej: 25.00, 50.00)"
        TIMESTAMPZ fecha_creacion "No Nulo"
    }

    cuotas {
        UUID id PK "Clave Primaria"
        UUID usuario_id FK "Clave Externa a usuarios.id"
        INTEGER tipo_de_cuota_id FK "Clave Externa a tipos_de_cuota.id"
        NUMERIC(10-2) importe_pagado "No Nulo (puede ser 0 si el admin lo perdona)"
        VARCHAR(50) estado_pago "No Nulo (ej: 'pendiente', 'completado')"
        TIMESTAMPZ fecha_pago "Nulo"
        tipo_metodo_pago metodo_pago "Nulo - ENUM"
        VARCHAR(255) id_transaccion_externa "Nulo, Único"
        TEXT notas_admin "Nulo"
        TIMESTAMPZ fecha_creacion "No Nulo"
    }

    usuarios ||--o{ tokens : "genera"
    
    usuarios ||--|{ cuotas : "paga"
    temporadas_cuota ||--|{ tipos_de_cuota : "define"
    tipos_de_cuota ||--|{ cuotas : "corresponde_a"
```

-----

## Tablas de la Base de Datos

-----

## Tabla: temporadascuotas

| Nombre de Columna | Tipo de Dato | Restricciones / Notas |
| :--- | :--- | :--- |
| **id** | INTEGER | Clave Primaria (Autoincremental) |
| **nombre\_temporada**| VARCHAR(100) | Único, No Nulo. Ej: "Temporada 2025-2026" |
| **fecha\_inicio** | DATE | No Nulo. Ej: '2025-10-01' |
| **fecha\_fin** | DATE | No Nulo. Ej: '2026-07-25' |
| **fecha\_creacion** | TIMESTAMPZ | No Nulo |

## Tabla: tipocuotas 

| Nombre de Columna | Tipo de Dato | Restricciones / Notas |
| :--- | :--- | :--- |
| **id** | INTEGER | Clave Primaria (Autoincremental) |
| **temporada\_id** | INTEGER | Clave Externa a `temporadas_cuota.id` |
| **nombre** | VARCHAR(100) | No Nulo. Ej: "Cuota General", "Cuota Nuevo Socio" |
| **importe** | NUMERIC(10, 2) | No Nulo. Ej: 25.00 |
| **fecha\_creacion** | TIMESTAMPZ | No Nulo |

## Tabla: cuotas 

| Nombre de Columna | Tipo de Dato | Restricciones / Notas |
| :--- | :--- | :--- |
| **id** | UUID | Clave Primaria |
| **usuario\_id** | UUID | Clave Externa a `usuarios.id` |
| **tipo\_de\_cuota\_id**| INTEGER | Clave Externa a `tipos_de_cuota.id` |
| **importe\_pagado** | NUMERIC(10, 2) | No Nulo. El importe real pagado (puede diferir). |
| **estado\_pago** | VARCHAR(50) | No Nulo. Ej: 'pendiente', 'completado', 'fallido' |
| **fecha\_pago** | TIMESTAMPZ | Nulo (se rellena cuando el estado es 'completado') |
| **metodo\_pago** | `tipo_metodo_pago` | Nulo. **ENUM:** ('stripe', 'efectivo', 'transferencia\_manual') |
| **id\_transaccion\_externa**| VARCHAR(255) | Nulo, Único. (Ej: el ID de Stripe) |
| **notas\_admin** | TEXT | Nulo. Para justificar pagos manuales, etc. |
| **fecha\_creacion** | TIMESTAMPZ | No Nulo |

-----

## Casos De Uso

-----

```plantuml
@startuml
!theme materia
' Título del Diagrama
title Diagrama de Casos de Uso - Slice Cuotas
left to right direction

' Definición de Actores
actor "Usuario Registrado" as User
actor Administrador
actor Sistema

' Herencia de Actores
User <|-- Administrador

' Contenedor del Sistema
rectangle "Sistema de Gestión de Cuotas" {
    
    ' --- Casos de Uso del Usuario ---
    usecase UC5 as "5. Obtener mi estado de pago"
    usecase UC6 as "6. Crear intento de pago"
    usecase UC7 as "7. Consultar mi historial de cuotas"

    User -- UC5
    User -- UC6
    User -- UC7

    ' --- Casos de Uso del Administrador ---
    ' (Hereda los casos de Uso del Usuario)
    usecase UC1 as "1. Crear nueva temporada\n(con sus tipos de cuota)"
    usecase UC2 as "2. Listar temporadas"
    usecase UC3 as "3. Actualizar temporada"
    usecase UC4 as "8. Listar todas las cuotas"
    usecase UC8 as "9. Ver detalle de una cuota"
    usecase UC9 as "10. Registrar cuota manual"
    usecase UC10 as "11. Generar informe de pendientes"
    
    Administrador -- UC1
    Administrador -- UC2
    Administrador -- UC3
    Administrador -- UC4
    Administrador -- UC8
    Administrador -- UC9
    Administrador -- UC10

    ' --- Casos de Uso del Sistema ---
    usecase UC11 as "12. Procesar webhook de Stripe"
    usecase UC12 as "13. Desactivar socios inactivos"

    Sistema -- UC11
    Sistema -- UC12
}
@enduml
```



-----

## Diagramas de Secuencia

-----

### CASO DE USO 1: Crear Nueva Temporada

```plantuml
@startuml
!theme materia
title Secuencia: 1. Crear Nueva Temporada (con sus tipos de cuota)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "CrearTemporadaUseCase" as UseCase
participant "ITemporadaCuotaRepository" as TemporadaRepo
participant "ITipoCuotaRepository" as TipoCuotaRepo
participant "Base de Datos (Postgres)" as DB

activate Administrador
Administrador -> API: POST /api/v1/admin/cuotas/temporadas\n(con datos de temporada y tipos de cuota)
activate API

API -> Auth: Validar Access Token y rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(datos_temporada_dto)
activate UseCase

UseCase -> TemporadaRepo: guardar_temporada(datos_temporada)
activate TemporadaRepo
TemporadaRepo -> DB: INSERT INTO temporadas_cuota (...)
DB --> TemporadaRepo: (temporada_creada_con_id)
deactivate DB
Repo --> UseCase: (entidad_temporada)
deactivate TemporadaRepo

UseCase -> UseCase: Asignar ID de temporada a los tipos de cuota
UseCase -> TipoCuotaRepo: guardar_varios(lista_tipos_cuota)
activate TipoCuotaRepo
TipoCuotaRepo -> DB: INSERT INTO tipos_de_cuota (...)
deactivate TipoCuotaRepo

UseCase --> API: TemporadaCreadaDTO
deactivate UseCase

API --> Administrador: 201 Created
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 2: Listar Temporadas

```plantuml
@startuml
!theme materia
title Secuencia: 2. Listar Temporadas

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "ListarTemporadasUseCase" as UseCase
participant "ITemporadaCuotaRepository" as TemporadaRepo

activate Administrador
Administrador -> API: GET /api/v1/admin/cuotas/temporadas
activate API

API -> Auth: Validar Access Token y rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute()
activate UseCase

UseCase -> TemporadaRepo: listar_todas()
activate TemporadaRepo
TemporadaRepo --> UseCase: (lista_entidades_temporada)
deactivate TemporadaRepo

UseCase --> API: ListaTemporadasDTO
deactivate UseCase

API --> Administrador: 200 OK
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 3: Actualizar Temporada

```plantuml
@startuml
!theme materia
title Secuencia: 3. Actualizar Temporada (y sus tipos de cuota)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "ActualizarTemporadaUseCase" as UseCase
participant "ITemporadaCuotaRepository" as TemporadaRepo
participant "ITipoCuotaRepository" as TipoCuotaRepo

activate Administrador
Administrador -> API: PUT /api/v1/admin/cuotas/temporadas/{id}
activate API

API -> Auth: Validar Access Token y rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(temporada_id, datos_actualizar_dto)
activate UseCase

UseCase -> TemporadaRepo: actualizar(temporada_id, datos_temporada)
activate TemporadaRepo
TemporadaRepo --> UseCase: (éxito)
deactivate TemporadaRepo

UseCase -> TipoCuotaRepo: actualizar_varios(datos_tipos_cuota)
activate TipoCuotaRepo
TipoCuotaRepo --> UseCase: (éxito)
deactivate TipoCuotaRepo

UseCase --> API: TemporadaActualizadaDTO
deactivate UseCase

API --> Administrador: 200 OK
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 4: Listar Todas las Cuotas (Admin)

```plantuml
@startuml
!theme materia
title Secuencia: 4. Listar Todas las Cuotas (Admin)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "ListarCuotasUseCase" as UseCase
participant "ICuotaRepository" as CuotaRepo

activate Administrador
Administrador -> API: GET /api/v1/admin/cuotas
activate API

API -> Auth: Validar Access Token y rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(filtros)
activate UseCase

UseCase -> CuotaRepo: listar_todas(filtros)
activate CuotaRepo
CuotaRepo --> UseCase: (lista_entidades_cuota)
deactivate CuotaRepo

UseCase --> API: ListaCuotasDTO
deactivate UseCase

API --> Administrador: 200 OK
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 5: Obtener Mi Estado de Pago

```plantuml
@startuml
!theme materia
title Secuencia: 5. Obtener Mi Estado de Pago

actor "Usuario Registrado" as User
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "ObtenerEstadoPagoUseCase" as UseCase
participant "ITemporadaCuotaRepository" as TemporadaRepo
participant "ICuotaRepository" as CuotaRepo
participant "ITipoCuotaRepository" as TipoCuotaRepo

activate User
User -> API: GET /api/v1/cuotas/mi-estado
activate API

API -> Auth: Validar Access Token
activate Auth
Auth --> API: (éxito, devuelve user_id)
deactivate Auth

API -> UseCase: execute(user_id)
activate UseCase

UseCase -> TemporadaRepo: get_temporada_activa()
activate TemporadaRepo
TemporadaRepo --> UseCase: (entidad_temporada_activa)
deactivate TemporadaRepo

UseCase -> CuotaRepo: buscar_por_usuario_y_temporada(user_id, temporada_activa.id)
activate CuotaRepo
CuotaRepo --> UseCase: (cuota_existente o null)
deactivate CuotaRepo

alt Cuota ya existe (estado 'completado' o 'pendiente')
    UseCase --> API: EstadoPagoDTO (con datos de la cuota)
else Cuota no existe (hay que calcularla)
    UseCase -> CuotaRepo: ha_pagado_cuota_alta_antes(user_id)
    activate CuotaRepo
    CuotaRepo --> UseCase: (true o false)
    deactivate CuotaRepo
    
    alt Es socio antiguo (ha_pagado_alta = true)
        UseCase -> TipoCuotaRepo: get_tipo_cuota_general(temporada_activa.id)
    else Es socio nuevo (ha_pagado_alta = false)
        UseCase -> TipoCuotaRepo: get_tipo_cuota_nuevo_socio(temporada_activa.id)
    end
    
    activate TipoCuotaRepo
    TipoCuotaRepo --> UseCase: (entidad_tipo_cuota)
    deactivate TipoCuotaRepo
    
    UseCase --> API: EstadoPagoDTO (con datos de la cuota a pagar)
end

deactivate UseCase
API --> User: 200 OK (con estado de pago)
deactivate API
deactivate User
@enduml
```

-----

### CASO DE USO 6: Crear Intento de Pago

```plantuml
@startuml
!theme materia
title Secuencia: 6. Crear Intento de Pago (Stripe)

actor "Usuario Registrado" as User
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "CrearIntentoPagoUseCase" as UseCase
participant "ObtenerEstadoPagoUseCase" as GetEstadoUC
participant "ICuotaRepository" as CuotaRepo
participant "IPaymentGateway" as PaymentGateway

activate User
User -> API: POST /api/v1/cuotas/crear-intento-pago
activate API

API -> Auth: Validar Access Token
activate Auth
Auth --> API: (éxito, devuelve user_id)
deactivate Auth

API -> UseCase: execute(user_id)
activate UseCase

' 1. Reutiliza la lógica del UC5 para saber qué cobrar
UseCase -> GetEstadoUC: execute(user_id)
activate GetEstadoUC
GetEstadoUC --> UseCase: (dto_con_cuota_a_pagar)
deactivate GetEstadoUC

' 2. Crea la cuota en estado 'pendiente'
UseCase -> CuotaRepo: guardar(nueva_cuota_pendiente)
activate CuotaRepo
CuotaRepo --> UseCase: (cuota_pendiente_con_id)
deactivate CuotaRepo

' 3. Crea la sesión de pago en Stripe
UseCase -> PaymentGateway: crear_sesion_pago(importe, cuota_pendiente.id)
activate PaymentGateway
PaymentGateway --> UseCase: (url_pago_stripe)
deactivate PaymentGateway

UseCase --> API: IntentoPagoDTO (con url_pago_stripe)
deactivate UseCase

API --> User: 200 OK (con URL de Stripe)
deactivate API
deactivate User
@enduml
```

-----

### CASO DE USO 7: Consultar Mi Historial de Cuotas

```plantuml
@startuml
!theme materia
title Secuencia: 7. Consultar Mi Historial de Cuotas

actor "Usuario Registrado" as User
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "ConsultarHistorialCuotasUseCase" as UseCase
participant "ICuotaRepository" as CuotaRepo

activate User
User -> API: GET /api/v1/cuotas/historial
activate API

API -> Auth: Validar Access Token
activate Auth
Auth --> API: (éxito, devuelve user_id)
deactivate Auth

API -> UseCase: execute(user_id)
activate UseCase

UseCase -> CuotaRepo: buscar_por_usuario_id_completadas(user_id)
activate CuotaRepo
CuotaRepo --> UseCase: (lista_cuotas_pagadas)
deactivate CuotaRepo

UseCase --> API: HistorialCuotasDTO
deactivate UseCase

API --> User: 200 OK
deactivate API
deactivate User
@enduml
```

-----

### CASO DE USO 8: Ver Detalle de una Cuota (Admin)

```plantuml
@startuml
!theme materia
title Secuencia: 8. Ver Detalle de una Cuota (Admin)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "VerDetalleCuotaUseCase" as UseCase
participant "ICuotaRepository" as CuotaRepo

activate Administrador
Administrador -> API: GET /api/v1/admin/cuotas/{id_cuota}
activate API

API -> Auth: Validar Access Token y rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(id_cuota)
activate UseCase

UseCase -> CuotaRepo: buscar_por_id_con_detalle(id_cuota)
activate CuotaRepo
CuotaRepo --> UseCase: (entidad_cuota_con_usuario_y_temporada)
deactivate CuotaRepo

UseCase --> API: DetalleCuotaDTO
deactivate UseCase

API --> Administrador: 200 OK
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 9: Registrar Cuota Manual (Admin)

```plantuml
@startuml
!theme materia
title Secuencia: 9. Registrar Cuota Manual (Admin)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "RegistrarCuotaManualUseCase" as UseCase
participant "ICuotaRepository" as CuotaRepo

activate Administrador
Administrador -> API: POST /api/v1/admin/cuotas/registrar-manual\n(con usuario_id, tipo_cuota_id, importe, metodo, notas)
activate API

API -> Auth: Validar Access Token y rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(datos_pago_manual_dto)
activate UseCase

UseCase -> UseCase: Crear entidad Cuota con estado 'completado'
UseCase -> CuotaRepo: guardar(cuota_manual_completada)
activate CuotaRepo
CuotaRepo --> UseCase: (cuota_guardada)
deactivate CuotaRepo

UseCase --> API: CuotaCompletadaDTO
deactivate UseCase

API --> Administrador: 201 Created
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 10: Generar Informe de Pendientes (Admin)

```plantuml
@startuml
!theme materia
title Secuencia: 10. Generar Informe de Pendientes (Admin)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "GenerarInformePendientesUseCase" as UseCase
participant "ICuotaRepository" as CuotaRepo

activate Administrador
Administrador -> API: GET /api/v1/admin/cuotas/informe-pendientes?temporada_id=...
activate API

API -> Auth: Validar Access Token y rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(temporada_id)
activate UseCase

' Este caso de uso hará una consulta compleja
UseCase -> CuotaRepo: get_usuarios_pendientes_por_temporada(temporada_id)
activate CuotaRepo
CuotaRepo --> UseCase: (lista_usuarios_pendientes)
deactivate CuotaRepo

UseCase --> API: InformePendientesDTO
deactivate UseCase

API --> Administrador: 200 OK
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 11: Procesar Webhook de Stripe

```plantuml
@startuml
!theme materia
title Secuencia: 11. Procesar Webhook de Stripe

actor Stripe
participant "Router (FastAPI)" as API
participant "ProcesarWebhookUseCase" as UseCase
participant "IPaymentGateway" as PaymentGateway
participant "ICuotaRepository" as CuotaRepo

activate Stripe
Stripe -> API: POST /api/v1/webhooks/stripe\n(con payload y firma)
activate API

API -> UseCase: execute(payload, firma_header)
activate UseCase

' 1. Validar que el evento viene de Stripe
UseCase -> PaymentGateway: validar_webhook(payload, firma_header)
activate PaymentGateway
PaymentGateway --> UseCase: (evento_validado)
deactivate PaymentGateway

' 2. Obtener el ID de nuestra cuota (guardado en metadata)
UseCase -> UseCase: Extraer cuota_id de evento.metadata

' 3. Buscar la cuota 'pendiente' en la BD
UseCase -> CuotaRepo: buscar_por_id(cuota_id)
activate CuotaRepo
CuotaRepo --> UseCase: (entidad_cuota_pendiente)
deactivate CuotaRepo

' 4. Actualizar la cuota a 'completado'
UseCase -> UseCase: cuota.marcar_como_completado(...)
UseCase -> CuotaRepo: actualizar(cuota_completada)
activate CuotaRepo
CuotaRepo --> UseCase: (éxito)
deactivate CuotaRepo

UseCase --> API: (éxito)
deactivate UseCase

API --> Stripe: 200 OK
deactivate API
deactivate Stripe
@enduml
```

-----

### CASO DE USO 12: Desactivar Socios Inactivos

```plantuml
@startuml
!theme materia
title Secuencia: 12. Desactivar Socios Inactivos

actor Sistema
participant "Scheduler (CronJob)" as Scheduler
participant "DesactivarSociosInactivosUseCase" as UseCase
participant "ICuotaRepository" as CuotaRepo
participant "IUsuarioRepository" as UserRepo

activate Scheduler
Scheduler -> UseCase: execute()
activate UseCase

' 1. Encontrar IDs de usuarios inactivos (lógica en el repo de cuotas)
UseCase -> CuotaRepo: get_usuarios_inactivos_desde(fecha_limite)
activate CuotaRepo
CuotaRepo --> UseCase: (lista_de_ids_usuarios_a_desactivar)
deactivate CuotaRepo

' 2. Desactivar a esos usuarios (lógica en el repo de usuarios)
alt Hay usuarios para desactivar
    UseCase -> UserRepo: desactivar_usuarios(lista_de_ids)
    activate UserRepo
    UserRepo --> UseCase: (éxito)
    deactivate UserRepo
end

UseCase --> Scheduler: (reporte_de_ejecucion)
deactivate UseCase
deactivate Scheduler
@enduml
```