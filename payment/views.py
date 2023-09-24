from django.shortcuts import render
from .models import Payment, Order
from .serializers import PaymentSerializer, CheckoutSerializer
from .permissions import IsPaymentByUser, IsPaymentPending
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from orders.permissions import IsOrderByBuyerOrAdmin, IsOrderPending
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CardInformationSerializer
import stripe 
from rest_framework import status
from django.conf  import settings
from django.shortcuts import get_object_or_404
from .tasks import send_payment_success_email_task
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator


# Create your views here.
stripe.api_key = "sk_test_51NtTGFSHsEba2yrqHZu5ab6jQZciMF2VHzJ7GO6wKVbOOocC9a3OinSpMBenPviye1Y27nYDfdaBTNC4J308TfGG00o2BvYLnB"
customer_id= "cus_OhB3SZQH9RrvCt"
BASE_URL= "https://api.stripe.com"

customer = stripe.Customer.retrieve(
  "cus_OhB3SZQH9RrvCt",
  api_key="sk_test_51NtTGFSHsEba2yrqHZu5ab6jQZciMF2VHzJ7GO6wKVbOOocC9a3OinSpMBenPviye1Y27nYDfdaBTNC4J308TfGG00o2BvYLnB"
)



customer = stripe.Customer.retrieve("cus_OhB3SZQH9RrvCt")
# customer.capture() # Uses the same API Key.


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
        return res.filter(order__user=user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes += [IsPaymentPending]

        return super().get_permissions()

class CheckoutAPIView(RetrieveUpdateAPIView):
    """
    Create, Retrieve, Update billing address, shipping address and payment of an order
    """
    queryset = Order.objects.all()
    serializer_class = CheckoutSerializer
    permission_classes = [IsOrderByBuyerOrAdmin]

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            self.permission_classes += [IsOrderPending]

        return super().get_permissions()
    



# class PaymentAPI(APIView):
#     serializer_class = CardInformationSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         response = {}

#         if serializer.is_valid():
#             data_dict = serializer.validated_data
#             customer_id = data_dict.get('customer_id')  # Get the customer_id from the serializer data

#             try:
#                 response = self.stripe_card_payment(data_dict=data_dict, customer_id=customer_id)
#             except stripe.error.StripeError as e:
#                 response = {
#                     'error': f"Stripe error: {e}",
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     "payment_intent": {"id": "Null"},
#                     "payment_confirm": {'status': "Failed"}
#                 }
#         else:
#             response = {
#                 'errors': serializer.errors,
#                 'status': status.HTTP_400_BAD_REQUEST
#             }

#         return Response(response)

#     def stripe_card_payment(self, data_dict, customer_id):
#         try:
#             card_details = {
#                 "type": "card",
#                 "card": {
#                     "number": data_dict['card_number'],
#                     "exp_month": data_dict['expiry_month'],
#                     "exp_year": data_dict['expiry_year'],
#                     "cvc": data_dict['cvc'],
#                 },
#             }

#             # Create a PaymentIntent and associate it with the customer_id
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=10000,
#                 currency='inr',
#                 customer=customer_id  # Associate the payment with the customer
#             )

#             # Attach the payment method to the PaymentIntent
#             payment_intent = stripe.PaymentIntent.modify(
#                 payment_intent.id,
#                 payment_method=card_details,
#             )

#             # Confirm the PaymentIntent
#             payment_intent = stripe.PaymentIntent.confirm(
#                 payment_intent.id
#             )

#             if payment_intent.status == 'succeeded':
#                 response = {
#                     'message': "Card Payment Success",
#                     'status': status.HTTP_200_OK,
#                     "card_details": card_details,
#                     "payment_intent": payment_intent,
#                 }
#             else:
#                 response = {
#                     'message': "Card Payment Failed",
#                     'status': status.HTTP_400_BAD_REQUEST,
#                     "card_details": card_details,
#                     "payment_intent": payment_intent,
#                 }
#         except stripe.error.StripeError as e:
#             response = {
#                 'error': f"Stripe error: {e}",
#                 'status': status.HTTP_400_BAD_REQUEST,
#                 "payment_intent": {"id": "Null"},
#             }
#         return response

@method_decorator(csrf_exempt, name='dispatch')
class PaymentAPI(APIView):
    serializer_class = CardInformationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        response = {}
        if serializer.is_valid():
            data_dict = serializer.data
          
            response = self.stripe_card_payment(data_dict=data_dict)

        else:
            response = {'errors': serializer.errors, 'status':
                status.HTTP_400_BAD_REQUEST
                }
                
        return Response(response)

    def stripe_card_payment(self, data_dict):
        try:
            card_details = {
            "type": "card",
            "card": {
                "number": data_dict['card_number'],
                "exp_month": data_dict['expiry_month'],
                "exp_year": data_dict['expiry_year'],
                "cvc": data_dict['cvc'],
            }
        }
            #  you can also get the amount from databse by creating a model
            payment_intent = stripe.PaymentIntent.create(
                amount=10000, 
                currency='inr',
            )
            payment_intent_modified = stripe.PaymentIntent.modify(
                payment_intent['id'],
                payment_method=card_details['id'],
            )
            try:
                payment_confirm = stripe.PaymentIntent.confirm(
                    payment_intent['id']
                )
                payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
            except:
                payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
                payment_confirm = {
                    "stripe_payment_error": "Failed",
                    "code": payment_intent_modified['last_payment_error']['code'],
                    "message": payment_intent_modified['last_payment_error']['message'],
                    'status': "Failed"
                }
            if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
                response = {
                    'message': "Card Payment Success",
                    'status': status.HTTP_200_OK,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
            else:
                response = {
                    'message': "Card Payment Failed",
                    'status': status.HTTP_400_BAD_REQUEST,
                    "card_details": card_details,
                    "payment_intent": payment_intent_modified,
                    "payment_confirm": payment_confirm
                }
        except:
            response = {
                'error': "Your card number is incorrect",
                'status': status.HTTP_400_BAD_REQUEST,
                "payment_intent": {"id": "Null"},
                "payment_confirm": {'status': "Failed"}
            }
        return response


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookAPIView(APIView):
    """
    Stripe webhook API view to handle checkout session completed and other events.
    """
    permission_classes = [AllowAny]


    def post(self, request, format=None):
        payload = request.body
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret)
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_email = session['customer_details']['email']
            order_id = session['metadata']['order_id']

            print('Payment successfull')

            payment = get_object_or_404(Payment, order=order_id)
            payment.status = 'C'
            payment.save()

            order = get_object_or_404(Order, id=order_id)
            order.status = 'C'
            order.save()

            # TODO - Decrease product quantity

            send_payment_success_email_task.delay(customer_email)

        # Can handle other events here.

        return Response(status=status.HTTP_200_OK)