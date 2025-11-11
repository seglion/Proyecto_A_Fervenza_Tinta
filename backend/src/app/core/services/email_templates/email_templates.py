from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from src.app.core.config import settings


class EmailTemplates:
    _template_dir = Path(__file__).parent / "sendgrid"

    @staticmethod
    def _load_template(template_name: str) -> str:
        return (EmailTemplates._template_dir / template_name).read_text()
    @staticmethod
    def _get_common_replacements() -> dict:
        """Devuelve un diccionario con reemplazos comunes (logo, año)."""
        return {
            "{{logo_url}}": f"{settings.FRONTEND_BASE_URL}/logo.png",
            "{{year}}": str(datetime.now().year)
        }   
    
    
    
    
    @staticmethod
    def get_verification_email_template(name: str, token: str) -> str:
        template = EmailTemplates._load_template("verification_email.html")
        # Obtenemos los reemplazos comunes
        replacements = EmailTemplates._get_common_replacements()
        
        # Creamos los reemplazos específicos
        verification_link = f"{settings.FRONTEND_BASE_URL}/verify-email?token={token}"
        button_html = EmailTemplates._load_template("button_section.html").replace("{{link}}", verification_link).replace("{{button_text}}", "Verify Email")

        replacements.update({
            "{{name}}": name,
            "{{button_section}}": button_html
        })

        # Aplicamos todos los reemplazos
        for key, value in replacements.items():
            template = template.replace(key, value)
            
        return template

    @staticmethod
    def get_welcome_email_template(name: str) -> str:
        template = EmailTemplates._load_template("welcome_email.html")
        replacements = EmailTemplates._get_common_replacements()
        
        replacements.update({
            "{{name}}": name,
            "{{button_section}}": ""
        })

        for key, value in replacements.items():
            template = template.replace(key, value)
            
        return template

    @staticmethod
    def get_reset_password_email_template(token: str) -> str:
        template = EmailTemplates._load_template("reset_password_email.html")
        replacements = EmailTemplates._get_common_replacements()

        # Usamos la ruta simple que acordamos: /reset-password
        reset_link = f"{settings.FRONTEND_BASE_URL}/reset-password?token={token}"
        button_html = EmailTemplates._load_template("button_section.html").replace("{{link}}", reset_link).replace("{{button_text}}", "Reset Password")

        replacements.update({
            "{{name}}": "there", # El template original usaba "there"
            "{{button_section}}": button_html
        })

        for key, value in replacements.items():
            template = template.replace(key, value)
            
        return template

    @staticmethod
    def get_rejection_email_template() -> str:
        template = EmailTemplates._load_template("rejection_email.html")
        replacements = EmailTemplates._get_common_replacements()

        replacements.update({
            "{{name}}": "there",
            "{{button_section}}": ""
        })
        
        for key, value in replacements.items():
            template = template.replace(key, value)
            
        return template

    @staticmethod
    def get_payment_confirmation_email_template(name: str, cuota_info: Dict[str, Any]) -> str:
        template = EmailTemplates._load_template("payment_confirmation_email.html")
        replacements = EmailTemplates._get_common_replacements()

        replacements.update({
            "{{name}}": name
        })
        
        # 1. Aplicamos los reemplazos comunes (logo, año, nombre)
        for key, value in replacements.items():
            template = template.replace(key, value)
        
        # 2. Aplicamos los reemplazos dinámicos de la cuota (con los 5 corchetes)
        for key, value in cuota_info.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
            
        return template

    @staticmethod
    def get_pedido_payment_confirmation_email_template(pedido_info: Dict[str, Any]) -> str:
        template = EmailTemplates._load_template("pedido_payment_confirmation_email.html")
        replacements = EmailTemplates._get_common_replacements()

        # 1. Aplicamos los reemplazos comunes (logo, año)
        for key, value in replacements.items():
            template = template.replace(key, value)
            
        # 2. Aplicamos los reemplazos dinámicos del pedido
        for key, value in pedido_info.items():
            template = template.replace(f"{{{{{key}}}}}", str(value))
            
        return template
