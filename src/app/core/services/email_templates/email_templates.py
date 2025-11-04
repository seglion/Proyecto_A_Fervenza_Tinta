from pathlib import Path
from typing import Dict, Any

from src.app.core.config import settings


class EmailTemplates:
    _template_dir = Path(__file__).parent / "sendgrid"

    @staticmethod
    def _load_template(template_name: str) -> str:
        return (EmailTemplates._template_dir / template_name).read_text()

    @staticmethod
    def get_verification_email_template(name: str, token: str) -> str:
        template = EmailTemplates._load_template("verification_email.html")
        verification_link = f"{settings.BASE_URL}{settings.API_V1_STR}/users/verificar-email?token={token}"
        button_html = EmailTemplates._load_template("button_section.html").replace("{{link}}", verification_link).replace("{{button_text}}", "Verify Email")
        return template.replace("{{name}}", name).replace("{{button_section}}", button_html)

    @staticmethod
    def get_welcome_email_template(name: str) -> str:
        template = EmailTemplates._load_template("welcome_email.html")
        return template.replace("{{name}}", name).replace("{{button_section}}", "")

    @staticmethod
    def get_reset_password_email_template(token: str) -> str:
        template = EmailTemplates._load_template("reset_password_email.html")
        reset_link = f"{settings.BASE_URL}{settings.API_V1_STR}users/confirmar-reseteo?token={token}"
        button_html = EmailTemplates._load_template("button_section.html").replace("{{link}}", reset_link).replace("{{button_text}}", "Reset Password")
        return template.replace("{{name}}", "there").replace("{{button_section}}", button_html)

    @staticmethod
    def get_rejection_email_template() -> str:
        template = EmailTemplates._load_template("rejection_email.html")
        return template.replace("{{name}}", "there").replace("{{button_section}}", "")

    @staticmethod
    def get_payment_confirmation_email_template(name: str, cuota_info: Dict[str, Any]) -> str:
        template = EmailTemplates._load_template("payment_confirmation_email.html")
        html_content = template.replace("{{name}}", name)
        for key, value in cuota_info.items():
            html_content = html_content.replace(f"{{{{{key}}}}}", str(value))
        return html_content

    @staticmethod
    def get_pedido_payment_confirmation_email_template(pedido_info: Dict[str, Any]) -> str:
        template = EmailTemplates._load_template("pedido_payment_confirmation_email.html")
        html_content = template
        for key, value in pedido_info.items():
            html_content = html_content.replace(f"{{{{{key}}}}}", str(value))
        return html_content
