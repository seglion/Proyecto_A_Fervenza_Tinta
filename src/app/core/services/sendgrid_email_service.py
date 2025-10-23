import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from app.core.services.i_email_service import IEmailService
from app.core.config import settings
from pathlib import Path

class SendGridEmailService(IEmailService):
    def __init__(self):
        api_key = settings.SENDGRID_API_KEY or os.environ.get("SENDGRID_API_KEY")
        if not api_key:
            raise ValueError("SENDGRID_API_KEY not found in settings or environment variables.")
        self.sg = sendgrid.SendGridAPIClient(api_key)
        self.sender_email = settings.MAIL_USERNAME

        # Load templates
        template_dir = Path(__file__).parent / "email_templates" / "sendgrid"
        self.verification_template = (template_dir / "verification_email.html").read_text()
        self.welcome_template = (template_dir / "welcome_email.html").read_text()
        self.reset_password_template = (template_dir / "reset_password_email.html").read_text()
        self.rejection_template = (template_dir / "rejection_email.html").read_text()
        self.button_template = (template_dir / "button_section.html").read_text()

    async def send_verification_email(self, email_to: str, name: str, token: str) -> None:
        subject = "Verify your email"
        verification_link = f"http://localhost:8000/users/verificar-email?token={token}"
        
        button_html = self.button_template.replace("{{link}}", verification_link).replace("{{button_text}}", "Verify Email")
        html_content = self.verification_template.replace("{{name}}", name).replace("{{button_section}}", button_html)

        message = Mail(
            from_email=Email(self.sender_email),
            to_emails=To(email_to),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        try:
            response = await self.sg.client.mail.send.post(request_body=message.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Error sending verification email: {e}")
            raise

    async def enviar_email_bienvenida(self, email_to: str, name: str) -> None:
        subject = "Welcome!"
        html_content = self.welcome_template.replace("{{name}}", name).replace("{{button_section}}", "")
        message = Mail(
            from_email=Email(self.sender_email),
            to_emails=To(email_to),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        try:
            response = await self.sg.client.mail.send.post(request_body=message.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Error sending welcome email: {e}")
            raise

    async def send_reset_password_email(self, email_to: str, token: str) -> None:
        subject = "Reset your password"
        reset_link = f"http://localhost:8000/users/confirmar-reseteo?token={token}"
        
        button_html = self.button_template.replace("{{link}}", reset_link).replace("{{button_text}}", "Reset Password")
        html_content = self.reset_password_template.replace("{{name}}", "there").replace("{{button_section}}", button_html)
        message = Mail(
            from_email=Email(self.sender_email),
            to_emails=To(email_to),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        try:
            response = await self.sg.client.mail.send.post(request_body=message.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Error sending reset password email: {e}")
            raise

    async def enviar_email_rechazo(self, email_to: str) -> None:
        subject = "Your registration was rejected"
        html_content = self.rejection_template.replace("{{name}}", "there").replace("{{button_section}}", "")
        message = Mail(
            from_email=Email(self.sender_email),
            to_emails=To(email_to),
            subject=subject,
            html_content=Content("text/html", html_content)
        )
        try:
            response = await self.sg.client.mail.send.post(request_body=message.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Error sending rejection email: {e}")
            raise
