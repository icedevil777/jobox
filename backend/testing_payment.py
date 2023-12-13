import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()
from django.core.mail import send_mail

send_mail(
    subject="Tema",
    message="Teks",
    from_email="support@myjobox.ru",
    recipient_list=['firdavs3akadov@gmail.com'],
)
