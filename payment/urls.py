from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import PaymentViewSet, CheckoutAPIView, PaymentAPI, StripeWebhookAPIView, initiate_stripe_payment
from .import views 


app_name='payment'

router=DefaultRouter()
# router.register(r'', PaymentViewSet)


urlpatterns = [
	path('product_page/', views.product_page, name='product_page'),
	path('payment_successful/', views.payment_successful, name='payment_successful'),
	path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
	path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
]


# urlpatterns = [
#     path('', include(router.urls)),
#     # path('checkout/<int:pk>', CheckoutAPIView.as_view(), name='checkout'), 
#     # path('make_payment/', PaymentAPI.as_view(), name= 'make-payment'),
#     # path('stripe/webhook/', StripeWebhookAPIView.as_view(), name='stripe-webhook'  ),
#     # path('initiate-stripe-payment/', initiate_stripe_payment, name='initiate-stripe-payment')

    


# ]
