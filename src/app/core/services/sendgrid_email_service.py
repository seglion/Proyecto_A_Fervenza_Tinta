import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.core.services.i_email_service import IEmailService
from app.core.config import settings

class SendGridEmailService(IEmailService):
    def __init__(self):
        api_key = settings.SENDGRID_API_KEY or os.environ.get("SENDGRID_API_KEY")
        if not api_key:
            raise ValueError("SENDGRID_API_KEY not found in settings or environment variables.")
        self.sg = sendgrid.SendGridAPIClient(api_key)
        self.sender_email = settings.MAIL_USERNAME

    async def send_verification_email(self, email_to: str, name: str, token: str) -> None:
        subject = "Verify your email"
        html_content = f"Hello {name}, please verify your email by clicking on this link: http://localhost:8000/users/verificar-email?token={token}"
        message = Mail(
            from_email=Email(self.sender_email),
            to_emails=To(email_to),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        try:
            response = self.sg.client.mail.send.post(request_body=message.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Error sending verification email: {e}")
            raise

    async def enviar_email_bienvenida(self, email_to: str, name: str) -> None:
        subject = "Welcome!"
        html_content = f"Hello {name}, welcome to our platform!"
        message = Mail(
            from_email=Email(self.sender_email),
            to_emails=To(email_to),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        try:
            response = self.sg.client.mail.send.post(request_body=message.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            raise

    async def send_reset_password_email(self, email_to: str, token: str) -> None:
        subject = "Reset your password"
        html_content = f"You requested a password reset. Please click on this link to reset your password: http://localhost:8000/users/confirmar-reseteo?token={token}"
        message = Mail(
            from_email=Email(self.sender_email),
            to_emails=To(email_to),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        try:
            response = self.sg.client.mail.send.post(request_body=message.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Error sending reset password email: {e}")
            raise

    async def enviar_email_rechazo(self, email_to: str) -> None:
        subject = "Your registration was rejected"
        html_content = "We regret to inform you that your registration has been rejected."
        message = Mail(
            from_email=Email(self.sender_email),
            to_emails=To(email_to),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        try:
            response = self.sg.client.mail.send.post(request_body=message.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Error sending rejection email: {e}")
            raise
