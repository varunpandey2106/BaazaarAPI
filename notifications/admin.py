from django.contrib import admin
from .models import Notification, TwilioNotif

# Register your models here.
admin.site.register(Notification)
admin.site.register(TwilioNotif)


