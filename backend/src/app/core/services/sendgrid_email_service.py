
from typing import Dict, Any

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.app.core.services.i_email_service import IEmailService
from src.app.core.services.email_templates.email_templates import EmailTemplates
from src.app.core.config import settings


class SendgridEmailService(IEmailService):
    def __init__(self):
        self.sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.sender_email = settings.SENDGRID_SENDER_EMAIL

    def send_verification_email(self, email_to: str, name: str, token: str) -> None:
        message = Mail(
            from_email=self.sender_email,
            to_emails=email_to,
            subject='Verifica tu cuenta',
            html_content=EmailTemplates.get_verification_email_template(name, token)
        )
        self.sg.send(message)

    def enviar_email_bienvenida(self, email_to: str, name: str) -> None:
        message = Mail(
            from_email=self.sender_email,
            to_emails=email_to,
            subject='Bienvenido a nuestra plataforma',
            html_content=EmailTemplates.get_welcome_email_template(name)
        )
        self.sg.send(message)

    def send_reset_password_email(self, email_to: str, token: str) -> None:
        message = Mail(
            from_email=self.sender_email,
            to_emails=email_to,
            subject='Restablece tu contraseña',
            html_content=EmailTemplates.get_reset_password_email_template(token)
        )
        self.sg.send(message)

    def enviar_email_rechazo(self, email_to: str) -> None:
        message = Mail(
            from_email=self.sender_email,
            to_emails=email_to,
            subject='Tu solicitud ha sido rechazada',
            html_content=EmailTemplates.get_rejection_email_template()
        )
        self.sg.send(message)

    def enviar_email_confirmacion_pago(self, email_to: str, name: str, cuota_info: Dict[str, Any]) -> None:
        message = Mail(
            from_email=self.sender_email,
            to_emails=email_to,
            subject='Confirmación de pago de cuota',
            html_content=EmailTemplates.get_payment_confirmation_email_template(name, cuota_info)
        )
        self.sg.send(message)

    def enviar_confirmacion_pago_pedido(self, email_to: str, pedido_info: Dict[str, Any]) -> None:
        message = Mail(
            from_email=self.sender_email,
            to_emails=email_to,
            subject='Confirmación de pago de pedido',
            html_content=EmailTemplates.get_pedido_payment_confirmation_email_template(pedido_info)
        )
        self.sg.send(message)