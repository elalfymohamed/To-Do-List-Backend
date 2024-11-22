from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from core.mail_config import mail_connection_config
from models.auth import EmailSchema


conf = ConnectionConfig(
  MAIL_USERNAME=mail_connection_config.MAIL_USERNAME,
  MAIL_PASSWORD=mail_connection_config.MAIL_PASSWORD,
  MAIL_FROM=mail_connection_config.MAIL_USERNAME,
  MAIL_PORT=int(mail_connection_config.MAIL_PORT),
  MAIL_SERVER=mail_connection_config.MAIL_SERVER,
  MAIL_STARTTLS=False,
  MAIL_SSL_TLS =True,
  USE_CREDENTIALS=True,
  VALIDATE_CERTS=True
)


async def send_email(email: EmailSchema, subject: str, message: str):
  message = MessageSchema(
    subject=subject,
    recipients=[email],
    body=message,
    subtype=MessageType.html
  )
  fm = FastMail(conf) 
  await fm.send_message(message)


