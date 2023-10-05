from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CartItemSerializer, CartItemUpdateSerializer, CartAddItemSerializer
from .models import Cart, CartItem
from products.models import Product
from rest_framework import permissions, status
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
# from notifications.utils import push_notification


# Create your views here.


class CartItemAPIView(ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart_id=self.kwargs['cart_id'] #to differentiate between diff users who have access to the cart
        queryset = CartItem.objects.filter(cart__user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_id=self.kwargs['cart_id']
        cart = get_object_or_404(Cart,id=cart_id, user=user)
        product = get_object_or_404(Product, pk=request.data["product"])
        product_id=request.data.get("product_id")
        current_item = CartItem.objects.filter(cart=cart, product=product)

        if user == product.user:
            raise PermissionDenied("This Is Your Product")

        if current_item.count() > 0:
            raise NotAcceptable("You already have this item in your shopping cart")

        try:
            quantity = int(request.data["quantity"])
        except Exception as e:
            raise ValidationError("Please Enter Your Quantity")

        if quantity > product.quantity:
            raise NotAcceptable("You order quantity more than the seller have")

        cart_item = CartItem(cart=cart, product=product, quantity=quantity)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        total = float(product.price) * float(quantity)
        cart.total = total
        cart.save()
        # push_notifications(
        #     cart.user,
        #     "New cart product",
        #     "you added a product to your cart " + product.title,
        # )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CartItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    # method_serializer_classes = {
    #     ('PUT',): CartItemUpdateSerializer
    # }
    queryset = CartItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        print(request.data)
        product = get_object_or_404(Product, pk=request.data["product"])
        product_id=request.data.get("product_id")

        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")

        try:
            quantity = int(request.data["quantity"])
        except Exception as e:
            raise ValidationError("Please, input vaild quantity")

        if quantity > product.quantity:
            raise NotAcceptable("Your order quantity more than the seller have")

        serializer = CartItemUpdateSerializer(cart_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        cart_item.delete()
        cart_item.cart.update_total()
        # push_notifications(
        #     cart_item.cart.user,
        #     "deleted cart product",
        #     "you have been deleted this product: "
        #     + cart_item.product.title
        #     + " from your cart",
        # )

        return Response(
            {"detail": _("your item has been deleted.")},
            status=status.HTTP_204_NO_CONTENT,
        )
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])

def add_to_cart(request, cart_id):
    serializer=CartAddItemSerializer(data=request.data)
    if serializer.is_valid():
        product_id=serializer.validated_data['product_id']
        quantity=serializer.validated_data['quantity']

        #ensure that the prvoided cart_id belongs to the user
        try:
            cart=Cart.objects.get(id=cart_id, user=request.user)
        except Product.DoesNotExist:
            return Response({
                "message":"cart not found"
            }, status=status.HTTP_400_NOT_FOUND)
        # Check if the product exists and is available
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Add the product to the cart or update its quantity
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()

        # Update the cart's total
        cart.update_total()

        return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)