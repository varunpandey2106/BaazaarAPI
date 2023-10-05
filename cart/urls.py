from django.urls import path
from .import views

urlpatterns = [
    path("cart/<int:pk>/", views.CartItemView.as_view(), name= "cart-item-detail"),
    path("cart-item/<int:pk>/", views.CartItemAPIView.as_view()), 
    path('cart/add/<int:cart_id>/', views.add_to_cart, name='add_to_cart')
    

]
