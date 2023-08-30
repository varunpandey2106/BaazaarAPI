from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from allauth.account.models import EmailAddress
from .models import SMSVerification, Profile
from rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.validators import UniqueValidator


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True, allow_blank=False)
    password=serializers.CharField(style={"input password": "password"})

    def authenticate(self, *kwargs):
        return authenticate(self)
    
    def _validate_email(self, email, password):
        user=None

        if email and password:
            user= self.authenticate(email=email, password=password)
        else:
            msg = _(
                'Must include "username or "email" or "phone number" and "password".'
            )
            raise exceptions.ValidationError(msg)
        return  user
    
    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user=self.authenticate(email=email, password=password)
        elif username and password:
            user=self.authenticate(username=username, password=password)
        else:
            msg = _(
                'Must include either "username" or "email" or "phone number" and "password".'
            )

            raise exceptions.ValidationError(msg)
        return user
    
        #REV

        def validate(self, attrs):
            username = attrs.get("username")
            password = attrs.get("password")

        user = None

        if "allauth" in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if (
                app_settings.AUTHENTICATION_METHOD
                == app_settings.AuthenticationMethod.EMAIL
            ):
                user = self._validate_email(email, password)

            # Authentication through username
            elif (
                app_settings.AUTHENTICATION_METHOD
                == app_settings.AuthenticationMethod.USERNAME
            ):
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            if username:
                user = self._validate_username_email(username, "", password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _("User account is inactive.")
                raise exceptions.ValidationError(msg)
        else:
            msg = _("please check your username or email or phone number or password.")
            raise exceptions.ValidationError(msg)

        # TODO user can't login if phone number and email address not verified.

        # If required, is the email verified?
        if "rest_auth.registration" in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            if (
                app_settings.EMAIL_VERIFICATION
                == app_settings.EmailVerificationMethod.MANDATORY
            ):
                try:
                    email_address = user.emailaddress_set.get(email=user.email)
                except EmailAddress.DoesNotExist:
                    raise serializers.ValidationError(
                        _(
                            "This account don't have E-mail address!, so that you can't login."
                        )
                    )
                if not email_address.verified:
                    raise serializers.ValidationError(_("E-mail is not verified."))

        # If required, is the phone number verified?
        try:
            phone_number = user.sms  # .get(phone=user.profile.phone_number)
        except SMSVerification.DoesNotExist:
            raise serializers.ValidationError(
                _("This account don't have Phone Number!")
            )
        if not phone_number.verified:
            raise serializers.ValidationError(_("Phone Number is not verified."))

        attrs["user"] = user
        return attrs

class CustomRegisterSerializer(RegisterSerializer):
    first_name=serializers.CharField(required=True, write_only=True)
    last_name=serializers.CharField(required=True, write_only= True)
    birth_date=serializers.CharField(required=True, write_only= True)
    phone_number=PhoneNumberField(required=True, write_only=True, 
                               validators=[
            UniqueValidator(
                queryset=Profile.objects.all(),
                message=_("A user is already registered with this phone number."),
            )
        ],
    )
    

    def get_cleaned_data(self):
        return{
            'first_name': self.validated_data.get("first_name", ""),
            'last_name': self.validated_data.get("last_name", ""),
            'birth_date': self.validated_data.get("birth_date", ""),
            'phone_number': self.validated_data.get("phone_number", ""),
        }

    def create_profile(self, user, validated_data):
        user.first_name= user.validated_data.get('first_name')
        user.last_name=  user.validated_data.get('last_name')
        user.save()

        user.profile.birth_date= user.validatded_data.get("birth_date")
        user.profile.phone_number= user.validated_data.get("phone_number")
        user.profile.save()

    def custom_signup(self, request, user):
        self.create_profile(user, self.get_cleaned_data_profile())

