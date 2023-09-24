from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

User= get_user_model()

class Cart:
    user = models.OneToOneField(
        User, related_name="user_cart", on_delete=models.CASCADE
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True
    )


class CartItem:
    pass
