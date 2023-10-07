from django.urls import path
from .import views

urlpatterns = [
    path("cart/<int:pk>/", views.CartItemView.as_view(), name= "cart-item-detail"),
    path("cart-item/<int:pk>/", views.CartItemAPIView.as_view()), 
    path('cart/add/<int:cart_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/<int:cart_item_id>', views.remove_from_cart, name="remove_from_cart")


    

]
