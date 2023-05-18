import os 
from fastapi import HTTPException, status, Path
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from dotenv import load_dotenv

load_dotenv('.env')

class SystemMailer:

    __config = ConnectionConfig(
        MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
        MAIL_FROM = os.getenv("MAIL_FROM"),
        MAIL_PORT = int(os.getenv("MAIL_PORT")),
        MAIL_SERVER = os.getenv("MAIL_SERVER"),
        MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME"),
        MAIL_STARTTLS=False,
        USE_CREDENTIALS = True,
        MAIL_SSL_TLS = True,
        VALIDATE_CERTS = True,
        TEMPLATE_FOLDER= './templates',
    )

    


    async def send_mail(self, subject : str, email_to: str, body: dict):
        msg = MessageSchema(
            subject = subject,
            recipients = [email_to],
            template_body = body,
            subtype = MessageType.html
        )

        fm = FastMail(self.__config)

        await fm.send_message(msg, template_name = "send_mail.html")





