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



urlpatterns = [
    #path('', include('router.urls')),
    path('login/', views.LoginAPIView.as_view(), name='account_login')

]


