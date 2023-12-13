import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.core.mail import send_mail
from django.conf import settings
from . import models

logger = logging.getLogger(__name__)


def send_user_email_confirmation_code(user):
    """Отправить код подтверждения"""

    code_with_defis = user.email_confirm_code
    _subject = "Код для подтверждения почты MYJOBOX"

    if user.user_type == 'APPLICANT':
        url = 'https://myjobox.ru/industrial/dashboardapp/'
    else:
        url = 'https://myjobox.ru/industrial/dashboard/'

    _message = f"Ваш код для подтверждения: {code_with_defis}\n\n{url}\n" \
               f"--------------------\n" \
               f"Выбирай то, что работает за тебя\n" \
               f"Удобная, интуитивно-понятная платформа для поиска соискателей"
    send_mail(
        subject=_subject,
        message=_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )


def send_forgot_pass(email: str, secret_key: str):
    """Отправить забытый пароль на почту"""
    # create message object instance
    msg = MIMEMultipart()

    message = f"Ваш ключ активации: {secret_key}  "
    logger.info('utils_key', secret_key)
    # setup the parameters of the message
    password = "elV1qaAhm1RF"
    msg['From'] = 'mode@myjobox.ru'
    msg['To'] = email
    msg['Subject'] = "Восстановление пароля"
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    # create server
    server = smtplib.SMTP('connect.smtp.bz: 2525')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print("successfully sent email to %s:" % (msg['To']))
