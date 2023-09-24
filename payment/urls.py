from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, CheckoutAPIView, PaymentAPI, StripeWebhookAPIView

app_name='payment'

router=DefaultRouter()
router.register(r'', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/<int:pk>', CheckoutAPIView.as_view(), name='checkout'), 
    path('make_payment/', PaymentAPI.as_view(), name= 'make-payment'),
    path('stripe/webhook/', StripeWebhookAPIView.as_view(), name='stripe-webhook'  )
]
