# Frontend - A Fervenza Tinta

Este directorio contiene el frontend del proyecto, una Single-Page Application (SPA) desarrollada con Vue.js.

**Nota:** Este es un paquete dentro de un monorepo. Para la visión general del proyecto, consulta el `README.md` en la raíz.

## Stack Tecnológico

*   **Framework:** Vue.js 3
*   **Bundler:** Vite
*   **Routing:** Vue Router
*   **Gestión de Estado:** Pinia
*   **Estilos:** TailwindCSS
*   **Internacionalización (i18n):** vue-i18n
*   **Peticiones HTTP:** Axios

---

## Puesta en Marcha del Entorno de Desarrollo

### 1. Prerrequisitos

Asegúrate de tener una versión de Node.js compatible con la especificada en `package.json` (por ejemplo, v20+).

### 2. Instalar Dependencias

Desde el directorio `Frontend/`, ejecuta el siguiente comando para instalar todas las dependencias del proyecto:

```sh
npm install
```
*(Si prefieres usar `yarn`, puedes ejecutar `yarn install`)*

### 3. Configurar Variables de Entorno

Crea un archivo `.env.local` en el directorio `Frontend/`. Este archivo contendrá la URL base de la API del backend.

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

## Comandos del Proyecto

### Compilar y Recargar en Caliente para Desarrollo

Para iniciar el servidor de desarrollo de Vite (normalmente en `http://localhost:5173`):

```sh
npm run dev
```

### Compilar y Minificar para Producción

Para generar la versión de producción del sitio en el directorio `dist/`:

```sh
npm run build
```

### Ejecutar Linter

Para encontrar y corregir problemas en el código con ESLint:

```sh
npm run lint
```

### Formatear Código

Para formatear todo el código del proyecto con Prettier:

```sh
npm run format
```
