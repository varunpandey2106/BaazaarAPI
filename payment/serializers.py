from rest_framework import serializers
from orders.models import Order, OrderItem
from payment.models import Payment
from user.models import Address


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer to CRUD payments for an order.
    """
    buyer = serializers.CharField(
        source='order.buyer.get_full_name', read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'buyer', 'status', 'payment_option',
                  'order', 'created_at', 'updated_at')
        read_only_fields = ('status', )

class PaymentOptionSerializer(serializers.ModelSerializer):
    """
    Payment serializer for checkout. Order will be automatically set during checkout.
    """
    buyer = serializers.CharField(
        source='order.buyer.get_full_name', read_only=True)

    class Meta:
        model = Payment
        fields = ('id', 'buyer', 'status', 'payment_option',
                  'order', 'created_at', 'updated_at')
        read_only_fields = ('status', 'order')

