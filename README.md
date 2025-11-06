# Proyecto de Gestion de A Fervenza Tinta
Este es un proyecto full-stack para la gestión de un club deportivo, compuesto por un backend con FastAPI y un frontend con
     Vue.js.

## Estructura del Monorepo

El proyecto está organizado como un monorepo con dos paquetes principales:
```
/
├── backend/      # API RESTful con FastAPI y PostgreSQL.
└── frontend/     # (Futuro) Aplicación de cliente con Vue.js.
```

Cada paquete tiene su propio `README.md` con instrucciones de instalación y desarrollo específicas.

## Stack Tecnológico

*   **Backend:** Python, FastAPI, SQLAlchemy, PostgreSQL, Docker.
*   **Frontend:** JavaScript, Vue.js, CSS/Sass.

## Puesta en Marcha del Entorno Completo

### Prerrequisitos

*   Git
*   Docker y Docker Compose
*   Python 3.12+ y Poetry (para el backend)
*   Node.js y npm/yarn (para el frontend)

### Instrucciones

1.  **Clonar el repositorio:**
```
      git clone <URL_DEL_REPOSITORIO>
      cd <NOMBRE_DEL_REPOSITORIO>
```

2.  **Configurar y ejecutar el Backend:**
     Sigue las instrucciones detalladas en el fichero `backend/README.md`.

3.  **Configurar y ejecutar el Frontend:**
     Sigue las instrucciones detalladas en el fichero `frontend/README.md`.
 
## Ejecución

Para una experiencia de desarrollo completa, necesitarás ejecutar ambos, el backend y el frontend, en terminales separadas.

*   **Para el Backend (desde la carpeta `backend/`):**
  (Asegúrate de que la base de datos Docker está corriendo)
      poetry run uvicorn src.app.main:app --reload

*   **Para el Frontend (desde la carpeta `frontend/`):**
      npm run dev
 

