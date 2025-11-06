# backend/Dockerfile

# 1. Usar una imagen base de Python
FROM python:3.12-slim

# 2. Establecer el directorio de trabajo
WORKDIR /app
ENV PYTHONPATH=/app
# 3. Instalar Poetry
RUN pip install poetry

# 4. Copiar los ficheros de dependencias e instalarlas
COPY pyproject.toml poetry.lock ./
# --no-root para no instalar el proyecto en sí, solo las dependencias
# --no-dev para un entorno de producción (puedes quitarlo para desarrollo)
RUN poetry install --no-root


# 5. Copiar el código fuente de la aplicación
COPY ./src ./src
COPY ./scripts ./scripts
COPY ./alembic ./alembic
COPY ./alembic.ini .

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
# 6. El comando para iniciar el servidor FastAPI
# El host 0.0.0.0 es necesario para que sea accesible desde fuera del contenedor
CMD ["poetry", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
