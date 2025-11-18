# 1. Imagen Base
# Usa una imagen "slim" para que sea ligera
FROM python:3.12-slim

# 2. Variables de Entorno
# Evita que Python genere archivos .pyc y buferice la salida
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Instalar Poetry
# Actualizamos pip e instalamos poetry
RUN pip install --upgrade pip
RUN pip install poetry

# 4. Configurar Poetry
# ¡IMPORTANTE! Le decimos a Poetry que NO cree un virtualenv
# Usará el entorno del contenedor, que ya está aislado.
RUN poetry config virtualenvs.create false

# 5. Establecer Directorio de Trabajo
WORKDIR /app

# 6. Instalar Dependencias
# Copiamos SOLO los archivos de dependencias
# Docker guardará esto en caché. Solo se re-ejecutará si 
# cambias tus dependencias (pyproject.toml).
COPY ./pyproject.toml ./poetry.lock* /app/

# Instalamos las dependencias (incluyendo las de desarrollo)
RUN poetry install --no-interaction --no-ansi --no-root
COPY . /app
EXPOSE 8000

# 7. Comando de Ejecución
# Este es el comando que arrancará tu servidor
# - Asume que tu app está en /app/src/main.py y se llama 'app'
# - --reload es VITAL para el hot-reload
# - --host 0.0.0.0 es VITAL para que sea accesible fuera del contenedor
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" , "--app-dir", 'src']