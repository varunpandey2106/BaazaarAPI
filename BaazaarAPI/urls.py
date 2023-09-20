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
# from djangorestframework_social_oauth2.views import AuthorizationView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('user/', include('user.urls')),
    # path('social_auth/', include(('social_auth.urls'),
    #                              namespace="social_auth")),
    # path('auth/', include('social_django.urls', namespace='drf')),
    # path('social/', include('rest_social_auth.urls_jwt')),
    # path('auth/', include('rest_framework_social_oauth2.urls')),
    path('authorize/', AuthorizationView.as_view(), name='authorize'),
    path('drf/', include('rest_framework.urls', namespace='drf')),
]

# reverse('authorize')

