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

    cart_item_id=serializers.SerializerMethodField()

    def get_cart_id(self, obj):
        return obj.cart.id
    
    class Meta:
        model = CartItem
        fields = [ 'cart_item_id' ,"cart", "product", "quantity"]

class CartItemMiniSerializer(serializers.ModelSerializer): #serialize CartItem instances
    product = CartProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

class CartItemUpdateSerializer(serializers.ModelSerializer): # updating CartItem instances.
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


#serializer to add items to cart

class CartAddItemSerializer(serializers.ModelSerializer):
    cart_id= serializers.IntegerField()
    product_id= serializers.IntegerField()
    quantity=serializers.IntegerField(min_value=1)

#serializer to remove items from cart

class CartRemoveItemSerializer(serializers.ModelSerializer):
    cart_id= serializers.IntegerField()
    cart_item_id= serializers.IntegerField()