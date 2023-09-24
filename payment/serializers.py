from rest_framework import serializers
from orders.models import Order, OrderItem
from payment.models import Payment
from user.models import Address
from user.serializers import ShippingAddressSerializer, BillingAddressSerializer
from datetime import datetime   


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


class CheckoutSerializer(serializers.ModelSerializer):
    """
    Serializer class to set or update shipping address, billing address and payment of an order.
    """
    shipping_address = ShippingAddressSerializer()
    billing_address = BillingAddressSerializer()
    payment = PaymentOptionSerializer()

    class Meta:
        model = Order
        fields = ('id', 'payment', 'shipping_address', 'billing_address', )

    def update(self, instance, validated_data):
        order_shipping_address = None
        order_billing_address = None
        order_payment = None

        shipping_address = validated_data['shipping_address'] #check if sjipping address is set

        # Shipping address for an order is not set
        if not instance.shipping_address:
            order_shipping_address = Address(**shipping_address)
            order_shipping_address.save()
        else:
            # Shipping address for an order is already set so update its value
            address = Address.objects.filter(shipping_orders=instance.id)
            address.update(**shipping_address)

            order_shipping_address = address.first()

        billing_address = validated_data['billing_address'] #check if billing address is set

        # Billing address is not set for an order
        if not instance.billing_address:
            order_billing_address = Address(**billing_address)
            order_billing_address.save()

        else:
            # Billing address is set so update its value
            address = Address.objects.filter(billing_orders=instance.id)
            address.update(**billing_address)

            order_billing_address = address.first()

        payment = validated_data['payment'] #check if payment option is set

        # Payment option is not set for an order
        if not instance.payment:
            order_payment = Payment(**payment, order=instance)
            order_payment.save()

        else:
            # Payment option is set so update its value
            p = Payment.objects.filter(order=instance)
            p.update(**payment)

            order_payment = p.first()

        # Update order
        instance.shipping_address = order_shipping_address
        instance.billing_address = order_billing_address
        instance.payment = order_payment
        instance.save()

        return instance




def check_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month.")

def check_expiry_year(value):
    today = datetime.now()
    if not int(value) >= today.year:
        raise serializers.ValidationError("Invalid expiry year.")

def check_cvc(value):
    if not 3 <= len(value) <= 4:
        raise serializers.ValidationError("Invalid cvc number.")

def check_payment_method(value):
    payment_method = value.lower()
    if payment_method not in ["card"]:
        raise serializers.ValidationError("Invalid payment_method.")

class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(
        max_length=150,
        required=True,
    )
    expiry_month = serializers.CharField(
        max_length=2,  # Assuming a valid month will be two digits
        required=True,
        validators=[check_expiry_month],
    )
    expiry_year = serializers.CharField(
        max_length=4,  # Assuming a valid year will be four digits
        required=True,
        validators=[check_expiry_year],
    )
    cvc = serializers.CharField(
        max_length=4,  # Assuming CVC can have 3 or 4 digits
        required=True,
        validators=[check_cvc],
    )
