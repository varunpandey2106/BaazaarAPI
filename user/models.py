from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.cache import cache
from datetime import datetime, timezone, timedelta
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _





class TimeStampedModel(models.Model):
    created_at= models.DateTimeField(auto_now_add=True) #profile create time
    updated_at= models.DateTimeField(auto_now_add=True) #profile update time

    class Meta:
        abstract= True

def user_directory_path(instance, filename):
    return "users/{0}/{1}".format(instance.user.username,filename)

class Profile(TimeStampedModel):
    GENDER_MALE='m'
    GENDER_FEMALE='f'

    GENDER_CHOICES=(
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    )

    user= models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE )
    profile_picture= models.ImageField(upload_to= user_directory_path, blank=True)
    phone_number= PhoneNumberField(blank= False)
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    birth_date=models.DateField(blank=False, null= False)

    def __str__(self):
        return "% " % self.user.username
    
    @property
    def last_seen(self):
        return cache.get(f"seen_{self.user.username}")
    
    @property #calculates online/offline status timestamp of last activity
    def online(self):
        if self.last_seen:
            now= datetime.now(timezone.utc)
            if now> self.last_seen+ timedelta(minutes=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False
        

@receiver(post_save,sender=User)
def create_user_profile(sender, instance,created,*args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Address(models.Model):
    BILLING= 'B'
    SHIPPING= 'S'

    ADDRESS_CHOICES=((BILLING,_('billing')), (SHIPPING,_('shipping')))

    user=models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    address_type=models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default=models.BooleanField(default=False)
    country= CountryField()
    city= models.CharField(max_length=100)
    street_address= models.CharField(max_length=100)
    apartment_address= models.CharField(max_length=100)
    postal_code= models.CharField(max_length=6, blank= False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now_add= True)

    class Meta:
        ordering= ('-created_at', )

        def __str__(self):
            return self.user.get_full_name()