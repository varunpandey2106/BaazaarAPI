from django.urls import path, include
from . import views 


urlpatterns = [
    path('', include('router.urls')),
    path('login/', views.LoginAPIView.as_view(), name='account_login')

]


