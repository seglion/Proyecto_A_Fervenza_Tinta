Entendido. É unha simplificación máis. Se as variantes só se definen pola súa talla e xénero (ex: "Camisa - Home - L"), o modelo é aínda máis directo.

Aquí tes o documento Markdown completo para o **SLICE PRENDAS**, co E-R e as táboas actualizadas para reflectir que `variantes_prenda` **non inclúe `cor` nin `sku`**.

-----

# SLICE PRENDAS

## Índice

  - [DIAGRAMA ER](#diagrama-er)
  - [Tablas de la Base de Datos](#tablas-de-la-base-de-datos)
      - [Tabla: prendas](#tabla-prendas)
      - [Tabla: variantes\_prenda](#tabla-variantes_prenda)
  - [Casos De Uso](#casos-de-uso)
  - [Diagramas de Secuencia](#diagramas-de-secuencia)

-----

## DIAGRAMA ER

-----

```mermaid
erDiagram
    usuarios {
        UUID id PK "Clave Primaria"
        VARCHAR email "Único, No Nulo"
        VARCHAR contrasena_hasheada "No Nulo"
        VARCHAR nombre
        VARCHAR apellidos
        VARCHAR apodo "Único, No Nulo"
        VARCHAR rol "admin | usuario"
        VARCHAR numero_telefono "Único, No Nulo"
        VARCHAR url_avatar
        BOOLEAN esta_activo "Default: true"
        BOOLEAN email_verificado "Default: false"
        BOOLEAN aprobado_por_admin "Default: false"
        TIMESTAMPZ fecha_creacion
        TIMESTAMPZ fecha_actualizacion
    }

    tokens {
        UUID id PK
        UUID usuario_id FK
        VARCHAR hash_token "Único, No Nulo"
        VARCHAR tipo_token "verificacion_email"
        TIMESTAMPZ fecha_expiracion
        BOOLEAN es_valido "Default: true"
        TIMESTAMPZ fecha_creacion
    }

    temporadas_cuotas {
        INTEGER id PK
        VARCHAR temporada "Único, No Nulo (ej. 2025-2026)"
        DATE fecha_inicio
        DATE fecha_fin
        TIMESTAMPZ fecha_creacion
    }

    tipos_cuota {
        INTEGER id PK
        INTEGER temporada_id FK
        VARCHAR nombre "Inscripción | Renovación | Otra"
        NUMERIC importe
        TIMESTAMPZ fecha_creacion
    }

    cuotas {
        UUID id PK
        UUID usuario_id FK
        INTEGER tipo_cuota_id FK
    }

    prendas {
        UUID id PK
        VARCHAR nombre "Único, No Nulo"
        TEXT descripcion
        NUMERIC precio
        VARCHAR imagen_url
        TIMESTAMPZ fecha_creacion
    }

    variantes_prenda {
        UUID id PK
        UUID prenda_id FK
        VARCHAR genero "Hombre | Mujer | Unisex"
        VARCHAR talla "XS | S | M | L | XL | Única"
        TIMESTAMPZ fecha_creacion
    }

    usuarios ||--o{ tokens : genera
    usuarios ||--|{ cuotas : paga
    temporadas_cuotas ||--|{ tipos_cuota : define
    tipos_cuota ||--|{ cuotas : corresponde
    prendas ||--|{ variantes_prenda : tiene

```

-----

## Tablas de la Base de Datos

-----

## Tabla: prendas

| Nombre de Columna | Tipo de Dato | Restricciones / Notas |
| :--- | :--- | :--- |
| **id** | UUID | Clave Primaria |
| **nome** | VARCHAR(100) | Único, No Nulo. Ej: "Camisa", "Polo", "Gorra" |
| **descripcion** | TEXT | Nulo. |
| **prezo** | NUMERIC(10, 2) | No Nulo. Precio de la prenda (independente de talla/genero). |
| **imaxe\_url** | VARCHAR(255) | Nulo. Imagen principal del produto. |
| **fecha\_creacion** | TIMESTAMPZ | No Nulo |

## Tabla: varianteprendas

| Nombre de Columna | Tipo de Dato | Restricciones / Notas |
| :--- | :--- | :--- |
| **id** | UUID | Clave Primaria |
| **prenda\_id** | UUID | Clave Externa a `prendas.id` |
| **xenero** | `tipogenero` | **ENUM:** ('Hombre', 'Mujer', 'Unisex'). |
| **talla** | `tipotalla` | **ENUM:** ('XS', 'S', 'M', 'L', 'XL', 'Unica'). |
| **fecha\_creacion** | TIMESTAMPZ | No Nulo |

-----

## Casos De Uso

-----

### 1\. Casos de Uso Públicos / Compartidos

1.  **Listar Prendas Disponibles**
      * **Lógica:** Un usuario (registrado o admin) solicita ver el catálogo. El sistema devuelve una lista de todas las `Prendas` con su nombre, precio general y foto principal.
2.  **Ver Detalle de una Prenda**
      * **Lógica:** Un usuario (registrado o admin) selecciona una prenda. El sistema devuelve la información detallada de esa `Prenda` y la lista completa de sus `Variantes` (tallas, géneros).

### 2\. Casos de Uso del Administrador (CRUD)

3.  **Crear Nueva Prenda Base**
      * **Lógica:** Un administrador añade un nuevo tipo de artículo al catálogo. El sistema le pide el nombre, la descripción, la foto principal y el **precio general** que tendrá ese artículo.
4.  **Actualizar Prenda Base**
      * **Lógica:** Un administrador edita la información de una prenda existente (ej: cambia la descripción, la foto o actualiza el **precio** general del artículo).
5.  **Eliminar Prenda Base**
      * **Lógica:** Un administrador elimina una prenda del catálogo. El sistema la borra, junto con todas las `Variantes` que tenía asociadas.
6.  **Añadir Variante a Prenda**
      * **Lógica:** Un administrador selecciona una prenda base (ej: "Camisa") y le añade una nueva combinación disponible (ej: "Mujer - Talla M").
7.  **Eliminar Variante de Prenda**
      * **Lógica:** Un administrador elimina una variante específica (ej: "Hombre - Talla S") de una prenda, sin necesidad de borrar la prenda completa.

-----

## Diagramas de Secuencia

-----

Aquí os tes.

Xerei os 7 diagramas de secuencia para o slice `Prendas`, seguindo a numeración da lista de casos de uso que consolidamos e a nosa arquitectura.

-----

## Diagramas de Secuencia

-----

### CASO DE USO 1: Listar Prendas Disponibles

```plantuml
@startuml
!theme materia
title Secuencia: 1. Listar Prendas Disponibles (Público)

actor "Usuario Registrado" as User
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "ListarPrendasUseCase" as UseCase
participant "IPrendaRepository" as PrendaRepo

activate User
User -> API: GET /api/v1/prendas
activate API

API -> Auth: Validar Access Token
activate Auth
Auth --> API: (éxito, devolve user_id)
deactivate Auth

API -> UseCase: execute()
activate UseCase

UseCase -> PrendaRepo: listar_todas()
activate PrendaRepo
PrendaRepo --> UseCase: (lista_entidades_prenda)
deactivate PrendaRepo

UseCase --> API: ListaPrendasDTO
deactivate UseCase

API --> User: 200 OK (con lista de prendas)
deactivate API
deactivate User
@enduml
```

-----

### CASO DE USO 2: Ver Detalle de una Prenda

```plantuml
@startuml
!theme materia
title Secuencia: 2. Ver Detalle de una Prenda (Público)

actor "Usuario Registrado" as User
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "VerDetallePrendaUseCase" as UseCase
participant "IPrendaRepository" as PrendaRepo

activate User
User -> API: GET /api/v1/prendas/{id_prenda}
activate API

API -> Auth: Validar Access Token
activate Auth
Auth --> API: (éxito, devolveve user_id)
deactivate Auth

API -> UseCase: execute(id_prenda)
activate UseCase

' O repo debe incluír as variantes na consulta
UseCase -> PrendaRepo: buscar_por_id_con_variantes(id_prenda)
activate PrendaRepo
PrendaRepo --> UseCase: (entidade_prenda_con_variantes)
deactivate PrendaRepo

alt Prenda atopada
    UseCase --> API: DetallePrendaDTO
else Prenda non atopada
    UseCase --> API: Error 404 Not Found
end

deactivate UseCase
API --> User: 200 OK (con detalle) ou 404
deactivate API
deactivate User
@enduml
```

-----

### CASO DE USO 3: Crear Nueva Prenda Base (Admin)

```plantuml
@startuml
!theme materia
title Secuencia: 3. Crear Nueva Prenda Base (Admin)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "CrearPrendaUseCase" as UseCase
participant "IPrendaRepository" as PrendaRepo

activate Administrador
Administrador -> API: POST /api/v1/admin/prendas\n(con nome, desc, prezo)
activate API

API -> Auth: Validar Access Token e rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(datos_prenda_dto)
activate UseCase

UseCase -> UseCase: Crear entidade Prenda
UseCase -> PrendaRepo: gardar(entidade_prenda)
activate PrendaRepo
PrendaRepo --> UseCase: (prenda_creada_con_id)
deactivate PrendaRepo

UseCase --> API: PrendaCreadaDTO
deactivate UseCase

API --> Administrador: 201 Created
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 4: Actualizar Prenda Base (Admin)

```plantuml
@startuml
!theme materia
title Secuencia: 4. Actualizar Prenda Base (Admin)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "ActualizarPrendaUseCase" as UseCase
participant "IPrendaRepository" as PrendaRepo

activate Administrador
Administrador -> API: PUT /api/v1/admin/prendas/{id_prenda}\n(con novos datos)
activate API

API -> Auth: Validar Access Token e rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(id_prenda, datos_actualizar_dto)
activate UseCase

UseCase -> PrendaRepo: buscar_por_id(id_prenda)
activate PrendaRepo
PrendaRepo --> UseCase: (entidade_prenda_actual)
deactivate PrendaRepo

alt Prenda atopada
    UseCase -> UseCase: Modificar entidade con novos datos (prezo, desc, etc.)
    UseCase -> PrendaRepo: gardar(prenda_actualizada)
    activate PrendaRepo
    PrendaRepo --> UseCase: (prenda_actualizada)
    deactivate PrendaRepo
    UseCase --> API: PrendaActualizadaDTO
else Prenda non atopada
    UseCase --> API: Error 404 Not Found
end

deactivate UseCase
API --> Administrador: 200 OK ou 404
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 5: Eliminar Prenda Base (Admin)

```plantuml
@startuml
!theme materia
title Secuencia: 5. Eliminar Prenda Base (Admin)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "EliminarPrendaUseCase" as UseCase
participant "IPrendaRepository" as PrendaRepo

activate Administrador
Administrador -> API: DELETE /api/v1/admin/prendas/{id_prenda}
activate API

API -> Auth: Validar Access Token e rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(id_prenda)
activate UseCase

' O repo encargarase do borrado en cascada das variantes
UseCase -> PrendaRepo: eliminar_por_id(id_prenda)
activate PrendaRepo
PrendaRepo --> UseCase: (éxito)
deactivate PrendaRepo

UseCase --> API: (éxito)
deactivate UseCase

API --> Administrador: 204 No Content
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 6: Añadir Variante a Prenda (Admin)

```plantuml
@startuml
!theme materia
title Secuencia: 6. Añadir Variante a Prenda (Admin)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "AnadirVarianteUseCase" as UseCase
participant "IPrendaRepository" as PrendaRepo
participant "IVariantePrendaRepository" as VarianteRepo

activate Administrador
Administrador -> API: POST /api/v1/admin/prendas/{id_prenda}/variantes\n(con xénero, talla)
activate API

API -> Auth: Validar Access Token e rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(id_prenda, datos_variante_dto)
activate UseCase

' 1. Comprobar que a prenda existe
UseCase -> PrendaRepo: buscar_por_id(id_prenda)
activate PrendaRepo
PrendaRepo --> UseCase: (entidade_prenda ou null)
deactivate PrendaRepo

alt Prenda atopada
    ' 2. Crear e gardar a nova variante
    UseCase -> UseCase: Crear entidade VariantePrenda
    UseCase -> VarianteRepo: gardar(nova_variante)
    activate VarianteRepo
    VarianteRepo --> UseCase: (variante_creada)
    deactivate VarianteRepo
    UseCase --> API: VarianteCreadaDTO
else Prenda non atopada
    UseCase --> API: Error 404 Not Found
end

deactivate UseCase
API --> Administrador: 201 Created ou 404
deactivate API
deactivate Administrador
@enduml
```

-----

### CASO DE USO 7: Eliminar Variante de Prenda (Admin)

```plantuml
@startuml
!theme materia
title Secuencia: 7. Eliminar Variante de Prenda (Admin)

actor Administrador
participant "Middleware Auth" as Auth
participant "Router (FastAPI)" as API
participant "EliminarVarianteUseCase" as UseCase
participant "IVariantePrendaRepository" as VarianteRepo

activate Administrador
Administrador -> API: DELETE /api/v1/admin/prendas/{id_prenda}/variantes/{id_variante}
activate API

API -> Auth: Validar Access Token e rol 'admin'
activate Auth
Auth --> API: (éxito)
deactivate Auth

API -> UseCase: execute(id_variante)
activate UseCase

' O UC podería comprobar que id_prenda coincide se fose necesario
UseCase -> VarianteRepo: eliminar_por_id(id_variante)
activate VarianteRepo
VarianteRepo --> UseCase: (éxito)
deactivate VarianteRepo

UseCase --> API: (éxito)
deactivate UseCase

API --> Administrador: 204 No Content
deactivate API
deactivate Administrador
@enduml
```