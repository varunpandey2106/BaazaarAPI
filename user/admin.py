from django.contrib import admin
from .models import Profile, Address, SMSVerification

# Register your models here.

admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(SMSVerification)

