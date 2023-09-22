from django.urls import path
from .import views

urlpatterns = [
    path("order/<int:pk>/",views.OrderView.as_view() ),
    path("payment/", views.Payment),
    path("payment/confirmation", views.payment_confirmation)

]
