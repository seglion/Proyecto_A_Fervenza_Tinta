# Backend - A Fervenza Tinta

Este directorio contiene el backend del proyecto, una API RESTful desarrollada con FastAPI para el sistema de gestión del club.

**Nota:** Este es un paquete dentro de un monorepo. Para la visión general del proyecto, consulta el `README.md` en la raíz.

## Arquitectura

El backend sigue los principios de la **Arquitectura Limpia (Clean Architecture)**, separando el código en cuatro capas principales:

-   **Domain:** Contiene las entidades de negocio, la lógica y las reglas más puras del sistema.
-   **Application:** Orquesta los flujos de datos y la lógica de la aplicación (casos de uso), pero sin depender de detalles externos como la base de datos o la web.
-   **Infrastructure:** Contiene las implementaciones concretas de tecnologías externas, como los repositorios de base de datos (PostgreSQL con SQLModel) y la conexión con otros servicios.
-   **Presentation:** Expone la aplicación al mundo exterior, en este caso, a través de una API REST con FastAPI.

## Stack Tecnológico

*   **Lenguaje:** Python 3.12
*   **Framework:** FastAPI
*   **Base de Datos:** PostgreSQL (gestionado con Docker)
*   **ORM:** SQLModel (sobre SQLAlchemy)
*   **Migraciones:** Alembic
*   **Gestión de Dependencias:** Poetry

---

## Puesta en Marcha del Entorno de Desarrollo

### 1. Configurar Variables de Entorno

Crea un fichero `.env` en el directorio `backend/` a partir del `.env.example` (si existe) o desde cero. Debe contener, como mínimo, la URL de la base de datos y las claves para JWT:

```env
# Configuración de la base de datos
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/club_db"

# Clave secreta para JWT
SECRET_KEY="tu_super_secreto_aqui"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Instalar Dependencias

Asegúrate de tener [Poetry](https://python-poetry.org/) instalado. Luego, desde el directorio `backend/`, ejecuta:

```sh
poetry install
```

### 3. Levantar la Base de Datos con Docker

Desde el directorio `backend/`, ejecuta el siguiente comando para iniciar el contenedor de PostgreSQL en segundo plano:

```sh
docker-compose up -d
```

### 4. Ejecutar Migraciones de Base de Datos

Con la base de datos ya corriendo, aplica las migraciones para crear las tablas necesarias:

```sh
poetry run alembic upgrade head
```

---

## Ejecución

Para iniciar el servidor de desarrollo (escuchará en `http://127.0.0.1:8000`):

```sh
poetry run uvicorn src.app.main:app --reload
```

## Testing

Para ejecutar la suite de tests automatizados:

```sh
poetry run pytest
```
