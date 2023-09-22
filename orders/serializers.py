from rest_framework import serializers
from .models import Order, OrderItem
from user.serializers import AddressSerializer, UserMiniSerializer
from products.serializers import ProductDetailSerializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = "modified"


