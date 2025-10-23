from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pathlib import Path
from typing import Dict, Any

from app.core.config import settings
from app.core.services.i_email_service import IEmailService

# Configuración de la conexión a partir de settings
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
    TEMPLATE_FOLDER=Path(settings.TEMPLATE_FOLDER) if settings.TEMPLATE_FOLDER else None
)

class ConsoleEmailService(IEmailService):
    async def send_verification_email(self, email_to: str, name: str, token: str) -> None:
        """
        Envía un correo de verificación al usuario.

        Args:
            email_to: El email del destinatario.
            name: El nombre del usuario para personalizar el saludo.
            token: El token de verificación a incluir en el correo.
        """
        template_body = {
            "name": name,
            "token": token,
        }

        message = MessageSchema(
            subject="Verifica tu cuenta",
            recipients=[email_to],
            template_body=template_body,
            subtype="html"
        )

        print(f"Attempting to send verification email to {email_to} with token {token}")
        fm = FastMail(conf)
        await fm.send_message(message, template_name="verification.html")

    async def enviar_email_bienvenida(self, email_to: str, name: str) -> None:
        """
        Envía un correo de bienvenida a un usuario aprobado.

        Args:
            email_to: El email del destinatario.
            name: El nombre del usuario para personalizar el saludo.
        """
        template_body = {
            "name": name,
        }

        message = MessageSchema(
            subject="¡Bienvenido/a a FCT App!",
            recipients=[email_to],
            template_body=template_body,
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="welcome.html")

    async def send_reset_password_email(self, email_to: str, token: str) -> None:
        template_body = {
            "token": token,
        }

        message = MessageSchema(
            subject="Restablecimiento de Contraseña",
            recipients=[email_to],
            template_body=template_body,
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="reset_password.html")

    async def enviar_email_rechazo(self, email_to: str) -> None:
        message = MessageSchema(
            subject="Actualización sobre tu registro",
            recipients=[email_to],
            template_body={},
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="rejection.html")