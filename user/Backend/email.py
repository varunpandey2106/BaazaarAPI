import smtplib
from django.conf import settings
from email.mime.text import MIMEText
from celery import shared_task