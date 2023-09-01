from django.urls import path, include
from . import views 
#from rest_framework import routers
from rest_auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
    LogoutView
)
from rest_auth.registration.views import RegisterView, VerifyEmailView
#router=routers.DefaultRouter()
from django.views.generic import TemplateView
from django.urls import re_path



urlpatterns = [
    #path('', include('router.urls')),
    path('register/', views.RegisterAPIView.as_view(), name='account_signup'),
    path('login/', views.LoginAPIView.as_view(), name='account_login'),
    



]


