from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartProductSerializer(serializers.ModelSerializer): #serialize the Product model.
    class Meta:
        model = Product
        fields = (
            "title",
            "seller",
            "quantity",
            "price",
            "image",
        )

class CartItemSerializer(serializers.ModelSerializer): #serialize the CartItem model.
    # product = CartProductSerializer(required=False)
    class Meta:
        model = CartItem
        fields = ["cart", "product", "quantity"]

class CartItemMiniSerializer(serializers.ModelSerializer): #serialize CartItem instances
    product = CartProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

class CartItemUpdateSerializer(serializers.ModelSerializer): # updating CartItem instances.
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]