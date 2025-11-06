# Backend - A Fervenza Tinta
 
Este directorio contiene el backend del proyecto, una API RESTful desarrollada con FastAPI.

**Nota:** Este es un paquete dentro de un monorepo. Para la visión general del proyecto, consulta el `README.md` en la raíz.

## Stack Tecnológico
 
*   **Lenguaje:** Python 3.12
*   **Framework:** FastAPI
*   **Base de Datos:** PostgreSQL (gestionado con Docker)
*   **ORM:** SQLAlchemy y SQLModel
*   **Migraciones:** Alembi
*   **Gestión de Dependencias:** Poetry

## Configuración y Puesta en Marcha
 
### 1. Configurar Variables de Entorno
 
Asegúrate de que estás en el directorio `backend/`. Crea un fichero `.env` a partir del `.env.example` (si existe) o desde cero con las variables necesarias.
Configuración de la base de datos
```
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/club_db"
```
Clave secreta para JWT
```
SECRET_KEY="tu_super_secreto_aqui"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
(otras variables como Stripe, SendGrid, etc.)

 ### 2. Instalar Dependencias
 ```
  poetry install
```
### 3. Levantar la Base de Datos con Docker

Desde el directorio `backend/`, ejecuta:
```
  docker-compose up -d
```

### 4. Ejecutar Migraciones de Base de Datos

Con la base de datos corriendo, crea las tablas:
```
  poetry run alembic upgrade head
```

## Ejecución

Para iniciar el servidor de desarrollo (escuchará en `http://127.0.0.1:8000`):

```
  poetry run uvicorn src.app.main:app --reload
```
## Testing

Para ejecutar la suite de tests:
```
  poetry run pytest
```
