from django.shortcuts import render
from .models import Payment, Order
from .serializers import PaymentSerializer, CheckoutSerializer
from .permissions import IsPaymentByUser, IsPaymentPending, Or
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView


# Create your views here.

class PaymentViewSet(ModelViewSet):
    """
    CRUD payment for an order
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsPaymentByUser]

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(order__buyer=user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes += [IsPaymentPending]

        return super().get_permissions()

# class CheckoutAPIView(RetrieveUpdateAPIView):
#     """
#     Create, Retrieve, Update billing address, shipping address and payment of an order
#     """
#     queryset = Order.objects.all()
#     serializer_class = CheckoutSerializer
#     permission_classes = [IsOrderByBuyerOrAdmin]

#     def get_permissions(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             self.permission_classes += [IsOrderPendingWhenCheckout]

#         return super().get_permissions()