from django.shortcuts import render
from django.http import response
from django.conf import settings
from rest_auth.registration.views import RegisterView
from django.views.decorators.debug import sensitive_post_parameters_m
from rest_auth.app_settings import JWTSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_auth.utils import jwt_encode
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from allauth.account.utils import send_email_confirmation

class RegisterAPIView(RegisterView):
    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterAPIView, self).dispatch(*args, **kwargs)
    
    def get_response_data(self, user):
        if getattr(settings, "REST_USE_JWT", False):
            data={"user":user, "token": self.token}
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
        user= serializer.save(self.request)
        if getattr(settings, "REST_USE_JWT", False):
            self.token= jwt_encode(user)

        email_address=EmailAddress.objects.get(email=user.email, user=user)
        send_email_confirmation(self.request, email_address)
        

