from django.db import models
from django.utils.translation import gettext_lazy as _
from orders.models import Order, OrderItem

# Create your models here.

class Payment(models.Model):
    #payment status
    PENDING="P"
    CONFIRMED="C"
    FAILED="F"

    STATUS_CHOICES= ((PENDING, _('pending')), (CONFIRMED,
                      _('confirmed')), (FAILED, _('failed')))
    
    #payment options
    PAYPAL='P'
    STRIPE='S'

    PAYMENT_CHOICES= ((PAYPAL, _('P')), (STRIPE,
                      _('S')))
    
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING)
    payment_option = models.CharField(max_length=1, choices=PAYMENT_CHOICES)
    order = models.ForeignKey(
        Order, related_name='payment', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.order.buyer.get_full_name()

    


