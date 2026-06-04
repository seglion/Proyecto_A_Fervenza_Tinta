from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List
from pathlib import Path

# Construir una ruta absoluta al directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding='utf-8')


    BASE_URL: str
    PROJECT_NAME: str 
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str]

    
    SENDGRID_API_KEY: str
    SENDGRID_SENDER_EMAIL: str
    
    
    STRIPE_SECRET_KEY: str
    STRIPE_CUOTAS_WEBHOOK_SECRET: str

    STRIPE_PEDIDOS_WEBHOOK_SECRET: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    # Email settings
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True
    TEMPLATE_FOLDER: Optional[str] = None

    FRONTEND_BASE_URL: str

    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "imagenes"
    MINIO_PUBLIC_URL_BASE: str = "http://localhost:9000/imagenes"
    MINIO_SECURE: bool = False


settings = Settings()
