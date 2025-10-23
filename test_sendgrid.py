import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv
from pathlib import Path

# Carga las variables de entorno desde .env.dev
env_path = Path(__file__).resolve().parent / ".env.dev"
load_dotenv(dotenv_path=env_path)

# Asegúrate de que estas variables estén configuradas en tu .env.dev
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDER_EMAIL = os.environ.get("MAIL_USERNAME") # O tu MAIL_FROM si es diferente

# Reemplaza con un correo electrónico real al que tengas acceso
RECIPIENT_EMAIL = "vigobaz@hotmail.com" 
RECIPIENT_NAME = "Nombre de Prueba"

if not SENDGRID_API_KEY:
    print("Error: SENDGRID_API_KEY no está configurada en .env.dev")
    exit()
if not SENDER_EMAIL:
    print("Error: MAIL_USERNAME (o MAIL_FROM) no está configurado en .env.dev")
    exit()

message = Mail(
    from_email=Email(SENDER_EMAIL),
    to_emails=To(RECIPIENT_EMAIL),
    subject="Prueba de SendGrid API Key",
    html_content=Content("text/html", f"Hola {RECIPIENT_NAME}, este es un correo de prueba de SendGrid.")
)

try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.client.mail.send.post(request_body=message.get())
    print(f"Correo enviado con éxito. Código de estado: {response.status_code}")
    print(f"Cuerpo de la respuesta: {response.body}")
    print(f"Cabeceras de la respuesta: {response.headers}")
except Exception as e:
    print(f"Error al enviar el correo: {e}")
