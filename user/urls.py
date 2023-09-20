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
from .views import LoginAPIView, TwitterConnectView


urlpatterns = [
    #path('', include('router.urls')),
    path('register/', views.RegisterAPIView.as_view(), name='account_signup'),
    path('login/', views.LoginAPIView.as_view(), name='account_login'),
    path('logout/',views.LogoutView.as_view(),name='account_logout' ),
    path('password/reset', views.PasswordResetView.as_view(), name='password_reset'),
    path('password/change', views.PasswordChangeView.as_view(), name='password_change'),
    path("profile/<int:pk>/", views.ProfileAPIView.as_view()),
    path("create/address/",views.CreateAddressAPIView.as_view() ),
    path("addresses/", views.ListAddressAPIView.as_view() ),
    path("address/<int:pk>/", views.AddressDetailAPIView.as_view() ), 
    path("facebook/", views.FacebookConnectView.as_view() ),
    path("twitter/", views.TwitterConnectView.as_view()),
    path("twitterlogin/", views.TwitterSocialAuthView.as_view() ),
    path("google/", views.GoogleConnectView.as_view()), 
    path("deactivate-user/", views.DeactivateUserView.as_view() ),
]


