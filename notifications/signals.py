

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .utils import send_sms_notification

@receiver(post_save, sender=User)
def user_login_notification(sender, instance, created, **kwargs):
    if created:  # This ensures the SMS is sent only on user creation (i.e., login)
        send_sms_notification(instance)
