# Proyecto de Gestion de A Fervenza Tinta
Este es un proyecto full-stack para la gestión de una asociacion, compuesto por un backend con FastAPI y un frontend con
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
      git clone https://github.com/seglion/Proyecto_A_Fervenza_Tinta.git
      cd Proyecto_A_Fervenza_Tinta
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
 
## Artefactos de Diseño

Este proyecto incluye una serie de diagramas UML y de planificación para documentar su arquitectura y diseño.

### Diagramas de Casos de Uso
*   [Diagrama de Casos de Uso (Markdown)](./use_case_diagram.md)
*   [Diagrama de Casos de Uso (PlantUML)](./use_case_diagram_semantic.puml)

### Diagramas de Clases (por Slice)
*   [Diagrama de Clases - Usuarios](./class_diagram_users.puml)
*   [Diagrama de Clases - Pedidos](./class_diagram_pedidos.puml)
*   [Diagrama de Clases - Prendas](./class_diagram_prendas.puml)
*   [Diagrama de Clases - Cuotas](./class_diagram_cuotas.puml)

### Planificación
*   [Diagrama de Gantt - Planificación del Proyecto](./gantt_chart_proyecto.puml)

