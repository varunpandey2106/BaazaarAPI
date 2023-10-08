"""
URL configuration for BaazaarAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, reverse
from oauth2_provider.views import AuthorizationView
from django.shortcuts import render
from  rest_framework.schemas import get_schema_view
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# from djangorestframework_social_oauth2.views import AuthorizationView

schema_view = get_schema_view(
   openapi.Info(
      title="Baazaar API ",
      default_version='v1',
      description="BaazaarAPI documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # path('BaazaarSchema/', get_schema_view(title='API SCHEMA', description='Guide for the rest API'), name= 'BaazaarSchema'), 

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.urls')),
    path('user/', include('user.urls')),
    # path('social_auth/', include(('social_auth.urls'),
    #                              namespace="social_auth")),
    # path('auth/', include('social_django.urls', namespace='drf')),
    # path('social/', include('rest_social_auth.urls_jwt')),
    # path('auth/', include('rest_framework_social_oauth2.urls')),
    path('authorize/', AuthorizationView.as_view(), name='authorize'),
    # path('drf/', include('rest_framework.urls', namespace='drf')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('payment/', include('payment.urls')),
    path('cart/', include('cart.urls') ), 
    path('notifications/', include('notifications.urls'))


    
]

reverse('authorize')

