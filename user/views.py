from django.shortcuts import render, get_object_or_404, redirect
from django.http import response
from django.urls import reverse
from django.conf import settings
from rest_auth.registration.views import RegisterView
from django.views.decorators.debug import sensitive_post_parameters
from rest_auth.app_settings import JWTSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_auth.utils import jwt_encode
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account.utils import send_email_confirmation
from rest_auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
    LogoutView,
)
from .models import DeactivateUser, Address, SMSVerification, Profile
#from django.utils.translation import gettext_lazy as v
from rest_framework.views import APIView
from django.contrib.auth.models import User, Permission
from rest_framework import permissions
from .serializers import PasswordResetConfirmSerializer
from .serializers import (
    ProfileSerializer, 
    UserSerializer,
    CreateAddressSerializer,
    AddressSerializer,
    PasswordChangeSerializer, 
    PasswordResetConfirmSerializer,
    DeactivateUserSerializer, 
    SMSPinSerializer,
    SMSVerificationSerializer, 
    VerifyEmailSerializer, 
    TwitterConnectSerializer, 
    TwitterAuthSerializer,
    UserPermissionSerializer, 
    GoogleSocialAuthSerializer,

)
from rest_framework.generics import (
    ListAPIView, 
    RetrieveAPIView,
    CreateAPIView, 
    GenericAPIView,
    UpdateAPIView
)

from rest_framework.exceptions import NotAcceptable
from .Backend.email import send_reset_password_email
from allauth.account.views import ConfirmEmailView

from rest_auth.registration.views import SocialConnectView, SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.instagram.views import InstagramOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter

from django.utils.decorators import method_decorator
from allauth.account.models import EmailAddress

from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.oauth.client import OAuthError
from allauth.socialaccount.providers.oauth2.client import OAuth2Error

from notifications.utils import send_sms_notification



#reg and login
class RegisterAPIView(RegisterView):

    token= None



    @method_decorator(sensitive_post_parameters())
    def dispatch(self,request, *args, **kwargs): #added request argument
        return super(RegisterAPIView, self).dispatch(request,*args, **kwargs)
    
    def get_response_data(self, user):
        data = {"user": user, "token": self.token}
        if not getattr(settings, "REST_USE_JWT", False):
        # You can set default values or handle the case where REST_USE_JWT is False here.
            pass

        return JWTSerializer(data).data


    
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=self.perform_create(serializer)
        headers= self.get_success_headers(serializer.data)

        return Response(
            self.get_response_data(user),
            status= status.HTTP_201_CREATED,
            headers= headers
        )
    
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, "REST_USE_JWT", False):
            self.token = jwt_encode(user)

        email = EmailAddress.objects.get(email=user.email, user=user)
        confirmation = EmailConfirmationHMAC(email)
        key = confirmation.key
        # TODO Send mail confirmation here .
        # send_register_mail.delay(user, key)
        print("account-confirm-email/" + key)
        return user



      
        

class LoginAPIView(LoginView):

 
    queryset = ""

    def get_response(self):
        response = super().get_response()  # Call the superclass's get_response method

        # Additional customization
        if self.user.is_authenticated:
            deactivate = DeactivateUser.objects.filter(user=self.user, deactive=True)
            if deactivate:
                deactivate.update(deactive=False)

        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(
            data=self.request.data, context={"request": request}
        )
        self.serializer.is_valid(raise_exception=True)
        self.login()

        # Create or retrieve a Token for the user
        token, created = Token.objects.get_or_create(user=self.user)

        # Send SMS notification after successful login
        if self.user.is_authenticated:
            send_sms_notification(self.user)  # Call the notification function

        return self.get_response()

#profile and user
class ProfileAPIView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request,pk):
        profile= Profile.objects.get(pk=pk)
        serializer=ProfileSerializer(profile,context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def get(self, request, pk):
    #     # Construct the URL for the user profile using the primary key
    #     profile_url = reverse('ProfileAPIView', kwargs={'pk': pk})  
    #     return redirect(profile_url)
    
class UserDetailView(RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=UserSerializer
    queryset=User.objects.all()
    lookup_field='username'

#address management
class CreateAddressAPIView(CreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=CreateAddressSerializer
    queryset=''

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressDetailAPIView(RetrieveAPIView):
    permission_classes= [permissions.IsAuthenticated]
    serializer_class= AddressSerializer
    queryset= Address.objects.all()

    def retreive(self, request, *args, **kwargs):
        user= request.user()
        address=self.get_object()
        if address.user!= user:
            raise NotAcceptable("wrong address")
        serializer= self.get_serializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListAddressAPIView(ListAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class= AddressSerializer

    def get_queryset(self):
        user=self.request.user
        queryset=Address.objects.filter(user=user)
        return queryset

#password management
class PasswordChangeView(GenericAPIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class=PasswordChangeSerializer

    @sensitive_post_parameters("password")
    def dispatch(self,request, *args, **kwargs): #added request argument
        return super(PasswordChangeView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request,*args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response({"detail": "Congratulations, password has been Changed."})

class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        email=request.data.get("email", None)
        try:
            user= User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotAcceptable("Please enter a valid email.")
        send_reset_password_email.delay(user)
        return Response(
            {"detail": "Password reset e-mail has been sent."},
            status=status.HTTP_200_OK,
        )
    
class PasswordResetConfirmView(GenericAPIView):
    permission_classes=(permissions.AllowAny,)
    serializer_class=PasswordResetConfirmSerializer

    @sensitive_post_parameters("password")
    def dispatch(self, request, *args, **kwargs): #added request argument
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serializer= self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset with the new password."})
    
#deactivate and cancel deactivate
class DeactivateUserView(CreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=DeactivateUserSerializer
    
    def create(self,request, *args, **kwargs):
        user= self.request.user
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response("your account will be deactivated in 24 hrs")
    

class CancelDeactivateUserView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def post(request, self,*args, **kwargs):
        user=request.user
        deactivate= DeactivateUser.objects.get(user=user)
        deactivate.deactive=False
        deactivate.save()
        user.is_active=True
        user.save()
        return Response("your account will be reactivated")

#sms
class VerifySMSView(APIView):
    permission_classes=(permissions.AllowAny)
    allowed_methods=('POST', 'OPTIONS', 'HEAD')


    def get_serializer(self, *args, **kwargs):
        return SMSPinSerializer(self, *args, **kwargs)
    
    def post(self, request,pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pin=int(request.data.get('pin'))
        #todo: get sms verification
        confirmation=get_object_or_404(SMSVerification, pk=pk)
        confirmation.confirm(pin=pin)
        return Response("Your phone number has been verified", status=status.HTTP_200_OK)
    
class ResendSMSView(GenericAPIView):
    permission_classes=permissions.AllowAny
    serializer_class= SMSVerificationSerializer
    allowed_methods=("POST",)

    def resend_or_create(self):
        phone=self.request.data.get("phone")
        send_new=self.request.data.get("new")
        sms_verification= None

        user=User.objects.filter(profile__phone_number=phone).first()

        if not send_new:
            sms_verification=(
                SMSVerification.objects.filter(user=user, verified=False)
                .order_by("-created")
                .first()

            )
        if sms_verification is None:
            sms_verification=SMSVerification.objects.create(user=user, phone=phone)
        return sms_verification.send_confirmation()
    
    def post(request, self, *args, **kwargs):
        success=self.resend_or_create()
        return Response(dict(success=success), status=status.HTTP_200_OK)

#email   
class VerifyEmail(APIView, ConfirmEmailView):
    permission_classes= permissions.AllowAny
    allowed_methods=('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key']=serializer.validated_data['key']
        confirmation=self.get_object()
        confirmation.confirm(self.request)
        return Response({"detail": ("ok")}, status=status.HTTP_200_OK)

class ResendEmailView(APIView, ConfirmEmailView):
    permission_classes = permissions.AllowAny
    http_method_names = ['post']  # Specify allowed methods

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)

#sociallogins

class FacebookConnectView(SocialLoginView):
    adapter_class=FacebookOAuth2Adapter

class TwitterConnectView(SocialLoginView):
    serializer_class=TwitterConnectSerializer
    adapter_class=TwitterOAuthAdapter

class TwitterSocialAuthView(GenericAPIView):
    serializer_class = TwitterAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class GoogleConnectView(SocialLoginView):
    adapater_class= GoogleOAuth2Adapter
    client_class= OAuth2Client
    callback_url= 'https://www.google.com'

#user permissions
class RetrievePermissionView(RetrieveAPIView):
    serializer_class=UserPermissionSerializer
    queryset=User.objects.all()
    lookup_field='username'

class UpdatePermissionView(UpdateAPIView):
    serializer_class=UserPermissionSerializer
    queryset=User.objects.all()
    lookup_field='username'

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial']= True
        return self.update(request, *args, **kwargs)



class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)






    


        




        





